#!/usr/bin/python3

import sqlite3
import os

db_name = 'test_sqlite.db'

# remove db if it exists because want to start fresh
if os.path.exists(db_name):
    os.remove(db_name)
    
cnxn = sqlite3.connect(db_name)
crsr = cnxn.cursor()

# create table
crsr.execute('''CREATE TABLE businesses 
    (name text, street_addr text, city text, state real, zip int)''')

# insert rows
fms = [('Fred Meyer', '21045 Bothell Everett Hwy', 'Bothell', 'WA', 98012),
    ('Fred Meyer', '915 NW 45th St', 'Seattle', 'WA', 98107),
    ('Fred Meyer', '2041 148th Ave NE', 'Bellevue', 'WA', 98007),
    ('Fred Meyer', '365 Renton Center Way SW', 'Renton', 'WA', 98057),
    ]
crsr.executemany('INSERT INTO businesses VALUES (?,?,?,?,?)', fms)

# print records
for row in crsr.execute('SELECT * FROM businesses ORDER BY zip'):
    print (row)

cnxn.close()