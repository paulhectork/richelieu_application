from sqlalchemy.engine.result import ChunkedIteratorResult
from psycopg2.extras import NumericRange
from sqlalchemy.sql.expression import and_
from sqlalchemy import select, func
from flask import current_app
import typing as t

import sqlparse


from ..orm import ( Iconography, Title, Actor, Theme, NamedEntity
                  , Institution, R_Institution, R_IconographyActor
                  , R_IconographyNamedEntity, R_IconographyTheme)
from ..utils.converters import list2int4range
from ..app import db

# *******************************************************
# advanced search engine for the iconography
# data.
# see: `frontend/src/modules/iconographyQueryParams.js`
# for what is sent from the frontend
# *******************************************************


def make_params(args: t.List[t.Tuple]) -> t.Tuple[t.Dict, bool]:
    """
    build a dict of query params from the `flask.request.args` object.
    this function also ensures that we only entered valid params
    (keys of `args`).

    :param args     : the ImmutableDict sent by Flask.
    :returns params : a t.Dict of query parameters
    :reutrns valid  : a bool that is False if unallowed params were passed
    """
    valid = True
    params = {}
    allowed_params = [ "title", "author", "publisher", "theme"
                     , "namedEntity", "institution", "dateFilter", "date[]" ]

    # check that only allowed params were passed
    if any( a not in allowed_params for a in args ):
        valid = False
    else:
         params = { "title"        : args.get("title", None),
                    "author"       : args.get("author", None),
                    "publisher"    : args.get("publisher", None),
                    "theme"        : args.get("theme", None),
                    "named_entity" : args.get("namedEntity", None),
                    "institution"  : args.get("institution", None),
                    "date_filter"  : args.get("dateFilter", None),
                    "date"         : args.getlist("date[]") }
    return params, valid



def sanitize_params(params:t.Dict) -> t.Tuple[t.Dict, bool]:
    """
    sanitize/validate the user-inputted query parameters.
    at each validation step, if there is an error of any kind,
    `params, valid` is returned. `valid` wll be False, and the
    caller function will know that the request parameters are
    invalid and that no query can be run.

    :param params   : the query parameters, as created by `make_params`
    :returns params : a t.Dict of sanitized query parameters
    :reutrns valid  : a bool that is False if there are errors in the `params` values.
    """
    #TODO type-check all values?

    valid = True

    # assert that the date is valid.

    # retype to int. if there's an error, then params["date"] contains
    # stuff that can't be retyped to date.
    try:
        params["date"] = [ int(d) for d in params["date"] ]
    except ValueError:
        return params, False
    # there is a "date", but no "date_filter" => don't know how to filter it
    if len(params["date"]) and "date_filter" not in params.keys():
        return params, False
    # invalid number of dates, depending on each `date_filter` value
    elif params["date_filter"] == "dateRange" and len(params["date"]) not in [0,2]:
        return params, False
    elif params["date_filter"] != "dateRange" and len(params["date"]) not in [0,1]:
        return params, False
    # convert to NumericRange when necessary.
    # a NumericRange will never be empty. if there is no data, then `params["date"] = []`
    if params["date_filter"] == "dateRange":
        params["date"] = list2int4range(params["date"])
    elif params["date_filter"] == "dateExact" and len(params["date"]) == 1:
        params["date"] = list2int4range([ params["date"][0], params["date"][0] ])

    #TODO add a try...except to catch problems here

    # add wildcards (%) to values that will be researched with
    # `ILIKE` or `LIKE`. '%' is a special char in python strings,
    # so we need the strings to be raw, with `r""`
    ilike = [ "title", "author", "publisher" ]
    params = { k:rf"%{v}%" if isinstance(v, str) and k in ilike else v
               for k,v in params.items() }

    return params, valid


def make_query(params:t.Dict) -> ChunkedIteratorResult:
    """
    build and run an SQL query based on the validated, user inputted
    parameters `params`.

    the date queries as raw sql:
        https://gitlab.inha.fr/snr/rich.data/documentation/-/blob/main/technologies/postgresql/queries/date_range_operations.sql?ref_type=heads
    sqlalchemy query structure:
        https://docs.sqlalchemy.org/en/20/orm/queryguide/select.html#chaining-multiple-joins
    postgreSQL int4range operators:
        https://www.postgresql.org/docs/current/functions-range.html#RANGE-OPERATORS-TABLE
    postgreSQL int4range functions:
        https://www.postgresql.org/docs/current/functions-range.html#RANGE-FUNCTIONS-TABLE

    :param params: the sanitized query parameters
    """
    # test query:
    # SELECT count (*) FROM iconography JOIN title ON title.id_iconography = iconography.id AND title.entry_name ILIKE '%le moniteur de la mode%' JOIN r_iconography_actor ON r_iconography_actor.id_iconography = iconography.id AND r_iconography_actor.role = 'author' JOIN actor ON r_iconography_actor.id_actor = actor.id AND actor.entry_name ILIKE '%jules david%'

    iq = select(Iconography)

    # at each `if`, `iq` is updated
    if params["title"]:
        iq = iq.join(Iconography
                     .title
                     .and_( Title.entry_name.ilike(params['title']) ) )
    if params["author"]:
        iq = (iq.join(Iconography
                      .r_iconography_actor
                      .and_( R_IconographyActor.role == "author" ))
                .join(R_IconographyActor
                      .actor
                      .and_( Actor.entry_name.ilike(params['author']) ) ))
    if params["publisher"]:
        iq = (iq.join(Iconography
                      .r_iconography_actor
                      .and_( R_IconographyActor.role == "publisher" ))
                .join(R_IconographyActor
                      .actor
                      .and_( Actor.entry_name.ilike(params['publisher']) ) ))
    if params["named_entity"]:
        iq = (iq.join(Iconography
                      .r_iconography_named_entity)
                .join(R_IconographyNamedEntity
                      .named_entity
                      .and_( NamedEntity.entry_name == params["named_entity"] ))  )
    if params["theme"]:
        iq = (iq.join(Iconography
                      .r_iconography_theme)
                .join(R_IconographyTheme
                      .theme
                      .and_( Theme.entry_name == params["theme"] ))  )
    if params["institution"]:
        iq = (iq.join(Iconography
                      .r_institution )
                .join(R_Institution
                      .institution
                      .and_( Institution.entry_name == params["institution"] ))  )
    # we do inclusive date filtering by default
    # based on what is defined in `sanitize_params`,
    # a `NumericRange` is never empty
    if ( params["date_filter"] == "dateRange"
         and isinstance(params["date"], NumericRange) ):
        iq = iq.filter(~func.isempty(Iconography  # ~ works the same as SQL NOT or SQLAlchemy `func.not_()`
                                     .date
                                     .intersection(params["date"]) ))
    elif ( params["date_filter"] == "dateExact"
           and isinstance(params["date"], NumericRange) ):
        iq = iq.filter(Iconography.date == params["date"])
    elif params["date_filter"] == "dateBefore" and len(params["date"]):
        iq = iq.filter(and_( ~func.isempty(Iconography.date)
                           , func.lower(Iconography.date) <= params["date"][0] ))
    elif params["date_filter"] == "dateAfter" and len(params["date"]):
        iq = iq.filter(and_( ~func.isempty(Iconography.date)
                           , func.upper(Iconography.date) >= params["date"][0] ))

    r = db.session.execute(iq.distinct())
    if current_app.config["TESTING"]:
        # `.all()` closes the transaction, which means that we won't be able
        # to access the query results down the road, which will raise unecessary
        # testing errors => we run a second query count the results.
        params_filtered = { k:v for k,v in params.items()
                            if isinstance(v, NumericRange)
                            or (v is not None and len(v)) }
        r_count = len( db.session.execute(iq.distinct()).all() )
        print(f">>>>>>>> {r_count} rows were found")
        print(f">>>>>>>> for params (empty params removed):\n{params_filtered}")
        print(f">>>>>>>> for query: \n{sqlparse.format(str(iq), reindent=True, keyword_case='upper')}")
    return r

