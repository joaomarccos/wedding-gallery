import datetime
import json

import flask_login
from flask import flash, request, redirect, render_template, jsonify
from flask_security import login_required, roles_required

from main import service, app
from views import main
from models.photo_model import Photo
from upload_utils import allowed_file


@main.route('/')
def home():
    page = request.args.get("page", None, type=int)
    if page is None:
        return redirect('/?page=1')
    photos = service.get_paginated_items(page, active=True)
    app.logger.info(photos)
    return render_template('index.html', photos=photos)


@main.route('/photos', methods=['POST'])
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


# private

@main.route('/manage')
@login_required
@roles_required('owner')
def manage():
    page = request.args.get("page", None, type=int)
    if page is None:
        return redirect('/manage?page=1')
    photos = service.get_paginated_items(page, active=False)
    func = lambda: print(photos)
    return render_template('manage-gallery.html', username=flask_login.current_user.email, photos=photos, func = func)
