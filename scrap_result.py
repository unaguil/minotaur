# -*- coding: utf-8 -*-

import urllib
from bs4 import BeautifulSoup

URL = 'https://www.educacion.gob.es/teseo/mostrarRef.do?ref=1030824'

conn = urllib.urlopen(URL)

soup = BeautifulSoup(conn)

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
                print unicode(advisor.next).strip()
        elif key == u'Tribunal':
            #multiple values
            for panel_member in field.ul.find_all('li'):
                print unicode(panel_member.next).strip()
        elif key == u'Descriptores':
            #multiple values
            for descriptor in field.ul.find_all('li'):
                print unicode(descriptor.next).strip()
        elif key == u'Resumen':
            print unicode(identifier.next_sibling.next_sibling.next).strip()
        else:
            print unicode(identifier.next_sibling).strip()
        
conn.close()
