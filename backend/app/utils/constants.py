import os


# filepaths
UTILS = os.path.abspath(os.path.dirname(__file__))
APP = os.path.abspath(os.path.join(UTILS, os.pardir))
TMP = os.path.abspath(os.path.join(APP, "tmp"))
BACKEND = os.path.abspath(os.path.join(APP, os.pardir))
ORM = os.path.abspath(os.path.join(APP, "orm"))
ROUTES = os.path.abspath(os.path.join(APP, "routes"))
STATICS = os.path.abspath(os.path.join(APP, "statics"))
INTERACT = os.path.abspath(os.path.join(APP, "interact"))
CONFIDENTIALS = os.path.abspath(os.path.join(UTILS, "confidentials"))

