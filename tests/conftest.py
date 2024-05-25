
from flask_package import app
import pytest 

@pytest.fixture()
def test_app():
    app.config.update(
        TESTING=True)
    yield app

@pytest.fixture()
def client(test_app):
    return test_app.test_client()

@pytest.fixture()
def runner(test_app):
    return test_app.test_cli_runner()

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