from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from app.config import config_options

# app init / bootstrap init (bootstrap.init_app(app))
app = Flask(__name__)
Bootstrap(app)
bootstrap = Bootstrap()

# set configurations
app.config.from_object(config_options['dev_config'])