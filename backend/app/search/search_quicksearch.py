"""
quick search module.

the frontend inputs a query string, we match this query string against the attributes:
- title.entry_name (to match iconography resources)
- actor.entry_name (to match iconography resources)
- named_entity.entry_name
- theme.entry_name
- address.address
- institution.entry_name

and return the objects:
- iconography
- named_entity
- theme
- institution
- place
"""
import typing as t
from uuid import uuid4
import re

from sqlalchemy import select, or_, bindparam

from ..app import db
from ..orm import ( Institution
                  , NamedEntity
                  , Theme
                  , Iconography
                  , Title
                  , Place
                  , Address
                  , Actor
                  , R_AddressPlace
                  , R_IconographyActor)


# *********************************************
# helpers

"""
prepare the string `s` to be inserted in an ILIKE filter
"""
to_ilike = lambda s: f"%{s.strip().lower()}%"

"""
sql queries return t.List[t.Tuple]. transform each tuple into a dict.
"""
restructure_row = lambda row: { "table_name" : row[0]
                              , "id_uuid"    : row[1]
                              , "entry_name" : row[2] }

# *********************************************
# sql query builders. all functions return
# the following columns: ( <table name:str>, <id_uuid:str>, <entry_name:str> )

"""
several tables are filtered using `table.entry_name ILIKE "..."`
=> this function does it all. it's curried for extra fanciness :)
:param orm_table: our orm class for a table
:param qstr: the query string
"""
query_basic = lambda orm_table: (
    lambda qstr : select( bindparam( f"table_{uuid4()}", orm_table.__tablename__)
                        , orm_table.id_uuid
                        , orm_table.entry_name
                        ).filter( orm_table.entry_name.ilike(qstr) ) )

"""
applications of query_basic
"""
query_theme        = lambda qstr: query_basic(Theme)(qstr)
query_named_entity = lambda qstr: query_basic(NamedEntity)(qstr)
query_institution  = lambda qstr: query_basic(Institution)(qstr)


"""
more complex sql selects
:param qstr: the query string
"""
# place is accessed by its address
query_place = lambda qstr: (
    select( bindparam( f"table_{uuid4()}", Place.__tablename__)
          , Place.id_uuid
          , Address.address
    ).filter( Place.id.in_(
        select( R_AddressPlace.id_place )
        .join(R_AddressPlace.address.and_( Address.address.ilike(qstr) )))
    ).join(Place.r_address_place).join(R_AddressPlace.address))

# Iconography objects where Title.entry_name or Actor.entry_name ILIKE qstr
query_iconography = lambda qstr: (
    select( bindparam( f"table_{uuid4()}", Iconography.__tablename__)
          , Iconography.id_uuid
          , Title.entry_name
    ).filter( or_(
        Iconography.id.in_(
            select( Title.id_iconography )
            .filter( Title.entry_name.ilike(qstr) ).subquery()), #Iconography.join(Iconography.title.and_( Title.entry_name.ilike(qstr) )),
        Iconography.id.in_(
            select(R_IconographyActor.id_iconography)
            .join(R_IconographyActor.actor.and_( Actor.entry_name.ilike(qstr) )).subquery())
    )).join(Iconography.title) )


# *********************************************
# pipeline

def quick_search(query_string:str) -> t.List[t.Dict]:
    """
    main process: combine above queries to build+run the query and format+return results.
    """
    # simplify
    query_string = to_ilike(query_string)

    r = (db.session.query( query_iconography(query_string).subquery() )
        .union( select( query_theme(query_string).subquery() )
              , select( query_named_entity(query_string).subquery() )
              , select( query_institution(query_string).subquery() )
              , select( query_place(query_string).subquery() )
              ))
    r = db.session.execute(r)
    return [ restructure_row(row) for row in r.all() ]