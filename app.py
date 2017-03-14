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
# validate that date1 is before date2
# need to validate the date is valid first
# (returns True if date1 is before or same as date 2, otherwise False)
def dateBeforeDate(date1, date2):
    dateRegex = re.compile(r'(\d\d\d\d)-(\d\d)-(\d\d)')
    matchObj1 = dateRegex.search(date1)
    matchObj2 = dateRegex.search(date2)
    try:
        dateOneYear = int(matchObj1.group(1))
        dateOneMonth = int(matchObj1.group(2))
        dateOneDay = int(matchObj1.group(3))
        dateTwoYear = int(matchObj2.group(1))
        dateTwoMonth = int(matchObj2.group(2))
        dateTwoDay = int(matchObj2.group(3))
        if dateOneYear > dateTwoYear:
            return False
        if dateOneYear < dateTwoYear:
            return True
        # if this far dateOneYear is equal to dateTwoYear
        if dateOneMonth > dateTwoMonth:
            return False
        if dateOneMonth < dateTwoMonth:
            return True
        # if this far dateOneMonth is equal dateTwoMonth and years are equal
        if dateOneDay > dateTwoDay:
            return False
        if dateOneDay <= dateTwoDay:
            return True
    except:
        return False

    return False

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
            bus_id = crsr.fetchone()
            if bus_id is None:
                cnxn.close()
                return 'usernotfound', 403

            #-------------------------------------------------------------------
            if flask.request.method == 'GET':
                pass

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
                        flask.flash('All fields must be filled in. Sorry, no blanks allowed!')
                        return flask.redirect(flask.url_for('bus_console', form_name = name, form_category = category, form_volume = volume, form_units = units, form_quantity = quantity, form_sellby = sellby, form_bestby = bestby, form_expiration = expiration))

                    if (len(quantity) == 0 or len(sellby) == 0 or len(bestby) == 0 or len(expiration) == 0):
                        cnxn.close()
                        flask.flash('All fields must be filled in. Sorry, no blanks allowed!')
                        return flask.redirect(flask.url_for('bus_console', form_name = name, form_category = category, form_volume = volume, form_units = units, form_quantity = quantity, form_sellby = sellby, form_bestby = bestby, form_expiration = expiration))

                    if (not volumeIsValid(volume)):
                        cnxn.close()
                        flask.flash('Volume must be greater than 0!')
                        return flask.redirect(flask.url_for('bus_console', form_name = name, form_category = category, form_volume = volume, form_units = units, form_quantity = quantity, form_sellby = sellby, form_bestby = bestby, form_expiration = expiration))

                    if (not quantityIsValid(quantity)):
                        cnxn.close()
                        flask.flash('Quantity must be and integer and greater than 0!')
                        return flask.redirect(flask.url_for('bus_console', form_name = name, form_category = category, form_volume = volume, form_units = units, form_quantity = quantity, form_sellby = sellby, form_bestby = bestby, form_expiration = expiration))

                    if (not dateIsValid(sellby)):
                        cnxn.close()
                        flask.flash('Dates should be YYYY-MM-DD')
                        return flask.redirect(flask.url_for('bus_console', form_name = name, form_category = category, form_volume = volume, form_units = units, form_quantity = quantity, form_sellby = sellby, form_bestby = bestby, form_expiration = expiration))

                    if (not dateIsValid(bestby)):
                        cnxn.close()
                        flask.flash('Dates should be YYYY-MM-DD')
                        return flask.redirect(flask.url_for('bus_console', form_name = name, form_category = category, form_volume = volume, form_units = units, form_quantity = quantity, form_sellby = sellby, form_bestby = bestby, form_expiration = expiration))

                    if (not dateIsValid(expiration)):
                        cnxn.close()
                        flask.flash('Dates should be YYYY-MM-DD')
                        return flask.redirect(flask.url_for('bus_console', form_name = name, form_category = category, form_volume = volume, form_units = units, form_quantity = quantity, form_sellby = sellby, form_bestby = bestby, form_expiration = expiration))

                    if (not dateBeforeDate(sellby,bestby)):
                        cnxn.close()
                        flask.flash('Sell by date should be on or before best by date')
                        return flask.redirect(flask.url_for('bus_console', form_name = name, form_category = category, form_volume = volume, form_units = units, form_quantity = quantity, form_sellby = sellby, form_bestby = bestby, form_expiration = expiration))
                
                    if (not dateBeforeDate(bestby,expiration)):
                        cnxn.close()
                        flask.flash('Best by date should be on or before expiration date')
                        return flask.redirect(flask.url_for('bus_console', form_name = name, form_category = category, form_volume = volume, form_units = units, form_quantity = quantity, form_sellby = sellby, form_bestby = bestby, form_expiration = expiration))
                
                    # going to make sure this solves it.
                    #bus_id = user
                
                    cnxn.execute('INSERT INTO foodlosses (name, category, volume, units, quantity, sellby, bestby, expiration, bus_id) VALUES (?,?,?,?,?,?,?,?,?)',
                        (name, category, volume, units, quantity, sellby, bestby, expiration, bus_id[0]))
                    cnxn.commit()
                    cnxn.close()
                    #flask.flash('Item Successfully added!')
                    return flask.redirect(flask.url_for('bus_console'))
                
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
                            flask.flash('op cancelled - no rows added - invalid record found: ' + str(row))
                            return flask.redirect(flask.url_for('bus_console'))

                        if all (k in row for k in ('name', 'category', 'volume', 'units', 'quantity', 'sellby', 'bestby', 'expiration')):
                            # all required fields were found
                            pass
                        else:
                            flask.flash('Operation canceled, No rows added, invalid record found: ' + str(row))
                            return flask.redirect(flask.url_for('bus_console'))

                        if (len(row['name']) == 0 or len(row['category']) == 0 or len(row['volume']) == 0 or len(row['units']) == 0):
                            cnxn.close()
                            flask.flash('Operation canceled, No rows added, invalid record found: ' + str(row))
                            return flask.redirect(flask.url_for('bus_console'))
                            
                        if (len(row['quantity']) == 0 or len(row['sellby']) == 0 or len(row['bestby']) == 0 or len(row['expiration']) == 0):
                            cnxn.close()
                            flask.flash('Operation canceled, No rows added, invalid record found: ' + str(row))
                            return flask.redirect(flask.url_for('bus_console'))

                        if (not volumeIsValid(row['volume'])):
                            cnxn.close()
                            flask.flash('Operation canceled, No rows added, invalid record found (Volume must be greater than zero): ' + str(row))
                            return flask.redirect(flask.url_for('bus_console'))

                        if (not quantityIsValid(row['quantity'])):
                            cnxn.close()
                            flask.flash('Operation canceled, No rows added, invalid record found (Quantity must be an integer and greater than zero): ' + str(row))
                            return flask.redirect(flask.url_for('bus_console'))

                        if (not dateIsValid(row['sellby'])):
                            cnxn.close()
                            flask.flash('Operation canceled, No rows added, invalid record found (dates should be YYYY-MM-DD): ' + str(row))
                            return flask.redirect(flask.url_for('bus_console'))

                        if (not dateIsValid(row['bestby'])):
                            cnxn.close()
                            flask.flash('Operation canceled, No rows added, invalid record found (dates should be YYYY-MM-DD): ' + str(row))
                            return flask.redirect(flask.url_for('bus_console'))

                        if (not dateIsValid(row['expiration'])):
                            cnxn.close()
                            flask.flash('Operation canceled, No rows added, invalid record found (dates should be YYYY-MM-DD): ' + str(row))
                            return flask.redirect(flask.url_for('bus_console'))
                        
                        if (not dateBeforeDate(row['sellby'],row['bestby'])):
                            cnxn.close()
                            flask.flash('Operation canceled, No rows added, Sell by date should be on or before best by date: ' + str(row))
                            return flask.redirect(flask.url_for('bus_console'))
                
                        if (not dateBeforeDate(row['bestby'],row['expiration'])):
                            cnxn.close()
                            flask.flash('Operation canceled, No rows added, Best by date should be on or before expiration date: ' + str(row))
                            return flask.redirect(flask.url_for('bus_console'))

                    inStream.seek(0)
                    insertData = []
                    firstRow = True
                    for row in csvData:
                        if firstRow:
                            firstRow = False
                            continue
                        #-------------------------------------------------------
                        # build list of tuples for insertion
                        print(row)
                        rowData = (row['name'], row['category'], row['volume'], row['units'], row['quantity'], row['sellby'], row['bestby'], row['expiration'], bus_id[0])
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
        crsr.execute('SELECT id FROM beneficiaries WHERE username=?', (user,))
        ben_id = crsr.fetchone()
        cnxn.execute('INSERT INTO preferences (kosh, glut, vegan, ovoveg, lactoveg, lactoovoveg, pesc, peanut, tree, milk, egg, wheat, soy, fish, shellfish, sesame, ben_id) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
            (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ben_id[0]))
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
# return particular business in database table 'business' for EXISTING SESSION
# https://projectbgroup7dev-timbram.c9users.io/bus_info
# takes no parameters
class BusInfo(Resource):     
    def get(self):
        cnxn = sqlite3.connect(db_name)
        crsr = cnxn.cursor()
        crsr.execute('SELECT name,addr,city,state,zip FROM businesses WHERE username=?', (flask.session['username'],))
        result = crsr.fetchone()
        cnxn.close()
        return result, 200
api.add_resource(BusInfo, '/bus_info')

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
# return particular beneficiarie in database table 'beneficiaries' for EXISTING SESSION
# https://projectbgroup7dev-timbram.c9users.io/ben_info
# takes no parameters
class BenInfo(Resource):     
    def get(self):
        cnxn = sqlite3.connect(db_name)
        crsr = cnxn.cursor()
        crsr.execute('SELECT first,last,addr,city,state,zip,famsize FROM beneficiaries WHERE username=?', (flask.session['username'],))
        result = crsr.fetchone()
        cnxn.close()
        return result, 200
api.add_resource(BenInfo, '/ben_info')

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
# https://projectbgroup7dev-timbram.c9users.io/food_loss_all
# takes no parameters
class FoodLossesAll(Resource):     
    def get(self):
        cnxn = sqlite3.connect(db_name)
        crsr = cnxn.cursor()
        crsr.execute('SELECT * FROM foodlosses')
        result = crsr.fetchall()
        cnxn.close()
        return result, 200
api.add_resource(FoodLossesAll, '/food_loss_all')

#-------------------------------------------------------------------------------
# return list of items in database table 'foodlosses' for a particular business
# https://projectbgroup7dev-timbram.c9users.io/food_loss
# takes no parameters
class FoodLosses(Resource):     
    def get(self):
        if 'username' in flask.session:
            # connect to the db
            cnxn = sqlite3.connect(db_name)
            crsr = cnxn.cursor()
            
            # get the business id
            user = flask.session['username']
            crsr.execute('SELECT id FROM businesses WHERE username=?', (user,))
            bus_id = crsr.fetchone()
            if bus_id is None:
                bus_id = -1
            print(bus_id)

            crsr.execute('SELECT id, name, category, volume, units, quantity, sellby, bestby, expiration FROM foodlosses WHERE bus_id=?', bus_id)
            result = crsr.fetchall()
            cnxn.close()
            return result, 200
        else: 
            return 'You are not logged in', 401
api.add_resource(FoodLosses, '/food_loss')

#-------------------------------------------------------------------------------
# return list of items in database table 'preferences'
# https://projectbgroup7dev-timbram.c9users.io/preferences_all
# takes no parameters
class PreferencesAll(Resource):     
    def get(self):
        cnxn = sqlite3.connect(db_name)
        crsr = cnxn.cursor()
        crsr.execute('SELECT * FROM preferences')
        result = crsr.fetchall()
        cnxn.close()
        return result, 200
api.add_resource(PreferencesAll, '/preferences_all')

#-------------------------------------------------------------------------------
# return list of items in database table 'preferences' for a particular beneficiary
# https://projectbgroup7dev-timbram.c9users.io/preferences
# takes no parameters
class Preferences(Resource):     
    def get(self):
        if 'username' in flask.session:
            # connect to the db
            cnxn = sqlite3.connect(db_name)
            crsr = cnxn.cursor()
            
            # get the beneficiary id
            user = flask.session['username']
            crsr.execute('SELECT id FROM beneficiaries WHERE username=?', (user,))
            ben_id = crsr.fetchone()
            if ben_id is None:
                ben_id = -1

            crsr.execute('SELECT kosh, glut, vegan, ovoveg, lactoveg, lactoovoveg, pesc, peanut, tree, milk, egg, wheat, soy, fish, shellfish, sesame FROM preferences WHERE ben_id=' + str(ben_id[0]))
            result = crsr.fetchall()
            cnxn.close()
            return result, 200
        else: 
            return 'You are not logged in', 401
api.add_resource(Preferences, '/preferences')

#-------------------------------------------------------------------------------
# updates record in database table 'preferences' for a particular beneficiary
# https://projectbgroup7dev-timbram.c9users.io/save_preferences
# takes no parameters
class SavePreferences(Resource):     
    def post(self):
        if 'username' in flask.session:
            # connect to the db
            cnxn = sqlite3.connect(db_name)
            crsr = cnxn.cursor()
            
            # get the beneficiary id
            user = flask.session['username']
            crsr.execute('SELECT id FROM beneficiaries WHERE username=?', (user,))
            ben_id = crsr.fetchone()
            if ben_id is None:
                ben_id = -1
            print("ben_id=" + str(ben_id[0]))

            kosh = flask.request.form['kosh']
            glut = flask.request.form['glut']
            vegan = flask.request.form['vegan']
            ovoveg = flask.request.form['ovoveg']
            lactoveg = flask.request.form['lactoveg']
            lactoovoveg = flask.request.form['lactoovoveg']
            pesc = flask.request.form['pesc']
            peanut = flask.request.form['peanut']
            tree = flask.request.form['tree']
            milk = flask.request.form['milk']
            egg = flask.request.form['egg']
            wheat = flask.request.form['wheat']
            soy = flask.request.form['soy']
            fish = flask.request.form['fish']
            shellfish = flask.request.form['shellfish']
            sesame = flask.request.form['sesame']

            query = 'UPDATE preferences SET '
            query += 'kosh=?, glut=?, vegan=?, ovoveg=?, lactoveg=?, lactoovoveg=?, pesc=?, '
            query += 'peanut=?, tree=?, milk=?, egg=?, wheat=?, soy=?, fish=?, shellfish=?, sesame=? WHERE ben_id=?'
            #print(query)
            crsr.execute(query, (kosh, glut, vegan, ovoveg, lactoveg, lactoovoveg, pesc, peanut, tree, milk, egg, wheat, soy, fish, shellfish, sesame, ben_id[0]))
            #crsr.execute('UPDATE preferences SET kosh=1 WHERE ben_id=1')
            cnxn.commit()
            #print(crsr.fetchall())
            cnxn.close()
            return 'success!', 200
        else: 
            return 'You are not logged in', 401
api.add_resource(SavePreferences, '/save_preferences')

#-------------------------------------------------------------------------------
# DANGER DANGER DANGER DANGER DANGER DANGER DANGER DANGER DANGER DANGER DANGER
# deletes item from database table (takes item id and table name)
# https://projectbgroup7dev-timbram.c9users.io/delete_item_from_table
# DANGER DANGER DANGER DANGER DANGER DANGER DANGER DANGER DANGER DANGER DANGER
class DeleteItem(Resource):
    def post(self):
        item_id = flask.request.form['item_id']
        tablename = flask.request.form['tablename']

        # connect to the db
        cnxn = sqlite3.connect(db_name)
        print('item_id=' + item_id)
        print('tablename=' + tablename)
        cnxn.execute('DELETE FROM ' + tablename + ' WHERE id=?', (item_id,))
        cnxn.commit()
        cnxn.close()
        return 'success!', 200
api.add_resource(DeleteItem, '/delete_item_from_table')
# DANGER DANGER DANGER DANGER DANGER DANGER DANGER DANGER DANGER DANGER DANGER

#-------------------------------------------------------------------------------
# DANGER DANGER DANGER DANGER DANGER DANGER DANGER DANGER DANGER DANGER DANGER
# deletes all items from database table (takes table name)
# https://projectbgroup7dev-timbram.c9users.io/delete_all_items_from_table
# DANGER DANGER DANGER DANGER DANGER DANGER DANGER DANGER DANGER DANGER DANGER
class DeleteAllItems(Resource):
    def post(self):
        tablename = flask.request.form['tablename']

        # connect to the db
        cnxn = sqlite3.connect(db_name)
        cnxn.execute('DELETE FROM ' + tablename)
        cnxn.commit()
        cnxn.close()
        return 'success!', 200
api.add_resource(DeleteAllItems, '/delete_all_items_from_table')
# DANGER DANGER DANGER DANGER DANGER DANGER DANGER DANGER DANGER DANGER DANGER

#-------------------------------------------------------------------------------
if __name__ == '__main__':
    # This is a special convention in python that causes the app.run function
    # to only be executed if this file is being run directly
    
    run_port = int(sys.argv[1]) # The second argument being passed to the script by the os
                                # filename is first
    app.run(host='0.0.0.0', debug=False, port=run_port)
    # with cloud9 we have to run the app on port 8080



