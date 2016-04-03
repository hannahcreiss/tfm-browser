from flask import Flask, session
from flask.ext.session import Session


app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')

sess = Session()
app.debug = True


from views import *

if __name__ == '__main__':
    app.run()



