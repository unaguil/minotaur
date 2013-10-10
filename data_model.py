# -*- coding: utf-8 -*-

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import UnicodeText, DateTime, create_engine, Column
from sqlalchemy import Integer, ForeignKey, Table
from sqlalchemy.orm import relationship

Base = declarative_base()

class University(Base):
    __tablename__ = 'university'
    
    id = Column(Integer, primary_key=True)
    name = Column(UnicodeText, nullable=False)
    
    def __init__(self, name):
        self.name = name
    
class Department(Base):
    __tablename__ = 'department'
    
    id = Column(Integer, primary_key=True)
    name = Column(UnicodeText, nullable=False)
    
    def __init__(self, name):
        self.name = name
    
class Person(Base):
    __tablename__ = 'person'
    
    id = Column(Integer, primary_key=True)
    name = Column(UnicodeText, nullable=False)
    position = Column(UnicodeText, nullable=False)
    
    def __init__(self, name, position):
        self.name = name
        self.position = position
    
class Descriptor(Base):
    __tablename__ = 'descriptor'
    
    id = Column(Integer, primary_key=True)
    text = Column(UnicodeText, nullable=False)
    
    def __init__(self, text):
        self.text = text
        
association_table_thesis_advisor = Table('thesis_advisor', Base.metadata,
    Column('thesis_id', Integer, ForeignKey('thesis.id')),
    Column('advisor.id', Integer, ForeignKey('person.id'))
)

class Thesis(Base):
    __tablename__ = 'thesis'
    
    id = Column(Integer, primary_key=True)
    title =  Column(UnicodeText, nullable=False)
    author = Column(UnicodeText, nullable=False)
    defense_date = Column(DateTime, nullable=False)
    
    university = Column(Integer, ForeignKey('university.id'))
    department = Column(Integer, ForeignKey('department.id'))
    
    advisors = relationship("Person", 
        secondary=association_table_thesis_advisor)
    #panel = relationship("Person")
    #descriptors = relationship("Descriptor")
    
    summary = Column(UnicodeText, nullable=False)

if __name__ == '__main__':
    USER = 'teseo'
    PASS = 'teseo'
    
    DB_NAME = 'teseo'
    
    engine = create_engine('mysql://%s:%s@localhost/%s' % (USER, PASS, DB_NAME), echo=True)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
