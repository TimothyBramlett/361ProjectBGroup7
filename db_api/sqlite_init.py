import csv
import os
import sqlite3

#db_name = 'grocery_upc.sql3'

# remove db if it exists because want to start fresh
#if os.path.exists(db_name):
#    os.remove(db_name)

# this will create a new db of db_name and open the connection
#cnxn = sqlite3.connect(db_name)
#crsr = cnxn.cursor()

# read contents of csv file into list
#with open('grocery_upc_database.csv') as inFil:
    # csv.DictReader uses first line in file for column headings by default
#    dr = csv.DictReader(inFil) # comma is default delimiter
    #for i in dr:
    #    print (i)
#    to_db = [(i['grp_id'], i['upc14'], i['upc12'], i['brand'], i['name']) for i in dr]

# insert list contents into table called 'grocery_upc_list'
#crsr.execute('''CREATE TABLE grocery_upc_list 
#    (grp_id int, upc14 text, upc12 text, brand text, name text)''')
#crsr.executemany('''INSERT INTO grocery_upc_list
#    (grp_id,upc14,upc12,brand,name) VALUES (?, ?, ?, ?, ?);''', to_db)
#cnxn.commit()

# close the connection to the database
#cnxn.close()







db_name = 'project.sql3'

# remove db if it exists because want to start fresh
if os.path.exists(db_name):
    os.remove(db_name)

# this will create a new db of db_name and open the connection
cnxn = sqlite3.connect(db_name)
crsr = cnxn.cursor()

crsr.execute('''CREATE TABLE businesses 
    (id INTEGER NOT NULL PRIMARY KEY, name text, addr text, city text, state text, zip text, password text)''')
crsr.execute('''CREATE TABLE users 
    (id INTEGER NOT NULL PRIMARY KEY, name text, addr text, city text, state text, zip text, famsize int, password text)''')


# close the connection to the database
cnxn.close()
