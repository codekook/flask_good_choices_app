import pytest
from flask_package.forms import RegistrationForm, LoginForm
from flask_package import app

@pytest.mark.skip(reason="incomplete")
@pytest.mark.parametrize("registration_info", [
    ("john.p.doe", 
     "john.p.doe@me.com", 
     "bestpasswordever1234", 
     "bestpasswordever1234")
])
def test_registration_form(registration_info):

    '''Test the functionality of the Registration Form'''

    with app.app_context():

        assert registration_info == RegistrationForm(
            username="john.p.doe",
            email="john.doe@me.com",
            password="bestpasswordever1234",
            confirm_password="bestpasswordever1234")