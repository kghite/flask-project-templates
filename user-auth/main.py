"""
Flask app serving user auth interface
"""


import yaml
from flask import Flask, request, redirect, render_template, flash, url_for
from flask_wtf import FlaskForm
from flask_login import LoginManager, UserMixin, login_required, login_user, current_user, logout_user
# Internal
from config import *
import user_management
from mongo_interface import MongoInterface


"""
Serve public page
"""


@app.route('/', methods=['GET', 'POST'])
def index():
	return "The app is alive."


"""
Serve public page
"""


@app.route('/public', methods=['GET', 'POST'])
def public():
	return "The app is alive."


"""
Serve home page
"""


@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
	return "The app is alive."


"""
Serve index status page to confirm the app is running
"""


@app.route('/status', methods=['GET', 'POST'])
@login_required
def status():
	return "The app is alive."


"""
Create a new user
"""


@app.route('/register', methods=['GET', 'POST'])
def register():
	form = user_management.RegistrationForm()
	if request.method == 'POST':
		if form.validate():
			# Check if user exists
			existing_user = User.objects(email=form.email.data).first()
			verified = mongo_interface.verify_code(form.code.data)
			if existing_user: flash('A user already exists with that email address.')
			elif not verified: flash('That ref code is not in the system.')
			else:
				# Hash password and store user in mongo
				hashpass = user_management.encrypt_password(form.password.data)
				user = User(name=form.name.data, 
							email=form.email.data,
							code=user_management.generate_code(),
							password=hashpass).save()
				# Log user into flask session
				login_user(user)
				current_user

				return redirect('/home')

	return render_template('registration.html', form=form)


"""
Check in to the app
"""


@app.route('/checkin', methods=['GET', 'POST'])
def checkin():
	if current_user.is_authenticated == True:
		return redirect(url_for('home'))
	form = user_management.CheckinForm()
	if request.method == 'POST':
		if form.validate():
			# Verify user exists and password is correct
			check_user = User.objects(email=form.email.data).first()
			if check_user:
				if user_management.verify_password(check_user['password'], 
													form.password.data):
					# Log user into flask session
					login_user(check_user)

					return redirect(url_for('home'))

	return render_template('checkin.html', form=form)


"""
Logout session user
"""


@app.route('/logout', methods = ['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('public'))


"""
User authentication handler
"""


class User(UserMixin, db.Document):
    meta = {'collection': 'users'}
    name = db.StringField(max_length=32)
    email = db.StringField(max_length=32)
    code = db.StringField(max_length=32)
    password = db.StringField()


@login_manager.user_loader
def load_user(user_id):
    return User.objects(pk=user_id).first() 


"""
Local app startup
"""


if __name__ == '__main__':
	# Load config
	with open('config.yaml', 'r') as ymlfile:
		config = yaml.load(ymlfile, Loader=yaml.FullLoader)

	# Set up the mongo interface
	mongo_interface = MongoInterface(config['mongo']['connection_string'], 
										config['mongo']['database'])

	# Run the app
	app.secret_key = config['flask']['private_key']
	app.config['TESTING'] = False
	app.run(host='0.0.0.0', debug=config['flask']['debug'])