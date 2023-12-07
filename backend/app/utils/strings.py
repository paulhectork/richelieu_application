import json
import re
import os

from .constants import CONFIDENTIALS
from .io import read_credfile


def build_uuid() -> str:
    """
    create a UUID tailored to our database:
    a 32 character hexadecimal string (without the `-`)
    and prefixed by `qr`
    these will be used to generate arks identifiers in Agorha.
    """
    return f"qr1{uuid.uuid4().hex}"


def validate_uuid(_uuid:str, tablename:str) -> str:
    """
    check that an uuid follows this structure:
    `qr1` + a 32char hexadecimal UUID, with no `-` separators, in lowercase
    
    :param _uuid: the identifier to validate
    :param tablename: the name of the table which we're
                      validating.
    :returns: the same identifier if it was validated.
    """
    if not re.search("^qr1[a-z0-9]{32}$", _uuid):
        raise ValueError("""
            Validation error on `%s.id`.
            A primary key must match `^qr1[a-z0-9]{32}$`.
            Input value: `%s`
        """ % ( tablename, _uuid ))
    return _uuid


def db_uri() -> str:
    """
    create an URI to the postgres database. the 
    targeted database is specified by the 
    `-d --database` argument provided by the user
    """
    fn = read_credfile()
    with open(os.path.join(CONFIDENTIALS, fn)) as fh:
        cred = json.load(fh)
    # create the engine
    return f"postgresql://{cred['username']}:{cred['password']}@{cred['uri']}/{cred['db']}"


