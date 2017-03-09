# imports the flask library
import flask
from flask_restful import Resource, Api
from json import dumps
import sqlite3
import sys
import io
import csv
import sys
import re

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
# validate zip code (returns True if input is valid, otherwise False)
def zipIsValid(zip):
    zipRegex = re.compile(r'\d{5}')
    matchObj = zipRegex.search(zip)
    if matchObj is None or len(zip) != 5:
        return False
    else:
        return True

#-------------------------------------------------------------------------------
# validate state (returns True if input is valid, otherwise False)
def stateIsValid(state):
    states = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
              'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
              'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
              'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
              'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY',
              'DC', 'GU', 'PR', 'VI']
    stateRegex = re.compile(r'\b(' + '|'.join(states) + r')\b')
    matchObj = stateRegex.search(state)
    if matchObj is None or len(state) != 2:
        return False
    else:
        return True

#-------------------------------------------------------------------------------
# validate family size(returns True if input is valid, otherwise False)
def famsizeIsValid(famsize):
    famsizeRegex = re.compile(r'\d{1}')
    matchObj = famsizeRegex.search(famsize)
    if matchObj is None:
        return False
    try:
        if int(famsize) < 1 or int(famsize) > 20:
            return False
        else:
            return True
    except:
        return False
        
#-------------------------------------------------------------------------------
# validate that volume is a real number greater than zero        
# (returns True if input is valid, otherwise False)
def volumeIsValid(volume):
    try:
        if float(volume) > 0.0:
            return True
    except:
        pass
    return False

#-------------------------------------------------------------------------------
# validate that quantity is an int greater than zero        
# (returns True if input is valid, otherwise False)
def quantityIsValid(quantity):
    try:
        if int(quantity) > 0:
            return True
    except:
        pass
    return False

#-------------------------------------------------------------------------------
# validate that date is valid format YYYY-MM-DD
# simple - not getting into complex thousand year leap years, etc...
# (returns True if input is valid, otherwise False)
def dateIsValid(date):
    dateRegex = re.compile(r'(\d\d\d\d)-(\d\d)-(\d\d)')
    matchObj = dateRegex.search(date)
    if matchObj is None or len(date) != 10:
        return False
    try:
        if int(matchObj.group(1)) < 2016:
            # no years before 2016 allowed
            return False
        if int(matchObj.group(2)) < 1 or int(matchObj.group(2)) > 12:
            # bad month
            return False
        if int(matchObj.group(3)) < 1 or int(matchObj.group(3)) > 31:
            # bad day of month
            return False
    except:
        return False

    return True

#-------------------------------------------------------------------------------
# business console route
@app.route('/bus_console', methods=['GET', 'POST']) # The acceptable HTTP methods for this
def bus_console():
    if 'username' in flask.session:
        if flask.session['usertype'] == 'bus':
            # connect to the db
            cnxn = sqlite3.connect(db_name)
            crsr = cnxn.cursor()
            
            # get the business id
            user = flask.session['username']
            crsr.execute('SELECT id FROM businesses WHERE username=?', (user,))
            userid = crsr.fetchone()
            if userid is None:
                cnxn.close()
                return 'usernotfound', 403

            #-------------------------------------------------------------------
            if flask.request.method == 'GET':
                # we need to somehow populate a list of all existing records for this business
                pass #remove this when you add code to this section
                
            #-------------------------------------------------------------------
            elif flask.request.method == 'POST':
                
                #---------------------------------------------------------------
                if all (k in flask.request.form for k in ('name', 'category', 'volume', 'units', 'quantity', 'sellby', 'bestby', 'expiration')):
                    # this is a POST request from the manual input
                    # all required fields were found

                    name = flask.request.form['name']
                    category = flask.request.form['category']
                    volume = flask.request.form['volume']
                    units = flask.request.form['units']
                    quantity = flask.request.form['quantity']
                    sellby = flask.request.form['sellby']
                    bestby = flask.request.form['bestby']
                    expiration = flask.request.form['expiration']
                    if (len(name) == 0 or len(category) == 0 or len(volume) == 0 or len(units) == 0):
                        cnxn.close()
                        return 'noblanksallowed', 400
                    if (len(quantity) == 0 or len(sellby) == 0 or len(bestby) == 0 or len(expiration) == 0):
                        cnxn.close()
                        return 'noblanksallowed', 400
                        
                    if (not volumeIsValid(volume)):
                        cnxn.close()
                        return 'volume<=0: ' + str(row), 400

                    if (not quantityIsValid(quantity)):
                        cnxn.close()
                        return 'non-int >0 quantity: ' + str(row), 400

                    if (not dateIsValid(sellby)):
                        cnxn.close()
                        return 'dates should be YYYY-MM-DD: ' + str(row), 400

                    if (not dateIsValid(bestby)):
                        cnxn.close()
                        return 'dates should be YYYY-MM-DD: ' + str(row), 400

                    if (not dateIsValid(expiration)):
                        cnxn.close()
                        return 'dates should be YYYY-MM-DD: ' + str(row), 400
                
                    cnxn.execute('INSERT INTO foodlosses (name, category, volume, units, quantity, sellby, bestby, expiration, bus_id) VALUES (?,?,?,?,?,?,?,?,?)',
                        (name, category, volume, units, quantity, sellby, bestby, expiration, bus_id))
                    cnxn.commit()
                    cnxn.close()
                    return 'success!', 200
                
                #---------------------------------------------------------------
                else:
                    # this is (assumed to be) a POST request from the CSV input
                    inFil = flask.request.files['food_loss_csv_file']
                    if not inFil:
                        return 'filenotfound', 404
                    inStream = io.StringIO(inFil.stream.read().decode('UTF-8'))
                    csvData = csv.DictReader(inStream)
    
                    for row in csvData:
                        #-------------------------------------------------------
                        # validate in row of input data
                        if (len(row) != 8):
                            return 'op cancelled - no rows added - invalid record found: ' + str(row), 415

                        if all (k in row for k in ('name', 'category', 'volume', 'units', 'quantity', 'sellby', 'bestby', 'expiration')):
                            # all required fields were found
                            pass
                        else:
                            return 'op cancelled - no rows added - invalid record found: ' + str(row), 415

                        if (len(row['name']) == 0 or len(row['category']) == 0 or len(row['volume']) == 0 or len(row['units']) == 0):
                            cnxn.close()
                            return 'op cancelled - no rows added - invalid record found: ' + str(row), 415
                            
                        if (len(row['quantity']) == 0 or len(row['sellby']) == 0 or len(row['bestby']) == 0 or len(row['expiration']) == 0):
                            cnxn.close()
                            return 'op cancelled - no rows added - invalid record found: ' + str(row), 415

                        if (not volumeIsValid(row['volume'])):
                            cnxn.close()
                            return 'op cancelled - no rows added - invalid record found - volume<=0: ' + str(row), 415

                        if (not quantityIsValid(row['quantity'])):
                            cnxn.close()
                            return 'op cancelled - no rows added - invalid record found - non-int >0 quantity: ' + str(row), 415

                        if (not dateIsValid(row['sellby'])):
                            cnxn.close()
                            return 'op cancelled - no rows added - invalid record found - dates should be YYYY-MM-DD: ' + str(row), 415

                        if (not dateIsValid(row['bestby'])):
                            cnxn.close()
                            return 'op cancelled - no rows added - invalid record found - dates should be YYYY-MM-DD: ' + str(row), 415

                        if (not dateIsValid(row['expiration'])):
                            cnxn.close()
                            return 'op cancelled - no rows added - invalid record found - dates should be YYYY-MM-DD: ' + str(row), 415

                    inStream.seek(0)
                    insertData = []
                    for row in csvData:
                        #-------------------------------------------------------
                        # build list of tuples for insertion
                        rowData = (row['name'], row['category'], row['volume'], row['units'], row['quantity'], row['sellby'], row['bestby'], row['expiration'], userid[0])
                        insertData.append(rowData)
    
                    try:
                        #-------------------------------------------------------
                        # insert the data into the db
                        crsr.executemany('INSERT INTO foodlosses (name, category, volume, units, quantity, sellby, bestby, expiration, bus_id) VALUES (?,?,?,?,?,?,?,?,?)', insertData)
                        cnxn.commit()
                    except sqlite3.Error as err:
                        cnxn.close()
                        return err.args[0], 500
    
                    cnxn.close()

            #-------------------------------------------------------------------
            else: # not GET or POST (can we even get here?)
                cnxn.close()
                
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

        if all (k in flask.request.form for k in ('name', 'addr', 'city', 'state', 'zip', 'username', 'password', 'confirm_password')):
            pass # all the args are included in the POST request
        else:
            return 'missing arguments', 400

        name = flask.request.form['name']
        addr = flask.request.form['addr']
        city = flask.request.form['city']
        state = flask.request.form['state']
        zip = flask.request.form['zip']
        if (len(name) == 0 or len(addr) == 0 or len(city) == 0 or len(state) == 0 or len(zip) == 0):
            cnxn.close()
            return 'noblanksallowed', 400
            
        if not zipIsValid(zip):
            return 'invalidzip', 400
        if not stateIsValid(state):
            return 'invalidstate', 400

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

        if all (k in flask.request.form for k in ('first', 'last', 'addr', 'city', 'state', 'zip', 'famsize', 'username', 'password', 'confirm_password')):
            pass # all the args are included in the POST request
        else:
            return 'missing arguments', 400

        first = flask.request.form['first']
        last = flask.request.form['last']
        addr = flask.request.form['addr']
        city = flask.request.form['city']
        state = flask.request.form['state']
        zip = flask.request.form['zip']
        famsize = flask.request.form['famsize']

        if (len(first) == 0 or len(last) == 0 or len(addr) == 0 or len(city) == 0 or len(state) == 0 or len(zip) == 0 or len(famsize) == 0):
            cnxn.close()
            return 'noblanksallowed', 400
            
        if not zipIsValid(zip):
            return 'invalidzip', 400
        if not stateIsValid(state):
            return 'invalidstate', 400
        if not famsizeIsValid(famsize):
            return 'invalidfamsize', 400

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
# https://projectbgroup7dev-timbram.c9users.io/bus_list_with_pass
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
# https://projectbgroup7dev-timbram.c9users.io/bus_list_with_pass
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
# return list of items in database table 'foodlosses'
# https://projectbgroup7dev-timbram.c9users.io/food_loss
# takes no parameters
class FoodLosses(Resource):     
    def get(self):
        cnxn = sqlite3.connect(db_name)
        crsr = cnxn.cursor()
        crsr.execute('SELECT * FROM foodlosses')
        result = crsr.fetchall()
        cnxn.close()
        return result, 200
api.add_resource(FoodLosses, '/food_loss')

#-------------------------------------------------------------------------------
if __name__ == '__main__':
    # This is a special convention in python that causes the app.run function
    # to only be executed if this file is being run directly
    
    run_port = int(sys.argv[1]) # The second argument being passed to the script by the os
                                # filename is first
    app.run(host='0.0.0.0', debug=False, port=run_port)
    # with cloud9 we have to run the app on port 8080



