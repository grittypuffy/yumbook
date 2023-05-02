"""YumBook: A beautiful recipe library and printable generator."""


from flask import Flask, render_template, request, flash, redirect
from werkzeug.utils import secure_filename
from libmat2 import images
import os
"""import sqlite3 as sql
import click
import json
"""

OS_CWD = os.getcwd()
UPLOAD_FOLDER = '../../sample_data'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app = Flask(__name__)
app.config['SECRET_KEY'] = 'APP_SECRET_KEY'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000


def allowed_file(filename):
    """Check whether a file has an allowed file extension."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def clean_file(filename):
    """Strip metadata from uploaded files to enhance privacy."""
    os.chdir(app.config['UPLOAD_FOLDER'])
    if filename.endswith(".jpg") or filename.endswith(".jpeg"):
        exif = images.GdkPixbufAbstractParser(filename)
        clean_exif(exif, filename)
    elif filename.endswith(".png"):
        exif = images.PNGParser(filename)
        clean_exif(exif, filename)
    else:
        flash('Invalid image file extension')
    os.chdir(OS_CWD)


def clean_exif(exif, filename):
    """Remove EXIF metadata from any file."""
    exif.remove_all()
    cleaned_file = "".join(filename.split(".")[:-1]+[".cleaned.",
                                                     filename.split(".")[-1]])
    return os.rename(cleaned_file, filename)


def export_json(data):
    """Export JSON data from the created recipe."""
    return data


@app.route("/", methods=["GET", "POST"])
def index():
    """Index of the application."""
    return render_template("index.html")


@app.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    return render_template("sign_up.html")

@app.route("/create", methods=["GET", "POST"])
def create():
    """Create a recipe."""
    return render_template("create.html")


@app.route("/preview", methods=["GET", "POST"])
def preview():
    """Create a preview of the recipe."""
    if request.method == "POST":
        if 'background' not in request.files:
            flash('No file part')
            return redirect(request.url)
        bg = request.files['background']
        if bg.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if bg and allowed_file(bg.filename):
            filename = secure_filename(bg.filename)
            bg.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            clean_file(filename)
        title = request.form["title"]
        ingredients = request.form["ingredients"]
        data = {"title": title,
                "ingredients": ingredients,
                "filename": os.path.join(app.config['UPLOAD_FOLDER'], filename)
                }
        return export_json(data)
    return render_template("preview.html")


@app.route('/export_html')
def export_to_html(data):
    """Export recipe to HTML file."""
    return render_template("export.html")


@app.errorhandler(404)
def not_found(err):
    return render_template("404.html")
