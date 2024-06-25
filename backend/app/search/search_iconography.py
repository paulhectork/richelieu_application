from sqlalchemy.engine.result import ChunkedIteratorResult
from psycopg2.extras import NumericRange
import sqlalchemy.dialects.postgresql as psql
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy import select, func
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


def make_params(args: t.List[t.Tuple[str]]) -> t.Dict:
    """
    build a dict of query params from the `ImmutableMultiDict`
    created by `flask.request.args`
    """
    return { "title"        : args.get("title", None),
             "author"       : args.get("author", None),
             "publisher"    : args.get("publisher", None),
             "theme"        : args.get("theme", None),
             "named_entity" : args.get("namedEntity", None),
             "institution"  : args.get("institution", None),
             "date_filter"  : args.get("dateFilter", None),
             "date"         : args.getlist("date[]")
    }



def sanitize_params(params:t.Dict) -> t.Tuple[t.Dict, bool]:
    """
    sanitize/validate the user-inputted query parameters
    :param params: the query parameters, as created by `make_params`
    :returns     : first, the cleaned parameters. then, a flag that
                   is `True` if all fields are valid
    """
    # if `date_filter` is `dateRange`, `date` must be of length 0 or 2
    # and be converted to int4range. else, `date` must be of length 0 or 1
    # and be a list of integers
    valid_date = True

    # assert that the date is valid
    params["date"] = [ int(d) for d in params["date"] ]
    if ( params["date_filter"] == "dateRange" and len(params["date"]) not in [0,2] ):
        valid_date = False
    elif ( params["date_filter"] != "dateRange" and len(params["date"]) not in [0,1] ):
        valid_date = False
    # convert to NumericRange when necessary.
    # a NumericRange will never be empty. if there is no data, then `params["date"] = []`
    if valid_date:
        if params["date_filter"] == "dateRange":
            params["date"] = list2int4range(params["date"])
        elif params["date_filter"] == "dateExact" and len(params["date"]) == 1:
            params["date"] = list2int4range([ params["date"][0], params["date"][0] ])

    # a flag. our query will only be run if `True`
    valid = all([valid_date])
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

    :param params: the query parameters
    """
    # test query:
    # SELECT count (*) FROM iconography JOIN title ON title.id_iconography = iconography.id AND title.entry_name ILIKE '%le moniteur de la mode%' JOIN r_iconography_actor ON r_iconography_actor.id_iconography = iconography.id AND r_iconography_actor.role = 'author' JOIN actor ON r_iconography_actor.id_actor = actor.id AND actor.entry_name ILIKE '%jules david%'

    iq = select(Iconography)

    # at each `if`, `iq` is updated
    if params["title"]:
        iq = iq.join(Iconography
                     .title
                     .and_( Title.entry_name.ilike(f"%{ params['title'] }%") ) )
    if params["author"]:
        iq = (iq.join(Iconography
                      .r_iconography_actor
                      .and_( R_IconographyActor.role == "author" ))
                .join(R_IconographyActor
                      .actor
                      .and_( Actor.entry_name.ilike(f"%{ params['author'] }%") ) ))
    if params["publisher"]:
        iq = (iq.join(Iconography
                      .r_iconography_actor
                      .and_( R_IconographyActor.role == "publisher" ))
                .join(R_IconographyActor
                      .actor
                      .and_( Actor.entry_name.ilike(f"%{ params['publisher'] }%") ) ))
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
    # print(f">>>>>>>> {len(r.all())} rows were found")
    # print(f">>>>>>>> for query: {iq}")
    return r

