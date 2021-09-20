from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from app.config import config_options

# app init / bootstrap init (bootstrap.init_app(app))
app = Flask(__name__)
Bootstrap(app)
bootstrap = Bootstrap()

# set configurations
app.config.from_object(config_options['dev_config'])

# init database
db = SQLAlchemy(app)

'''
we import views after app initialization so as to avoid circular imports.
the app variable is used in views.py to create routes, therefore it should be created before
it is used anywhere 
we need to import it from a package for it to work
'''
from app import views
from app import models