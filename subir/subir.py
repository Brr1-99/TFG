from flask import redirect, render_template, request, Blueprint, flash, url_for
import os
from werkzeug.utils import secure_filename
from lib.comprobar_sesión import comprobar_sesion
from lib.db_cursor import db_cursor


uploads = Blueprint('bp_upload', __name__, static_folder="static", template_folder="templates_upload")

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@uploads.route('/<string:db>/<string:table>/<string:id>', methods=['GET'])
def upload(db, table, id):
    login = comprobar_sesion()[0]
    if login:
        return render_template('upload.html')
    else:
        return render_template('ingresar.html')


@uploads.route('', methods=['POST'])
def upload_commit():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        db = request.referrer.split('/')[-3]
        table = request.referrer.split('/')[-2]
        num_id = request.referrer.split('/')[-1]
        filename = secure_filename(file.filename)
        file.save(os.path.join('static/uploads/', filename))

        base, cursor = db_cursor(db)
        cursor.execute(" UPDATE `{0}` SET `imagen`='{1}' WHERE `id` = '{2}'".format(table, filename, num_id))
        base.commit()

        flash('Image successfully uploaded')
        return redirect(url_for('bp_index.index', db=db))
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)


@uploads.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename='uploads/' + filename), code=301)
