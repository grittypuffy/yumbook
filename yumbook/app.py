from flask import Flask, render_template, request
from flask import g, flash, redirect, url_for
import sqlite3 as sql
import click
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'APP_SECRET_KEY'

"""def db_conn():
    conn = sql.connect("details.db")
    with open("query.sql") as qry:
        conn.executescript(qry.read())
    return conn
"""

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")
