
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

# Example of a SQLAlchemy ORM model with relationships

class Parent(Base):
    __tablename__ = 'parents'
    id = Column(Integer, primary_key=True)
    children = relationship("Child", back_populates="parent")

class Child(Base):
    __tablename__ = 'children'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('parents.id'))
    parent = relationship("Parent", back_populates="children")
