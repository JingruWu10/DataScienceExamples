#Why: User pysql and pandas to create and load a db, and use it.
#Where:  https://courses.thinkful.com/data-001v2/project/1.3.3

#SF# To do, add sys library and accept used input

import sqlite3 as sql
import pandas as pd
##SF## New library
import sys

if len(sys.argv)==1:
    month = "July"
elif len(sys.argv)==2:
    month = sys.argv[1]
else:
    month = sys.argv[1]
    print "Additional parameters ignored"

# Sanitize the string
month = month.capitalize()

print "Selected month: ", month

cities = (
	('New York City','NY'),
	('Boston','MA'),
	('Chicago','IL'),
	('Miami', 'FL'),
    ('Dallas', 'TX'),
    ('Seattle', 'WA'),
    ('Portland', 'OR'),
    ('San Francisco', 'CA'),
    ('Los Angeles', 'CA'),
    ('Washington', 'DC'),
    ('Houston', 'TX'),
    ('Las Vegas',' NV'),
    ('Atlanta','GA'))

weather = (
	('New York City','2013','July','January','62'),
	('Boston','2013','July','January','59'),
	('Chicago','2013','July','January','59'),
	('Miami', '2013','August','January','84'),
    ('Dallas', '2013','July','January','77'),
    ('Seattle', '2013','July','January','61'),
    ('Portland', '2013','July','December','63'),
    ('San Francisco', '2013','September','December','64'),
    ('Los Angeles', '2013','September','December','75'),
    ('Washington', '2013','July','January','63'),  #value interpreted
    ('Houston', '2013','July','January','77') ,    #value interpreted
    ('Las Vegas',' 2013','July','December','88'),	  #value interpreted
    ('Atlanta','2013','July','January','82'))		  #value interpreted

#connect to the data base
con = sql.connect('getting_started.db')

with con:
	cur = con.cursor()
        #SF# Try to explain why you're doing this, it'll make easier to reuse your code!
        # Avoid conflict if table cities already exist by deleting it
	cur.execute("DROP TABLE IF EXISTS cities;")
	cur.execute("CREATE TABLE cities (name text, state text);")
        # Avoid conflict if table cities already exist by deleting it
	cur.execute("DROP TABLE IF EXISTS weather;")
	cur.execute("CREATE TABLE weather (city text, year integer, warm_month text, cold_month text, average_high integer);")
        # Populate the database
	cur.executemany("INSERT INTO cities VALUES(?,?)", cities)
	cur.executemany("INSERT INTO weather VALUES(?,?,?,?,?)", weather)
        #SF# Notice how you can break lines so it can be read
	"""
	query = "SELECT name, state, year,warm_month,cold_month,average_high \
                 FROM cities INNNER JOIN weather ON name=city \
                 GROUP BY city HAVING warm_month=='%s'" %month
	print query
	cur.execute(query)
	# cur.execute("SELECT name,state")
	rows = cur.fetchall()
	cols = [desc[0] for desc in cur.description]
        """	
	
#SF# Now you're ready with the answer, there's no need to keep in the "with con:" loop
#df = pd.DataFrame(rows, columns=cols)

#connect to the data base
with sql.connect('getting_started.db') as con:
    cur = con.cursor()
    # Get the cities where the warmest month is July
    cur.execute("SELECT name, state \
                 FROM cities INNNER JOIN weather ON name=city \
                 GROUP BY city HAVING warm_month=='%s'" %month )
    # cur.execute("SELECT name,state")
    cities_and_states = cur.fetchall()

if len(cities_and_states)>0:
    cities_coma_states = [c+" ("+s+")" for (c,s) in cities_and_states]
    formated_answer = ", ".join(cities_coma_states[:-1]) + " and " + cities_coma_states[-1]
    print('The cities that are warmest in {0} are: {1}'.format(month, formated_answer))
else:
    print('No city is warmest in {0}'.format(month))

#SF# Hope you like the answers. There's some really advanced python there, so don't get disapointed.
#SF# You'll get that in no time. The string.join method is really powerful on strings.
#SF# Also, list comprehensions are one of the coolest features in python.
