"""
a super simple flask app to use as a
statics file server in local development
"""

from flask import Flask, send_file
import os


STATICS             = os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), "statics"))
STATICS_ICONOGRAPHY = os.path.abspath(os.path.join(STATICS, "iconography"))
STATICS_CARTOGRAPHY = os.path.abspath(os.path.join(STATICS, "cartography"))
STATICS_OSD         = os.path.abspath(os.path.join(STATICS, "openseadragon-icons"))
STATICS_OTHER       = os.path.abspath(os.path.join(STATICS, "other"))

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


@app.route("/openseadragon-icons/<string:fn>")
def osdicons(fn:str):
    """send openseadragon icons to the frontend"""
    if os.path.isfile(os.path.join(STATICS_OSD, fn)):
        return send_file(os.path.join(STATICS_OSD, fn))
    else:
        return "Error: file not found", 404

@app.route("/other/<string:fn>")
def other(fn:str):
    """send an image in the other/ dir the frontend"""
    if os.path.isfile(os.path.join(STATICS_OTHER, fn)):
        return send_file(os.path.join(STATICS_OTHER, fn))
    else:
        return "Error: file not found", 404