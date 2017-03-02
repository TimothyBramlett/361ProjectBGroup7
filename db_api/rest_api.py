# copied from here as a starting point (then heavily modified)
# https://impythonist.wordpress.com/2015/07/12/build-an-api-under-30-lines-of-code-with-python-and-flask/

from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps

#Create a engine for connecting to SQLite3.
e = create_engine('sqlite:///grocery_upc.sql3')

app = Flask(__name__)
api = Api(app)

class Products(Resource):
    def get(self):
        #Connect to databse
        conn = e.connect()
        #Perform query and return JSON data
        query = conn.execute("SELECT * FROM grocery_upc_list")
        return {'grocery_upc_list': [i for i in query.cursor.fetchall()]}

api.add_resource(Products, '/grocery_upc_list')


#
#class Departmental_Salary(Resource):
#    def get(self, department_name):
#        conn = e.connect()
#        query = conn.execute("select * from salaries where Department='%s'"%department_name.upper())
#        #Query the result and get cursor.Dumping that data to a JSON is looked by extension
#        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
#        return result
#        #We can have PUT,DELETE,POST here. But in our API GET implementation is sufficient
# 
#api.add_resource(Departmental_Salary, '/dept/<string:department_name>')

if __name__ == '__main__':
    # This is a special convention in python that causes the app.run function
    # to only be executed if this file is being run directly
    app.run(host='0.0.0.0', debug=False, port=8080)
    # with cloud9 we have to run the app on port 8080