from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from sqlalchemy import ForeignKey, Text, Boolean, ARRAY, TEXT
from sqlalchemy.dialects import postgresql as psql
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import func, select
import typing as t
import random

from ..utils.converters import int4range2list
from ..utils.strings import _validate_uuid
from ..app import db


# *******************************************************************
# secondary tables tables qualifying (giving extra information) on
# other tables
#
# contains
# ********
# * `Title`: the title of a ressource
# * `Annotation`: an annotation on an iconographic ressource
# * `Theme`: the theme of an iconographic ressource
# * `NamedEntity`: the named entity referenced/represented by
#   a ressource
# * `Actor`: a physical or moral person represented by a ressource
# * `PlaceGroup`: a table grouping different versions of the
#   same place throughout time (expressed as entries in
#   `Place`)
# *******************************************************************


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


# *******************************************************************


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


# *******************************************************************


class Theme(db.Model):
    """
    themes, created using a controlled vocabulary specific to our project
    """
    __tablename__: str = "theme"

    id          : Mapped[int] = mapped_column(psql.INTEGER, nullable=False, primary_key=True)
    id_uuid     : Mapped[str] = mapped_column(Text, nullable=False)
    entry_name  : Mapped[str] = mapped_column(Text, nullable=False)
    category    : Mapped[str] = mapped_column(Text, nullable=False)
    description : Mapped[str] = mapped_column(Text, nullable=True)

    r_iconography_theme : Mapped[t.List["R_IconographyTheme"]] = relationship("R_IconographyTheme", back_populates="theme")

    @validates("id_uuid", include_backrefs=False)
    def validate_uuid(self, key, _uuid):
        return _validate_uuid(_uuid, self.__tablename__)

    @hybrid_property
    def iconography_count(self):
        """
        number of `r_iconography_theme` rows related to `self`
        """
        out  = len(self.r_iconography_theme)
        return out

    @iconography_count.expression
    def iconography_count(cls):
        return (db.select( db.func.count(R_IconographyTheme.id)
                                  .label("iconography_count") )
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
        return { "id_uuid": self.id_uuid,                     # str
                 "entry_name": self.entry_name,               # str
                 "category": self.category,                   # str
                 "thumbnail": self.get_thumbnail(),           # t.List[str]
                 "iconography_count": self.iconography_count  # int
        }

    def serialize_full(self):
        return { "id_uuid": self.id_uuid,                     # str
                 "entry_name": self.entry_name,               # str
                 "description": self.description,             # str
                 "category": self.category,                   # str
                 "iconography": self.get_iconography(),       # t.List[t.Dict]
                 "iconography_count": self.iconography_count  # int
        }

    @classmethod
    def get_categories(cls, preview:bool) -> t.Dict:
        """
        return all categories mapped to the number
        of themes for that category. thumbnails for each
        category are selected manually and stored in `thumbnail_mapper`

        if `preview`, include the 3 first theme.category_name as a list of strings
        """
        thumbnail_mapper = { "consommer"  : "qr11e03469c172e4e0e98a155d15489cdd0_thumbnail.jpg",
                             "habiter"    : "qr1c70f59a032b241478d17a61289839edc_thumbnail.jpg",
                             "représenter": "qr1b30d13da1cb84c82be62c2b035afae53_thumbnail.jpg",
                             "se divertir": "qr128b29a8e91a349989d4522e59e874681_thumbnail.jpg",
                             "s'habiller" : "qr15b61f33ed5874465a17335b3dabec35d_thumbnail.jpg",
                             "s'informer" : "qr13f4af1da6eee4caabdc8e39f30ac92a6_thumbnail.jpg"  }
        if not preview:
            query = select( Theme.category
                          , func.count(Theme.id_uuid).label("count"))
        else:
            query = select( Theme.category
                          , func.count(Theme.id_uuid).label("count")
                          , func.array_agg(Theme.entry_name, type_=ARRAY(TEXT))
                            [0:3]
                            .label("preview") )
        query = query.group_by( Theme.category ).order_by( Theme.category )
        r = db.session.execute(query).all()
        # structure as JSON
        if not preview:
            out = [ { "category_name": row[0],                       # str
                      "count"        : row[1],                       # int
                      "thumbnail"    : [ thumbnail_mapper[row[0]] ]  # t.List[str] (is a list for consistency with other serializations)
                    }
                    for row in r ]
        else:
            out = [ { "category_name": row[0],                       # str
                      "count"        : row[1],                       # int
                      "thumbnail"    : [ thumbnail_mapper[row[0]] ], # t.List[str] (is a list for consistency with other serializations)
                      "preview"      : row[2]                        # t.List[str]
                    }
                    for row in r ]
        return out


    @classmethod
    def get_themes_for_category(cls, category:str):
        """
        return all themes for category `category`
        """
        query = (select(Theme)
                .filter(Theme.category==category)
                .order_by(Theme.entry_name))
        r = db.session.execute(query).all()
        return [ t[0].serialize_lite() for t in r ]


# *******************************************************************


class NamedEntity(db.Model):
    """
    table holding all the named entities represented
    by or mentionned by an iconographic ressource
    """
    __tablename__: str = "named_entity"

    id          : Mapped[int] = mapped_column(psql.INTEGER, nullable=False, primary_key=True)
    id_uuid     : Mapped[str] = mapped_column(Text, nullable=False)
    entry_name  : Mapped[str] = mapped_column(Text, nullable=False)
    category    : Mapped[str] = mapped_column(Text, nullable=False)
    description : Mapped[str] = mapped_column(Text, nullable=True)

    r_iconography_named_entity : Mapped[t.List["R_IconographyNamedEntity"]] = relationship("R_IconographyNamedEntity", back_populates="named_entity")

    @validates("id_uuid", include_backrefs=False)
    def validate_uuid(self, key, _uuid):
        return _validate_uuid(_uuid, self.__tablename__)

    # see `Theme` for a detailed explanation
    @hybrid_property
    def iconography_count(self) -> int:
        """number of `r_iconography_named_entity` rows related to `self`"""
        return len(self.r_iconography_named_entity)

    @iconography_count.expression
    def iconography_count(cls):
        """the same but at class/table level, to use the property in queries"""
        return (db.select( db.func.count(R_IconographyNamedEntity.id)
                                  .label("iconography_count") )
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
        return { "id_uuid": self.id_uuid,                     # str
                 "entry_name": self.entry_name,               # str
                 "category": self.category,                   # str
                 "thumbnail": self.get_thumbnail(),           # t.List[str]
                 "iconography_count": self.iconography_count  # int
        }

    def serialize_full(self):
        return { "id_uuid": self.id_uuid,                     # str
                 "entry_name": self.entry_name,               # str
                 "category": self.category,                   # str
                 "description": self.description,             # str
                 "iconography": self.get_iconography(),       # t.List[t.Dict]
                 "iconography_count": self.iconography_count  # int
        }

    @classmethod
    def get_categories(cls, preview:bool) -> t.Dict:
        """
        return all categories mapped to the
        number of named entities for that category
        if `preview`, each category will be mapped to a string list of 3 named entities
        """
        thumbnail_mapper = { "acteurs et actrices"          : "qr1003a5dfa14564d69a2e75dc3318d7c17_thumbnail.jpg",
                             "banques"                      : "qr11de4bc16498c4423b678dd112b30698f_thumbnail.jpg",
                             "cafés et restaurants"         : "qr1ecd7392d03ae4690b46ca0b48d6a306b_thumbnail.jpg",
                             "commerces"                    : "qr12fe8eb0ffbab4973978313ed196f8b86_thumbnail.png",
                             "épiceries et alimentation"    : "qr183ed41474751443e8906971a5c905fd4_thumbnail.jpg",
                             "évènements"                   : "qr1f0353117f52e4c39b3d85deff2c45fec_thumbnail.jpg",
                             "institutions et organisations": "qr1a879411aaa4d4582b22f19c7fb1c2891_thumbnail.jpg",
                             "mode et objets"               : "qr1c37f846c694a460cb893aef61f8b9014_thumbnail.jpg",
                             "personnalités et fiction"     : "qr14fb78a7405444466ae93af73058854e2_thumbnail.png",
                             "publications et photographies": "qr1387abb06ea094ee995755d12d4331a5c_thumbnail.jpg",
                             "santé"                        : "qr162c6f039762f400582d68d92fa0cf113_thumbnail.jpg",
                             "théâtres et spectacles"       : "qr15e18895353984bdb95b80107caf8e98c_thumbnail.jpg",
                             "ville et architecture"        : "qr14ed31d174a8845219f452c6a09071628_thumbnail.jpg"
                           }
        if not preview:
            query = select( NamedEntity.category
                          , func.count(NamedEntity.id_uuid).label("count"))
        else:
            query = select( NamedEntity.category
                          , func.count(NamedEntity.id_uuid).label("count")
                          , func.array_agg(NamedEntity.entry_name, type_=ARRAY(TEXT))
                            [0:3]
                            .label("preview") )
        query = query.group_by( NamedEntity.category ).order_by( NamedEntity.category )
        r = db.session.execute(query).all()
        if not preview:
            out = [ { "category_name": row[0],
                      "count": row[1],
                      "thumbnail": [ thumbnail_mapper[row[0]] if row[0] in thumbnail_mapper.keys() else "" ]
                    }
                    for row in r ]
        else:
            out = [ { "category_name": row[0],                       # str
                      "count"        : row[1],                       # int
                      "thumbnail"    : [ thumbnail_mapper[row[0]] ], # t.List[str] (is a list for consistency with other serializations)
                      "preview"      : row[2]                        # t.List[str]
                    }
                    for row in r ]
        return out

    @classmethod
    def get_named_entities_for_category(cls, category:str):
        """
        return all named entities for category `category`
        """
        query = (select(NamedEntity)
                .filter(NamedEntity.category==category)
                .order_by(NamedEntity.entry_name))
        r = db.session.execute(query).all()
        return [ t[0].serialize_lite() for t in r ]



# *******************************************************************


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