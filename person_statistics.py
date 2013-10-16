import MySQLdb

host = 'localhost'
user = 'teseo'
password = 'teseo'
database='teseo'
conn = MySQLdb.Connection(db=database, host=host, user=user, passwd=password)
cursor = conn.cursor()

cursor.execute('select count(*) from person;')
total_persons = cursor.fetchall()[0][0]

#cursor.execute('select count(distinct name) from person;')
#total_distinct_persons = cursor.fetchall()[0][0]

regex = '^((de(l?|([[:space:]]+la))|san)[[:space:]])?[[:alpha:]-]+([[:space:]]+((de(l?|([[:space:]]+la))|san)[[:space:]])?[[:alpha:]-]+)?[[:space:]]*,[[:space:]]+[[:alpha:][:space:]\.-]+$'

cursor.execute("select count(*) from person where name like '%,%';")
total_persons_with_comma = cursor.fetchall()[0][0]

cursor.execute("select count(*) from person where lower(name) regexp '%s';" % regex)
total_persons_matched = cursor.fetchall()[0][0]

#print 'Distinct persons: %.2f' % (total_distinct_persons / float(total_persons) * 100)

cursor.execute("select count(*) from person where name like '%%,%%' and lower(name) not regexp '%s';" % regex)
total_missing_persons = cursor.fetchall()[0][0]

print "select name from person where name like '%%,%%' and lower(name) not regexp '%s' limit 10;" % regex

print 'Persons with comma: %.2f' % (total_persons_with_comma / float(total_persons) * 100)
print '\t Matching: %.2f' % (total_persons_matched / float(total_persons_with_comma) * 100)
print '\t Missing: %.2f' % (total_missing_persons / float(total_persons_with_comma) * 100)

print ''
print 'Total missing: %.2f' % ((total_persons - total_persons_with_comma + total_missing_persons) / float(total_persons) * 100)
