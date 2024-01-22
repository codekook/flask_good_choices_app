"""Forms uses flask WTForms to manage form data from the browser.  There are two forms, the Registration Form and the Login Form in the application."""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask import flash
from flask_package.models import User

class RegistrationForm(FlaskForm):

    """RegistrationForm class creates registration requirements on the website"""

    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), 
                                                                     EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            flash('Username already exists')
            raise ValidationError()

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            flash('Email already exists')
            raise ValidationError()


class LoginForm(FlaskForm):

    """LoginForm class creates the requirements to login on the website"""

    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(),])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')