from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from sqlalchemy import ForeignKey, Text, Boolean, ARRAY
from sqlalchemy.dialects import postgresql
from typing import List, Dict

from ..utils.strings import validate_uuid, int4range2list
from ..app import db 


# -----------------------------------------------------------------
# secondary tables tables qualifying (giving extra information) on 
# other tables
#
# contains
# ~~~~~~~~
# * `Title`: the title of a ressource
# * `Annotation`: an annotation on an iconographic ressource
# * `Theme`: the theme of an iconographic ressource
# * `NamedEntity`: the named entity referenced/represented by 
#   a ressource
# * `Actor`: a physical or moral person represented by a ressource
# * `LocationGroup`: a table grouping different versions of the
#   same location throughout time (expressed as entries in 
#   `Location`)
# -----------------------------------------------------------------


class Title(db.Model):
    """
    the title of an iconographic ressource.
    """
    __tablename__: str = "title"
    
    id             : Mapped[int]  = mapped_column(postgresql.INTEGER, nullable=False, primary_key=True)
    uuid           : Mapped[str]  = mapped_column(Text, nullable=False)
    name           : Mapped[str]  = mapped_column(Text, nullable=False)
    ismain         : Mapped[bool] = mapped_column(Boolean, nullable=False)
    id_iconography : Mapped[int]  = mapped_column(postgresql.INTEGER, ForeignKey("iconography.id"), nullable=False)
    
    iconography : Mapped["Iconography"] = relationship("Iconography", back_populates="title")
    
    @validates("uuid", include_backrefs=False)
    def validate_uuid(self, key, _uuid):
        return validate_uuid(_uuid, self.__tablename__)
    

class Annotation(db.Model):
    """
    an annotation for a IIIF manifest. 
    it must be a valid IIIF annotation json.
    """
    __tablename__: str = "annotation"

    id             : Mapped[int]  = mapped_column(postgresql.INTEGER, nullable=False, primary_key=True)
    uuid           : Mapped[str]  = mapped_column(Text, nullable=False)
    content        : Mapped[Dict] = mapped_column(postgresql.JSON, nullable=False)
    id_iconography : Mapped[int]  = mapped_column(postgresql.INTEGER, ForeignKey("iconography.id"), nullable=False)
    
    iconography : Mapped["Iconography"] = relationship("Iconography", back_populates="annotation")

    @validates("uuid", include_backrefs=False)
    def validate_uuid(self, key, _uuid):
        return validate_uuid(_uuid, self.__tablename__)


class Theme(db.Model):
    """
    themes, created using a controlled vocabulary specific to our project
    """
    __tablename__: str = "theme"
    
    id          : Mapped[int] = mapped_column(postgresql.INTEGER, nullable=False, primary_key=True)
    uuid        : Mapped[str] = mapped_column(Text, nullable=False)
    name        : Mapped[str] = mapped_column(Text, nullable=False)
    description : Mapped[str] = mapped_column(Text, nullable=True)

    r_iconography_theme : Mapped[List["R_IconographyTheme"]] = relationship("R_IconographyTheme"
                                                                            , back_populates="theme")

    @validates("uuid", include_backrefs=False)
    def validate_uuid(self, key, _uuid):
        return validate_uuid(_uuid, self.__tablename__)

    def serialize_lite(self):
        return { "uuid": self.uuid,
                 "name": self.name }


class NamedEntity(db.Model):
    """
    table holding all the named entities represented 
    by or mentionned by an iconographic ressource
    """
    __tablename__: str = "named_entity"
    
    id          : Mapped[int] = mapped_column(postgresql.INTEGER, nullable=False, primary_key=True)
    uuid        : Mapped[str] = mapped_column(Text, nullable=False)
    name        : Mapped[str] = mapped_column(Text, nullable=False)
    description : Mapped[str] = mapped_column(Text, nullable=True)
    
    r_iconography_named_entity : Mapped[List["R_IconographyNamedEntity"]] = relationship("R_IconographyNamedEntity"
                                                                                         , back_populates="named_entity")
    
    @validates("uuid", include_backrefs=False)
    def validate_uuid(self, key, _uuid):
        return validate_uuid(_uuid, self.__tablename__)
    
    def serialize_lite(self):
        return { "uuid": self.uuid,
                 "name": self.name }


class Actor(db.Model):
    """
    actors related to iconographic ressources: people who 
    created those ressources, who are represented in them...
    """
    __tablename__: str = "actor"
    
    id         : Mapped[int]       = mapped_column(postgresql.INTEGER, nullable=False, primary_key=True)
    uuid       : Mapped[str]       = mapped_column(Text, nullable=False)
    last_name  : Mapped[str]       = mapped_column(Text, nullable=False)
    first_name : Mapped[str]       = mapped_column(Text, nullable=True)
    date       : Mapped[str]       = mapped_column(postgresql.INT4RANGE, nullable=True)        # range between two dates of activity in YYYY YYYY format
    sources    : Mapped[List[str]] = mapped_column(ARRAY(Text, dimensions=1), nullable=False)  # the text in the sources linked to an actor (can be used as alternative forms of the name we've given the actor)
    
    r_iconography_actor : Mapped[List["R_IconographyActor"]] = relationship("R_IconographyActor"
                                                                            , back_populates="actor")
    
    @validates("uuid", include_backrefs=False)
    def validate_uuid(self, key, _uuid):
        return validate_uuid(_uuid, self.__tablename__)
    
    def serialize_lite(self):
        return { "uuid": self.uuid,              # str
                 "first_name": self.first_name,  # str
                 "last_name": self.last_name }   # str
    
    def serialize_full(self):
        return { "uuid"       : self.uuid,                  # str
                 "first_name" : self.first_name,            # str
                 "last_name"  : self.last_name,             # str
                 "date"       : int4range2list(self.date),  # t.List[int]
                 "sources"    : self.sources                # t.List[str]
         }
    

class LocationGroup(db.Model):
    """
    a location group regroups different locations together to group together
    different expressions of the same location throughout time (place de la Bourse
    in 1850, 1860 ... can be represented by different locations if they change with
    time).
    """
    __tablename__ = "location_group"
    
    id          : Mapped[int] = mapped_column(postgresql.INTEGER, nullable=False, primary_key=True)
    uuid        : Mapped[str] = mapped_column(Text, nullable=False)
    name        : Mapped[str] = mapped_column(Text, nullable=False)
    description : Mapped[str] = mapped_column(Text, nullable=True)
    
    location : Mapped[List["Location"]] = relationship("Location"
                                                       , back_populates="location_group")

    @validates("uuid", include_backrefs=False)
    def validate_uuid(self, key, _uuid):
        return validate_uuid(_uuid, self.__tablename__)

