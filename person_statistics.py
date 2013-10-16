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

regex_comma_simple_surnames = '^[[:alpha:]-]+[[:space:]]+[[:alpha:]-]+,[[:space:]]+[[:alpha:][:space:]\.-]+$'
regex_command_one_surname = '^[[:alpha:]-]+,[[:space:]]+[[:alpha:][:space:]\.-]+$'

cursor.execute("select count(*) from person where name like '%,%';")
total_persons_with_comma = cursor.fetchall()[0][0]

cursor.execute("select count(*) from person where name regexp '%s';" % regex_comma_simple_surnames)
total_persons_with_comma_simple_surnames = cursor.fetchall()[0][0]

cursor.execute("select count(*) from person where name regexp '%s';" % regex_command_one_surname)
total_persons_with_comma_one_surname = cursor.fetchall()[0][0]

#print 'Distinct persons: %.2f' % (total_distinct_persons / float(total_persons) * 100)

cursor.execute("select count(*) from person where name like '%%,%%' and name not regexp '%s' and name not regexp '%s';" % (regex_comma_simple_surnames, regex_command_one_surname))
missing_persons_with_comma = cursor.fetchall()[0][0]

print 'Persons with comma: %.2f' % (total_persons_with_comma / float(total_persons) * 100)
print '\t Persons with comma and simple surnames: %.2f' % (total_persons_with_comma_simple_surnames / float(total_persons_with_comma) * 100)
print '\t Persons with comma and one surname: %.2f' % (total_persons_with_comma_one_surname / float(total_persons_with_comma) * 100)
print '\t Persons with comma missing: %.2f' % (missing_persons_with_comma / float(total_persons_with_comma) * 100)

print ''
print 'Total missing: %.2f' % ((total_persons - total_persons_with_comma + missing_persons_with_comma) / float(total_persons) * 100)
