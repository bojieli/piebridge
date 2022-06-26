#!/usr/bin/python3
from flask import Flask, render_template, request, abort, send_from_directory, url_for, redirect
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/var/www/ring0.me/piebridge/files'

@app.route('/piebridge/')
def index():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('upload.html', files=files)


def filename2path(filename):
    return os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(filename))


@app.route('/piebridge/upload/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save(filename2path(f.filename))
        return redirect(url_for('index'))
    abort(400)


@app.route('/piebridge/download/<string:filename>')
def download_file(filename):
    if not os.path.exists(filename2path(filename)):
        abort(404)
    return send_from_directory(app.config['UPLOAD_FOLDER'], secure_filename(filename))


@app.route('/piebridge/delete/<string:filename>')
def delete_file(filename):
    path = filename2path(filename)
    if not os.path.exists(path):
        return 'file does not exist'
    os.remove(path)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(port=38325, debug=False)
