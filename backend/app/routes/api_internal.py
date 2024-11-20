"""
routes for the internal API
basepath: `<APP URL>/i/`
"""

from flask import jsonify, request
from psycopg2.extras import NumericRange
from sqlalchemy import text, func
from sqlalchemy.sql.expression import bindparam
import random
import json

from ..search.search_iconography import sanitize_params, make_params, make_query
from ..utils.spatial import featurelist_to_featurecollection, geometry_to_feature
from ..app import app, db
from ..orm import *


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
def iconography_from_uuid():
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
# theme
# *************************************************************************

@app.route("/i/theme")
def index_theme():
    """
    return an index of theme categories or an
    index of themes for a single category.
    2 optional arguments can be passed in the query string:
    * "category" (null|str):
        a value of `theme.category_slug`.
        category determines the kind of index returned:
        * category is null: an index of distinct categories is returned
        * category == all: all themes are returned
        * category is not null (a category is given): all themes for this
            category are returned.
    * "preview" (bool):
        when category is None (returning an index of categories)
        and preview is true, we'll also return a few themes as an example
    """
    category_slug = request.args.get("category", None)
    preview       = request.args.get("preview", None)
    if not category_slug:
        out = Theme.get_categories(preview=preview)
    elif category_slug == "all":
        out = [ t[0].serialize_lite()
                for t in db.session.execute(Theme.query).all() ]
    else:
        out = Theme.get_themes_for_category(category_slug)
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

@app.route("/i/theme-category-name/<string:category_slug>")
def theme_category_name(category_slug:str):
    """
    returns as a string the category name corresponding to a category_slug
    (or empty string if category_slug is not in the database)
    """
    r = db.session.execute(select(Theme.category)
                          .filter(Theme.category_slug==category_slug)
                          .limit(1)).all()
    if len(r):
        return r[0][0]
    else:
        return ""



# *************************************************************************
# named_entity
# *************************************************************************


@app.route("/i/named-entity")
def index_named_entity():
    """
    return an index of named entity categories or an index of named entities.
    2 optional arguments can be passed in the query string:
    * "category" (null|str):
        a value of `named_entity.category_slug`.
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
    category_slug = request.args.get("category", None)
    preview       = request.args.get("preview", None)
    if not category_slug:
        out = NamedEntity.get_categories(preview=preview)
    elif category_slug == "all":
        out = [ n[0].serialize_lite()
                for n in db.session.execute(NamedEntity.query).all() ]
    else:
        out = NamedEntity.get_named_entities_for_category(category_slug)
    return jsonify(out)


@app.route("/i/named-entity/<id_uuid>")
def main_named_entity(id_uuid:str):
    """
    fetch all iconographic resources related to a named entity.
    """
    r = db.session.execute(NamedEntity.query.filter( NamedEntity.id_uuid==id_uuid ))
    return jsonify([ n[0].serialize_full() for n in r.all() ])


@app.route("/i/named-entity-name/<id_uuid>")
def main_named_entity_name(id_uuid:str):
    """
    get the name of a named entity from its UUID
    used in the main pages for a named entity.
    """
    r = db.session.execute(NamedEntity.query.filter( NamedEntity.id_uuid == id_uuid ))
    return jsonify([ n[0].entry_name for n in r.all() ])


@app.route("/i/named-entity-category-name/<string:category_slug>")
def named_entity_category_name(category_slug:str):
    """
    returns as a string the category name corresponding to a category_slug
    (or empty string if category_slug is not in the database)
    """
    r = db.session.execute(select(NamedEntity.category)
                          .filter(NamedEntity.category_slug==category_slug)
                          .limit(1)).all()
    if len(r):
        return r[0][0]
    else:
        return ""



# *************************************************************************
# cartography
# *************************************************************************

# @app.route("/i/cartography")
# def index_cartography():
#     """
#     get all `cartography` ressources.
#     """
#     r = db.session.execute(Cartography.query)
#     return jsonify([ _[0].serialize_lite() for _ in r.all() ])


# *************************************************************************
# institution
# *************************************************************************

@app.route("/i/institution")
def institution():
    """
    get all institution elements
    """
    # { <institution UUID>: <thumbnail filename> }
    inst2thumb = { "qr1ea925dc913804199ac1c0576480da5aa": "qr1a9a823e79d324dcdada5a7eb1b761de3_thumbnail.jpg"   # "Paris Musées"
                 , "qr18d6914c2135449f8ad5fc8300330c34c": "qr1a8db9e2be4f14571a99d814077ba4208_thumbnail.jpg"  # "Musée Carnavalet"
                 , "qr1e592407a3eac4928bbf09cb9646b6442": "qr145c0ac40ad5d4840aa9c985751bcb92a_thumbnail.png"  # "Palais Galliera"
                 , "qr10e70091de4a84c439d015709c8dc231f": "qr170575ace1f514f2e9651cf461963684e_thumbnail.jpg"  # "Maison de Balzac"
                 , "qr10569e23940cc4e51a58a3c6e11ec5b15": "qr136ca7ccdb402484aad0ce11805a56b5d_thumbnail.jpg"  # "Maison Victor Hugo"
                 , "qr18bd3abcff61c43589bd4832c4dffb09c": "qr1a64d9cdfbcc94140a5503525bcad6815_thumbnail.jpg"  # "Musée de la Vie Romantique"
                 , "qr152fb32c9ed2b4d48a943b4009f79f744": "qr1000160a5037549298f09510d68b36625_thumbnail.jpg"  # "Petit Palais. Musée des Beaux-Arts de la Ville de Paris"
                 , "qr19b5a6f70e5174a47be128d7d16cf871e": "qr1d4ddcb8f8589426e913118c89ab5ccdc_thumbnail.png"  # "Musée Bourdelle"
                 , "qr1dd89263f396e4f4ea99c4e581056f6b9": "qr177380f23b1b34e2dba9a9daae0ef0ecc_thumbnail.png"  # "Musée de la Libération Leclerc Moulin"
                 , "qr1882f452734fc4049ae13bab3ae018981": "qr118531ea2f689409d9aa2639d1ae70971_thumbnail.jpg"  # "Bibliothèques spécialisées de la Ville de Paris"
                 , "qr1ca5f8a45cb6a47b3b061ab0fae4dea82": "qr174c20bfec0364b56baca363bdca8c545_thumbnail.png"  # "Bibliothèque historique de la Ville de Paris"
                 , "qr14351c77b3dfa4111999c061af5a3a916": "qr1c32441bdb6124348bd672a93c6bdae58_thumbnail.jpg"  # "Bibliothèque de l'Hôtel de Ville"
                 , "qr1ee06b75474624e36a51b81497bc9fbda": "qr1e0962628672d428e97e597b831995342_thumbnail.jpg"  # "Bibliothèque Marguerite Durand"
                 , "qr13745abfe1ee94c73aa1fcd253b95430c": "qr120ab66fe685c41ba88dd15eeb5536493_thumbnail.jpg"  # "Bibliothèque Forney"
                 , "qr16884f242eafd4ddf912de09ca781fb8a": "qr194bb5b3ae08a45b48d7c8bf23f98c039_thumbnail.jpg"  # "Médiathèque musicale de Paris"
                 , "qr13b8e3da4301c4968ad2dbb09b9cf1dd5": "qr1716753b57de94d2b838007568d8a2147_thumbnail.png"  # "Bibliothèque des littératures policières"
                 , "qr13d1f6905f87144c69215e1ec02617a6a": "qr1b6d1d2fd24c44befb21432d3f0a5fce1_thumbnail.png"  # "Bibliothèque du tourisme et des voyages - Germaine Tillion"
                 , "qr1e60d7b097d4c4992af50cd72c04cc201": "qr16c11b578d5d34a4f9fa34c26280561ea_thumbnail.jpg"  # "Bibliothèque nationale de France"
                 , "qr1216b8ae2f04d4f68b84af8b741acbfd7": "qr1cea1aed793b149e28369ac54fbb89b7a_thumbnail.jpg"  # "British Museum"
                 , "qr1d6719fcd30c0411fb6aa6f518bec9339": "qr147e634fc598d47a48943a1abcf2f044b_thumbnail.jpg"  # "Institut national d'histoire de l'art"
                 , "qr1f82c23e4552e492fb7b176e2440e914e": "qr1db9aaa7da856404a9e5cd61731730c6b_thumbnail.jpg"  # "Musée Albert Kahn"
                 , "qr115bbf999ddf243c2ad45c8ab74e681c7": "qr12514d40f367e4bb5971772833d7d0d99_thumbnail.jpeg"  # "Archives de Paris"
                 , "qr1f7eaf6cfa0984af6a19e19c34d023b95": "qr198bca81c64034f7687eb2c4070046c55_thumbnail.jpg"  # "Médiathèque Marguerite Duras"
                 , "qr1d60bd0309bd248b08ee2278a574066c6": "qr1b05b286d81c240a6aaffd8f00361904d_thumbnail.jpg"  # "Bibliothèque municipale et partimoniale Villon"
                 }
    subq_count = (select(R_Institution.id_institution, func.count(R_Institution.id))
                 .group_by(R_Institution.id_institution)
                 .subquery() )
    subq_id = (select(R_Institution.id_institution)
              .filter(R_Institution.id_iconography != None))
    q = (select(Institution.id_uuid, Institution.entry_name, subq_count.c.count)   # in a subquery, `subq.c` allows to get the columns of a subquery object. see: https://stackoverflow.com/a/30311684/17915803
        .join(subq_count, subq_count.c.id_institution == Institution.id)
        .filter(Institution.id.in_(subq_id)) )

    r = db.session.execute(q)
    return jsonify([ { "id_uuid"           : i[0],
                       "entry_name"        : i[1],
                       "iconography_count" : i[2],
                       "thumbnail"         : [ inst2thumb[i[0]] ] }
                     for i in r.all() ])


@app.route("/i/institution/<string:id_uuid>")
def main_institution(id_uuid: str):
    """
    return data for a specific institution
    """
    r = db.session.execute(select(Institution).filter(Institution.id_uuid == id_uuid))
    return jsonify([ i[0].serialize_full() for i in r.all() ])

@app.route("/i/institution-name/<string:id_uuid>")
def main_institution_name(id_uuid:str):
    """
    get the name of an institution from its UUID
    used in the main pages for an institution.
    """
    r = db.session.execute(select(Institution.entry_name)
                          .filter(Institution.id_uuid == id_uuid) )
    return jsonify([ n[0] for n in r.all() ])


# *************************************************************************
# place
# *************************************************************************

@app.route("/i/place")
def index_place():
    """
    get all `place` ressources
    """
    r = db.session.execute(Place.query)
    return jsonify([ _[0].serialize_lite() for _ in r.all() ])

@app.route("/i/place/<string:id_uuid>")
def place_main(id_uuid:str):
    """
    fetch a place from its `id_uuid` and return all iconography.
    """
    r = db.session.execute(select(Place).filter(Place.id_uuid == id_uuid))
    return jsonify([ _[0].serialize_full() for _ in r.all() ])


@app.route("/i/place-lite/<string:place_uuid>")
def place_lite(place_uuid:str):
    """
    get a single `place` item and return its `serialize_lite()` repr
    """
    r = db.session.execute(Place.query.filter(Place.id_uuid==place_uuid).limit(1))
    return jsonify([ _[0].serialize_lite() for _ in r.all() ])

@app.route("/i/place-address/<string:id_uuid>")
def place_address(id_uuid):
    """
    get an address for a place based on this place's `id_uuid`
    """
    r = db.session.execute(select( Address )
                          .join( Address.r_address_place )
                          .join( R_AddressPlace.place )
                          .filter( Place.id_uuid == id_uuid )
                          )
    return jsonify([ addr[0].serialize_lite() for addr in r.all() ])


# *************************************************************************
# directory
# *************************************************************************

@app.route("/i/directory")
def index_directory():
    """
    get all directory ressources. currently unused (?)
    """
    r = db.session.execute(Directory.query)
    return jsonify([ _[0].serialize_lite() for _ in r.all() ])


# *************************************************************************
# CartographyView.vue routes (frontend cartographic interface)
# *************************************************************************

@app.route("/i/cartography-main/places")
def cartography_places():
    """
    get all places and return them as a geojson FeatureCollection
    """
    places = [ p[0].serialize_lite()
               for p in db.session.execute( Place.query ).all() ]
    places = [
        geometry_to_feature( geometry=p["vector"]
                           , custom_properties={
                               "address"           : p["address"],
                               "iconography_count" : p["iconography_count"],
                               "id_uuid"           : p["id_uuid"]
                           })
               for p in places ]
    places = featurelist_to_featurecollection(places)
    return jsonify(places)

@app.route("/i/cartography-main/cartography/source")
def cartography_sources():
    """
    get a list of all distinct Cartography.map_source
    and return it as a list of strings
    """
    sources = (db.session
              .execute( select(func.distinct(Cartography.map_source)) )
              .all())
    sources = [ s[0] for s in sources ]
    return jsonify(sources)


@app.route("/i/cartography-main/cartography/source/<string:cartography_source>")
def cartography_for_source(cartography_source:str):
    """
    return a list of Cartography objects with Cartography.map_source == cartography_source
    """
    r = (db.session
        .execute( select(Cartography).filter(Cartography.map_source == cartography_source) )
        .all())
    return jsonify([ c[0].serialize_lite() for c in r ])


@app.route("/i/cartography-main/cartography/granularity")
def cartography_granularity():
    """
    get a list of all distinct `Cartography.granularity` values
    and return it as a list of strings
    """
    gran = (db.session
           .execute( select(func.distinct(Cartography.granularity)) )
           .all())
    gran = [ g[0] for g in gran ]
    return jsonify(gran)

@app.route("/i/cartography-main/cartography/granularity/<string:cartography_granularity>")
def cartography_for_granularity(cartography_granularity: str):
    """
    get all cartography sources for a certain granularity
    """
    r = (db.session
        .execute( select(Cartography).filter(Cartography.granularity == cartography_granularity) )
        .all() )
    return jsonify([ c[0].serialize_lite() for c in r ])


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
        results = make_query(params).all()
        return jsonify([ r[0].serialize_lite() for r in results ])
    else:
        return "This route only accepts HTTP with JSON parameters", 400


# *************************************************************************
# associations
# *************************************************************************

@app.route("/i/association/theme-from-theme/<string:id_uuid>")
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


@app.route("/i/association/named-entity-from-theme/<string:id_uuid>")
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


@app.route("/i/association/named-entity-from-named-entity/<string:id_uuid>")
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

@app.route("/i/association/theme-from-named-entity/<string:id_uuid>")
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


@app.route("/i/association/place-from-place/<string:id_uuid>")
def association_place_from_place(id_uuid:str):
    """
    returns the UUIDs of the 5 places most often places tagged with
    the place `id_uuid`, together with a count of the number of
    associations with the place

    :arguments:
        id_uuid: a Place.id_uuid
    :returns:
        a list of dicts with 2 keys, `id_uuid` and `count`
        [ { id_uuid   : <string:place.id_uuid>,
            entry_name: <string: address of the associated place>
            count     : <int:number of relations between input place and related places>
          }
        ]

    equivalent to (slightly optimized equivalent of
    the above association queries):

    >>> -- 3) get the place.id related to
    ... --    all r_iconography_place.id_iconography
    ... --    retrieved in the subquery 2)
    ... SELECT place.id_uuid,
    ...        COUNT(place.id_uuid) AS cnt
    ... FROM place
    ... JOIN r_iconography_place
    ... ON r_iconography_place.id_place = place.id
    ... JOIN r_address_place
    ... ON r_address_place.id_place = place.id
    ... JOIN address
    ... ON r_address_place.id_address = address.id
    ... AND address.source = place.vector_source
    ... WHERE r_iconography_place.id_iconography IN (
    ...   -- 2) get the r_iconography_place.id_iconography
    ...   --    for r_iconography_place.id_place
    ...   SELECT r_iconography_place.id_iconography
    ...   FROM r_iconography_place
    ...   WHERE r_iconography_place.id_place = (
    ...     -- 1) get the place.id for place.id_uuid
    ...     SELECT place.id
    ...     FROM place
    ...     WHERE place.id_uuid = 'qr14c0bf395f74f460a845c4cab8d2c83a2'
    ...     LIMIT 1
    ...   )
    ... )
    ... GROUP BY place.id_uuid, address.address;
    ... ORDER BY cnt DESC
    ... LIMIT 5
    """
    # returns Place.id for `id_uuid`
    id_place = select( Place.id ).filter( Place.id_uuid == id_uuid ).scalar_subquery()
    # returns all `Iconography.id` related to the `Place.id`
    id_icono = (select( func.distinct(R_IconographyPlace.id_iconography) )
               .filter( R_IconographyPlace.id_place == id_place ))
    # returns all `Place.id` related to all `Iconography.id` related to the `Place.id`,
    # with a count of number of relations
    query    = (select( Place.id_uuid, Address.address, func.count(Place.id_uuid) )
               .join( Place.r_address_place )
               .join( R_AddressPlace.address.and_(Address.source == Place.vector_source) )
               .join( Place.r_iconography_place )
               .filter( R_IconographyPlace.id_iconography.in_(id_icono)
                      , R_IconographyPlace.id_place != id_place )
               .group_by( Place.id_uuid, Address.address )
               .order_by( func.count(Place.id_uuid).desc() )
               .limit(5) )
    r = [ { "id_uuid": row[0], "entry_name": row[1], "count": row[2] }
          for row in db.session.execute(query).all() ]
    return jsonify(r)


@app.route("/i/association/index")
def association_index():
    """
    build an index of `iconography` resources where
    from_table.id_uuid == from_id_uuid and to_table.id_uuid == to_id_uuid.

    this function is as generic as possible, BUT
    * behaviour is defined table-by-table
    * only behaviour that will actually appear in the site is implemented
      (for example, only associations from place to place is implemented,
      so associations between a place and another table doesn't exist)

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
        q.join(Iconography.r_iconography_named_entity)
         .join(R_IconographyNamedEntity
              .named_entity
              .and_( NamedEntity.id_uuid == id_uuid )))
    by_place = lambda q, id_uuid: (
        q.join(Iconography.r_iconography_place)
         .join(R_IconographyPlace
              .place
              .and_( Place.id_uuid == id_uuid )))

    # 3) build query
    base_query = select(func.distinct(Iconography.id))  # base query

    # associating between 2 id_uuids of the same table. this will need
    # an inner join with a subquery, main query for themeA, subquery for themeB
    if ( params["from_table"] == params["to_table"]
         and params["from_table"] == "theme" ):
        base_query = by_theme( base_query, params["from_id_uuid"] )
        to_query   = by_theme( select(Iconography.id), params["to_id_uuid"] )
        base_query = base_query.filter( Iconography.id.in_(to_query) )
    # named_entityA and named_entityB
    elif ( params["from_table"] == params["to_table"]
           and params["from_table"] == "named_entity" ):
        base_query = by_named_entity( base_query, params["from_id_uuid"] )
        to_query   = by_named_entity( select(Iconography.id), params["to_id_uuid"] )
        base_query = base_query.filter( Iconography.id.in_(to_query) )
    # placeA and placeB
    elif ( params["from_table"] == params["to_table"]
           and params["from_table"] == "place" ):
        base_query = by_place( base_query, params["from_id_uuid"] )
        to_query   = by_place( select(Iconography.id), params["to_id_uuid"] )
        base_query = base_query.filter( Iconography.id.in_(to_query) )

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
    r = db.session.execute( query )

    # import sqlparse
    # print(sqlparse.format(str(query), keyword_case="upper", reindent=True))

    return [ i[0].serialize_lite() for i in r.all() ]

# *************************************************************************
# other
# *************************************************************************

@app.route("/i/database-counts")
def dbcounts():
    """
    returns the number of rows for each table as json of
    `{ <tablename> : <number of rows> }`.
    the `bindparam` allows to select a text literal
    see: https://stackoverflow.com/a/7546802/17915803
    """
    q = (db.session.query( bindparam("tablename_0", "iconography"), func.count(Iconography.id) )
        .union( select( bindparam("tablename_1", "theme"), func.count(Theme.id))
              , select( bindparam("tablename_2", "named_entity"), func.count(NamedEntity.id))
              , select( bindparam("tablename_3", "place"), func.count(Place.id))
              , select( bindparam("tablename_4", "institution"), func.count(Institution.id)))
        )
    r = db.session.execute(q).all()
    return { row[0] : row[1] for row in r }


# *************************************************************************

# @app.route("/i/raise")
# def do_raise():
#     """test error raising and printing in prod"""
#     print(r"%%%%% this should raise")
#     raise ValueError("\n%%%%% hello ! \n%%%%% this has raised. \n%%%%% goodbye !")





# # *************************************************************************
# # table viewer
# # *************************************************************************
#
#
# @app.route("/i/list-tables")
# def list_tables():
#     """
#     list all public tables in the database
#     """
#     r = db.session.execute(text( "SELECT table_name "
#                                + "FROM information_schema.tables "
#                                + "WHERE table_schema = 'public';"))
#     return jsonify([ _[0] for _ in r.all() ])
#
#
# @app.route("/i/table-viewer/<tablename>")
# def table_viewer(tablename:str):
#     """
#     get and return an entire table as a json
#     """
#     # convert postgres-specific datatypes into json-compliant ones.
#     maybe_convert = lambda el: el if not isinstance(el, NumericRange) else int4range2list(el)
#     # transform a row of values into a dict of `{ <colname>: <value> }`
#     mapper = lambda row: { colnames[i]: maybe_convert(row[i]) for i, r in enumerate(row) }
#     # process the SQL response into a list of `{ <colname>: <value> }` elts
#     response_process = lambda x: [ mapper(row) for row in x ]
#
#     # run the query
#     r = db.session.execute(text(f"SELECT * FROM {tablename};"))
#     colnames = list(r.keys())  # column names for the query
#
#     # process the results. if there are no results, generate
#     # a 1 item list mapping all column names to `None`, to
#     # be able to display something in the frontend.
#     # `r.rowcount` returns the number of rows in the `CursorResult`;
#     # contrary to `all()`, it doesn't close the result after being run
#     r = response_process(r) if r.rowcount else [{ c:None for c in colnames }]
#     return  jsonify(r)
#
#
#
#
#
# # *************
# # DUMMY ROUTE *
# # *************
# @app.route("/i")
# def __():
#     # run the query
#     l = [ random.choice([ _ for _ in range(5, 100) ]) for i in range(20) ]
#     x = db.session.execute(R_IconographyActor.query
#                                              .filter(R_IconographyActor.id.in_(l)))
#
#     # create an html list
#     ul = "<ul>"               # html unordered list
#     for _ in x.all():         # access each row
#         print(_)              # `_` is a tuple, `_[0]` is row itself
#         print(_[0].__dict__)  # print the dict rpr of row
#         ul += f"""<li><dl>
#             <dt>{ _[0].actor.entry_name.upper() }</dt>
#             <dd><i>{ _[0].iconography.title[0].entry_name }</i></dd>
#         </dl></li>"""
#     ul += "</ul>"
#
#     return f"""
#         <html>
#             <head><title>RICH.DATA</title></head>
#             <body><h1>RICH.DATA</h1>{ ul }</body>
#         </html>
#     """
