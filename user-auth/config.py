import yaml
from flask import Flask
from flask_login import LoginManager
from flask_mongoengine import MongoEngine

app = Flask(__name__)
with open('config.yaml', 'r') as ymlfile:
	config = yaml.load(ymlfile, Loader=yaml.FullLoader)
app.config['SECRET_KEY'] = config['flask']['private_key']

# Database setup
app.config['MONGODB_SETTINGS'] = {
	'db': config['mongo']['database'],
	'host': config['mongo']['connection_string']
}
db = MongoEngine()
db.init_app(app)

# Auth setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'