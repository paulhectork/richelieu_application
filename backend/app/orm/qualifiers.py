from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from sqlalchemy import ForeignKey, Text, Boolean, ARRAY
from sqlalchemy.dialects import postgresql as psql
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import func, select
import typing as t
import random

from ..utils.strings import _validate_uuid, int4range2list
from ..app import db





#














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





    #








    #


    #



    @hybrid_property
    def count_iconography(self):
        """
        number of `r_iconography_theme` rows related to `self`
        """
        out  = len(self.r_iconography_theme)
        return out

    @count_iconography.expression
    def count_iconography(cls):
        return (db.select( db.func.count(R_IconographyTheme.id)
                                  .label("count_iconography") )
                  .filter(R_IconographyTheme.id_theme == cls.id)
                  .label("total_rel")
        )

    def get_thumbnail(self):
        """get a thumbnail image for the current theme"""
        return [ f.url
                 for f in random.choice(self.r_iconography_theme)
                          .iconography.filename
                 if "thumbnail" in f.url ]

    def get_iconography(self):
        return [ r.iconography.serialize_lite()
                 for r in self.r_iconography_theme ]

    def serialize_lite(self):
        return { "id_uuid": self.id_uuid,
                 "entry_name": self.entry_name,
                 "thumbnail": self.get_thumbnail(),
        }

    def serialize_full(self):
        return { "id_uuid": self.id_uuid,
                 "entry_name": self.entry_name,
                 "description": self.description,
                 "iconography": self.get_iconography()
        }


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

    # see `Theme` for a detailed explanation
    @hybrid_property
    def count_iconography(self) -> int:
        """number of `r_iconography_named_entity` rows related to `self`"""
        return len(self.r_iconography_named_entity)

    @count_iconography.expression
    def count_iconography(cls):
        """the same but at class/table level, to use the property in queries"""
        return (db.select( db.func.count(R_IconographyNamedEntity.id)
                                  .label("count_iconography") )
                  .filter(R_IconographyNamedEntity.id_named_entity == cls.id)
                  .label("total_rel")
        )

    def get_thumbnail(self):
        """get a thumbnail image for the current named entity"""
        return [ f.url
                 for f in random.choice(self.r_iconography_named_entity)
                          .iconography.filename
                 if "thumbnail" in f.url ]

    def get_iconography(self):
        return [ r.iconography.serialize_lite()
                 for r in self.r_iconography_named_entity ]

    def serialize_lite(self):
        return { "id_uuid": self.id_uuid,
                 "entry_name": self.entry_name,
                 "thumbnail": self.get_thumbnail()
        }

    def serialize_full(self):
        return { "id_uuid": self.id_uuid,
                 "entry_name": self.entry_name,
                 "description": self.description,
                 "iconography": self.get_iconography()
        }


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
                 for r in self.r_iconography_actor
                 if r.role == "author" ]

    def get_iconography_publisher(self):
        return [ r.iconography.serialize_lite()
                 for r in self.r_iconography_actor
                 if r.role == "publisher" ]

    def serialize_lite(self):
        return { "id_uuid": self.id_uuid,
                 "entry_name": self.entry_name }

    def serialize_full(self):
        return { "id_uuid": self.id_uuid,
                 "entry_name": self.entry_name,
                 "iconography_from_author": self.get_iconography_author(),
                 "iconography_from_publisher": self.get_iconography_publisher() }


from .relationships import R_IconographyNamedEntity, R_IconographyTheme