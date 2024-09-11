from flask import render_template, jsonify, request
from psycopg2.extras import NumericRange
from sqlalchemy import text, func
import random
import json

from ..search.search_iconography import sanitize_params, make_params, make_query
from ..utils.spatial import featurelist_to_featurecollection, geometry_to_feature
from ..app import app, db
from ..orm import *


# ********************************************************************************
# routes for the internal API
# basepath: `<APP URL>/i/`
# ********************************************************************************



# *************************************************************************
# iconography
# *************************************************************************

@app.route("/i/iconography")
def index_iconography():
    """
    get all `iconography` ressources.
    we mimic `flask.jsonify` with `Response` because
    the json isn't sent to the client using `jsonify`
    """
    r = db.session.execute(Iconography.query)
    return jsonify([ _[0].serialize_lite() for _ in r.all() ])


@app.route("/i/iconography/<id_uuid>")
def main_iconography(id_uuid):
    """return an `Iconography` object based on its `id_uuid`"""
    r = db.session.execute(Iconography
                           .query
                           .filter(Iconography.id_uuid == id_uuid))
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


@app.route("/i/iconography-from-uuid")
def iconography_from_uuid():#id_uuid_arr:t.List[str]):
    """
    return Iconography objects matching the UUIDs in `id_uuid_arr`.
    the UUIDs desired have the parameter name `id_uuid`.
    """
    id_uuid_arr = request.args.getlist("id_uuid")
    out = []

    if len(id_uuid_arr):
        query = select( Iconography ).filter( Iconography.id_uuid.in_(id_uuid_arr) )
        r = db.session.execute( query ).all()
        out = [ icono[0].serialize_full() for icono in r ]

    return jsonify(out)


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


# *************************************************************************
# place
# *************************************************************************

@app.route("/i/place")
def index_place():
    """
    get all `place` ressources
    """
    r = db.session.execute(Place.query)
    return jsonify([  _[0].serialize_lite() for _ in r.all() ])


@app.route("/i/place-lite/<place_uuid>")
def place_lite(place_uuid:str):
    """
    get a single `place` item and return its `serialize_lite()` repr
    """
    r = db.session.execute(Place.query.filter(Place.id_uuid==place_uuid).limit(1))
    return jsonify([ _[0].serialize_lite() for _ in r.all() ])


# *************************************************************************
# theme
# *************************************************************************

@app.route("/i/theme")
def index_theme():
    """
    return an index of theme categories or an
    index of themes for a single category.
    2 optional arguments can be passed in the query string:
    * "category" (null|str):
        category determines the kind of index returned:
        * category is null: an index of distinct categories is returned
        * category == all: all themes are returned
        * category is not null (a category is given): all themes for this
            category are returned.
    * "preview" (bool):
        when category is None (returning an index of categories)
        and preview is true, we'll also return a few themes as an example
    """
    category_name = request.args.get("category", None)
    preview       = request.args.get("preview", None)
    if not category_name:
        out = Theme.get_categories(preview=preview)
    elif category_name == "all":
        out = [ t[0].serialize_lite()
                for t in db.session.execute(Theme.query).all() ]
    else:
        out = Theme.get_themes_for_category(category_name)
    return jsonify(out)


@app.route("/i/theme/<id_uuid>")
def main_theme(id_uuid:str):
    """fetch all iconographic resources related to a theme"""
    r = db.session.execute(Theme.query.filter( Theme.id_uuid == id_uuid ))
    return jsonify([ t[0].serialize_full() for t in r.all() ])


@app.route("/i/theme-name/<id_uuid>")
def main_theme_name(id_uuid:str):
    """
    get the name of a theme from its UUID. used in the main page for a theme.
    """
    r = db.session.execute(Theme.query.filter( Theme.id_uuid == id_uuid ))
    return jsonify([ t[0].entry_name for t in r.all() ])


# *************************************************************************
# named_entity
# *************************************************************************


@app.route("/i/named-entity")
def index_named_entity():
    """
    return an index of named entity categories or an index of named entities.
    2 optional arguments can be passed in the query string:
    * "category" (null|str):
        category determines the kind of index returned:
        * category is null: an index of distinct categories is returned
        * category == all: all named entities are returned
        * category is not null (a category is given): all named entities
          for this category are returned.
    * "preview" (bool):
        when category is None (returning an index of categories)
        and preview is true, we'll also return a few named entities as
        an example
"""
    category_name = request.args.get("category", None)
    preview       = request.args.get("preview", None)
    if not category_name:
        out = NamedEntity.get_categories(preview=preview)
    elif category_name == "all":
        out = [ n[0].serialize_lite()
                for n in db.session.execute(NamedEntity.query).all() ]
    else:
        out = NamedEntity.get_named_entities_for_category(category_name)
    return jsonify(out)


@app.route("/i/named-entity/<id_uuid>")
def main_named_entity(id_uuid:str):
    """
    fetch all iconographic resources related to a named entity.
    """
    r = db.session.execute(NamedEntity.query.filter( NamedEntity.id_uuid == id_uuid ))
    return jsonify([ n[0].serialize_full() for n in r.all() ])


@app.route("/i/named-entity-name/<id_uuid>")
def main_named_entity_name(id_uuid:str):
    """
    get the name of a named entity from its UUID
    used in the main pages for a named entity.
    """
    r = db.session.execute(NamedEntity.query.filter( NamedEntity.id_uuid == id_uuid ))
    return jsonify([ n[0].entry_name for n in r.all() ])


# *************************************************************************
# cartography
# *************************************************************************

@app.route("/i/cartography")
def index_cartography():
    """
    get all `cartography` ressources.
    """
    r = db.session.execute(Cartography.query)
    return jsonify([ _[0].serialize_lite() for _ in r.all() ])


# *************************************************************************
# institution
# *************************************************************************

@app.route("/i/institution")
def institution():
    """
    get all institution elements
    """
    r = db.session.execute(Institution.query)
    return jsonify([ i[0].serialize_lite() for i in r.all() ])


# *************************************************************************
# directory
# *************************************************************************

@app.route("/i/directory")
def index_directory():
    """
    get all directory ressources
    """
    r = db.session.execute(Directory.query)
    return jsonify([ _[0].serialize_lite() for _ in r.all() ])


# *************************************************************************
# advanced search
# *************************************************************************
@app.route("/i/search/iconography", methods=["GET", "POST"])
def advanced_search_iconography():
    """
    the heavy work is done in `../search/search_iconography.py`

    allowed query parameters:
    * `title`       :
    * `author`      :
    * `publisher`   :
    * `theme`       :
    * `namedEntity` :
    * `institution` :
    * `dateFilter`  :
    * `date[]`      :

    """
    if request.method == "POST" and request.is_json:
        results = []
        params, valid = make_params(request.get_json(cache=True))
        if not valid:
            return "Internal server error at `make_params`", 500
        params, valid = sanitize_params(params)
        if not valid:
            return "Internal server error at `sanitize_params`", 500
        print(r"%%%%% let's rock")
        results = make_query(params).all()
        return jsonify([ r[0].serialize_lite() for r in results ])
    else:
        return "This route only accepts HTTP with JSON parameters", 400


# *************************************************************************
# associations
# *************************************************************************

@app.route("/i/association/theme-from-theme/<id_uuid>")
def association_theme_from_theme(id_uuid:str):
    """
    get the most frequently associated themes from a theme:
    fetch the themes that are most frequently used to tag
    iconography ressources that have the theme `id_uuid`.

    the logic is:
    1) get all iconography ressources with the good theme
    2) get all the themes that are used to tag those iconography resources
    3) groupby + count + order: count the number of occurrences of each
       theme, and keep only the 5 most used themes.

    the query below is analog to:
    >>> SELECT
    ...   theme.id
    ...   , theme.entry_name
    ...   , COUNT (theme.id) AS count_associated
    ... FROM theme
    ... JOIN r_iconography_theme
    ... ON theme.id = r_iconography_theme.id_theme
    ... JOIN iconography
    ... ON r_iconography_theme.id_iconography = iconography.id
    ... AND iconography.id IN (
    ...   SELECT iconography.id
    ...   FROM iconography
    ...   JOIN r_iconography_theme
    ...   ON r_iconography_theme.id_iconography = iconography.id
    ...   JOIN theme ON theme.id = r_iconography_theme.id_theme
    ...   AND theme.id = 1
    ... )
    ... WHERE theme.id != 1
    ... GROUP BY theme.id
    ... ORDER BY count_associated DESC
    ... LIMIT 5;

    return structure:
    >>> [
    ...    # 1st theme
    ...    { "id_uuid"    : "<uuid for a theme>",
    ...      "entry_name" : "<name of the theme>",
    ...      "count"      : "<number of times a theme is associated with the theme on which we run a query>"
    ...    },
    ...    # other themes
    ...    {...}
    ... ]

    :param id_uuid: the UUID of the theme to get associations from
    :returns: a jsonified list of dicts, with the structure described above
    """
    # all iconography tagged with theme with `id_uuid`
    icono_for_theme = (select(Iconography.id)
                       .join( Iconography.r_iconography_theme )
                       .join( R_IconographyTheme
                              .theme
                              .and_(Theme.id_uuid == id_uuid)))
    # main query
    q = (select( Theme.id_uuid
                , Theme.entry_name
                , func.count(Theme.id).label("associates_count") )  # `.label()` is compulsory !!! (and not `.alias()` !!)
         # fetch all themes that are connected to the current theme
         .join( Theme.r_iconography_theme )
         .join( R_IconographyTheme
                .iconography
                .and_( Iconography.id.in_(icono_for_theme) ))
         # ensure we don't process the current theme
         .filter( Theme.id_uuid != id_uuid )
         # groupby, orders and limits.
         .group_by(Theme.id)
         .order_by(func.count(Theme.id).desc() )
         .limit(5) )

    # run query, restructure results, return
    r = db.session.execute(q).all()
    r = [ { "id_uuid": row[0], "entry_name": row[1], "count": row[2] } for row in r ]
    return jsonify(r)


@app.route("/i/association/named-entity-from-theme/<id_uuid>")
def association_named_entity_from_theme(id_uuid:str):
    """
    get the most frequently associated named entites from a theme:
    fetch the NEs that are most frequently used to tag iconography
    ressources that have the theme `id_uuid`.

    see the doc of `associated_theme_from_theme` for details.
    """
    # all iconography tagged with theme with `id_uuid`
    icono_for_theme = (select(Iconography.id)
                       .join( Iconography.r_iconography_theme )
                       .join( R_IconographyTheme
                              .theme
                              .and_(Theme.id_uuid == id_uuid)))
    # main query
    q = (select( NamedEntity.id_uuid
               , NamedEntity.entry_name
               , func.count(NamedEntity.id).label("associates_count") )  # `.label()` is compulsory !!! (and not `.alias()` !!)
         # fetch all themes that are connected to the current theme
         .join( NamedEntity.r_iconography_named_entity )
         .join( R_IconographyNamedEntity
                .iconography
                .and_( Iconography.id.in_(icono_for_theme) ))
         # groupby, orders and limits.
         .group_by(NamedEntity.id)
         .order_by(func.count(NamedEntity.id).desc() )
         .limit(5) )

    # run query, restructure results, return
    r = db.session.execute(q).all()
    r = [ { "id_uuid": row[0], "entry_name": row[1], "count": row[2] } for row in r ]
    return jsonify(r)


@app.route("/i/association/named-entity-from-named-entity/<id_uuid>")
def association_named_entity_from_named_entity(id_uuid:str):
    """
    get the most frequently associated named entites from a named entity:
    fetch the NEs that are most frequently used to tag iconography
    ressources that have the named entity with UUID `id_uuid`.

    see the doc of `associated_theme_from_theme` for details.
    """
    # all iconography tagged with NE with `id_uuid`
    icono_for_ne = (select(Iconography.id)
                    .join( Iconography.r_iconography_named_entity )
                    .join( R_IconographyNamedEntity
                           .named_entity
                           .and_(NamedEntity.id_uuid == id_uuid)))
    # main query
    q = (select( NamedEntity.id_uuid
               , NamedEntity.entry_name
               , func.count(NamedEntity.id).label("associates_count") )  # `.label()` is compulsory !!! (and not `.alias()` !!)
         # fetch all themes that are connected to the current theme
         .join( NamedEntity.r_iconography_named_entity )
         .join( R_IconographyNamedEntity
                .iconography
                .and_( Iconography.id.in_(icono_for_ne) ))
         # ensure we don't process the current named entity
         .filter( NamedEntity.id_uuid != id_uuid )
         # groupby, orders and limits.
         .group_by(NamedEntity.id)
         .order_by(func.count(NamedEntity.id).desc() )
         .limit(5) )

    # run query, restructure results, return
    r = db.session.execute(q).all()
    r = [ { "id_uuid": row[0], "entry_name": row[1], "count": row[2] } for row in r ]
    return jsonify(r)

@app.route("/i/association/theme-from-named-entity/<id_uuid>")
def association_theme_from_named_entity(id_uuid:str):
    """
    get the most frequently associated themes from a named entity:
    fetch the themes that are most frequently used to tag iconography
    ressources that have the NE with UUID `id_uuid`.

    see the doc of `associated_theme_from_theme` for details.
    """
    # all iconography tagged with NE with `id_uuid`
    icono_for_ne = (select(Iconography.id)
                    .join( Iconography.r_iconography_named_entity )
                    .join( R_IconographyNamedEntity
                           .named_entity
                           .and_(NamedEntity.id_uuid == id_uuid)))
    # main query
    q = (select( Theme.id_uuid
               , Theme.entry_name
               , func.count(Theme.id).label("associates_count") )  # `.label()` is compulsory !!! (and not `.alias()` !!)
         # fetch all themes that are connected to the current theme
         .join( Theme.r_iconography_theme )
         .join( R_IconographyTheme
                .iconography
                .and_( Iconography.id.in_(icono_for_ne) ))
         # groupby, orders and limits.
         .group_by(Theme.id)
         .order_by(func.count(Theme.id).desc() )
         .limit(5) )

    # run query, restructure results, return
    r = db.session.execute(q).all()
    r = [ { "id_uuid": row[0], "entry_name": row[1], "count": row[2] } for row in r ]
    return jsonify(r)


@app.route("/i/association/index")
def association_index():
    """
    build an index of `iconography` resources where
    from_table.id_uuid == from_id_uuid and to_table.id_uuid == to_id_uuid

    query params:
    * from_table   str : tableA's name in the database
    * to_table     str : tableB's name in the database
    * from_id_uuid str : id_uuid in tableA
    * to_id_uuid   str : id_uuid in tableB
    """
    # 1) get and test params
    params = { "from_table"  : request.args.get("from_table", None),
               "to_table"    : request.args.get("to_table", None),
               "from_id_uuid": request.args.get("from_id_uuid", None) ,
               "to_id_uuid"  : request.args.get("to_id_uuid", None) }

    # check that we have valid data
    tablenames = db.session.execute(text( "SELECT table_name "
                                        + "FROM information_schema.tables "
                                        + "WHERE table_schema = 'public';"))
    tablenames = [ _[0] for _ in tablenames.all() ]  # list of allowed table names
    if ( any( v == None or v == "" for v in params.values() )
         or params["from_table"] not in tablenames
         or params["to_table"] not in tablenames ):
        return "Internal server error at `make_params`", 500

    # 2) helper functions
    # a lambda function is defined for each filter on
    # the Iconography table, for a modular approach:
    # we apply different filters at different points, but the
    # filtering used is the same (filter by a theme UUID will
    # always look the same). so, those functions will be used
    # at the needed places with the params needed.
    # params:
    #   * q           : the query
    #   * id_uuid     : an uuid string
    #   * id_uuid_arr : an array of id_uuids, when we're getting the association
    #                   between 2 rows of the same table
    by_theme = lambda q, id_uuid: (
        q.join(Iconography.r_iconography_theme)
              .join(R_IconographyTheme
                    .theme
                    .and_( Theme.id_uuid == id_uuid )))
    by_named_entity = lambda q, id_uuid: (
        (q.join(Iconography.r_iconography_named_entity)
          .join(R_IconographyNamedEntity
                .named_entity
                .and_( NamedEntity.id_uuid == id_uuid ))))
    # USELESS: these would be equivalent to an OR between
    # different values of the same table (an SQL OUTER JOIN
    # between from_id_uuid and to_id_uuid), where we want an
    # INNER JOIN.
    # by_named_entity_arr = lambda q, id_uuid_arr: (
    #     (q.join(Iconography.r_iconography_named_entity)
    #       .join(R_IconographyNamedEntity
    #            .named_entity
    #            .and_( NamedEntity.id_uuid.in_(id_uuid_arr) ))) )
    # by_theme_arr = lambda q, id_uuid_arr: (
    #     q.join(Iconography.r_iconography_theme)
    #           .join(R_IconographyTheme
    #                .theme
    #                .and_( Theme.id_uuid.in_(id_uuid_arr) )))

    # 3) build query
    base_query = select(func.distinct(Iconography.id))  # base query

    # associating between 2 id_uuids of the same table. this will need
    # an inner join with a subquery, main query for themeA, subquery for themeB
    if ( params["from_table"] == params["to_table"]
         and params["from_table"] == "theme" ):
        base_query = by_theme( base_query, params["from_id_uuid"] )
        to_query   = by_theme( select(Iconography.id)
                             , params["to_id_uuid"] )
        base_query = base_query.filter(Iconography.id.in_(to_query))
    # named_entityA and named_entityB
    elif ( params["from_table"] == params["to_table"]
           and params["from_table"] == "named_entity" ):
        base_query = by_named_entity( base_query, params["from_id_uuid"] )
        to_query   = by_named_entity( select(Iconography.id)
                                    , params["to_id_uuid"] )
        base_query = base_query.filter(Iconography.id.in_(to_query))

    # associating 2 different tables. no subqueries, just chain joins.
    else:
        # from a theme
        if params["from_table"] == "theme":
            base_query = by_theme(base_query, params["from_id_uuid"])
        # from a named entity
        elif params["from_table"] == "named_entity":
            base_query = by_named_entity(base_query, params["from_id_uuid"])
        # to a theme
        if params["to_table"] == "theme":
            base_query = by_theme(base_query, params["to_id_uuid"])
        # to a named entity
        elif params["to_table"] == "named_entity":
            base_query = by_named_entity(base_query, params["to_id_uuid"])

    query = select( Iconography ).filter( Iconography.id.in_(base_query) )
    r = db.session.execute(query)

    # import sqlparse
    # print(sqlparse.format(str(query), keyword_case="upper", reindent=True))

    return [ i[0].serialize_lite() for i in r.all() ]







# *************************************************************************
# table viewer
# *************************************************************************


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
