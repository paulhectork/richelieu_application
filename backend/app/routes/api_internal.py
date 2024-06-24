from flask import render_template, jsonify, request
from psycopg2.extras import NumericRange
from sqlalchemy import text, desc, asc
import random
import json

from ..search.search_iconography import sanitize_params, make_params, make_query
from ..utils.spatial import featurelist_to_featurecollection, geometry_to_feature
from ..app import app, db
from ..orm import *


# *************************************************
# routes for the internal API
# basepath: `<APP URL>/i/`
# *************************************************



# ******************************************
# indexes
# ******************************************
@app.route("/i/iconography")
def index_iconography():
    """
    get all `iconography` ressources.
    we mimic `flask.jsonify` with `Response` because
    the json isn't sent to the client using `jsonify`
    """
    r = db.session.execute(Iconography.query)
    return jsonify([ _[0].serialize_lite() for _ in r.all() ])


@app.route("/i/cartography")
def index_cartography():
    """
    get all `cartography` ressources.
    """
    r = db.session.execute(Cartography.query)
    return jsonify([ _[0].serialize_lite() for _ in r.all() ])


@app.route("/i/place")
def index_place():
    """
    get all `place` ressources
    """
    r = db.session.execute(Place.query)
    return jsonify([  _[0].serialize_lite() for _ in r.all() ])


@app.route("/i/directory")
def index_directory():
    """
    get all directory ressources
    """
    r = db.session.execute(Directory.query)
    return jsonify([ _[0].serialize_lite() for _ in r.all() ])


@app.route("/i/theme")
def index_theme():
    """
    get all theme elements
    """
    r = (db.session.query(Theme, Theme.iconography_count)
                   .order_by(Theme.iconography_count.desc()) )
    # to check the result: print( [_[0].iconography_count for _ in r.all()] )
    return jsonify([ _[0].serialize_lite() for _ in r.all() ])


@app.route("/i/named-entity")
def index_named_entity():
    """
    get all named entity elements
    """
    r = (db.session.query(NamedEntity, NamedEntity.iconography_count)
                   .order_by(NamedEntity.iconography_count.desc()) )
    return jsonify([ _[0].serialize_lite() for _ in r.all() ])


@app.route("/i/institution")
def institution():
    """
    get all institution elements
    """
    r = db.session.execute(Institution.query)
    return jsonify([ i[0].serialize_lite() for i in r.all() ])


# ******************************************
# main pages
# ******************************************
@app.route("/i/iconography/<id_uuid>")
def main_iconography(id_uuid):
    """return an `Iconography` object based on its `id_uuid`"""
    r = db.session.execute(Iconography
                           .query
                           .filter( Iconography.id_uuid == id_uuid ))
    out = [ _[0].serialize_full() for _ in r.all() ]
    for icono in out:
        # avec des boucles inline
        icono["place"] = [ geometry_to_feature( place["vector"]
                                              , custom_properties={"id_uuid": place["id_uuid"]} )
                           for place in icono["place"] ]
        icono["place"] = featurelist_to_featurecollection(icono["place"])

        # la même chose, en plus verbeux:
        # featurelist = []            # liste de features geoson
        # for loc in icono["place"]:  # loc = le lieu associé à notre objet iconographique `icono`
        #     loc = geometry_to_feature(loc["vector"], custom_properties={ "id_uuid": loc["id_uuid"] })
        #     featurelist.append(loc)
        # featurecollection = featurelist_to_featurecollection(featurelist)  # on crée notre feature collection à partir de notre liste de features
        # icono["place"] = featurecollection   # on met à jour notre objet `icono`
    return jsonify(out)



# ******************************************
# advanced search
# ******************************************
@app.route("/i/avanced-search-iconography/")
def advanced_search_iconography():
    """
    """
    params = make_params(request.args)
    params, valid = sanitize_params(params)
    if valid:
        results = make_query(params)
    else:
        print("INVALID QUERY PARAMETERS !!!!")
    return jsonify([])


# ******************************************
# utils
# ******************************************
@app.route("/i/place-lite/<place_uuid>")
def place_lite(place_uuid:str):
    """
    get a single `place` item and return
    its `serialize_lite()` repr
    """
    r = db.session.execute(Place.query.filter(Place.id_uuid==place_uuid).limit(1))
    return jsonify([ _[0].serialize_lite() for _ in r.all() ])


@app.route("/i/iconography-overall-date-range")
def iconography_overall_date_range():
    """
    get the overall minimum/maximum
    dates on the iconography table
    """
    r = db.session.execute(text("""(
                                  SELECT lower(iconography.date)
                                  FROM iconography
                                  WHERE iconography.date IS NOT NULL
                                  ORDER BY iconography.date ASC
                                  LIMIT 1
                                )
                                UNION
                                (
                                  SELECT upper(iconography.date)
                                  FROM iconography
                                  WHERE iconography.date IS NOT NULL
                                  ORDER BY iconography.date DESC
                                  LIMIT 1
                                );"""))
    return jsonify(sorted([ d[0] for d in r.all() ]))


# ******************************************
# table viewer
# ******************************************


@app.route("/i/list-tables")
def list_tables():
    """
    list all public tables in the database
    """
    r = db.session.execute(text( "SELECT table_name "
                               + "FROM information_schema.tables "
                               + "WHERE table_schema = 'public';"))
    return jsonify([ _[0] for _ in r.all() ])


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
    return  jsonify(r)





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
