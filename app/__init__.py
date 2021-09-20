from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

# app init / bootstrap init (bootstrap.init_app(app))
app = Flask(__name__)
Bootstrap(app)
bootstrap = Bootstrap()