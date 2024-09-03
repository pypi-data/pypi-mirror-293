from dataclasses import asdict
from decimal import Decimal
from types import UnionType
from typing import get_type_hints, get_origin, get_args, Sequence, Iterable, Mapping

from graphql import GraphQLResolveInfo
from aiodataloader import DataLoader

from ..database import DBInterface
from ..exceptions import NoRowsError, MultipleRowsError, QueryBuilderException
from ..models_utils import BaseModel
from ..querybuilder import (
    Table, Term, And, Any, Tuple, JoinTypes,
    Select, Insert, Update, Delete,
    ParameterDict, ParameterList
)
from ..request_utils import get_state, get_db


def table(model: type[BaseModel] | BaseModel) -> Table:
    return model.__metadata__.table


def build_from_tuple[T: BaseModel](model: type[T], rec: Sequence | None) -> T | None:
    if rec is None:
        return None
    return model(*rec)


def build_from_mapping[T: BaseModel](model: type[T], rec: Mapping | None) -> T | None:
    if rec is None:
        return None
    return model(**rec)


def build[T: BaseModel](model: type[T], rec) -> T | None:
    try:
        return build_from_mapping(model, rec)
    except TypeError:
        return build_from_tuple(model, rec)


def build_all[T: BaseModel](model: type[T], recs: Sequence) -> list[T]:
    try:
        return [build_from_mapping(model, rec) for rec in recs]
    except TypeError:
        return [build_from_tuple(model, rec) for rec in recs]


def primary_key_filter(model: type[BaseModel], **primary_keys) -> Term:
    """ Return Criterion to be used in a .where() """
    if not len(primary_keys):
        raise QueryBuilderException("Primary key filter must have at least one value")
    metadata = model.__metadata__
    terms = []
    for pk, value in primary_keys:
        if pk not in metadata.primary_keys:
            raise QueryBuilderException(f"Column {pk} in not in {model.__name__}'s primary keys")
        terms.append(metadata.table.columns[pk] == value)
    return And(*terms)


def get_query(model: type[BaseModel], **primary_keys) -> Select:
    """ Primary keys can be Params """
    q = Select(model).select_main_columns().where(primary_key_filter(model, **primary_keys))
    return q


async def get[T: BaseModel](db: DBInterface, model: type[T], **primary_keys) -> T | None:
    db_type = model.__metadata__.registry.db_type
    p = ParameterDict(db_type)
    q = get_query(model, **{key: p.add(key) for key in primary_keys.keys()})
    rows = await db.fetch(q, *p.params(**primary_keys))
    row_count = len(rows)
    if row_count == 0:
        return None
    if row_count > 1:
        raise MultipleRowsError

    if db_type == 'sqlserver':
        return build_from_tuple(model, rows[0])
    else:
        return build_from_mapping(model, rows[0])


async def get_or_error[T: BaseModel](db: DBInterface, model: type[T], **primary_keys) -> T:
    row = await get(db, model, **primary_keys)
    if row is None:
        raise NoRowsError
    return row


def delete_query(model: type[BaseModel], **primary_keys) -> Delete:
    q = Delete(model).where(primary_key_filter(model, **primary_keys))
    return q


async def delete(db: DBInterface, model: type[BaseModel], **primary_keys) -> None:
    p = ParameterDict(model.__metadata__.registry.db_type)
    q = delete_query(model, **{key: p.add(key) for key in primary_keys.keys()})
    await db.execute(q, *p.params(**primary_keys))


async def insert[T: BaseModel](db: DBInterface, model: type[T], obj: T):
    obj_dict = asdict(obj)
    p = ParameterDict(model.__metadata__.registry.db_type)
    q = Insert(model).set_columns_from_table().values(**{key: p.add(key) for key in obj_dict})
    await db.execute(q, *p.params(**obj_dict))


async def insert_many[T: BaseModel](db: DBInterface, model: type[T], objs: Iterable[T]):
    if not objs:  # Ensure at least one
        return
    obj_dicts = [asdict(obj) for obj in objs]
    p = ParameterDict(model.__metadata__.registry.db_type)
    q = Insert(model).set_columns_from_table().values(**{key: p.add(key) for key in obj_dicts[0]})
    await db.executemany(q, (p.params(**obj_dict) for obj_dict in obj_dicts))


def update_query(model: type[BaseModel], **primary_keys) -> tuple[Update, ParameterDict]:
    """ specifiying primary keys allows for renaming a record. They're prefixed by pk_ """
    metadata = model.__metadata__
    table_columns = metadata.table.columns
    p = ParameterDict(metadata.registry.db_type)
    q = Update(model)

    if primary_keys:
        if pk_diff := set(primary_keys.keys()) != set(metadata.primary_keys):
            raise QueryBuilderException(f"Please specify the correct primary keys for model {model.__name__}."
                                        f" Difference is {pk_diff}")
        for field_name, value in primary_keys.items():
            q = q.where(table_columns[field_name] == p.add('pk_' + field_name))

    for field_name, column_name in table_columns.items():
        if not primary_keys and field_name in metadata.primary_keys:
            q = q.where(column_name == p.add(field_name))
        else:
            q = q.set(**{column_name: p.add(field_name)})
    return q, p


async def update[T: BaseModel](db: DBInterface, model: type[T], obj: T, **primary_keys):
    """ specifiying primary keys allows for renaming a record. They're prefixed by pk_ """
    q, p = update_query(model, **primary_keys)
    await db.execute(q, *p.params(**asdict(obj), **{'pk_' + k: v for k, v in primary_keys.items()}))


async def update_many[T: BaseModel](db: DBInterface, model: type[T], objs: Iterable[T]):
    q, p = update_query(model)
    await db.executemany(q, (p.params(**asdict(obj)) for obj in objs))


def get_relation_model(model: type[BaseModel], relation_name: str) -> type[BaseModel]:
    try:
        relation = model.__metadata__.relations[relation_name]
    except KeyError:
        raise Exception(f"Could not find Relation {relation_name} in model {model.__name__}")
    return relation.rel_model


def join_relation(q: Select, model: type[BaseModel], relation_name: str, join_type: JoinTypes = JoinTypes.INNER) -> Select:
    try:
        relation = model.__metadata__.relations[relation_name]
    except KeyError:
        raise Exception(f"Could not find Relation {relation_name} in model {model.__name__}")

    if not q.is_joined(relation.rel_model):
        q = q.join(
            relation.rel_model,
            *(
                getattr(model, col_name) == rel_column
                for col_name, rel_column in relation.join_on.items()
            ),
            how=join_type
        )
    return q


async def batch_get[T: BaseModel](db: DBInterface, model: type[T], keys_list: Sequence[dict]) -> list[T | None]:
    """ Gets one object per keys according to the model's primary key """
    p = ParameterList(model.__metadata__.registry.db_type)

    # Convert dict to tuples and check keys
    pk_names = model.__metadata__.primary_keys
    tuple_list = [tuple(pks[pk_name] for pk_name in pk_names) for pks in keys_list]
    # Build query
    any_clause = Any(
        Tuple(*(p.add(pk) for pk in pks))
        for pks in tuple_list
    )
    q = Select(model).select_main_columns().where(
        Tuple(*(getattr(model, pk_name) for pk_name in pk_names)) == any_clause
    )
    # Build dict
    d = {
        tuple(getattr(obj, pk) for pk in pk_names): obj
        for obj in build_all(model, await db.fetch(q, *p.params()))
    }
    return [d.get(keys) for keys in tuple_list]


async def dataloader_get[T: BaseModel](info: GraphQLResolveInfo, model: type[T], **primary_keys) -> T | None:
    state = get_state(info)
    if not hasattr(state, 'auto_loaders'):
        state.auto_loaders = {}

    try:
        dl = state.auto_loaders[model.__name__]
    except KeyError:
        db = model.__metadata__.registry.db_connection_factory or get_db(info)
        async def batch_get_wrapper(keys_list: Sequence[dict]):
            return await batch_get(db, model, keys_list)  # attach info
        dl = state.auto_loaders[model.__name__] = DataLoader(batch_get_wrapper)
    return await dl.load(primary_keys)


def set_dataclass_attribute(obj: BaseModel, field_name: str, field_value):
    """ Like setattr but try to handle types"""
    field_type = get_type_hints(obj.__class__)[field_name]

    if get_origin(field_type) is UnionType:
        field_type = get_args(field_type)[0]

    if field_type is Decimal and isinstance(field_value, float):  # Convert float to Decimal
        field_value = Decimal(field_value)

    setattr(obj, field_name, field_value)


def extract_main_from_union_type(type_) -> type:
    """ Return main type when nullable """
    if get_origin(type_) is UnionType:
        unioned_types = []
        for unioned_type in get_args(type_):
            if unioned_type is not type(None):
                unioned_types.append(unioned_type)
        assert len(unioned_types) == 1
        return unioned_types[0]
    return type_


def extract_main_from_list_type(type_) -> type:
    """ Return main type when list """
    if get_origin(type_) is list:
        return get_args(type_)[0]
    return type_


def extract_main_type(type_) -> type:
    type_ = extract_main_from_union_type(type_)  # Handle first level of nullable
    type_ = extract_main_from_list_type(type_)  # Dig into one level of list
    return extract_main_from_union_type(type_)  # Handle second level of nullable


def is_field_list_type(model: type[BaseModel], field_name: str) -> type:
    type_ = model.__metadata__.dataclass_fields[field_name].type
    # Handle first level of nullable
    type_ = extract_main_from_union_type(type_)
    return get_origin(type_) is list


def get_field_main_type(model: type[BaseModel], field_name: str) -> type:
    type_ = model.__metadata__.dataclass_fields[field_name].type
    return extract_main_type(type_)