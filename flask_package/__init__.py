"""Create the application, instantiate and configure the sqlite
database passing in the app, instantiate Bcrypt for hashing the
password and instantiate a login_manager object and pass in the app"""

from logging import DEBUG
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from dotenv import load_dotenv
import os

app = Flask(__name__)

load_dotenv()

<<<<<<< HEAD
app.secret_key = os.getenv("SECRET_KEY").encode(
    'utf-8', errors='replace').decode()

SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{username}:{password}@{hostname}:3306/{databasename}".format(
=======
app.secret_key = os.getenv("SECRET_KEY")

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
>>>>>>> 4677c1a8f4402d932cdc64f7cc1b1f9ccb82ace2
    username=os.getenv("USERNAME"),
    password=os.getenv("PASSWORD"),
    hostname=os.getenv("HOSTNAME"),
    databasename=os.getenv("DBNAME")
)

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_POOL_RECYCLE'] = 299
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = False

app.logger.setLevel(DEBUG)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from flask_package import routes
