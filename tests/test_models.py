import flask_package.models 
from flask_package import app, bcrypt
import pytest 

@pytest.mark.skip(reason="need better mocking")
def test_register_user(db_session):

    '''Tests that a User is created and added to the database'''

    with app.app_context():

        hashed_password = bcrypt.generate_password_hash("test")
        test_user = flask_package.models.User(
            date="2024-06-11",
            username="jane.doe.test",
            email="jane.doe.test@gmail.com",
            password=hashed_password
            )
        db_session.add(test_user)
        assert db_session.commit()
        '''select_users = text("select * from user")
        assert (
        7, 
        datetime.date(2024, 6, 11), 
        'jane.doe.test', 
        'jane.doe.test@gmail.com',
        '$2b$12$nO2nGyJXPwRqstcRqPzlQe5nLRfvTy35paUVGl66.xpaNwwCuXAPq',
        'default.jpg'
        ) in db.session.execute(select_users).fetchall()'''

@pytest.mark.skip(reason="need better mocking")
def test_chore(db_session):

    '''Tests that a chore is created and added to the database'''

    with app.app_context():

        test_chore = flask_package.models.Chore(
            chore="Clean Room Test",
            completed="\U0001F636",
            frequency="Weekly",
            username="jane.doe.test"
            )
        db_session.add(test_chore)
        assert db_session.commit()
        '''select_chores = text("select * from chores")
        assert (
            95, 
            "Clean Room Test", 
            "\U0001F636",
            "Weekly",
            "jane.doe.test"
            ) in db.session.execute(select_chores).fetchall()'''
