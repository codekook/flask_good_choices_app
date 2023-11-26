from flask import Flask
from logging import DEBUG
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.secret_key = b'/\xeb~\xd7\xca(%\xf7'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

app.logger.setLevel(DEBUG)

db = SQLAlchemy(app)

from flask_package import routes
