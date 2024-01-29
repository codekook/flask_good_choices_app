"""Create the application, instantiate and configure the sqlite 
database passing in the app, instantiate Bcrypt for hashing the 
password and instantiate a login_manager object and pass in the app"""

from logging import DEBUG
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from dotenv import dotenv_values

app = Flask(__name__)

conf = dotenv_values(".env")

app.secret_key = conf["SECRET_KEY"]

app.config['SQLALCHEMY_DATABASE_URI'] = conf["DB_CONFIG"]

app.logger.setLevel(DEBUG)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from flask_package import routes
