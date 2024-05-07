from flask import render_template, jsonify, Response
from psycopg2.extras import NumericRange
from sqlalchemy import text, select
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


@app.route("/i/named-entity")
def catalog_named_entity():
    """
    get all named entity elements
    """
    r = db.session.execute(NamedEntity.query)
    return Response( json.dumps([ _[0].serialize_lite() for _ in r.all() ])
                   , mimetype="application/json"
                   , content_type="application/json")


@app.route("/i/theme")
def catalog_theme():
    """
    get all theme elements
    """
    r = db.session.execute(Theme.query)
    return Response( json.dumps([ _[0].serialize_lite() for _ in r.all() ])
                   , mimetype="application/json"
                   , content_type="application/json")


@app.route("/i/list-tables")
def list_tables():
    """
    list all public tables in the database
    """
    r = db.session.execute(text( "SELECT table_name "
                               + "FROM information_schema.tables "
                               + "WHERE table_schema = 'public';"))
    return Response( json.dumps([ _[0] for _ in r.all() ])
                   , mimetype="application/json"
                   , content_type="application/json")


@app.route("/i/table-viewer/<tablename>")
def table_viewer(tablename:str):
    """
    get and return an entire table as a json
    """
    # convert postgres-specific datatypes into json-compliant ones.
    maybe_convert = lambda el: el if not isinstance(el, NumericRange) else int4range2list(el)
    # transform a row of values into a dict of `{ <colname>: <value> }`
    mapper = lambda row: { colnames[i]: maybe_convert(row[i]) for i, r in enumerate(row) }
    # process the SQL response into a list of `{ <colname>: <value> }` elts
    response_process = lambda x: [ mapper(row) for row in x ]

    # run the query
    r = db.session.execute(text(f"SELECT * FROM {tablename};"))
    colnames = list(r.keys())  # column names for the query

    # process the results. if there are no results, generate
    # a 1 item list mapping all column names to `None`, to
    # be able to display something in the frontend.
    # `r.rowcount` returns the number of rows in the `CursorResult`;
    # contrary to `all()`, it doesn't close the result after being run
    r = response_process(r) if r.rowcount else [{ c:None for c in colnames }]
    return  Response( json.dumps(r)
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
            <dt>{ _[0].actor.entry_name.upper() }</dt>
            <dd><i>{ _[0].iconography.title[0].entry_name }</i></dd>
        </dl></li>"""
    ul += "</ul>"

    return f"""
        <html>
            <head><title>RICH.DATA</title></head>
            <body><h1>RICH.DATA</h1>{ ul }</body>
        </html>
    """
