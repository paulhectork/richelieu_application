from flask import Flask
from flask.logging import default_handler
from sqlalchemy.orm import DeclarativeBase
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import logging

from .config import CONFIGS
from .utils.constants import STATICS


# **********************************************************
# create and configure the backend app object
# **********************************************************


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
    # config loading and database connexion
    assert cfgname in CONFIGS.keys(), \
           f"config.config_app: `cfg_name` must be one of `{CONFIGS.keys()}`, got `{cfgname}`"
    app.config.from_object(CONFIGS[cfgname])
    db.init_app(app)

    # CORS config
    # https://readthedocs.org/projects/flask-cors/downloads/pdf/latest/
    # CORS(app, resources={ r"/i/*": {"origins": "*"} })
    CORS(app, origins=[ "https://quartier-richelieu-retour.inha.fr"   # server: apache frontend (no port specification !!!!)
                      , "http://localhost:5173"                       # local frontend
                      ])

    # Flask and SQlachemy logging configuration
    # with this config,
    # > every Flask query is logged
    # > sqlalchemy's WARNING + ERROR levels are logged
    # > with the try...except in main, the error stacks will be printed
    # https://flask.palletsprojects.com/en/2.3.x/logging/#other-libraries
    # for more fine grained config than is done here, see:
    #   https://medium.com/@haroonayaz76/centralized-logging-system-in-flask-the-backbone-of-multithreaded-python-applications-in-depth-7bfc45aae1b3
    if cfgname == "prod":
        format = "%(levelname)s in %(module)s: %(message)s"  # server journals aldready print datetime => no need to reprint them
    else:
        format = "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
    default_handler.setFormatter(logging.Formatter(format))

    root = logging.getLogger()
    root.addHandler(default_handler)
    logging.getLogger("sqlalchemy").addHandler(default_handler)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARN)
    logging.getLogger("sqlalchemy.engine").addHandler(default_handler)
    return app


from .routes import *

