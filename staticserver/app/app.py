"""
a super simple flask app to use as a
statics file server in local development
"""

from flask import Flask, send_file
import os


STATICS             = os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), "statics"))
STATICS_ICONOGRAPHY = os.path.abspath(os.path.join(STATICS, "iconography"))
STATICS_CARTOGRAPHY = os.path.abspath(os.path.join(STATICS, "cartography"))


app = Flask("RICH.DATA.STATICS", static_folder=STATICS)


@app.route("/iconography/<string:fn>")
def iconography(fn:str):
    """send the iconography file named `fn`"""
    print(os.path.join(STATICS_ICONOGRAPHY, fn))
    if os.path.isfile(os.path.join(STATICS_ICONOGRAPHY, fn)):
        return send_file(os.path.join(STATICS_ICONOGRAPHY, fn))
    else:
        return "Error: file not found", 404


@app.route("/cartography/<string:fn>")
def cartography(fn:str):
    """send the cartography file named `fn`"""
    if os.path.isfile(os.path.join(STATICS_CARTOGRAPHY, fn)):
        return send_file(os.path.join(STATICS_CARTOGRAPHY, fn))
    else:
        return "Error: file not found", 404



