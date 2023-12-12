from flask import render_template, jsonify, Response
import random
import json

from ..app import app, db
from ..orm import *


# *************************************************
# routes for the internal API
# basepath: `<APP URL>/i/`
# *************************************************


@app.route("/i/iconography")
def catalog_iconography():
    """
    get all `iconography` ressources.
    we mimic `flask.jsonify` with `Response` because
    the json isn't sent to the client using `jsonify`
    """
    r = db.session.execute(Iconography.query)
    return Response(json.dumps([ _[0].serialize_lite() for _ in r.all() ])
                    , mimetype="application/json"
                    , content_type="application/json")


@app.route("/i/cartography")
def catalog_cartography():
    """
    get all `cartography` ressources.
    """
    r = db.session.execute(Cartography.query)
    return Response(json.dumps([ _[0].serialize_lite() for _ in r.all() ])
                    , mimetype="application/json"
                    , content_type="application/json")


@app.route("/i/directory")
def catalog_directory():
    """
    get all directory ressources
    """
    r = db.session.execute(Directory.query)
    return Response(json.dumps([ _[0].serialize_lite() for _ in r.all() ])
                    , mimetype="application/json"
                    , content_type="application/json")


# *************
# DUMMY ROUTE *
# *************
@app.route("/i")
def __():
    # run the query
    l = [ random.choice([ _ for _ in range(5, 100) ]) for i in range(20) ]
    x = db.session.execute(R_IconographyActor.query
                                             .filter(R_IconographyActor.id.in_(l)))

    # create an html list
    ul = "<ul>"               # html unordered list
    for _ in x.all():         # access each row
        print(_)              # `_` is a tuple, `_[0]` is row itself
        print(_[0].__dict__)  # print the dict rpr of row
        ul += f"""<li><dl>
            <dt>{ _[0].actor.last_name.upper() }</dt>
            <dd><i>{ _[0].iconography.title[0].name }</i></dd>
        </dl></li>"""
    ul += "</ul>"

    return f"""
        <html>
            <head><title>RICH.DATA</title></head>
            <body><h1>RICH.DATA</h1>{ ul }</body>
        </html>
    """
