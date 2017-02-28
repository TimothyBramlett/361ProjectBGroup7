# imports the flask library
import flask


# instantiates a Flask object named app
# passing in the special variable __name__
app = flask.Flask(__name__)
# sets the 'SECRET_KEY' of the app
app.config['SECRET_KEY'] = 'secret!'


# creates the default route of the web application
@app.route('/', methods=['GET', 'POST']) # The acceptable HTTP methods for this
def index():
    return flask.render_template('index.html')
    # renders the 'index.html' file stored in the templates directory


if __name__ == '__main__':
    # This is a special convention in python that causes the app.run function
    # to only be executed if this file is being run directly
    app.run(host='0.0.0.0', debug=False, port=8080)
    # with cloud9 we have to run the app on port 8080



