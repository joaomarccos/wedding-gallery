import os

import boto3
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mongoengine import MongoEngine
from flask_security import Security, MongoEngineUserDatastore

from logger_utils import setup_logger
from models.security_model import User, Role
from services.gallery_service import GalleryService

setup_logger()
app = Flask(__name__)
Bootstrap(app)

# app.config['DEBUG'] = True
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

# MongoDB Config
app.config['MONGODB_SETTINGS'] = {
    'db': 'wedding',
    'host': os.environ['MONGO_URI']
}

app.secret_key = os.environ['APP_SECRET']
app.config['SECURITY_PASSWORD_SALT'] = os.environ['APP_SECRET']

# Create database connection object
db = MongoEngine(app)

# Setup Flask-Security
user_datastore = MongoEngineUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# AWS S3 instance
s3 = boto3.resource('s3')


# Create a user to test with
@app.before_first_request
def create_user():
    user_datastore.find_or_create_role(name='owner', description='Gallery Owner')
    if not user_datastore.get_user('joao'):
        user_datastore.create_user(email='joao', password='123')
        user_datastore.add_role_to_user('joao', 'owner')
    if not user_datastore.get_user('maria'):
        user_datastore.create_user(email='maria', password='123')
        user_datastore.add_role_to_user('maria', 'owner')


# Gallery service instance
service = GalleryService(s3)

from views import main as main_blueprint
from api import api as api_blueprint

app.register_blueprint(main_blueprint)
app.register_blueprint(api_blueprint, url_prefix='/api/photos')

if __name__ == '__main__':
    app.run()
