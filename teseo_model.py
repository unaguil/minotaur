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
    
    def __init__(self, name):
        self.name = name
    
class Descriptor(Base):
    __tablename__ = 'descriptor'
    
    id = Column(Integer, primary_key=True)
    text = Column(UnicodeText, nullable=False)
    
    def __init__(self, text):
        self.text = text

class Advisor(Base):
    __tablename__ = 'advisor'

    thesis_id = Column(Integer, ForeignKey('thesis.id'), primary_key=True)
    thesis = relationship("Thesis")
    
    person_id = Column(Integer, ForeignKey('person.id'), primary_key=True)
    person = relationship("Person")
    
    role = Column(UnicodeText, nullable=False)
    
    def __init__(self, person, role):
        self.person = person
        self.role = role
        
class PanelMember(Base):
    __tablename__ = 'panel_member'
    
    thesis_id = Column(Integer, ForeignKey('thesis.id'), primary_key=True)
    thesis = relationship("Thesis")
    
    person_id = Column(Integer, ForeignKey('person.id'), primary_key=True)
    person = relationship("Person")
    
    role = Column(UnicodeText, nullable=False)
    
    def __init__(self, person, role):
        self.person = person
        self.role = role

association_thesis_description = Table('association_thesis_description', 
    Base.metadata,
    Column('thesis_id', Integer, ForeignKey('thesis.id')),
    Column('descriptor_id', Integer, ForeignKey('descriptor.id'))
)        

class Thesis(Base):
    __tablename__ = 'thesis'
    
    id = Column(Integer, primary_key=True)
    title =  Column(UnicodeText, nullable=False)
    author = Column(UnicodeText, nullable=False)
    defense_date = Column(DateTime, nullable=False)
    
    university_id = Column(Integer, ForeignKey('university.id'))
    university = relationship("University")
    
    department_id = Column(Integer, ForeignKey('department.id'))
    department = relationship("Department")
    
    advisors = relationship("Advisor")
    panel = relationship("PanelMember")
    
    descriptors = relationship("Descriptor",
            secondary=association_thesis_description)
    
    summary = Column(UnicodeText)

if __name__ == '__main__':
    USER = 'teseo'
    PASS = 'teseo'
    
    DB_NAME = 'teseo'
    
    engine = create_engine('mysql://%s:%s@localhost/%s?charset=utf8' % (USER, PASS, DB_NAME))
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
