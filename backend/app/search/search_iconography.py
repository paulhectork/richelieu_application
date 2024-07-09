from sqlalchemy.engine.result import ChunkedIteratorResult
from sqlalchemy.sql.expression import and_, any_, or_
from psycopg2.extras import NumericRange
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


def sanitize_date(date: t.List[t.Dict]) -> t.Tuple[ t.List[t.Dict], bool ]:
    """
    helper function to assert that the date is valid and pre-process it
    so that it can be usable by `make_query`

    :example input:
    >>> [ {'filter': 'dateRange', 'data': [1850, 1860]}
        , {'filter': 'dateExact', 'data': [1871]}
        , {'filter': 'dateBefore', 'data': [1800]}
        , {'filter': 'dateAfter', 'data': [1900]} ]

    :example output:
    >>> [ {'filter': 'dateRange', 'data': NumericRange(1850, 1861, '[)')}
        , {'filter': 'dateExact', 'data': NumericRange(1871, 1872, '[)')}
        , {'filter': 'dateBefore', 'data': [1800]}
        , {'filter': 'dateAfter', 'data': [1900]} ]

    :param date: the "date" field in the parameters dictionnary
    :returns: 2 values:
        1) the processed and cleaned date
        2) a boolean that is True if the date is valid, False if there was an error
    """
    # 1) validate the structure of each date object: { "filter": <...>, "data": [...] }
    # print(">>> input  :\n", date)
    valid_date_structure = lambda x: ( len(x.keys()) == 2
                                       and "filter" in x.keys()
                                       and "data" in x.keys()
                                       and type(x["data"]) == list )
    if not all([ valid_date_structure(d) for d in date ]):
        return date, False
    # 2) retype all dates to int. if there's an error, then date
    #    contains stuff that can't be retyped to date, and is invalid
    try:
        for d in date:
            d["data"] = sorted([ int(d) for d in d["data"] ])
    except ValueError:
        return date, False
    # 3) invalid number of dates, depending on each `date_filter` value
    valid_date_numbers = lambda x: ( len(x["data"]) in [0,2]
                                     if x["filter"]=="dateRange"
                                     else len(x["data"]) in [0,1] )
    if not all([ valid_date_numbers(d) for d in date ]):
        print("oh, no")
        return date, False
    # 4) convert to NumericRange when necessary. a NumericRange will never be empty.
    #    if there is no data in an item of our date array, then that item is removed,
    #    which will greatly simplify things down the road.
    date2int4range = lambda x: ( list2int4range(x["data"])
                                 if x["filter"] == "dateRange"
                                 else list2int4range([ x["data"][0], x["data"][0] ]) if x["filter"] == "dateExact"
                                 else x["data"] )
    date = [ { "filter": d["filter"], "data": date2int4range(d) }
               for d in date if len(d["data"]) ]
    # print(">>> output :\n", date)
    return date, True

def sanitize_array(params: t.Dict) -> t.Tuple[ t.Dict, bool ]:
    """
    all of our fields (except boolean ops) are expected to be arrays
    :returns: 2 values:
        1) the params
        2) a boolean that is True if the expected array fields are arrays, False otherwise
    """
    return params, all( isinstance(v, list) for k,v in params.items() if "boolean_op" not in k )


def sanitize_op(params: t.Dict) -> t.Tuple[ t.Dict , bool ]:
    """
    helper function to make sure that all our boolean operators
    are valid (one of 'and', 'or', 'not')
    :returns: 2 values:
        1) the params
        2) a boolean that is True if boolean operators are valid, False otherwise
    """
    return params, all( v in ["and", "or", "not"] for k,v in params.items() if "boolean_op" in k )  # True if the data is valid, false otherwise


def sanitize_ilike(params: t.Dict) -> t.Tuple[ t.Dict, bool ]:
    """
    add wildcards to fields that will be filtered with postgreSQL ILIKE
    """
    #TODO ADD TRY...EXCEPT HERE?
    ilike = [ "title", "author", "publisher" ]  # the fields to process
    add_wildcard = lambda x: [ rf"%{el}%" for el in x if isinstance(el, str) ]
    params = { k:add_wildcard(v) if k in ilike else v for k,v in params.items() }
    return params, True


def make_params(args: t.Dict) -> t.Tuple[t.Dict, bool]:
    """
    build a dict of query params from the `flask.request.args` object.
    this function also ensures that `args` contains only valid fields
    see `allowed_params`. validation is done in `sanitize_params`.

    :param args     : the dict sent from the frontend.
    :returns params : a t.Dict of query parameters
    :reutrns valid  : a bool that is False if unallowed params were passed
    """
    valid = True
    params = {}  # the output parameters
    allowed_params = [ "title", "author", "publisher", "theme"
                     , "namedEntity", "institution", "date"
                     , "titleBooleanOp", "authorBooleanOp"
                     , "publisherBooleanOp", "themeBooleanOp"
                     , "namedEntityBooleanOp", "institutionBooleanOp"
                     , "dateBooleanOp" ]

    # helper functions
    # extract an array field to add it to `params`, defaulting to `[]`
    # :param _args: the user submitted arguments
    # :param x    : the key of _args we're extracting
    extract_array = lambda _args, x: _args[x] if x in args.keys() else []
    # extract a boolean operator field to add it to `params`, defaulting to `[]`
    # :param _args: the user submitted arguments
    # :param x    : the key of _args we're extracting
    extract_op = lambda _args, x: _args[x] if x in args.keys() and len(_args[x]) else "and"

    # check that only allowed params were passed
    if any( k not in allowed_params for k in args.keys() ):
        valid = False
    else:
        params = { "title"        : extract_array(args, "title"),
                   "author"       : extract_array(args, "author"),
                   "publisher"    : extract_array(args, "publisher"),
                   "theme"        : extract_array(args, "theme"),
                   "named_entity" : extract_array(args, "namedEntity"),
                   "institution"  : extract_array(args, "institution"),
                   "date"         : extract_array(args, "date"),

                   "title_boolean_op"        : extract_op(args, "titleBooleanOp"),
                   "author_boolean_op"       : extract_op(args, "authorBooleanOp"),
                   "publisher_boolean_op"    : extract_op(args, "publisherBooleanOp"),
                   "theme_boolean_op"        : extract_op(args, "themeBooleanOp"),
                   "named_entity_boolean_op" : extract_op(args, "namedEntityBooleanOp"),
                   "institution_boolean_op"  : extract_op(args, "institutionBooleanOp"),
                   "date_boolean_op"         : extract_op(args, "dateBooleanOp")
        }

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
    #TODO add a try...except to catch problems here

    valid = True

    # make sure that all of our fields are arrays, which is what's expected

    # clean the date
    params["date"], valid = sanitize_date(params["date"])
    if not valid:
        return params, False

    # validate the array (repeatable) fields
    params, valid = sanitize_array(params)

    # validate the boolean operators
    params, valid = sanitize_op(params)
    if not valid:
        return params, False

    # add wildcards to ilike fields
    params, valid = sanitize_ilike(params)
    if not valid:
        return params, False

    return params, valid


def make_query(params:t.Dict) -> ChunkedIteratorResult:
    """
    build and run an SQL query based on the validated, user inputted
    parameters `params`. at each `if`, `iq` (our query) is updated.
    date filtering is inclusive by default.

    the date queries as raw sql:
        https://gitlab.inha.fr/snr/rich.data/documentation/-/blob/main/technologies/postgresql/queries/date_range_operations.sql?ref_type=heads
    sqlalchemy query structure:
        https://docs.sqlalchemy.org/en/20/orm/queryguide/select.html#chaining-multiple-joins
    postgreSQL int4range operators:
        https://www.postgresql.org/docs/current/functions-range.html#RANGE-OPERATORS-TABLE
    postgreSQL int4range functions:
        https://www.postgresql.org/docs/current/functions-range.html#RANGE-FUNCTIONS-TABLE
    like on an array of values in postgresql:
        https://stackoverflow.com/a/78705653/17915803
    like on an array of values in sqlalchemy:
        https://stackoverflow.com/a/78705653/17915803
    postgresql unaccent:
        https://www.postgresql.org/docs/current/unaccent.html

    :param params: the sanitized query parameters
    """
    # test query:
    # SELECT count (*) FROM iconography JOIN title ON title.id_iconography = iconography.id AND title.entry_name ILIKE '%le moniteur de la mode%' JOIN r_iconography_actor ON r_iconography_actor.id_iconography = iconography.id AND r_iconography_actor.role = 'author' JOIN actor ON r_iconography_actor.id_actor = actor.id AND actor.entry_name ILIKE '%jules david%'

    iq = select(Iconography)

    # at each `if`, `iq` is updated
    if len(params["title"]):
        # WARNING *****************************************
        # we can get different results in sqlalchemy and
        # pure sql because sqlalchemy returns the number
        # of iconography objects, while pure sql duplicates
        # rows when there are several titles.
        iq = iq.join(Iconography
                     .title
                     .and_( Title.entry_name.ilike(any_(params['title']))))
    if len(params["author"]):
        iq = (iq.join(Iconography
                      .r_iconography_actor
                      .and_( R_IconographyActor.role == "author" ))
                .join(R_IconographyActor
                      .actor
                      .and_( Actor.entry_name.ilike(any_(params['author'])))))
    if len(params["publisher"]):
        iq = (iq.join(Iconography
                      .r_iconography_actor
                      .and_( R_IconographyActor.role == "publisher" ))
                .join(R_IconographyActor
                      .actor
                      .and_( Actor.entry_name.ilike(any_(params['publisher'])))))
    if len(params["named_entity"]):
        iq = (iq.join(Iconography
                      .r_iconography_named_entity)
                .join(R_IconographyNamedEntity
                      .named_entity
                      .and_( NamedEntity.entry_name.in_(params["named_entity"]))))
    if len(params["theme"]):
        iq = (iq.join(Iconography
                      .r_iconography_theme)
                .join(R_IconographyTheme
                      .theme
                      .and_( Theme.entry_name.in_(params["theme"]))))
    if len(params["institution"]):
        iq = (iq.join(Iconography
                      .r_institution )
                .join(R_Institution
                      .institution
                      .and_( Institution.entry_name.in_(params["institution"]))))

    # date filter expression builder. in all `*_expr`
    # functions below, x is the date array or numeric range
    date_range_expr  = lambda x: ~func.isempty(Iconography  # ~ works the same as SQL NOT or SQLAlchemy `func.not_()`
                                               .date
                                               .intersection(x))
    date_exact_expr  = lambda x: Iconography.date == x
    date_before_expr = lambda x: and_( ~func.isempty(Iconography.date)
                                     , func.lower(Iconography.date) <= x[0] )
    date_after_expr  = lambda x: and_( ~func.isempty(Iconography.date)
                                     , func.upper(Iconography.date) >= x[0] )

    # depending on the `filter` type used, decide which function above to use
    # dateobj is an item in our `params['date']` array.
    date_expr_builder = lambda dateobj: (date_range_expr(dateobj["data"])
                                         if dateobj["filter"]=="dateRange"
                                         else date_exact_expr(dateobj["data"]) if dateobj["filter"]=="dateExact"
                                         else date_before_expr(dateobj["data"]) if dateobj["filter"]=="dateBefore"
                                         else date_after_expr(dateobj["data"]) if dateobj["filter"]=="dateAfter"
                                         else None)  # a final else is necessary, None will be removed below

    if len(params["date"]):
        # print(params["date"])
        date_filters = [ date_expr_builder(date) for date in params["date"] ]
        date_filters = [ f for f in date_filters if f is not None ]
        # for d in date_filters:
        #     print(">", d)
        # assert len(params["date"]) == len(date_filters)
        iq = iq.filter(or_(*date_filters))

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

