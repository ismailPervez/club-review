from app import app
from flask import render_template, redirect, url_for, request


# routes
@app.route("/")
def home():
    return render_template('index.html')