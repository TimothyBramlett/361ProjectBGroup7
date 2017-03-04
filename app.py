# imports the flask library
import flask
from flask_restful import Resource, Api
from json import dumps
import sqlite3
import sys

# instantiates a Flask object named app
# passing in the special variable __name__
app = flask.Flask(__name__)
# sets the 'SECRET_KEY' of the app
app.config['SECRET_KEY'] = 'secret!'

api = Api(app)

# default route
# test it out by visting: https://projectbgroup7dev-timbram.c9users.io/
# creates the default route of the web application
@app.route('/', methods=['GET', 'POST']) # The acceptable HTTP methods for this
def index():
    return flask.render_template('index.html')
    # renders the 'index.html' file stored in the templates directory

# registration route
# test it out by visting: https://projectbgroup7dev-timbram.c9users.io:8081/registration
# creates the registration route of the web application
@app.route('/registration', methods=['GET', 'POST']) # The acceptable HTTP methods for this
def registration():
    return flask.render_template('registration.html')
    # renders the 'registration.html' file stored in the templates directory

# login route
# test it out by visting: https://projectbgroup7dev-timbram.c9users.io:8081/login
# creates the login route of the web application
@app.route('/login', methods=['GET', 'POST']) # The acceptable HTTP methods for this
def login():
    return flask.render_template('login.html')
    # renders the 'login.html' file stored in the templates directory

# test it out by visting:  https://projectbgroup7dev-timbram.c9users.io/print_message/hello    
@app.route('/print_message/<message>')
def print_message(message):
    return 'You sent the message: {}'.format(message) # only sends back raw text (no HTML)
    


db_name = 'project.sql3'

# add one business to the database in table 'businesses'
# https://projectbgroup7dev-timbram.c9users.io/bus_register
# takes 5 key/value pairs in POST (not in URL like GET) x-www-form-urlencoded
# keys are 'name', 'addr', 'city', 'state', 'zip'
class RegBusiness(Resource):
    def post(self):
        cnxn = sqlite3.connect(db_name)
        name = flask.request.form['name']
        addr = flask.request.form['addr']
        city = flask.request.form['city']
        state = flask.request.form['state']
        zip = flask.request.form['zip']
        cnxn.execute('INSERT INTO businesses (name, addr, city, state, zip) VALUES (?,?,?,?,?)', (name, addr, city, state, zip))
        cnxn.commit()
        return 'success!'
        cnxn.close()
api.add_resource(RegBusiness, '/bus_register')

# return list of business in database table 'businesses'
# https://projectbgroup7dev-timbram.c9users.io/bus_list
# takes no parameters
class ListBusiness(Resource):     
    def get(self):
        cnxn = sqlite3.connect(db_name)
        crsr = cnxn.cursor()
        crsr.execute('SELECT * FROM businesses ORDER BY zip')
        retVal = crsr.fetchall()
        cnxn.close()
        return retVal 
api.add_resource(ListBusiness, '/bus_list')

if __name__ == '__main__':
    # This is a special convention in python that causes the app.run function
    # to only be executed if this file is being run directly
    
    run_port = int(sys.argv[1]) # The second argument being passed to the script by the os
                                # filename is first
    app.run(host='0.0.0.0', debug=False, port=run_port)
    # with cloud9 we have to run the app on port 8080



