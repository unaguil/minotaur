import MySQLdb
import sys
import re

host = 'localhost'
user = 'teseo'
password = 'teseo'
database='teseo'
conn = MySQLdb.Connection(db=database, host=host, user=user, passwd=password)
cursor = conn.cursor()

sql_regex = '^([[:space:]]*((de(l?|([[:space:]]+la))|san|la)[[:space:]]+)?[[:alpha:]-]+){1,2}[[:space:]]*,?[[:space:]]+[[:alpha:][:space:]\.-]+$'

pattern = re.compile('^(\s*(?:(?:de(?:l?|(?:\s+la))|san|la)\s+)?[\w-]+)(\s*(?:(?:de(?:l?|(?:\s+la))|san|la)\s+)?[\w-]+)?\s*,?\s+([\w\s\.-]+)$')

cursor.execute("select id, lower(name) from person where lower(name) regexp '%s';" % sql_regex)

result = cursor.fetchall()
total = len(result)
for (index, (id, name)) in enumerate(result):    
    match = re.search(pattern, name)
    if match:
        if match.group(1) is not None:
            first_surname = match.group(1).strip()
        else:
            first_surname = ''
        
        if match.group(2) is not None:
            second_surname = match.group(2).strip()    
        else:
            second_surname = ''
        
        if match.group(3) is not None:
            first_name = match.group(3).strip()
        else:
            first_name = ''
            
        cursor.execute("update person set first_name='%s', first_surname='%s', second_surname='%s' where id='%s'" % (first_name, first_surname, second_surname, id))

    sys.stdout.write('\r Processed %s of %s' % (index + 1, total))
    sys.stdout.flush()

conn.close()
