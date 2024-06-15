import flask_package.models 
from flask_package import app, db, bcrypt
from sqlalchemy import text
import datetime

def test_register_user():

    '''Tests that a User is created and added to the database'''

    with app.app_context():
        hashed_password = bcrypt.generate_password_hash("test")
        test_user = flask_package.models.User(
            date="2024-06-11",
            username="meara.corey.test",
            email="meara.corey.test@gmail.com",
            password=hashed_password
        )
        db.session.add(test_user)
        assert db.session.commit()
        '''select_users = text("select * from user")
        assert (
        7, 
        datetime.date(2024, 6, 11), 
        'whitney.corey.test', 
        'whitney.corey.test@gmail.com',
        '$2b$12$nO2nGyJXPwRqstcRqPzlQe5nLRfvTy35paUVGl66.xpaNwwCuXAPq',
        'default.jpg'
        ) in db.session.execute(select_users).fetchall()'''

def test_chore():

    '''Tests that a chore is created and added to the database'''

    with app.app_context():
        test_chore = flask_package.models.Chore(
            chore="Clean Room Test",
            completed="\U0001F636",
            frequency="Weekly",
            username="meara.corey.test"
        )
        db.session.add(test_chore)
        assert db.session.commit()
        '''select_chores = text("select * from chores")
        assert (
            95, 
            "Clean Room Test", 
            "\U0001F636",
            "Weekly",
            "whitney.corey.test"
            ) in db.session.execute(select_chores).fetchall()'''
