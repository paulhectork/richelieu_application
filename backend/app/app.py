from sqlalchemy.orm import DeclarativeBase
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask import Flask

from .config import CONFIGS
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

# specific configuration of the app
def config_app(cfgname:str):
    assert cfgname in CONFIGS.keys(), \
           f"config.config_app: `cfg_name` must be one of `{CONFIGS.keys()}`, got `{cfgname}`"

    app.config.from_object(CONFIGS[cfgname])
    db.init_app(app)
    CORS(app, origins=[ "http://localhost:5173"     # frontend as localhost
                      , "http://172.17.1.142:5173"  # frontend as server IP addr
                      , "http://localhost:5000"    # backend as localhost (should be useless but hey)
    ])
    return app


from .routes import *

