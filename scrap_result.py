# -*- coding: utf-8 -*-

import urllib
from bs4 import BeautifulSoup
import re

from data_model import Thesis, Person, Descriptor, Department
from data_model import University, Advisor, PanelMember

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from datetime import datetime

def clean_str(source_str):
    return unicode(source_str).strip()
    
def extract_groups(source_str):
    matched = re.match(r'(.*?)\((.*?)\)', source_str, re.DOTALL)
    if matched is not None:
        return matched.groups()[0].strip(), matched.groups()[1].strip()
    return None, None
    
def scrap_page(page_url, university, session):
    thesis = Thesis()
    thesis.university = university
    
    for field in data_section[0].find_all('li'):
        identifier = field.strong
        if identifier is not None:
            key = unicode(identifier.next).strip().replace(':', '')
            
            if key == u'Dirección':
                #multiple values
                for advisor in field.ul.find_all('li'):
                    name, role = extract_groups(clean_str(advisor.next))
                    advisor = Advisor(Person(name), role)
                    thesis.advisors.append(advisor)                    
            elif key == u'Tribunal':
                #multiple values
                for panel_member in field.ul.find_all('li'):
                    name, role = extract_groups(clean_str(panel_member.next))
                    panelMember = PanelMember(Person(name), role)
                    thesis.panel.append(panelMember)
            elif key == u'Descriptores':
                #multiple values
                for descriptor in field.ul.find_all('li'):
                    text = clean_str(descriptor.next)
                    descriptor = session.query(Descriptor).filter_by(text=text).first()
                    if descriptor is None:
                        descriptor = Descriptor(text)
                    thesis.descriptors.append(descriptor)
            elif key == u'Resumen':
                thesis.summary = clean_str(identifier.next_sibling.next_sibling.next)            
            else:
                value = clean_str(identifier.next_sibling)
                if key == u'Título':
                    thesis.title = value
                elif key == u'Autor':
                    thesis.author = value
                elif key == u'Fecha de Lectura':
                    thesis.defense_date = datetime.strptime(value, '%d/%m/%Y')
                elif key == u'Departamento':
                    department = session.query(Department).filter_by(name=value).first()
                    if department is None:
                        department = Department(value)
                    thesis.department = department

    session.add(thesis)            
    session.commit()

URL = 'https://www.educacion.gob.es/teseo/mostrarRef.do?ref=1030824'
data = urllib.urlopen(URL)
soup = BeautifulSoup(data.read().decode('utf-8'))
data_section = soup.find_all('div', attrs={'class': 'datos-resultado'})

if len(data_section) != 1:
    print 'Error getting data section element'

USER = 'teseo'
PASS = 'teseo'
DB_NAME = 'teseo'
engine = create_engine('mysql://%s:%s@localhost/%s?charset=utf8' % (USER, PASS, DB_NAME))
Session = sessionmaker(bind=engine)
session = Session()

university = University('Deusto')

scrap_page(URL, university, session)
