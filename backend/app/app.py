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
    # https://readthedocs.org/projects/flask-cors/downloads/pdf/latest/
    # CORS(app, resources={ r"/i/*": {"origins": "*"} })
    CORS(app, origins=[ "https://quartier-richelieu-retour.inha.fr"   # server: apache frontend (no port specification !!!!)
                      , "http://localhost:5173"                       # local frontend
                      ])
    return app


from .routes import *

