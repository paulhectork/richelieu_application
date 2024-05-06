from sqlalchemy.orm import DeclarativeBase
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask import Flask

from .config import CONFIGS
# from .utils.strings import db_uri
from .utils.constants import STATICS


# **********************************************************
# create and configure the backend app object
# **********************************************************

# dummy base class for all sqlalchemy models
class Base(DeclarativeBase):
    pass

# generic configuration of the app
app = Flask( "RICH.DATA"
           , static_folder=STATICS)
db = SQLAlchemy(model_class=Base)
# db.init_app(app)

# specific configuration of the app
def config_app(cfgname:str):
    assert cfgname in CONFIGS.keys(), \
           f"config.config_app: `cfg_name` must be one of `{CONFIGS.keys()}`, got `{cfgname}`"

    app.config.from_object(CONFIGS[cfgname])
    db.init_app(app)
    CORS(app)  # allow cors requests
    return app

from .routes import *

