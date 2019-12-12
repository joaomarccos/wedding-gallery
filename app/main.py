import datetime
import json
import os

import boto3
import flask_login
from flask import Flask, flash, request, redirect, render_template
from flask_bootstrap import Bootstrap
from flask_mongoengine import MongoEngine
from flask_security import Security, MongoEngineUserDatastore, login_required

from logger_utils import setup_logger
from models.photo_model import Photo
from models.security_model import User, Role
from services.gallery_service import GalleryService
from upload_utils import allowed_file

setup_logger()
app = Flask(__name__)
Bootstrap(app)

app.config['DEBUG'] = True

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
    user_datastore.create_user(email='joao@email.com', password='password')


# Gallery service instance
service = GalleryService(db, s3)


# Views
@app.route('/manage')
@login_required
def manage():
    return render_template('manage-gallery.html', username=json.dumps(flask_login.current_user.email))


@app.route('/')
def home():
    page = request.args.get("page", 0)
    photos = service.get_paginated_items(page, filters={'active': True})
    return render_template('index.html', photos=photos)


@app.route('/photos', methods=['POST'])
def upload_file():
    app.logger.info('uploading new file')
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        if 'author' not in request.form:
            flash('No author name')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            service.put_item(
                Photo(author=request.form['author'], likes=0, timestamp=datetime.datetime.now(), active=False), file)
            app.logger.info(f'new photo from {request.form["author"]}')
            flash('File successfully uploaded')
            return redirect('/')
        else:
            flash('Allowed file types are png, jpg, jpeg, gif')
            return redirect(request.url)


if __name__ == '__main__':
    app.run()
