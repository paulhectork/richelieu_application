from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from sqlalchemy import ForeignKey, Text, Boolean, ARRAY
from sqlalchemy.dialects import postgresql as psql
import typing as t

from ..utils.strings import _validate_uuid, int4range2list
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
# * `PlaceGroup`: a table grouping different versions of the
#   same place throughout time (expressed as entries in
#   `Place`)
# -----------------------------------------------------------------


class Title(db.Model):
    """
    the title of an iconographic ressource.
    """
    __tablename__: str = "title"

    id             : Mapped[int]  = mapped_column(psql.INTEGER, nullable=False, primary_key=True)
    id_uuid        : Mapped[str]  = mapped_column(Text, nullable=False)
    entry_name     : Mapped[str]  = mapped_column(Text, nullable=False)
    ismain         : Mapped[bool] = mapped_column(Boolean, nullable=False)
    id_iconography : Mapped[int]  = mapped_column(psql.INTEGER, ForeignKey("iconography.id"), nullable=False)

    iconography : Mapped["Iconography"] = relationship("Iconography", back_populates="title")

    @validates("id_uuid", include_backrefs=False)
    def validate_uuid(self, key, _uuid):
        return _validate_uuid(_uuid, self.__tablename__)


class Annotation(db.Model):
    """
    an annotation for a IIIF manifest.
    it must be a valid IIIF annotation json.
    """
    __tablename__: str = "annotation"

    id             : Mapped[int]    = mapped_column(psql.INTEGER, nullable=False, primary_key=True)
    id_uuid        : Mapped[str]    = mapped_column(Text, nullable=False)
    content        : Mapped[t.Dict] = mapped_column(psql.JSON, nullable=False)
    id_iconography : Mapped[int]    = mapped_column(psql.INTEGER, ForeignKey("iconography.id"), nullable=False)

    iconography : Mapped["Iconography"] = relationship("Iconography", back_populates="annotation")

    @validates("id_uuid", include_backrefs=False)
    def validate_uuid(self, key, _uuid):
        return _validate_uuid(_uuid, self.__tablename__)


class Theme(db.Model):
    """
    themes, created using a controlled vocabulary specific to our project
    """
    __tablename__: str = "theme"

    id          : Mapped[int] = mapped_column(psql.INTEGER, nullable=False, primary_key=True)
    id_uuid     : Mapped[str] = mapped_column(Text, nullable=False)
    entry_name  : Mapped[str] = mapped_column(Text, nullable=False)
    description : Mapped[str] = mapped_column(Text, nullable=True)

    r_iconography_theme : Mapped[t.List["R_IconographyTheme"]] = relationship("R_IconographyTheme", back_populates="theme")

    @validates("id_uuid", include_backrefs=False)
    def validate_uuid(self, key, _uuid):
        return _validate_uuid(_uuid, self.__tablename__)

    def get_iconography(self):
        return [ r.iconography.serialize_lite()
                 for r in self.r_iconography_theme ]

    def serialize_lite(self):
        return { "id_uuid": self.id_uuid,
                 "entry_name": self.entry_name }

    def serialize_full(self):
        return { "id_uuid": self.id_uuid,
                 "entry_name": self.entry_name,
                 "description": self.description,
                 "iconography": self.get_iconography() }


class NamedEntity(db.Model):
    """
    table holding all the named entities represented
    by or mentionned by an iconographic ressource
    """
    __tablename__: str = "named_entity"

    id          : Mapped[int] = mapped_column(psql.INTEGER, nullable=False, primary_key=True)
    id_uuid     : Mapped[str] = mapped_column(Text, nullable=False)
    entry_name  : Mapped[str] = mapped_column(Text, nullable=False)
    description : Mapped[str] = mapped_column(Text, nullable=True)

    r_iconography_named_entity : Mapped[t.List["R_IconographyNamedEntity"]] = relationship("R_IconographyNamedEntity", back_populates="named_entity")

    @validates("id_uuid", include_backrefs=False)
    def validate_uuid(self, key, _uuid):
        return _validate_uuid(_uuid, self.__tablename__)

    def get_iconography(self):
        return [ r.iconography.serialize_lite()
                 for r in self.r_iconography_theme ]

    def serialize_lite(self):
        return { "id_uuid": self.id_uuid,
                 "entry_name": self.entry_name }

    def serialize_full(self):
        return { "id_uuid": self.id_uuid,
                 "entry_name": self.entry_name,
                 "description": self.description,
                 "iconography": self.get_iconography() }


class Actor(db.Model):
    """
    actors related to iconographic ressources: people who
    created those ressources, who are represented in them...
    """
    __tablename__: str = "actor"

    id         : Mapped[int] = mapped_column(psql.INTEGER, nullable=False, primary_key=True)
    id_uuid    : Mapped[str] = mapped_column(Text, nullable=False)
    entry_name : Mapped[str] = mapped_column(Text, nullable=False)

    r_iconography_actor : Mapped[t.List["R_IconographyActor"]] = relationship("R_IconographyActor", back_populates="actor")

    @validates("id_uuid", include_backrefs=False)
    def validate_uuid(self, key, _uuid):
        return _validate_uuid(_uuid, self.__tablename__)

    def get_iconography_author(self):
        return [ r.iconography.serialize_lite()
                 for r in self.r_iconography_theme
                 if r.role == "author" ]

    def get_iconography_publisher(self):
        return [ r.iconography.serialize_lite()
                 for r in self.r_iconography_theme
                 if r.role == "publisher" ]

    def serialize_lite(self):
        return { "id_uuid": self.id_uuid,
                 "entry_name": self.entry_name }

    def serialize_full(self):
        return { "id_uuid": self.id_uuid,
                 "entry_name": self.entry_name,
                 "iconography_from_author": self.get_iconography_author(),
                 "iconography_from_publisher": self.get_iconography_publisher() }


class PlaceGroup(db.Model):
    """
    a place group regroups different places together to group together
    different expressions of the same place throughout time (place de la Bourse
    in 1850, 1860 ... can be represented by different places if they change with
    time).
    """
    __tablename__ = "place_group"

    id          : Mapped[int] = mapped_column(psql.INTEGER, nullable=False, primary_key=True)
    id_uuid     : Mapped[str] = mapped_column(Text, nullable=False)
    entry_name  : Mapped[str] = mapped_column(Text, nullable=False)
    description : Mapped[str] = mapped_column(Text, nullable=True)

    place : Mapped[t.List["Place"]] = relationship("Place", back_populates="place_group")

    @validates("id_uuid", include_backrefs=False)
    def validate_uuid(self, key, _uuid):
        return _validate_uuid(_uuid, self.__tablename__)

    def get_place(self):
        return [ p.serialize_lite()
                 for p in self.place ]

    def serialize_lite(self):
        return { "id_uuid": self.id_uuid,
                 "entry_name": self.entry_name }

    def serialize_lite(self):
        return { "id_uuid": self.id_uuid,
                 "entry_name": self.entry_name,
                 "description": self.description,
                 "place": self.get_place() }

