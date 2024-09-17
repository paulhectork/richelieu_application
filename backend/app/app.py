from flask import Flask# , has_request_context, request
from flask.logging import default_handler
from sqlalchemy.orm import DeclarativeBase
from flask_sqlalchemy import SQLAlchemy
from logging.config import dictConfig
from flask_cors import CORS
import logging

from .config import CONFIGS
from .utils.constants import STATICS


# **********************************************************
# create and configure the backend app object
# **********************************************************

# ***************************************************************
# logging configuration
# https://flask.palletsprojects.com/en/2.3.x/logging/#other-libraries
root = logging.getLogger()
root.addHandler(default_handler)
logging.getLogger("sqlalchemy").addHandler(default_handler)  # sqlalchemy logger is passed to Flask


# ***************************************************************
# dummy base class for all sqlalchemy models
class Base(DeclarativeBase):
    pass


# ***************************************************************
# app configuration

# 1) generic configuration of the app
app = Flask( "RICH.DATA"
           , static_folder=STATICS)
db = SQLAlchemy(model_class=Base)

# 2) specific configuration of the app
def config_app(cfgname:str):
    assert cfgname in CONFIGS.keys(), \
           f"config.config_app: `cfg_name` must be one of `{CONFIGS.keys()}`, got `{cfgname}`"

    app.config.from_object(CONFIGS[cfgname])
    db.init_app(app)
    # https://readthedocs.org/projects/flask-cors/downloads/pdf/latest/
    # CORS(app, resources={ r"/i/*": {"origins": "*"} })
    CORS(app, origins=[ "https://quartier-richelieu-retour.inha.fr"   # server: apache frontend (no port specification !!!!)
                      , "http://localhost:5173"                       # local frontend
                      ])
    return app


from .routes import *

