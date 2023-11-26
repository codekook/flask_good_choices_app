from flask import Flask
from logging import DEBUG
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt 

app = Flask(__name__)

app.secret_key = b'/\xeb~\xd7\xca(%\xf7'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

app.logger.setLevel(DEBUG)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from flask_package import routes
