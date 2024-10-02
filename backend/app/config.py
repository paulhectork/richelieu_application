from sqlalchemy import URL
import json
import os

from .utils.constants import CONFIDENTIALS


# ***************************************************************************************************************
# different app configuration options
#
# see:
# https://flask.palletsprojects.com/en/3.0.x/config/
# https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/config/
# https://docs.sqlalchemy.org/en/20/core/engines.html
# # https://github.com/PonteIneptique/cours-python/blob/master/Chapitre%2014%20-%20Ecrire%20des%20tests.ipynb
# ***************************************************************************************************************


def db_uri(params:dict) -> str:
    """
    create an URI to connect to the database based on the dict `params`
    """
    return URL.create( "postgresql"
                     , username=params['username']
                     , password=params["password"]
                     , host=params["uri"]
                     , database=params["db"] )


# testing the app locally
class TEST:
    with open(os.path.join(CONFIDENTIALS, "postgresql_credentials_local.json"), mode="r") as fh:
        params = json.load(fh)
    SQLALCHEMY_DATABASE_URI = db_uri(params)
    SQLALCHEMY_ECHO = False
    TESTING = True

# local development
class DEV:
    with open(os.path.join(CONFIDENTIALS, "postgresql_credentials_local.json"), mode="r") as fh:
        params = json.load(fh)
    SQLALCHEMY_DATABASE_URI = db_uri(params)
    SQLALCHEMY_ECHO = False

# on production / server
class PROD:
    with open(os.path.join(CONFIDENTIALS, "postgresql_credentials_server.json"), mode="r") as fh:
        params = json.load(fh)
    SQLALCHEMY_DATABASE_URI = db_uri(params)
    SQLALCHEMY_ECHO = False
    #SERVER_NAME = "172.17.1.142:5001"
    SERVER_NAME = "quartier-richelieu-retour.inha.fr:5001"

# dict to choose the config based on a key
CONFIGS = { "dev": DEV,
            "test": TEST,
            "prod": PROD }
