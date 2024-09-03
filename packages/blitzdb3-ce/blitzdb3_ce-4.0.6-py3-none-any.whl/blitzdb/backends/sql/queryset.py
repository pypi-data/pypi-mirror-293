
from sqlalchemy import select, func, asc, desc
from sqlalchemy.orm import Query

class QuerySet:
    def __init__(self, session, cls):
        self.session = session
        self.cls = cls
        self._query = session.query(cls)

    def filter(self, *criterion):
        self._query = self._query.filter(*criterion)
        return self

    def order_by(self, *order_by):
        self._query = self._query.order_by(*order_by)
        return self

    def all(self):
        return self._query.all()

    def count(self):
        return self._query.count()

    def first(self):
        return self._query.first()

    def limit(self, limit):
        self._query = self._query.limit(limit)
        return self

    def offset(self, offset):
        self._query = self._query.offset(offset)
        return self

    def __iter__(self):
        return iter(self._query)
