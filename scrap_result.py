# -*- coding: utf-8 -*-

import urllib
from bs4 import BeautifulSoup
import re

def clean_str(source_str):
    return unicode(source_str).strip()
    
def extract_groups(source_str):
    matched = re.match(r'(.*?)\((.*?)\)', source_str, re.DOTALL)
    if matched is not None:
        return matched.groups()[0].strip(), matched.groups()[1].strip()
    return None, None

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
                name, position = extract_groups(clean_str(advisor.next))
                print '(%s) %s' % (position, name)
        elif key == u'Tribunal':
            #multiple values
            for panel_member in field.ul.find_all('li'):
                name, position = extract_groups(clean_str(panel_member.next))
                print '(%s) %s' % (position, name)
        elif key == u'Descriptores':
            #multiple values
            for descriptor in field.ul.find_all('li'):
                print clean_str(descriptor.next)
        elif key == u'Resumen':
            print clean_str(identifier.next_sibling.next_sibling.next)
        else:
            print clean_str(identifier.next_sibling)
            
            
