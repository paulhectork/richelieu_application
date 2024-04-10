from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


from .admin import *
from .data_sources import *
from .places import *
from .qualifiers import *
from .relationships import *

