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
db_name = 'project.sql3'

#-------------------------------------------------------------------------------
# default route
# test it out by visting: https://projectbgroup7dev-timbram.c9users.io/
# creates the default route of the web application
@app.route('/', methods=['GET']) # The acceptable HTTP methods for this
def index():
    return flask.render_template('index.html')
    # renders the 'index.html' file stored in the templates directory

#-------------------------------------------------------------------------------
# registration route
# test it out by visting: https://projectbgroup7dev-timbram.c9users.io:8081/registration
# creates the registration route of the web application
@app.route('/registration', methods=['GET']) # The acceptable HTTP methods for this
def registration():
    # GET Request, first check if the user is logged in already, redirect to console if so.
    # if not logged in then display the login form
    if 'username' in flask.session:
        #flask.flash('You were already logged in')
        if flask.session['usertype'] == 'bus':
            return flask.redirect(flask.url_for('bus_console'))
        elif flask.session['usertype'] == 'ben':
            return flask.redirect(flask.url_for('ben_console'))

    return flask.render_template('registration.html')
    # renders the 'registration.html' file stored in the templates directory

#-------------------------------------------------------------------------------
# login route
# test it out by visting: https://projectbgroup7dev-timbram.c9users.io:8081/login
# creates the login route of the web application
@app.route('/login', methods=['GET', 'POST']) # The acceptable HTTP methods for this
def login():
    if flask.request.method == 'POST':
        cnxn = sqlite3.connect(db_name)
        crsr = cnxn.cursor()
        user = flask.request.form['username']
        pwd = flask.request.form['password']
        
        # check if business
        crsr.execute('SELECT password FROM businesses WHERE username=?', (user,))
        result = crsr.fetchone()
        if result is not None and result[0] == pwd:
            cnxn.close()
            flask.session['username'] = user
            flask.session['usertype'] = 'bus'
            #flask.flash('You were successfully logged in')
            return flask.redirect(flask.url_for('bus_console'))

        # check if beneficiary
        crsr.execute('SELECT password FROM beneficiaries WHERE username=?', (user,))
        result = crsr.fetchone()
        if result is not None and result[0] == pwd:
            cnxn.close()
            flask.session['username'] = user
            flask.session['usertype'] = 'ben'
            #flask.flash('You were successfully logged in')
            return flask.redirect(flask.url_for('ben_console'))

        cnxn.close()
        flask.flash('Login Failed')
        return flask.redirect(flask.url_for('login'))
        # fall through indicates login failed 
        # return 'failed login'
    else:
        # GET Request, first check if the user is logged in already, redirect to console if so.
        # if not logged in then display the login form
        if 'username' in flask.session:
            #flask.flash('You were already logged in')
            if flask.session['usertype'] == 'bus':
                return flask.redirect(flask.url_for('bus_console'))
            elif flask.session['usertype'] == 'ben':
                return flask.redirect(flask.url_for('ben_console'))

        return flask.render_template('login.html')
        # renders the 'login.html' file stored in the templates directory
        
#-------------------------------------------------------------------------------
# logout route
@app.route('/logout', methods=['GET']) # The acceptable HTTP methods for this
def logout():
    # remove the username from the session if it's there
    flask.session.pop('username', None)
    flask.session.pop('userid', None)
    flask.session.pop('usertype', None)
    #flask.flash('You were successfully logged out')
    return flask.redirect(flask.url_for('index'))

#-------------------------------------------------------------------------------
# business console route
@app.route('/bus_console', methods=['GET']) # The acceptable HTTP methods for this
def bus_console():
    if 'username' in flask.session:
        if flask.session['usertype'] == 'bus':
            return flask.render_template('bus_console.html')

    return flask.redirect(flask.url_for('index'))

#-------------------------------------------------------------------------------
# beneficiary console route
@app.route('/ben_console', methods=['GET']) # The acceptable HTTP methods for this
def ben_console():
    if 'username' in flask.session:
        if flask.session['usertype'] == 'ben':
            return flask.render_template('ben_console.html')

    return flask.redirect(flask.url_for('index'))

#-------------------------------------------------------------------------------
# test it out by visting:  https://projectbgroup7dev-timbram.c9users.io/print_message/hello    
@app.route('/print_message/<message>')
def print_message(message):
    return 'You sent the message: {}'.format(message) # only sends back raw text (no HTML)
    
#-------------------------------------------------------------------------------
# add one business to the database in table 'businesses'
# https://projectbgroup7dev-timbram.c9users.io/bus_register
# takes key/value pairs in POST (not in URL like GET) x-www-form-urlencoded
class BusRegister(Resource):
    def post(self):
        cnxn = sqlite3.connect(db_name)
        crsr = cnxn.cursor()

        name = flask.request.form['name']
        addr = flask.request.form['addr']
        city = flask.request.form['city']
        state = flask.request.form['state']
        zip = flask.request.form['zip']
        if (len(name) == 0 or len(addr) == 0 or len(city) == 0 or len(state) == 0 or len(zip) == 0):
            cnxn.close()
            return 'noblanksallowed', 400
            
        # should probably also add integer check and 5-char check for zip

        user = flask.request.form['username']
        opas = flask.request.form['password']
        cpas = flask.request.form['confirm_password']
        if (len(user) == 0 or len(opas) == 0 or len(cpas) == 0):
            cnxn.close()
            return 'noblanksallowed', 400
        if (opas != cpas):
            cnxn.close()
            return 'passmismatch', 409
            
        crsr.execute('SELECT * FROM businesses WHERE username=?', (user,))
        result = crsr.fetchall()
        if len(result) > 0:
            cnxn.close()
            return 'usertaken', 409
    
        crsr.execute('SELECT * FROM beneficiaries WHERE username=?', (user,))
        result = crsr.fetchall()
        if len(result) > 0:
            cnxn.close()
            return 'usertaken', 409
    
        # shouldn't store or even send passwords as plain text but probably okay for this assignment
        cnxn.execute('INSERT INTO businesses (name, addr, city, state, zip, username, password) VALUES (?,?,?,?,?,?,?)',
            (name, addr, city, state, zip, user, opas))
        cnxn.commit()
        cnxn.close()
        return 'success!', 200
api.add_resource(BusRegister, '/bus_register')

#-------------------------------------------------------------------------------
# add one beneficiary to the database in table 'beneficiaries'
# https://projectbgroup7dev-timbram.c9users.io/ben_register
# takes key/value pairs in POST (not in URL like GET) x-www-form-urlencoded
class BenRegister(Resource):
    def post(self):
        cnxn = sqlite3.connect(db_name)
        crsr = cnxn.cursor()

        first = flask.request.form['first']
        last = flask.request.form['last']
        addr = flask.request.form['addr']
        city = flask.request.form['city']
        state = flask.request.form['state']
        zip = flask.request.form['zip']
        famsize = flask.request.form['famsize']

        if (len(first) == 0 or len(last) == 0 or len(addr) == 0 or len(city) == 0 or len(state) == 0 or len(zip) == 0 or famsize == 0):
            cnxn.close()
            return 'noblanksallowed', 400
            
        # should probably also add integer check and 5-char check for zip
        # should probably also add integer check for famsize
            
        user = flask.request.form['username']
        opas = flask.request.form['password']
        cpas = flask.request.form['confirm_password']
        if (len(user) == 0 or len(opas) == 0 or len(cpas) == 0):
            cnxn.close()
            return 'noblanksallowed', 400
        if (opas != cpas):
            cnxn.close()
            return 'passmismatch', 409
            
        crsr.execute('SELECT * FROM businesses WHERE username=?', (user,))
        result = crsr.fetchall()
        if len(result) > 0:
            cnxn.close()
            return 'usertaken', 409
    
        crsr.execute('SELECT * FROM beneficiaries WHERE username=?', (user,))
        result = crsr.fetchall()
        if len(result) > 0:
            cnxn.close()
            return 'usertaken', 409
    
        # shouldn't store or even send passwords as plain text but probably okay for this assignment
        cnxn.execute('INSERT INTO beneficiaries (first, last, addr, city, state, zip, famsize, username, password) VALUES (?,?,?,?,?,?,?,?,?)',
            (first, last, addr, city, state, zip, famsize, user, opas))
        cnxn.commit()
        cnxn.close()
        return 'success!', 200
api.add_resource(BenRegister, '/ben_register')

#-------------------------------------------------------------------------------
# return list of business in database table 'businesses'
# https://projectbgroup7dev-timbram.c9users.io/bus_list
# takes no parameters
class BusList(Resource):     
    def get(self):
        cnxn = sqlite3.connect(db_name)
        crsr = cnxn.cursor()
        crsr.execute('SELECT name,addr,city,state,zip,username FROM businesses')
        result = crsr.fetchall()
        cnxn.close()
        return result, 200
api.add_resource(BusList, '/bus_list')

#-------------------------------------------------------------------------------
# return list of business in database table 'businesses' (INCLUDING PASSWORDS)
# https://projectbgroup7dev-timbram.c9users.io/bus_list
# takes no parameters
class BusListFull(Resource):     
    def get(self):
        cnxn = sqlite3.connect(db_name)
        crsr = cnxn.cursor()
        crsr.execute('SELECT * FROM businesses')
        result = crsr.fetchall()
        cnxn.close()
        return result, 200
api.add_resource(BusListFull, '/bus_list_with_pass')

#-------------------------------------------------------------------------------
# return list of beneficiarie in database table 'beneficiaries'
# https://projectbgroup7dev-timbram.c9users.io/bus_list
# takes no parameters
class BenList(Resource):     
    def get(self):
        cnxn = sqlite3.connect(db_name)
        crsr = cnxn.cursor()
        crsr.execute('SELECT first,last,addr,city,state,zip,famsize,username FROM beneficiaries')
        result = crsr.fetchall()
        cnxn.close()
        return result, 200
api.add_resource(BenList, '/ben_list')

#-------------------------------------------------------------------------------
# return list of beneficiaries in database table 'beneficiaries' (INCLUDING PASSWORDS)
# https://projectbgroup7dev-timbram.c9users.io/bus_list
# takes no parameters
class BenListFull(Resource):     
    def get(self):
        cnxn = sqlite3.connect(db_name)
        crsr = cnxn.cursor()
        crsr.execute('SELECT * FROM beneficiaries')
        result = crsr.fetchall()
        cnxn.close()
        return result, 200
api.add_resource(BenListFull, '/ben_list_with_pass')

#-------------------------------------------------------------------------------
if __name__ == '__main__':
    # This is a special convention in python that causes the app.run function
    # to only be executed if this file is being run directly
    
    run_port = int(sys.argv[1]) # The second argument being passed to the script by the os
                                # filename is first
    app.run(host='0.0.0.0', debug=False, port=run_port)
    # with cloud9 we have to run the app on port 8080



