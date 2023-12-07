from sqlalchemy.orm import DeclarativeBase
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

from .utils.strings import db_uri
from .utils.constants import STATICS


# **********************************************************
# create and configure the backend app object
# **********************************************************

# dummy base class for all sqlalchemy models
class Base(DeclarativeBase):
    pass

# basic initialization
app = Flask("RICH.DATA"
            , static_folder=STATICS)
db = SQLAlchemy(model_class=Base)
app.config["SQLALCHEMY_DATABASE_URI"] = db_uri()
app.config["SQLALCHEMY_ECHO"] = True
db.init_app(app)

# from .orm import *
# with app.app_context():
#     db.create_all()

from .routes import *

