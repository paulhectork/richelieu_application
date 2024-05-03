from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
import json
import os

from ..utils.io import read_credfile
from ..utils.constants import CONFIDENTIALS


# **************************************
# create the engine used by tests
# **************************************


def build_engine() -> Engine:
    # read the credentials
    fn = read_credfile()
    with open(os.path.join(CONFIDENTIALS, fn)) as fh:
        cred = json.load(fh)
        print(cred)

    # create the engine
    return create_engine(
        f"postgresql://{ cred['username'] }:{ cred['password'] }@{ cred['uri'] }/{ cred['db'] }"
        , echo=True
    )

