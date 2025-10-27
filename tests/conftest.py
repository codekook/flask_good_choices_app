from flask_package import app, db, bcrypt
from sqlalchemy import create_engine
from flask_package.models import User
from datetime import date 
import pytest
import os

@pytest.fixture()
def test_app():
    app.config.update(
        TESTING=True)
    yield app

@pytest.fixture()
def client(test_app):
    return test_app.test_client()

@pytest.fixture()
def test_user(test_app):
    with test_app.app_context():
        existing_user = User.query.filter_by(email="test@example.com").first()
        if existing_user:
            db.session.delete(existing_user)
            db.session.commit()

        hashed_password = bcrypt.generate_password_hash("testpassword123")
        test_user = User(
            date=date.today(),
            username="testuser",
            email="test@example.com",
            password=hashed_password
        )
        db.session.add(test_user)
        db.session.commit()

        yield test_user

        db.session.delete(test_user)
        db.session.commit()

@pytest.fixture()
def auth_client(test_app, test_user):
    client = test_app.test_client()
    response = client.get("/login")
    csrf_token = response.data.decode().split('name="csrf_token" type="hidden" value="')[1].split('"')[0]

    client.post("/login", data={
        "email": test_user.email,
        "password":"testpassword123",
        "csrf_token":csrf_token})
    return client

@pytest.fixture()
def database():
    # Use environment variables for database connection
    username = os.getenv("USERNAME", "root")
    password = os.getenv("PASSWORD", "")
    hostname = os.getenv("HOSTNAME", "localhost:3306")
    dbname = os.getenv("TEST_DBNAME", os.getenv("DBNAME", "goodchoicesdb"))

    connection_string = f"mysql+pymysql://{username}:{password}@{hostname}/{dbname}?autocommit=true"
    engine = create_engine(connection_string)

    database = engine.connect()
    return database

@pytest.fixture()
def _db(database):
    return database

@pytest.fixture()
def affirmations_list():

    '''Provide the affirmations list''' 

    affirmations = [
        "Great job!",
        "Keep it up!",
        "Awesome!",
        "Thank you for your hard work!",
        "I appreciate you!",
        "I'm grateful for you!",
        "That's kind of you!",
        "Your help means a lot!",
        "It means the world to me!"
    ]

    return affirmations