""" 
User authentication tools
"""


from random import choice
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from passlib.hash import sha256_crypt


"""
Authentication management
"""


def encrypt_password(password):
	return sha256_crypt.encrypt(password)


def verify_password(mongo_hash, password):
	return sha256_crypt.verify(password, mongo_hash)


def generate_code():
	return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
	


"""
Authentication forms
"""


class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    code = StringField('Ref Code', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Join')


class CheckinForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')