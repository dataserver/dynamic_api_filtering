import re
from datetime import datetime

import pytz
from helper import literalquery, local_date
from sqlalchemy import Column, Integer, String, column, inspect, or_
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql.expression import Select, select

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    nickname = Column(String)
    day_of_birth = Column(String)
    city = Column(String)
    phone = Column(String)
    timestamp = Column(Integer)
    created_at = Column(String, nullable=False, default=local_date)
    updated_at = Column(String, onupdate=local_date)


class DynamicFilteringBase:
    """
    Dynamic API filtering using query parameters

    Base Select Statement builder for all models
    """

    def __init__(self, model, args, ignore_empty: bool = True) -> None:
        """
        model SQLAlchemy model
        args  dict
        ignore_empty  bool  ignore parameteres with empty value.
        """
        self._model = model
        self.req_args = args
        self.ignore_empty = ignore_empty
        self._params = {}
        self._stmt = select(model)
        self._get_columns()
        self._get_data_types()
        if not isinstance(args, dict):
            self._args = dict(args)
        self._args = args

    def _get_columns(self) -> None:
        inst = inspect(self._model)
        self.attr_names = [c_attr.key for c_attr in inst.mapper.column_attrs]

    def stmt(self) -> Select:
        return self._stmt

    def params(self):
        return self._params

    def _get_data_types(self):
        """
        return dictionary with column name as key and data type as value
        """
        d = {}
        for c in self._model.__table__.columns:
            d[str(c.name)] = str(c.type)
        self.columns_types = d

    def query_base(self) -> None:
        # table columns
        for key in self._args:
            key = key
            value = self._args[key]

            if value == "" and self.ignore_empty:
                continue

            result = re.match(
                r"(?P<c_name>[a-za-zA-Z0-9_]+)\[(?P<operator>[a-z]{0,})\]", key
            )
            if result is not None:
                if result["c_name"] in self.attr_names:
                    c_name = result["c_name"]
                    operator = str(result["operator"]).lower()

                    if operator == "eq" or operator == "equals":
                        self._stmt = self._stmt.where(column(c_name) == value)
                    elif operator == "ne" or operator == "not_equals":
                        self._stmt = self._stmt.where(column(c_name) != value)

                    elif operator == "qt" or operator == "greater_than":
                        self._stmt = self._stmt.where(column(c_name) > value)
                    elif operator == "gte" or operator == "greater_than_equals":
                        self._stmt = self._stmt.where(column(c_name) >= value)

                    elif operator == "lt" or operator == "less_than":
                        self._stmt = self._stmt.where(column(c_name) < value)
                    elif operator == "lte" or operator == "less_than_equals":
                        self._stmt = self._stmt.where(column(c_name) <= value)

                    elif operator == "in":
                        items = value if value != "" else None
                        if items is not None:
                            if isinstance(items, str):
                                items = items.split(",")
                                if self.columns_types[c_name] == "INTEGER":
                                    items = [int(i) for i in items]
                            elif isinstance(items, list):
                                items = items
                            self._stmt = self._stmt.where(column(c_name).in_(items))

                    elif operator == "notin":
                        items = value if value != "" else None
                        if items is not None:
                            if isinstance(items, str):
                                items = items.split(",")
                                if self.columns_types[c_name] == "INTEGER":
                                    items = [int(i) for i in items]
                            elif isinstance(items, list):
                                items = items
                            self._stmt = self._stmt.where(column(c_name).not_in(items))

                    elif operator == "between":
                        result = re.match(r"^(?P<v1>.+)[:|](?P<v2>.+)$", value)
                        if result is not None:
                            v1 = result["v1"]
                            v2 = result["v2"]
                            if self.columns_types[c_name] == "INTEGER":
                                v1 = int(v1)
                            if self.columns_types[c_name] == "INTEGER":
                                v2 = int(v2)
                            self._stmt = self._stmt.where(
                                column(c_name).between(v1, v2)
                            )

                    elif operator == "like":
                        search = "{}".format(value)
                        self._stmt = self._stmt.where(column(c_name).like(search))
                    elif operator == "ilike":
                        search = "{}".format(value)
                        self._stmt = self._stmt.where(column(c_name).ilike(search))

                    elif operator == "contains":
                        search = "%{}%".format(value)
                        self._stmt = self._stmt.where(column(c_name).like(search))
                    elif operator == "icontains":
                        search = "%{}%".format(value)
                        self._stmt = self._stmt.where(column(c_name).ilike(search))
                    elif operator == "startswith":
                        search = "{}%".format(value)
                        self._stmt = self._stmt.where(column(c_name).like(search))
                    elif operator == "istartswith":
                        search = "{}%".format(value)
                        self._stmt = self._stmt.where(column(c_name).ilike(search))
                    elif operator == "endswith":
                        search = "%{}".format(value)
                        self._stmt = self._stmt.where(column(c_name).like(search))
                    elif operator == "iendswith":
                        search = "%{}".format(value)
                        self._stmt = self._stmt.where(column(c_name).ilike(search))

                    elif operator == "isnull":
                        self._stmt = self._stmt.where(column(c_name).is_(None))
                    elif operator == "isnotnull":
                        self._stmt = self._stmt.where(column(c_name).is_not(None))

                    self._params[key] = value
            else:
                if key in self.attr_names:
                    if value != "":
                        self._stmt = self._stmt.where(column(key) == value)
                        self._params[key] = value

        ### order by, limit and offset
        order_by = self._args["order_by"] if "order_by" in self._args else None
        if order_by is not None:
            if order_by in self.attr_names:
                self._stmt = self._stmt.order_by(column(order_by))
                self._params["order_by"] = order_by

        limit = self._args["limit"] if "limit" in self._args else None
        if limit is not None:
            limit = int(limit) if int(limit) > 0 else 50
            self._stmt = self._stmt.limit(int(limit))
            self._params["limit"] = limit

        start = self._args["start"] if "start" in self._args else None
        if start is not None:
            start = int(start) if start else 0
            self._stmt = self._stmt.offset(int(start))
            self._params["start"] = start

        offset = self._args["offset"] if "offset" in self._args else None
        if offset is not None:
            offset = int(offset) if offset else 0
            self._stmt = self._stmt.offset(int(offset))
            self._params["offset"] = offset


class UserQueryBuilder(DynamicFilteringBase):
    def __init__(self, args, ignore_empty: bool = True) -> None:
        super().__init__(User, args, ignore_empty)
        self.query_base()
        self.query()

    def query(self) -> None:
        # Add some custom query parameters NOT in the table column
        # This is the same param[notin] but it's here as example
        exclude = self._args["exclude"] if "exclude" in self._args else ""
        exclude = exclude if exclude != "" else None
        if exclude is not None:
            exclude = exclude.split(",")
            if isinstance(exclude, list) and len(exclude) > 0:
                self._stmt = self._stmt.where(column("id").not_in(exclude))
                self._params["exclude"] = exclude


def main():
    """
    note query string parameters have values as string.
    """
    args = {
        "name[ilike]": "john",
        "phone": "123456",
    }
    query = UserQueryBuilder(args)
    print(literalquery(query.stmt()))
    # output:
    # SELECT users.id, users.name, users.fullname, users.nickname, users.day_of_birth, users.city, users.phone, users.created_at, users.updated_at
    # FROM users
    # WHERE lower(name) LIKE lower('john') AND phone = '123456'

    args = {
        "phone": "",
        "city[ilike]": "New York",
    }
    query = UserQueryBuilder(args, ignore_empty=True)
    print(literalquery(query.stmt()))
    # output:
    # SELECT users.id, users.name, users.fullname, users.nickname, users.day_of_birth, users.city, users.phone, users.created_at, users.updated_at
    # FROM users
    # WHERE lower(city) LIKE lower('New York')

    args = {
        "day_of_birth[startswith]": "2001",
    }
    query = UserQueryBuilder(args)
    print(literalquery(query.stmt()))
    # output:
    # SELECT users.id, users.name, users.fullname, users.nickname, users.day_of_birth, users.city, users.phone, users.created_at, users.updated_at
    # FROM users
    # WHERE day_of_birth LIKE '2001%'

    args = {
        "id[notin]": "1,2,3",
    }
    query = UserQueryBuilder(args)
    print(literalquery(query.stmt()))
    # SELECT users.id, users.name, users.fullname, users.nickname, users.day_of_birth, users.city, users.phone, users.created_at, users.updated_at
    # FROM users
    # WHERE (id NOT IN (1, 2, 3))

    args = {
        "timestamp[between]": "1640525719:1672061719",
    }
    query = UserQueryBuilder(args)
    print(literalquery(query.stmt()))
    # output:
    # SELECT users.id, users.name, users.fullname, users.nickname, users.day_of_birth, users.city, users.phone, users.created_at, users.updated_at
    # FROM users
    # WHERE timestamp BETWEEN 1640525719 AND 1672061719

    args = {
        "city[isnull]": "1",  # in this case value is irrelevante but just add some value
    }
    query = UserQueryBuilder(args)
    print(literalquery(query.stmt()))
    # output:
    # SELECT users.id, users.name, users.fullname, users.nickname, users.day_of_birth, users.city, users.phone, users.created_at, users.updated_at
    # FROM users
    # WHERE city IS NULL

    args = {
        "city[]": "1",  # [] empty is ignored
    }
    query = UserQueryBuilder(args)
    print(literalquery(query.stmt()))
    # output:
    # SELECT users.id, users.name, users.fullname, users.nickname, users.day_of_birth, users.city, users.phone, users.created_at, users.updated_at
    # FROM users


if __name__ == "__main__":
    main()
