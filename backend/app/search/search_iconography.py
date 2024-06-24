from sqlalchemy import select
import typing as t


from ..orm import ( Iconography, Title, Actor, Theme, NamedEntity
                  , Institution, R_Institution, R_IconographyActor
                  , R_IconographyNamedEntity, R_IconographyTheme)
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
    return { "title"      : args.get("title", None),
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
    # `date` must be a list of integers; if `date_filter` is `dateRange`,
    # `date` must be of length 0 or 2. else, it must be of length 0 or 1.
    params["date"] = [ int(d) for d in params["date"] ]
    valid_date = True

    if (params["date_filter"] == "dateRange"
        and len(params["date"]) not in [0,2] ):
        valid_date = False
    elif (params["date_filter"] != "dateRange"
         and len(params["date"]) not in [0,1] ):
        valid_date = False

    # a flag. our query will only be run if `True`
    valid = all([valid_date])
    return params, valid


def make_query(params:t.Dict):
    """
    build and run an SQL query based on the validated, user inputted
    parameters `params`.

    see: https://docs.sqlalchemy.org/en/20/orm/queryguide/select.html#chaining-multiple-joins
    :param params: the query parameters
    """
    # test query:
    # SELECT count (*) FROM iconography JOIN title ON title.id_iconography = iconography.id AND title.entry_name ILIKE '%le moniteur de la mode%' JOIN r_iconography_actor ON r_iconography_actor.id_iconography = iconography.id AND r_iconography_actor.role = 'author' JOIN actor ON r_iconography_actor.id_actor = actor.id AND actor.entry_name ILIKE '%jules david%'

    print(params)

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

    r = db.session.execute(iq.distinct())
    print(f">>>>>>>> {len(r.all())} rows were found")
    print(f">>>>>>>> for query: {iq}")
    return

