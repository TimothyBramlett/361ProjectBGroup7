import csv
import os
import sqlite3

db_name = 'project.sql3'

# remove db if it exists because want to start fresh
if os.path.exists(db_name):
    os.remove(db_name)

# this will create a new db of db_name and open the connection
cnxn = sqlite3.connect(db_name)
crsr = cnxn.cursor()

crsr.execute('''CREATE TABLE businesses 
    (id INTEGER NOT NULL PRIMARY KEY, name text, addr text, city text, state text, zip text, username text, password text)''')
crsr.execute('''CREATE TABLE beneficiaries
    (id INTEGER NOT NULL PRIMARY KEY, first text, last text, addr text, city text, state text, zip text, famsize int, username text, password text)''')
crsr.execute('''CREATE TABLE foodlosses 
    (id INTEGER NOT NULL PRIMARY KEY, name text, category text, volume real, units text, quantity integer, sellby text, bestby text, expiration text, bus_id integer, FOREIGN KEY (bus_id) REFERENCES businesses(id))''')
crsr.execute('''CREATE TABLE preferences
    (id INTEGER NOT NULL PRIMARY KEY, kosh integer, glut integer, vegan integer, ovoveg integer, lactoveg integer, lactoovoveg integer, pesc integer, peanut integer, tree integer, milk integer, egg integer, wheat integer, soy integer, fish integer, shellfish integer, sesame integer, ben_id integer, FOREIGN KEY (ben_id) REFERENCES beneficiaries(id))''')

# close the connection to the database
cnxn.close()
