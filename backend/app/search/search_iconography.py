from sqlalchemy.engine.result import ChunkedIteratorResult
from sqlalchemy.sql.expression import and_, any_, or_
from psycopg2.extras import NumericRange
from sqlalchemy import select, func, union
from flask import current_app
import typing as t

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


def sanitize_date(date: t.List[t.Dict] | t.Any) -> t.Tuple[ t.List[t.Dict], bool ]:
    """
    helper function to assert that the date is valid and pre-process it
    so that it can be usable by `make_query`.
    if unclean input (see example below) is given, the date is invalid,
    which will stop running the query.

    :example clean input:
    >>> [ {'filter': 'dateRange', 'data': [1850, 1860]}
    ... , {'filter': 'dateExact', 'data': [1871]}
    ... , {'filter': 'dateBefore', 'data': [1800]}
    ... , {'filter': 'dateAfter', 'data': [1900]} ]

    :example output:
    >>> [ {'filter': 'dateRange', 'data': NumericRange(1850, 1861, '[)')}
    ... , {'filter': 'dateExact', 'data': NumericRange(1871, 1872, '[)')}
    ... , {'filter': 'dateBefore', 'data': [1800]}
    ... , {'filter': 'dateAfter', 'data': [1900]} ]

    :param date: the "date" field in the parameters dictionnary.
        it is expected to be an array: [{"data": [int], "filter": str}],
        but it can be something else if the user passes invalid data.

    :returns:
        1) the processed and cleaned date
        2) a boolean that is True if the date is valid, False if there was an error
    """
    # check that the basic types are valid: we have an array of dicts.
    if not (isinstance(date, list) and all(isinstance(d, dict) for d in date)):
        return date, False

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
    :returns:
        1) the params
        2) a boolean that is True if the expected array fields are arrays, False otherwise
    """
    return params, all( isinstance(v, list) for k,v in params.items() if "boolean_op" not in k )


def sanitize_op(params: t.Dict) -> t.Tuple[ t.Dict , bool ]:
    """
    helper function to make sure that all our boolean operators
    are valid (one of 'and', 'or', 'not') and that at least one
    of the boolean operators is 'and'.

    in `params`, we have couples of [<filter_value>, <boolean_op>]
    (ex: "date" and "date_boolean_op", "theme" and "theme_boolean_op").
    if all params that are not empty also have the boolean op `or`,
    the first of those boolean op is replaced by `and`.

    this is because, by default, our query begins with
    >>> SELECT * FROM iconography;
    before adding filters. if we only have `or` parameters, there are
    no filters, so our final query will be :
    >>> SELECT * FROM iconography
    ... UNION (<subquery on iconography>);
    not only this is useless, it will return meaningless results
    (we will be doing a union between a full table and a subset
    of this full table).

    transforming the first `or` by an `and` will change the query to:
    >>> SELECT * FROM iconography
    ... WHERE <first parameter>
    ... UNION (<other OR filters on iconography>);
    in logical terms, it will mean we will be doing:
    `<subset of iconography 1> UNION <subset of iconography 2>`

    :returns:
        1) the params
        2) a boolean that is True if boolean operators are valid, False otherwise
    """
    # True if all the boolean ops are valid, false otherwise
    valid = all( v in ["and", "or", "not"] for k,v in params.items() if "boolean_op" in k )

    # if necessary, replace the first "or" by an "and".
    # 1) create a list of boolean operators, where the
    #    associated parameter is not empty.
    nonempty = [ f"{k}_boolean_op" for k,v in params.items()
                 if "_boolean_op" not in k
                 and len(v) ]
    # 2) if all non-empty parameters have the boolean op "or",
    #    replace the 1st "or" by an "and"
    if all( params[n] == "or" for n in nonempty ):
        for op in nonempty:
            if params[op] == "or":
                params[op] = "and"
                break
    return params, valid


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
    if not valid:
        return params, False

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
    parameters `params`. at each `if`, new parameters are added, either
    to our main query object (`base_query`), or to a dict of sub-queries
    (`subqueries`).
    date filtering is inclusive by default.

    the way the different parameters are processed varies depending on
    the value of the booleanOp related to that parameter ("title" and
    "title_boolean_op", for ex).
    - if the boolean op is "and", we just need to update our main sql query
    - else (boolean op is "or" or "not"), we add it to the dict of subqueries.
      this is because the boolean op defines the relationship between filters
      and within a filter (like doing OR/NOT on a JOIN) (see examples below).
    at the end, we will build the full query.

    process:
    - the aim is to get a list of all of the Iconography.id that
      match `params`. from this list, we'll query `Iconography` to
      get all the related objects.
    - we populate two objects and then combine them
      to build the final query:
      - `base_query` is an sqlalchemy.Select. we add to base_query
        all fields with an `and` booleanOp: those don't need subqueries
      - `subqueries` is a dict of: { <field_name>: [ <sql_query>, <boolean_op> ] }.
        basically, it's a dict of subqueries when booleanOps are `or` or `not`.
    - then, we build the final query.
      - all `and` parameters jave been added to `base_query`:
        >>> SELECT iconography.id FROM iconography WHERE ...
      - `not` parameters are added by using an SQL WHERE on a
        subquery of ids to reject:
        >>> SELECT base_query UNION other_query
      - `or` parameters are added by using an SQL UNION:
        >>> SELECT * FROM base_query AS icn WHERE icn.id NOT IN ( other_query ).

    in SQL terms, the constructed SQL request is:
    >>> SELECT *
    ... FROM iconography
    ... WHERE   <"and" filters>
    ... AND NOT <"not" filters>
    ... UNION   <"or" filters>

    example of raw sql not on a join:
    >>> SELECT q1.id
    ... FROM
    ...   ( SELECT iconography.id FROM iconography
    ...     WHERE iconography.id IN (1,2,3) ) AS q1
    ... WHERE q1.id NOT IN
    ...   ( SELECT iconography.id FROM iconography
    ...     WHERE iconography.id IN (2,5,6) );

    example of raw sql or on a join:
    >>> SELECT *
    ... FROM
    ...   ( SELECT iconography.id FROM iconography
    ...     WHERE iconography.id IN (1,2,3) ) AS q1
    ... UNION
    ...   ( SELECT iconography.id FROM iconography
    ...     WHERE iconography.id IN (2,5,6) )
    ... ORDER BY "id" ASC;

    help:
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

    # the base query object. for now, we only query the `id`,
    # which will make unions and whatnot easier.
    base_query = select(func.distinct(Iconography.id))
    # dict of subqueries o complete `base_query` with. structure:
    #  { <filter name>: [ <sql filter>, <boolean op> ] }.
    subqueries = {}

    # 1) build the different query parameters.
    if len(params["title"]):
        # `sqlbuilder` builds an sql expression and applies it to `ctx`.
        # the expression is always the same, only the `ctx` to which it is
        # applied changes: if booleanOp is `and`, then it is added to `base_qusery`.
        # else, it is added to a subquery.
        sqlbuilder = lambda ctx: (
            ctx.join(Iconography
                     .title
                     .and_( Title.entry_name.ilike(any_(params['title'])) )))
        if params["title_boolean_op"] == "and":
            base_query = sqlbuilder(base_query)
        else:
            subqueries["title"] = [ sqlbuilder(select(Iconography.id))
                                  , params["title_boolean_op"] ]

    if len(params["author"]):
        sqlbuilder = lambda ctx: (
            ctx.join(Iconography
                    .r_iconography_actor
                    .and_( R_IconographyActor.role == "author" ))
               .join(R_IconographyActor
                    .actor
                    .and_( Actor.entry_name.ilike(any_(params['author'])))))
        if params["author_boolean_op"] == "and":
            base_query = sqlbuilder(base_query)
        else:
            subqueries["author"] = [ sqlbuilder(select(Iconography.id))
                                   , params["author_boolean_op"] ]

    if len(params["publisher"]):
        sqlbuilder = lambda ctx: (
            ctx.join(Iconography
                    .r_iconography_actor
                    .and_( R_IconographyActor.role == "publisher" ))
               .join(R_IconographyActor
                    .actor
                    .and_( Actor.entry_name.ilike(any_(params['publisher'])))))

        if params["publisher_boolean_op"] == "and":
            base_query = sqlbuilder(base_query)
            subqueries["publisher"] = [ sqlbuilder(select(Iconography.id))
                                      , params["publisher_boolean_op"] ]

    if len(params["named_entity"]):
        sqlbuilder = lambda ctx: (
            ctx.join( Iconography.r_iconography_named_entity )
               .join( R_IconographyNamedEntity
                      .named_entity
                      .and_( NamedEntity.entry_name.in_(params["named_entity"])) ))
        if params["named_entity_boolean_op"] == "and":
            base_query = sqlbuilder(base_query)
        else:
            sqlbuilder(select(Iconography))
        subqueries["named_entity"] = [ sqlbuilder(select(Iconography.id)), params["named_entity_boolean_op"]  ]

    if len(params["theme"]):
        sqlbuilder = lambda ctx: (
            ctx.join( Iconography.r_iconography_theme )
               .join( R_IconographyTheme
                      .theme
                      .and_( Theme.entry_name.in_(params["theme"])) ))
        if params["theme_boolean_op"] == "and":
            base_query = sqlbuilder(base_query)
        else:
            subqueries["theme"] = [ sqlbuilder(select(Iconography.id))
                                  , params["theme_boolean_op"] ]

    if len(params["institution"]):
        sqlbuilder = lambda ctx: (
            ctx.join( Iconography.r_institution )
               .join( R_Institution
                      .institution
                      .and_( Institution.entry_name.in_(params["institution"]))) )
        if params["institution_boolean_op"] == "and":
            base_query = sqlbuilder(base_query)
        else:
            subqueries["institution"] = [ sqlbuilder(select(Iconography.id))
                                        , params["institution_boolean_op"] ]

    # date filter expression builder. in all `*_expr`
    # functions below, x is the date array or numeric range
    # ~ works the same as SQL NOT or SQLAlchemy `func.not_()`
    date_range_expr  = lambda x: ~func.isempty( Iconography.date.intersection(x) )
    date_exact_expr  = lambda x: Iconography.date == x
    date_before_expr = lambda x: and_( ~func.isempty(Iconography.date)
                                     , func.lower(Iconography.date) <= x[0] )
    date_after_expr  = lambda x: and_( ~func.isempty(Iconography.date)
                                     , func.upper(Iconography.date) >= x[0] )

    # depending on the `filter` type used, decide which function above to use
    # dateobj is an item in our `params['date']` array.
    date_expr_builder = lambda dateobj: (date_range_expr(dateobj["data"]) if dateobj["filter"]=="dateRange"
                                         else date_exact_expr(dateobj["data"]) if dateobj["filter"]=="dateExact"
                                         else date_before_expr(dateobj["data"]) if dateobj["filter"]=="dateBefore"
                                         else date_after_expr(dateobj["data"]) if dateobj["filter"]=="dateAfter"
                                         else None)  # a final else is necessary, None will be removed below

    if len(params["date"]):
        date_filters = [ date_expr_builder(date) for date in params["date"] ]
        date_filters = [ f for f in date_filters if f is not None ]
        if params["date_boolean_op"] == "and":
            base_query = base_query.filter(or_(*date_filters))
        else:
            subqueries["date"] = [ select(Iconography.id).filter(or_(*date_filters))
                                 , params["date_boolean_op"] ]

    # 2) build the complete sql queries by combining all parameters
    #
    # all of the `and` fields constitute the base `base_query`.
    # here, `base_query` is completed by the `or` and `not` fields
    full_query = base_query
    if len(subqueries.keys()):
        # do the NOT statements
        stmt_not = [ v[0] for v in subqueries.values() if v[1] == "not" ]
        for s in stmt_not:
            # for some obscure reason, using `s.subquery()` throws a warning:
            # there's no need to transform `s` into a subquery.
            full_query = full_query.filter(~Iconography.id.in_( s ))
        # do the OR statements
        stmt_or  = [ v[0] for v in subqueries.values() if v[1] == "or" ]
        full_query = union(full_query, *[ s for s in stmt_or ])

    r = db.session.execute(select( Iconography ).filter( Iconography.id.in_(full_query) ))

    if current_app.config["TESTING"]:
        import sqlparse
        # `.all()` closes the transaction, which means that we won't be able
        # to access the query results down the road, which will raise unecessary
        # testing errors => we run a second query count the results.
        params_filtered = { k:v for k,v in params.items()
                            if isinstance(v, NumericRange)
                            or (v is not None and len(v)) }
        r_count = len( db.session.execute(full_query).all() )
        print(f">>>>>>>> {r_count} rows were found")
        print(f">>>>>>>> for params (empty params removed):\n{params_filtered}")
        print(f">>>>>>>> for query: \n{sqlparse.format( str(full_query), reindent=True, keyword_case='upper')}")
    return r

