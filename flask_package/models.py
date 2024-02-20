"""Creates the database schema for the sqlite database"""

from flask_login import UserMixin
from flask_package import db, login_manager

@login_manager.user_loader
def load_user(user_id):

    """Loads the appropriate user based on the user_id"""

    return User.query.get(int(user_id))

class User(db.Model, UserMixin):

    """Creates six columns for a User table in the sqlite database"""

    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Date, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    image_file = db.Column(db.String(20), nullable=False,
                           default='default.jpg')

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Chore(db.Model):

    """Creates four columns for a Chore table in the sqlite database"""

    __tablename__ = 'chores'
    chore_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    chore = db.Column(db.String(255), nullable=False)
    completed = db.Column(db.String(255), nullable=False)
    frequency = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"Chore('{self.chore_id}','{self.chore}', '{self.completed}', '{self.frequency}', '{self.username}')"
