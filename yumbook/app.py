"""YumBook: A beautiful recipe library and printable generator."""


from flask import Flask, render_template, request, flash, redirect
from flask import send_from_directory
from werkzeug.utils import secure_filename
from libmat2 import images
import os
import sqlite3 as sql
import click
import json


OS_CWD = os.getcwd()
UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
SCHEMA_DIR = 'schema'
DB_DIR = 'schema/database'
app = Flask(__name__)
app.config['SECRET_KEY'] = 'APP_SECRET_KEY'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000


def allowed_file(filename):
    """Check whether a file has an allowed file extension."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def database_name(name):
    db_name = ''.join(name.split(" ")).lower()+".db"
    return db_name

def database_connect(name, data):
    db_name = ''.join(name.split(" ")).lower()+".db"
    db_path = os.path.join(DB_DIR, db_name)
    db_script = os.path.join(SCHEMA_DIR, "recipe.sql")
    connection = sql.connect(os.path.join(DB_DIR, db_name))
    with open(db_script) as schema:
        connection.executescript(schema.read())
    cursor = connection.cursor()
    cursor.execute("INSERT INTO recipe (recipename, filename, ingredients, directions) VALUES (?, ?, ?, ?)", (data["name"], data["filename"], data["ingredients"], (data["directions"])))
    connection.commit()
    connection.close()
    return db_path


def clean_file(filename):
    """Strip metadata from uploaded files to enhance privacy."""
    validfile = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if validfile.endswith(".jpg") or validfile.endswith(".png") or validfile.endswith(".jpeg"):
        exif = images.GdkPixbufAbstractParser(validfile)
        clean_exif(exif, validfile)
    elif validfile.endswith(".png"):
        exif = images.PNGParser(validfile)
        clean_exif(exif, validfile)
    else:
        flash('Invalid image file extension')


def clean_exif(exif, filename):
    """Remove EXIF metadata from any file."""
    exif.remove_all()
    cleaned_file = "".join(filename.split(".")[:-1]+[".cleaned.",
                                                     filename.split(".")[-1]])
    return os.rename(cleaned_file, filename)


def export_json(data):
    """Export JSON data from the created recipe."""
    return data

def display_image(name):
    OS_STATIC = os.path.join(app.config["UPLOAD_FOLDER"], name)
    return OS_STATIC


@app.route("/", methods=["GET", "POST"])
def index():
    """Index of the application."""
    return render_template("index.html")


@app.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    return render_template("sign_up.html")

@app.route("/sign_in", methods=["GET", "POST"])
def sign_in():
    return render_template("sign_in.html")

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
        name = request.form["name"]
        ingredients = request.form["ingredients"]
        directions = request.form["directions"]
        data = {"name": name,
                "filename": display_image(filename),
                "ingredients": ingredients,
                "directions": directions
                }
        dbname = database_name(name)
        db = database_connect(name, data)
        return render_template("preview.html", data=export_json(data))
    return render_template("404.html")


@app.route('/explore')
def explore():
    """Export recipe to HTML file."""
    return render_template("explore.html")

@app.route('/export')
def export():
    """The value is hardcoded for pancakes till a working logic is obtained."""
    return send_from_directory(DB_DIR, "pancakes.db")

@app.errorhandler(404)
def not_found(err):
    return render_template("404.html")
