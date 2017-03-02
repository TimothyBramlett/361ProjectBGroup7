# imports the flask library
import flask
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps

#Create a engine for connecting to SQLite3.
e = create_engine('sqlite:///grocery_upc.sql3')

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


# test it out by visting:  https://projectbgroup7dev-timbram.c9users.io/print_message/hello    
@app.route('/print_message/<message>')
def print_message(message):
    return 'You sent the message: {}'.format(message) # only sends back raw text (no HTML)
    
  
  
# https://projectbgroup7dev-timbram.c9users.io/grocery_upc_list  
class Products(Resource):
    def get(self):
        #Connect to databse
        conn = e.connect()
        #Perform query and return JSON data
        query = conn.execute("SELECT * FROM grocery_upc_list")
        return {'grocery_upc_list': [i for i in query.cursor.fetchall()]}

api.add_resource(Products, '/grocery_upc_list')



if __name__ == '__main__':
    # This is a special convention in python that causes the app.run function
    # to only be executed if this file is being run directly
    app.run(host='0.0.0.0', debug=False, port=8080)
    # with cloud9 we have to run the app on port 8080



