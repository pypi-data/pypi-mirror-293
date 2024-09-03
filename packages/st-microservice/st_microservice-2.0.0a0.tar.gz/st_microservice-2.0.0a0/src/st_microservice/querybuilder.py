from abc import ABC, abstractmethod
from enum import Enum
from inspect import isclass
from typing import Sequence

from .exceptions import QueryBuilderException


class DBTypes(Enum):
    POSTGRESQL = 'postgresql'
    SQLSERVER = 'sqlserver'


class JoinTypes(Enum):
    INNER = 'inner'
    OUTER = 'outer'
    LEFT = 'left'
    RIGHT = 'right'


class QueryObjectBase(ABC):
    @abstractmethod
    def to_sql(self) -> str:
        pass

    def __str__(self):
        return self.to_sql()


class TableBase(QueryObjectBase, ABC):
    """ Can be used in a FROM clause """
    def __init__(self, alias: str | None = None):
        self.alias = alias
        self.columns: dict[str, Column] = {}

    @property
    def columns_list(self) -> list['Column']:
        if not self.columns:
            raise QueryBuilderException("Table does not have columns specified")
        return list(self.columns.values())

    @property
    @abstractmethod
    def identifier(self) -> str:
        pass

    def add_column(self, name: str, alias: str | None = None) -> 'Column':
        c = Column(name, self, alias)
        self.columns[name] = c
        return c


class Table(TableBase):
    def __init__(self, name: str, schema: str | None = None, alias: str | None = None):
        super().__init__(alias)
        self.name = name
        self.schema = schema

    @property
    def identifier(self) -> str:
        return self.alias or self.name

    def as_alias(self, alias) -> 'Table':
        atable = Table(self.name, self.schema, alias)
        for column in self.columns.values():
            atable.add_column(column.name, column.alias)
        return atable

    def to_sql(self):
        res = f'"{self.name}"'
        if self.schema is not None:
            res = f'"{self.schema}".' + res
        if self.alias is not None:
            res = res + f' "{self.alias}"'
        return res


class ModelInterface(ABC):
    class MetadataInterface:
        class RegistryInterface:
            db_type: DBTypes

        table: Table
        registry: RegistryInterface

    __metadata__: MetadataInterface


type TableParam = type[ModelInterface] | TableBase | str


class Term(QueryObjectBase, ABC):
    def __eq__(self, other) -> 'Expression':
        return Expression(self, '=', _try_term(other))

    def __and__(self, other) -> 'Expression':
        return Expression(self, 'AND', _try_term(other))

    def __or__(self, other) -> 'Expression':
        return Expression(self, 'OR', _try_term(other), parenthesised=True)

    def __lt__(self, other) -> 'Expression':
        return Expression(self, '<', _try_term(other))

    def __le__(self, other) -> 'Expression':
        return Expression(self, '<=', _try_term(other))

    def __gt__(self, other) -> 'Expression':
        return Expression(self, '>', _try_term(other))

    def __ge__(self, other) -> 'Expression':
        return Expression(self, '>=', _try_term(other))

    def __invert__(self) -> 'Expression':
        return Expression(None, 'NOT', self)

    def __add__(self, other) -> 'Expression':
        return Expression(self, '+', _try_term(other))

    def like(self, other) -> 'Expression':
        return Expression(self, 'LIKE', other)


def _try_term(t) -> Term:
    return t if isinstance(t, Term) else Value(t)


def _try_value(v):
    if isinstance(v, Value):
        if v.alias is not None:
            raise QueryBuilderException("Value in insert cannot have alias")
    else:
        if isinstance(v, Term):
            raise QueryBuilderException("Term can only be of instance Value")
        v = Value(v)
    return v


def _check_term(term):
    """ Ensure is term """
    if not isinstance(term, Term):
        raise QueryBuilderException(f"{term} must be of type Term")


def _check_terms(terms):
    """ Ensure all are terms """
    for term in terms:
        _check_term(term)


def _get_table(table: TableParam) -> TableBase:
    if isclass(table) and issubclass(table, ModelInterface):
        return table.__metadata__.table
    if isinstance(table, TableBase):
        return table
    if isinstance(table, str):
        return Table(table)
    raise QueryBuilderException("Cannot handle from_table parameter")


def _init_db_type(from_table: TableParam, db_type: DBTypes | None) -> DBTypes:
    if db_type is None:
        if not issubclass(from_table, ModelInterface):
            raise QueryBuilderException('db_type must be specified if from_table is not a Model')
        return from_table.__metadata__.registry.db_type
    return db_type


class Value(Term):
    def __init__(self, value: str | int | float | None, alias: str | None = None):
        self.value = value
        self.alias = alias

    def to_sql(self) -> str:
        alias_str = '' if self.alias is None else f' "{self.alias}"'
        if isinstance(self.value, str):
            return f"'{self.value}'" + alias_str
        if isinstance(self.value, (int, float)):
            return f'{self.value}' + alias_str
        if self.value is None:
            return 'NULL' + alias_str
        else:
            raise QueryBuilderException(f"Cannot handle value {self.value}")


class Expression(Term):
    def __init__(
            self, left: Term | None, operator: str, right: Term,
            *, alias: str | None = None, parenthesised: bool = False
    ):
        self.left = left
        self.operator = operator
        self.right = right
        self.alias = alias
        self.parenthesised = parenthesised or alias is not None

    def to_sql(self):
        res = self.operator + f' {self.right}'
        if self.left is not None:
            res = f'{self.left} ' + res
        if self.parenthesised:
            res = f'({res})'
        if self.alias is not None:
            res += f' "{self.alias}"'
        return res


class Column(Term):
    def __init__(self, name: str, table: TableBase | str | None = None, alias: str | None = None):
        self.name = name
        self.table = table
        self.alias = alias

    def to_sql(self):
        if self.name == '*':
            res = '*'
        else:
            res = f'"{self.name}"'

        if self.table is not None:
            if isinstance(self.table, TableBase):
                if self.table.alias is not None:
                    res = f'"{self.table.alias}".' + res
                else:
                    if isinstance(self.table, Table):
                        res = f'"{self.table.name}".' + res
                        if self.table.schema is not None:
                            res = f'"{self.table.schema}".' + res
                    else:
                        raise QueryBuilderException("TableBase object does not have alias or name property")
            else:  # is str
                res = f'"{self.table}".' + res

        if self.alias is not None:
            if self.name == '*':
                raise QueryBuilderException("Cannot alias *")
            res = f'{res} "{self.alias}"'

        return res


class Descending(Term):
    def __init__(self, term):
        _check_term(term)
        self.term = term

    def to_sql(self) -> str:
        return f'{self.term} DESCENDING'


class ParameterList:
    class Parameter(Term):
        def __init__(self, collection: 'ParameterList', value):
            self.collection = collection
            self.value = value

        def to_sql(self):
            self.collection.ordered_values.append(self.value)
            return '?' if self.collection.db_type == DBTypes.SQLSERVER else f'${len(self.collection.ordered_values)}'


    def __init__(self, db_type: DBTypes = DBTypes.POSTGRESQL):
        self.collection: list[ParameterList.Parameter] = []
        self.db_type = db_type
        self.ordered_values = []

    def add(self, value) -> Parameter:
        p = self.Parameter(self, value)
        self.collection.append(p)
        return p

    def params(self):
        if len(self.ordered_values) != len(self.collection):
            raise QueryBuilderException("Some parameter were not injected")
        return [value for value in self.ordered_values]


class ParameterDict:
    class Parameter(Term):
        def __init__(self, collection: 'ParameterDict', key: str):
            self.collection = collection
            self.key = key

        def to_sql(self):
            if self.collection.db_type == DBTypes.SQLSERVER:
                self.collection.ordered_keys.append(self.key)
                return '?'

            if self.key not in self.collection.ordered_keys:  # Re-use same postgres parameter
                self.collection.ordered_keys.append(self.key)
            return f'${self.collection.ordered_keys.index(self.key) + 1}'

    def __init__(self, db_type: DBTypes = DBTypes.POSTGRESQL):
        self.collection: list[ParameterDict.Parameter] = []
        self.db_type = db_type
        self.ordered_keys: list[str] = []

    def add(self, key) -> Parameter:
        p = self.Parameter(self, key)
        self.collection.append(p)
        return p

    def params(self, **kwvalues):
        if keys_diff := set(kwvalues.keys()).symmetric_difference(set(self.ordered_keys)):
            raise QueryBuilderException(f"Please provide exact parameters to ParameterDict: difference is {', '.join(keys_diff)}")
        return [kwvalues[key] for key in self.ordered_keys]


class _JoinClause:
    def __init__(self, table: TableBase, on_conditions, how: JoinTypes | None = None):
        self.table = table
        self.how: JoinTypes = JoinTypes.INNER if how is None else how
        self.on_conditions: list[Term] = on_conditions


class QueryBuilderBase(QueryObjectBase, ABC):
    def __init__(self, db_type: DBTypes):
        self._db_type = db_type
        self._parameter_list: ParameterList | None = None

    def use_parameters[T](self: T) -> T:
        if self._parameter_list is None:
            self._parameter_list = ParameterList(self._db_type)
        return self

    def get_params(self) -> list:
        if self._parameter_list is None:
            return []
        return self._parameter_list.params()

    def add_parameter[T](self, value: T) -> ParameterList.Parameter | T:
        if self._parameter_list is None:
            return value
        p = self._parameter_list
        return p.add(value)


class Select(QueryBuilderBase):
    def __init__(
            self,
            from_table: TableParam,
            db_type: DBTypes | None = None
    ):
        super().__init__(_init_db_type(from_table, db_type))
        self._table = _get_table(from_table)

        self._select: list[Term] = []
        self._joinlist: list[_JoinClause] = []
        self._where: list[Term] = []
        self._groupby: list[Term] = []
        self._having: list[Term] = []
        self._orderby: list[Term] = []
        self._limit: int | None = None
        self._offset: int | None = None

    def select_all(self):
        self._select.append(Column('*'))
        return self

    def select(self, *columns):
        _check_terms(columns)
        self._select.extend(columns)
        return self

    def select_main_columns(self):
        if not self._table.columns:
            raise QueryBuilderException(f"Main Table {self._table.identifier} does not have columns")
        self._select.extend(self._table.columns_list)
        return self

    def is_joined(self, table: TableParam):
        return _get_table(table).identifier in [t.table.identifier for t in self._joinlist]

    def join(self, table: TableParam, *on_conditions, how: JoinTypes | None = None):
        table = _get_table(table)
        if self.is_joined(table):
            raise QueryBuilderException(f"Table {table.identifier} already in JOIN clause")
        _check_terms(on_conditions)

        self._joinlist.append(_JoinClause(table, on_conditions, how))
        return self

    def where(self, condition):
        _check_term(condition)
        self._where.append(condition)
        return self

    def groupby(self, *columns):
        if self._groupby:
            raise QueryBuilderException("GROUP BY already set")
        _check_terms(columns)
        self._groupby = columns
        return self

    def having(self, condition):
        _check_term(condition)
        self._having.append(condition)
        return self

    def orderby(self, *columns):
        _check_terms(columns)
        self._orderby = columns
        return self

    def limit(self, limit: int | Term):
        self._limit = limit
        return self

    def offset(self, offset: int | Term):
        self._offset = offset
        return self

    def to_sql(self):  # Make sure to build the SQL in top-down order so SQL Server paramters get injected in order
        # Validating
        if not self._select:
            raise QueryBuilderException('SELECT is not defined')
        if self._having and not self._groupby:
            raise QueryBuilderException('Cannot use HAVING without GROUP BY')

        # Building
        select_str = ', '.join(str(s) for s in self._select)
        res = f'SELECT {select_str}\nFROM {self._table}'
        if self._joinlist:
            for jc in self._joinlist:
                res += f'\n{jc.how.value.upper()} JOIN {jc.table} ON {And(*jc.on_conditions)}'
        if self._where:
            where_str = ' AND '.join(f'({str(w)})' for w in self._where)
            res += f'\nWHERE {where_str}'
        if self._groupby:
            groupby_str = ', '.join(str(s) for s in self._groupby)
            res += f'\nGROUP BY {groupby_str}'
            if self._having:
                res += f'\nHAVING {And(*self._having)}'
        if self._orderby:
            res += f'\nORDER BY {', '.join(str(col) for col in self._orderby)}'
        if self._limit is not None:
            if self._db_type == DBTypes.SQLSERVER:
                res += f'\nFETCH NEXT {self._limit} ROWS ONLY'
            else:
                res += f'\nLIMIT {self._limit}'
        if self._offset is not None:
            res += f'\nOFFSET {self._offset}' + (' ROWS' if self._db_type == DBTypes.SQLSERVER else '')

        return res


class Insert(QueryBuilderBase):
    def __init__(self, into_table: TableParam, db_type: DBTypes | None = None):
        super().__init__(_init_db_type(into_table, db_type))
        self._table = _get_table(into_table)

        self._column_names: list[str] = []
        self._values_list: list[Sequence[Value]] = []


    def set_columns_from_table(self):
        self._column_names = [c.name for c in self._table.columns_list]
        if not self._column_names:
            raise QueryBuilderException(f"Table {self._table.identifier} does not have columns")
        return self

    def columns(self, *column_names: str):
        self._column_names = column_names
        return self

    def values(self, *pos_values, **kw_values):
        if not self._column_names:
            raise QueryBuilderException("Please set column names first")

        if pos_values and kw_values:
            raise QueryBuilderException("Cannot use positional and keyword values together")

        if pos_values:
            if len(self._column_names) != len(pos_values):
                raise QueryBuilderException("Please provide the exact number of values")
            values = pos_values
        else:
            if set(self._column_names) != set(kw_values.keys()):
                raise QueryBuilderException("Column names do not match")
            values = [kw_values[cn] for cn in self._column_names]

        self._values_list.append([_try_value(v) for v in values])
        return self


    def to_sql(self) -> str:
        res = f'INSERT INTO {self._table} ({', '.join(f'"{cn}"' for cn in self._column_names)}) VALUES\n'
        res += ',\n'.join(f'({', '.join(str(v) for v in values)})' for values in self._values_list)
        return res


class Update(QueryBuilderBase):
    def __init__(self, update_table: TableParam, db_type: DBTypes | None = None):
        super().__init__(_init_db_type(update_table, db_type))
        self._table = _get_table(update_table)

        self._where: list[Term] = []
        self._values: dict[str, Value] = {}

    def where(self, condition):
        _check_term(condition)
        self._where.append(condition)
        return self

    def set(self, **kw_values):
        for k, v in kw_values.items():
            if self._table.columns and k not in self._table.columns:
                raise QueryBuilderException(f'Column "{k}" does not exist on table {self._table.identifier}')
            if k in self._values:
                raise QueryBuilderException(f"Column {k} already set")
            self._values[k] = _try_value(v)
        return self

    def to_sql(self) -> str:
        if not self._where:
            raise QueryBuilderException("Cannot use UPDATE without WHERE clause")

        res = f'UPDATE {self._table} SET\n'
        res += ',\n'.join(f'"{cn}" = {value}' for cn, value in self._values.items())
        res += '\nWHERE' + '\nAND '.join(f'({str(w)})' for w in self._where)
        return res


class Delete(QueryBuilderBase):
    def __init__(self, from_table: TableParam, db_type: DBTypes | None = None):
        super().__init__(_init_db_type(from_table, db_type))
        self._table = _get_table(from_table)

        self._where: list[Term] = []

    def where(self, condition):
        _check_term(condition)
        self._where.append(condition)
        return self

    def to_sql(self) -> str:
        if not self._where:
            raise QueryBuilderException("Cannot use DELETE without WHERE clause")

        res = f'DELETE FROM {self._table} WHERE\n'
        res += '\nAND '.join(f'({str(w)})' for w in self._where)
        return res


class And(Term):
    def __init__(self, *terms):
        _check_terms(terms)
        self.terms = terms

    def to_sql(self):
        return ' AND '.join(str(terms) for terms in self.terms)


class Or(Term):
    def __init__(self, *terms):
        _check_terms(terms)
        self.terms = terms

    def to_sql(self):
        return ' OR '.join(str(terms) for terms in self.terms)


class Function(Term):
    def __init__(self, function_name: str, *parameters, alias: str | None = None):
        self.function_name = function_name
        self.parameters = [_try_term(p) for p in parameters]
        self.alias = alias

    def to_sql(self):
        res = f'{self.function_name}({', '.join(str(p) for p in self.parameters)})'
        if self.alias is not None:
            res += f' "{self.alias}"'
        return res


class Cast(Term):
    def __init__(self, term, newtype: str):
        _check_term(term)
        self.term = term
        self.newtype = newtype

    def to_sql(self):
        return f'CAST({self.term} AS {self.newtype})'


class Tuple(Term):
    def __init__(self, *terms):
        if not terms:
            raise QueryBuilderException("Tuple cannot be empty")
        _check_terms(terms)
        self.terms = terms

    def to_sql(self):
        if len(self.terms) == 1:
            return str(self.terms[0])
        return f'({', '.join(str(term) for term in self.terms)})'


class Any(Term):
    def __init__(self, *terms):
        if not terms:
            raise QueryBuilderException("Any cannot be empty")
        _check_terms(terms)
        self.terms = terms

    def to_sql(self):
        return f'ANY({', '.join(str(term) for term in self.terms)})'


class SubQuery(TableBase):
    def __init__(self, sub: Select | str, alias: str | None = None):
        super().__init__(alias)
        self.sub = sub

    @property
    def identifier(self) -> str:
        if self.alias is None:
            raise QueryBuilderException("SubQuery does not have identifier. Please supply an alias")
        return self.alias

    def to_sql(self):
        res = f'(\n{self.sub}\n)'
        if self.alias is not None:
            res += f' {self.alias}'
        return res


class Unnest(TableBase):
    def __init__(self, *array_column_list: Term, alias: str | None = None, column_names: list[str] | None = None):
        super().__init__(alias)
        self.arrays_list = array_column_list
        if column_names is not None:
            if self.alias is None:
                raise QueryBuilderException("Cannot add columns if not alias is specified")
            if len(array_column_list) != len(column_names):
                raise QueryBuilderException("Please provide the same number of column names as there are arrays")
            for cn in column_names:
                self.add_column(cn)

    @property
    def identifier(self) -> str:
        if self.alias is None:
            raise QueryBuilderException("UNNEST function does not have identifier. Please supply an alias")
        return self.alias

    def to_sql(self) -> str:
        res = f'UNNEST({', '.join(str(array_col) for array_col in self.arrays_list)})'
        if self.alias is not None:
            res += f' AS {self.alias}'
            if self.columns_list:
                res += f'({', '.join(str(c.name) for c in self.columns_list)})'
        return res



class Exists(Term):
    def __init__(self, subselect: Select):
        self.subquery = subselect

    def to_sql(self):
        return f'EXISTS(\n{self.subquery}\n)'
