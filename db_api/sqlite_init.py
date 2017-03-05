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
crsr.execute('''CREATE TABLE f_loss 
    (id INTEGER NOT NULL PRIMARY KEY, name text, units text, amount integer, bus_id integer, FOREIGN KEY (bus_id) REFERENCES businesses(id))''')

# close the connection to the database
cnxn.close()
