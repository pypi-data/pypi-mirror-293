
from sqlalchemy import create_engine, Table, MetaData, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base, scoped_session
from sqlalchemy.ext.declarative import DeclarativeMeta
from contextlib import contextmanager

Base: DeclarativeMeta = declarative_base()

class SQLBackend:
    def __init__(self, database_url):
        self.engine = create_engine(database_url)
        self.Session = scoped_session(sessionmaker(bind=self.engine))
        self.metadata = MetaData(bind=self.engine)

    def create_tables(self):
        Base.metadata.create_all(self.engine)

    def drop_tables(self):
        Base.metadata.drop_all(self.engine)

    @contextmanager
    def transaction(self):
        session = self.Session()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def add(self, obj):
        with self.transaction() as session:
            session.add(obj)

    def delete(self, obj):
        with self.transaction() as session:
            session.delete(obj)

    def query(self, *args, **kwargs):
        with self.transaction() as session:
            return session.query(*args, **kwargs).all()

    def filter(self, model, *criterion):
        with self.transaction() as session:
            return session.query(model).filter(*criterion).all()
