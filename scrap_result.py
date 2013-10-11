# -*- coding: utf-8 -*-

import urllib
import urllib2
import cookielib
from bs4 import BeautifulSoup
import cookielib
import re

from teseo_model import Thesis, Person, Descriptor, Department
from teseo_model import University, Advisor, PanelMember

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from datetime import datetime

cookies = cookielib.LWPCookieJar()
handlers = [
        urllib2.HTTPHandler(),
        urllib2.HTTPSHandler(),
        urllib2.HTTPCookieProcessor(cookies)
    ]
opener = urllib2.build_opener(*handlers)

def clean_str(source_str):
    return unicode(source_str).strip()
    
def extract_groups(source_str):
    matched = re.match(r'(.*?)\((.*?)\)', source_str, re.DOTALL)
    if matched is not None:
        return matched.groups()[0].strip(), matched.groups()[1].strip()
    return None, None
    
def scrap_data(data):
    soup = BeautifulSoup(data.read().decode('utf-8'))
    data_section = soup.find_all('div', attrs={'class': 'datos-resultado'})
    
    if len(data_section) != 1:
        raise Exception('Error getting data section element')
    
    thesis = Thesis()
    
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

    return thesis
    
def get_universities():
    page_url = 'https://www.educacion.gob.es/teseo/irGestionarConsulta.do'
    data = urllib.urlopen(page_url)
    soup = BeautifulSoup(data.read().decode('utf-8'))
    
    universities = {}
    for option in soup.find_all('option'):
        if not option['value'] == '0':
            universities[(clean_str(option.next))] = option['value']
        
    return universities
    
def request_theses(theses_ids):
    page_url = 'https://www.educacion.gob.es/teseo/mostrarSeleccion.do'
            
    selection = ''
    for thesis_id in theses_ids:
        selection = selection + '%s:' % thesis_id
    
    post_data = {'seleccionFichas': selection}
    
    post_data_encoded = urllib.urlencode(post_data)
    
    request_object = urllib2.Request(page_url, post_data_encoded)
    response = opener.open(request_object)
    
    page_url = 'https://www.educacion.gob.es/teseo/mostrarDetalle.do'
        
    theses = []
    for index in theses_ids:
        post_data = {'indice': index}
        
        post_data_encoded = urllib.urlencode(post_data)
        
        request_object = urllib2.Request(page_url, post_data_encoded)
        response = opener.open(request_object)
    
        thesis = scrap_data(response)
        theses.append(thesis)
    
    return theses
    
def get_theses(university_id, courseFrom, courseUntil, max_rpp = 5000, limit=None):
    page_url = 'https://www.educacion.gob.es/teseo/listarBusqueda.do'
    
    post_data = {
                'tipo': 'simple',
                'rpp': max_rpp,
                'titulo': '',
                'doctorando': '',
                'nif': '',
                'idUni': university_id,
                'cursoDesde': '%s' % courseFrom,
                'cursoDesde2': '%s' % (courseFrom + 1),
                'cursoHasta': '%s' % courseUntil,
                'cursoHasta2': '%s' % (courseUntil + 1) }
    
    post_data_encoded = urllib.urlencode(post_data)
    
    request_object = urllib2.Request(page_url, post_data_encoded)
    response = opener.open(request_object)
    
    soup = BeautifulSoup(response.read().decode('utf-8'))
    num_theses = len(soup.find_all('input', attrs = {'id': re.compile("\d+")}))
    
    retrieved_theses = min(limit, num_theses)
    
    print 'Retrieving %s theses of %s' % (retrieved_theses, num_theses)
    
    return request_theses(range(0, retrieved_theses))

URL = 'https://www.educacion.gob.es/teseo/mostrarRef.do?ref=1030824'
USER = 'teseo'
PASS = 'teseo'
DB_NAME = 'teseo'
engine = create_engine('mysql://%s:%s@localhost/%s?charset=utf8' % (USER, PASS, DB_NAME))
Session = sessionmaker(bind=engine)
session = Session()

for thesis in get_theses(1, 95, 95, limit=2):
    print thesis.title
