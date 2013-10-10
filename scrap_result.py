# -*- coding: utf-8 -*-

import urllib
from bs4 import BeautifulSoup

def clean_str(source_str):
    return unicode(source_str).strip()

URL = 'https://www.educacion.gob.es/teseo/mostrarRef.do?ref=1030824'

data = urllib.urlopen(URL)

soup = BeautifulSoup(data.read().decode('utf-8'))

data_section = soup.find_all('div', attrs={'class': 'datos-resultado'})

if len(data_section) != 1:
    print 'Error getting data section element'
    
for field in data_section[0].find_all('li'):
    identifier = field.strong
    if identifier is not None:
        key = unicode(identifier.next).strip().replace(':', '')
        
        print key       
        
        if key == u'Dirección':
            #multiple values
            for advisor in field.ul.find_all('li'):
                print clean_str(advisor.next)
        elif key == u'Tribunal':
            #multiple values
            for panel_member in field.ul.find_all('li'):
                print clean_str(panel_member.next)
        elif key == u'Descriptores':
            #multiple values
            for descriptor in field.ul.find_all('li'):
                print clean_str(descriptor.next)
        elif key == u'Resumen':
            print clean_str(identifier.next_sibling.next_sibling.next)
        else:
            print clean_str(identifier.next_sibling)
            
            
