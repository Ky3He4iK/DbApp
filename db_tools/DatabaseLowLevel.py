from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Union, Iterable, List, Callable, Type
import logging
import os
from typing import TypeVar

import mysql.connector

#  Сокращение некоторых внутренних типов
STR_OR_INT = Union[str, int]
STR_OR_ITER = Union[str, Iterable[str]]
STR_OR_INT_OR_ITER = Union[STR_OR_INT, Iterable[STR_OR_INT]]
T = TypeVar('T')  # generic variable


@dataclass
class TableInfo:
    name: str
    primary_keys: List[str]
    # foreign_keys: Optional[List[str, str, str]]  # # field name - origin table - origin name
    other_fields: List[str]
    primary_types: List[Type]
    other_types: List[Type]
    class_constructor: Optional[Callable[[List], object]] = None


# Развитие моей полуавтоматической ORM из роллбота [туда стырил наработки из бота очередей]
# по информации о классе и конструктору сам стоит запрос и все такое. Нужно только объект TableInfo подать
class DatabaseLowLevel:
    def __init__(self):
        if "MARIADB_USER" not in os.environ or "MARIADB_PASSWORD" not in os.environ:
            raise RuntimeError("`MARIADB_USER` or `MARIADB_PASSWORD` are not set")

        self._base: mysql.connector.MySQLConnection = mysql.connector.connect(
            host='localhost', user=os.environ.get("MARIADB_USER"),
            password=os.environ.get("MARIADB_PASSWORD"),
            database='plate_manufacturing'
        )

    def close(self):
        self._base.close()

    def commit(self):
        self._base.commit()

    # internal universal methods
    def set(self, obj: T, table_info: TableInfo) -> None:
        if self.contains(obj, table_info):
            return self.update(obj, table_info)
        self.insert(obj, table_info)

    def insert(self, obj: T, table_info: TableInfo) -> None:
        columns = table_info.primary_keys + table_info.other_fields
        fields = [getattr(obj, c) for c in columns]
        self._insert(table_info.name, columns, fields)

    def update(self, obj: T, table_info: TableInfo) -> None:
        f_columns = table_info.primary_keys
        f_fields = [getattr(obj, c) for c in f_columns]
        columns = table_info.other_fields
        fields = [getattr(obj, c) for c in columns]
        self._update(table_info.name, columns, fields, f_columns, f_fields)

    def contains(self, obj: T, table_info: TableInfo) -> bool:
        return self.get(obj, table_info) is not None

    def get(self, obj: T, table_info: TableInfo) -> Optional[T]:
        columns = table_info.primary_keys
        fields = [getattr(obj, c) for c in columns]
        res = self._select(table_info.name, columns, fields)
        if len(res) == 1 and table_info.class_constructor is not None:
            return table_info.class_constructor(*res[0])
        return None

    def filter(self, obj: T, table_info: TableInfo, order_by: Optional[str] = None) -> List[T]:
        fields_map = {c: getattr(obj, c) for c in table_info.primary_keys if getattr(obj, c) is not None}
        return self._create_list_objects(self._select(table_info.name, fields_map.keys(), fields_map.values(),
                                                      order_by=order_by), table_info)

    def search(self, obj: T, table_info: TableInfo, order_by: Optional[str] = None) -> List[T]:
        fields_map = {c: getattr(obj, c) for c in table_info.primary_keys if getattr(obj, c) is not None}
        fields_map.update({c: getattr(obj, c) for c in table_info.other_fields if getattr(obj, c) is not None})
        return self._create_list_objects(self._select(table_info.name, fields_map.keys(), fields_map.values(),
                                                      order_by=order_by), table_info)

    def get_all(self, table_info: TableInfo, order_by: Optional[str] = None) -> List[T]:
        return self._create_list_objects(self._select(table_info.name, None, None, order_by=order_by), table_info)

    def remove(self, obj: T, table_info: TableInfo) -> None:
        columns = table_info.primary_keys
        fields = [getattr(obj, c) for c in columns]
        return self._delete(table_info.name, columns, fields)

    @staticmethod
    def _create_list_objects(contents: Optional[List[Iterable]], table_info: TableInfo) -> List[T]:
        if table_info.class_constructor is None or contents is None:
            return []
        return list(map(lambda content: table_info.class_constructor(*content), contents))

    # выполнение SQL запроса
    # возвращает результат запроса
    def execute(self, query: str) -> Optional[List[tuple]]:
        try:
            with self._base.cursor() as cursor:
                cursor.execute(query)
                res = cursor.fetchall()
                self._base.commit()
            return res
        except Exception as e:
            logging.error('Error: {} ({}) caused by query `{}`'.format(e, type(e), query))
            return None

    # возвращает id последнего добавленного ряда (для таблиц с AUTOINCREMENT)
    # возможно, стоит просто смотреть на параметр lastrowid у запроса INSERT
    def get_last_selected_id(self) -> int:
        res = self.execute("SELECT last_insert_id()")
        if res is not None and len(res) > 0:
            return res[0][0]
        return -1

    def _select(self, table: Optional[str],
                filter_columns: Optional[STR_OR_ITER],
                filter_values: Optional[STR_OR_INT_OR_ITER],
                rest: str = "",
                select_columns: Optional[Iterable[str]] = None,
                order_by: Optional[str] = None
                ) -> List[tuple]:
        """
        выполнение запроса SELECT к БД - получение записей из таблицы
        параметры:
    table:              str                                                 название таблицы
    filter_columns:     str, int либо None                                  колонки, по которым будет фильтроваться
    filter_values:      str, int, либо итератор по (str|int) либо None      значения соответствующих колонок для фильра
    rest:               str                                                 дополнительный текст в конце запроса
    select_columns:     итератор либо None                                  колонки, которые возвращать
                                                                                (по умолчанию все)
        возвращает таблицу либо ее фрагмент (возможно, пустой)
        """

        # если select_columns не указан, то брать всё
        if select_columns is None:
            select_columns = '*'
        else:
            select_columns = "(" + ", ".join(select_columns) + ")"
        # первая часть запроса
        query = "SELECT " + select_columns
        if table is not None:
            query += " FROM " + table

        # если есть фильтрация, то добавить ее в запрос
        if filter_columns is not None:
            query += " WHERE " + self._construct_condition(filter_columns, filter_values)
        if order_by is not None:
            query += " ORDER BY " + self._to_str(order_by)
        query += rest

        return self.execute(query)

    def _insert(self,
                table: str,
                columns: Iterable[str],
                values: Iterable[STR_OR_INT]):
        """
        выполнение запроса INSERT к БД - добавление записи
        параметры:
    table:      str                     название таблицы
    columns:    итератор по str         колонки, в которые проходить вставка (должны быть указаны все колонки в таблице)
    values:     итератор по (str|int)   значение для каждой колонки
        возвращает успешность вставки
        """
        query = "INSERT INTO {} ({}) VALUES ({})".format(table, ", ".join(columns),
                                                         ", ".join(map(self._to_str, values)))
        self.execute(query)

    def _update(self,
                table: str,
                columns: STR_OR_ITER,
                values: STR_OR_INT_OR_ITER,
                filter_columns: Optional[STR_OR_ITER],
                filter_values: Optional[STR_OR_INT_OR_ITER]):
        """
        выполнение запроса UPDATE к БД - обновление отдельных полей записей
        параметры:
    table:              str                                     название таблицы
    columns:            str либо итератор по str                изменяемые колотки
    values:             str, int либо итератор по (str|int)     значение для каждой колонки
    filter_columns:     str, int                                колонки, по которым будет фильтроваться
    filter_values:      str, int, либо итератор по (str|int)    значения соответствующих колонок для фильра
        возвращает успешность обновления
        """
        query = "UPDATE {} SET {}".format(table, self._construct_condition(columns, values, ", "))
        if filter_columns is not None:
            query += " WHERE " + self._construct_condition(filter_columns, filter_values)
        self.execute(query)

    def _delete(self,
                table: str,
                filter_columns: Optional[STR_OR_ITER],
                filter_values: Optional[STR_OR_INT_OR_ITER]):
        """
        выполнение запроса DELETE к БД - удаление записей
        параметры:
    filter_columns:     str, int                                колонки, по которым будет фильтроваться
    filter_values:      str, int, либо итератор по (str|int)    значения соответствующих колонок для фильра
        возвращает количество удаленных записей
        """
        query = "DELETE FROM " + table
        if filter_columns is not None:
            query += " WHERE " + self._construct_condition(filter_columns, filter_values)
        self.execute(query)

    def _construct_condition(self,
                             filter_columns: STR_OR_ITER,
                             filter_values: STR_OR_INT_OR_ITER,
                             sep: str = " AND ") -> str:
        """
        построение условий для директивы WHERE (и не только)
        параметры:
    filter_columns:     str, int                                колонки, по которым будет фильтроваться
    filter_values:      str, int, либо итератор по (str|int)    значения соответствующих колонок для фильра
    sep                 str                                     разделитель. Для WHERE это " AND "
        возвращает строку с условием
        """
        # если только одна запись то всё просто
        if isinstance(filter_columns, str):
            return "{}={}".format(filter_columns, self._to_str(filter_values))
        # если это не список, то каст к нему
        if not isinstance(filter_columns, list) or not isinstance(filter_values, list):
            filter_columns, filter_values = map(list, [filter_columns, filter_values])  # convert iterable to list
        # и немного магии однострочников
        return sep.join(filter_columns[i] + "=" + self._to_str(filter_values[i]) for i in range(len(filter_columns)))

    @staticmethod
    def _to_str(val: STR_OR_INT) -> str:
        """
        преобразование аргумента в строку для SQL запроса
            (экранирование и оборачивание в кавычки строку и преобразование в строку для остальных)
    val:    str, int    аргумент
        Не-строки дополнительно кастуются к числу, потому что sqlite не умеет в bool знвчения
        """
        # int(val) converts bool to 0/1
        if isinstance(val, (int, bool)):
            return str(int(val))
        elif val is None:
            return "null"
        elif isinstance(val, str):
            return "'" + val.replace("'", "''") + "'"
        elif isinstance(val, datetime):
            return "'" + str(val) + "'"
        else:
            return str(val).replace("'", "''")
