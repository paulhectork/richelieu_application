from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from sqlalchemy import ForeignKey, Text, Boolean, Float
from sqlalchemy.dialects import postgresql as psql
import typing as t
import intervals

from ..utils.strings import _validate_uuid, int4range2list
from ..app import db


# -----------------------------------------------------------------
# tables describing external ressources gathered by the project.
# these are the "main" tables, since they contain all of our
# documentary research
#
# contains
# ~~~~~~~~
# * `Iconography`: iconographic ressources (paintings, print...)
# * `Cartography`: cartographic ressources
# * `Filename`: external files, especially images of iconographic
#   and cartographic ressources
# * `Directory`: the Bottins et Annuaires.
# -----------------------------------------------------------------


class Iconography(db.Model):
    """
    main class for the iconography, describing image and documents
    presented on the website.
    """
    __tablename__: str = "iconography"

    id               : Mapped[int]         = mapped_column(psql.INTEGER, nullable=False, primary_key=True)
    id_uuid          : Mapped[str]         = mapped_column(Text, nullable=False)
    iiif_url         : Mapped[str]         = mapped_column(Text, nullable=True)
    iiif_folio       : Mapped[t.List[int]] = mapped_column(psql.ARRAY(psql.INTEGER, dimensions=1), nullable=True)
    source_url       : Mapped[str]         = mapped_column(Text, nullable=True)
    date_source      : Mapped[str]         = mapped_column(Text, nullable=True)
    date_corr        : Mapped[str]         = mapped_column(Text, nullable=True)
    date             : Mapped[t.List[int]] = mapped_column(psql.INT4RANGE, nullable=True)
    technique        : Mapped[t.List[str]] = mapped_column(psql.ARRAY(Text, dimensions=1), nullable=True)
    description      : Mapped[str]         = mapped_column(Text, nullable=True)
    inscription      : Mapped[str]         = mapped_column(Text, nullable=True)
    corpus           : Mapped[str]         = mapped_column(Text, nullable=True)
    inventory_number : Mapped[str]         = mapped_column(Text, nullable=True)
    produced         : Mapped[bool]        = mapped_column(Boolean, nullable=True)
    represents       : Mapped[bool]        = mapped_column(Boolean, nullable=True)
    id_licence       : Mapped[int]         = mapped_column(psql.INTEGER, ForeignKey("licence.id"), nullable=False)

    title                      : Mapped[t.List["Title"]]                    = relationship("Title", back_populates="iconography")
    annotation                 : Mapped[t.List["Annotation"]]               = relationship("Annotation", back_populates="iconography")
    filename                   : Mapped[t.List["Filename"]]                 = relationship("Filename", back_populates="iconography")
    licence                    : Mapped["Licence"]                          = relationship("Licence", back_populates="iconography")
    r_iconography_theme        : Mapped[t.List["R_IconographyTheme"]]       = relationship("R_IconographyTheme", back_populates="iconography")
    r_iconography_actor        : Mapped[t.List["R_IconographyActor"]]       = relationship("R_IconographyActor", back_populates="iconography")
    r_iconography_place        : Mapped[t.List["R_IconographyPlace"]]       = relationship("R_IconographyPlace", back_populates="iconography")
    r_iconography_named_entity : Mapped[t.List["R_IconographyNamedEntity"]] = relationship("R_IconographyNamedEntity", back_populates="iconography")
    r_admin_person             : Mapped[t.List["R_AdminPerson"]]            = relationship("R_AdminPerson", back_populates="iconography")
    r_institution              : Mapped[t.List["R_Institution"]]            = relationship("R_Institution", back_populates="iconography")

    @validates("id_uuid", include_backrefs=False)
    def validate_uuid(self, key, _uuid):
        return _validate_uuid(_uuid, self.__tablename__)

    def get_author(self) -> t.List[t.Dict]:
        """
        return a t.list of authors, with the main author first
        """
        l = [ [ r.actor.serialize_lite(), r.ismain ]
              for r in self.r_iconography_actor
              if r.role == "author" ]
        l = [ a[0] for a in sorted(l, key=lambda x: x[1]) ]  # reorder + remove the `ismain` flag. the first item is the main author
        return l

    def get_title(self) -> t.List[str]:
        """
        get the title(s) for a ressource and return them as a list of strings.
        """
        l = [ [t.entry_name, t.ismain] for t in self.title ]
        l = [ t[0] for t in sorted(l, key=lambda x: x[1]) ]  # [<main title>, <other title>, <...> ]
        return l

    def get_publisher(self) -> t.List[t.Dict]:
        """
        get the list of publishers associated to a ressource
        """
        return [ r.actor.serialize_lite()
                 for r in self.r_iconography_actor
                 if r.role == "publisher" ]

    def get_theme(self) -> t.List[t.Dict]:
        return [ r.theme.serialize_lite()
                 for r in self.r_iconography_theme ]

    def get_named_entity(self) -> t.List[t.Dict]:
        return [ r.named_entity.serialize_lite()
                 for r in self.r_iconography_named_entity ]

    def get_admin_person(self) -> t.Dict:
        return [ r.admin_person.serialize_lite()
                 for r in self.r_admin_person ]

    def get_institution(self) -> t.Dict:
        return [ r.institution.serialize_lite()
                 for r in self.r_institution ]

    def get_filename(self) -> t.List:
        return [ f.serialize_lite()
                 for f in self.filename ]

    def get_thumbnail(self) -> t.List:
        """get thumbnails only"""
        return [ f.url
                 for f in self.filename
                 if "thumbnail" in f.url ]

    def serialize_lite(self) -> t.Dict:
        return { "id_uuid"   : self.id_uuid,               # str
                 "iiif_url"  : self.iiif_url,              # str
                 "date"      : int4range2list(self.date),  # t.List[int]
                 "authors"   : self.get_author(),          # t.List[str]
                 "title"     : self.get_title(),           # t.List[str]
                 "thumbnail" : self.get_thumbnail(),       # t.List[str]
        }

    def serialize_full(self) -> t.Dict:
        return { "id_uuid"          : self.id_uuid,                      # str
                 "iiif_url"         : self.iiif_url,                     # str
                 "source_url"       : self.source_url,                   # str
                 "date"             : int4range2list(self.date),         # t.List[int]
                 "date_source"      : self.date_source,                  # str
                 "technique"        : self.technique,                    # str
                 "corpus"           : self.corpus,                       # str
                 "inventory_number" : self.inventory_number,             # str
                 "produced"         : self.produced,                     # bool
                 "represents"       : self.represents,                   # bool

                 "institution"      : self.get_institution(),            # t.List[t.Dict]
                 "filename"         : self.get_filename(),               # t.List[t.Dict]
                 "author"           : self.get_author(),                 # t.List[t.Dict]
                 "title"            : self.get_title(),                  # t.List[str]
                 "licence"          : self.licence.serialize_lite(),     # t.Dict
                 "publisher"        : self.get_publisher(),              # t.List[t.Dict]
                 "theme"            : self.get_theme(),                  # t.List[t.Dict]
                 "named_entity"     : self.get_named_entity(),           # t.List[t.Dict]
                 "admin_person"     : self.get_admin_person()            # t.List[t.Dict]
        }



class Cartography(db.Model):
    """
    class describing our cartographic ressources

    * `vector` is the shape of the place on a cartographic space. it
      is stored as a JSON (the structure is a GeoJSON geometry multipolygon)
    """
    __tablename__: str = "cartography"

    id               : Mapped[int]                   = mapped_column(psql.INTEGER, nullable=False, primary_key=True)
    id_uuid          : Mapped[str]                   = mapped_column(Text, nullable=False)
    source_url       : Mapped[str]                   = mapped_column(Text, nullable=True)
    title            : Mapped[str]                   = mapped_column(Text, nullable=True)
    date_source      : Mapped[str]                   = mapped_column(Text, nullable=True)
    inventory_number : Mapped[str]                   = mapped_column(Text, nullable=True)
    date             : Mapped[intervals.IntInterval] = mapped_column(psql.INT4RANGE, nullable=True)
    vector           : Mapped[t.Dict]                = mapped_column(psql.JSON, nullable=False)
    crs_epsg         : Mapped[int]                   = mapped_column(psql.INTEGER, nullable=False)
    granularity      : Mapped[str]                   = mapped_column(Text, nullable=False)
    map_source       : Mapped[str]                   = mapped_column(Text, nullable=False)
    id_licence       : Mapped[int]                   = mapped_column(psql.INTEGER, ForeignKey("licence.id"), nullable=False)

    filename            : Mapped[t.List["Filename"]]           = relationship("Filename", back_populates="cartography")
    licence             : Mapped["Licence"]                    = relationship("Licence", back_populates="cartography")
    r_cartography_place : Mapped[t.List["R_CartographyPlace"]] = relationship("R_CartographyPlace", back_populates="cartography")
    r_admin_person      : Mapped[t.List["R_AdminPerson"]]      = relationship("R_AdminPerson", back_populates="cartography")
    r_institution       : Mapped[t.List["R_Institution"]]      = relationship("R_Institution", back_populates="cartography")

    @validates("id_uuid", include_backrefs=False)
    def validate_uuid(self, key, _uuid):
        return _validate_uuid(_uuid, self.__tablename__)

    def get_filename(self) -> t.List[t.Dict]:
        return [ f.serialize_lite() for f in self.filename ]

    def get_admin_person(self) -> t.List[t.Dict]:
        return [ r.admin_person.serialize_lite()
                 for r in self.r_admin_person ]

    def get_institution(self) -> t.List[t.Dict]:
        return [ r.institution.serialize_lite()
                 for r in self.r_institution ]

    def get_place(self) -> t.List[t.Dict]:
        """
        retrieve places associated to a cartographic ressource
        """
        return [ r.place.serialize_lite()
                 for r in self.r_cartography_place ]

    def serialize_lite(self) -> t.Dict:
        return { "id_uuid"  : self.id_uuid,               # str
                 "title"    : self.title,                 # str
                 "date"     : int4range2list(self.date),  # t.List[int]
                 "place"    : self.get_place(),           # t.List[t.Dict]
                 "filename" : self.get_filename()         # t.list[str]
        }

    def serialize_full(self) -> t.Dict:
        return { "id_uuid"          : self.id_uuid,                  # str
                 "title"            : self.title,                    # str
                 "date"             : int4range2list(self.date),     # t.List[int]
                 "date_source"      : self.date_source,              # str
                 "source_url"       : self.source_url,               # str
                 "inventory_number" : self.inventory_number,         # str
                 "vector"           : self.vector,                   # t.Dict
                 "granularity"      : self.granularity,              # str
                 "map_source"       : self.map_source,               # str

                 "filename"         : self.get_filename(),           # t.List[t.Dict]
                 "licence"          : self.licence.serialize_lite(), # t.Dict
                 "place"            : self.get_place(),              # t.List[t.Dict]
                 "admin_person"     : self.get_admin_person(),       # t.List[t.Dict]
                 "institution"      : self.get_institution()         # t.List[t.Dict]
         }


class Directory(db.Model):
    """
    the third data source: directory (Bottins et Annuaires),
    mapping persons to an address and to the activity they
    practiced there. the Bottins were extracted from Gallica.
    """
    __tablename__ = "directory"

    id           : Mapped[int]         = mapped_column(psql.INTEGER, nullable=False, primary_key=True)
    id_uuid      : Mapped[str]         = mapped_column(Text, nullable=False)
    gallica_ark  : Mapped[str]         = mapped_column(Text, nullable=False)
    gallica_page : Mapped[str]         = mapped_column(Text, nullable=False)  # the page on the directory
    gallica_row  : Mapped[str]         = mapped_column(Text, nullable=False)  # the page row in the directory
    entry_name   : Mapped[str]         = mapped_column(Text, nullable=False)
    occupation   : Mapped[str]         = mapped_column(Text, nullable=False)
    date         : Mapped[str]         = mapped_column(psql.INT4RANGE, nullable=False)
    tags         : Mapped[t.List[str]] = mapped_column(psql.ARRAY(Text, dimensions=1), nullable=True)
    id_address   : Mapped[int]         = mapped_column(psql.INTEGER, ForeignKey("address.id"), nullable=False)
    id_licence   : Mapped[int]         = mapped_column(psql.INTEGER, ForeignKey("licence.id"), nullable=False)

    address        : Mapped["Address"]               = relationship("Address", back_populates="directory")
    licence        : Mapped["Licence"]               = relationship("Licence", back_populates="directory")
    r_admin_person : Mapped[t.List["R_AdminPerson"]] = relationship("R_AdminPerson", back_populates="directory")
    r_institution  : Mapped[t.List["R_Institution"]] = relationship("R_Institution", back_populates="directory")

    @validates("id_uuid", include_backrefs=False)
    def validate_uuid(self, key, _uuid):
        return _validate_uuid(_uuid, self.__tablename__)

    def get_admin_person(self) -> t.Dict:
        return [ r.admin_person.serialize_lite()
                 for r in self.r_admin_person ]

    def get_institution(self) -> t.Dict:
        return [ r.institution.serialize_lite()
                 for r in self.r_institution ]

    def serialize_lite(self) -> t.Dict:
        return { "id_uuid"    : self.id_uuid,
                 "entry_name" : self.entry_name,
                 "occupation" : self.occupation,
                 "date"       : self.date,
                 "address"    : self.address.to_string() }

    def serialize_full(self):
        return { "id_uuid"      : self.id_uuid,
                 "entry_name"   : self.entry_name,
                 "occupation"   : self.occupation,
                 "date"         : self.date,
                 "licence"      : self.licence.serialize_lite(),
                 "address"      : self.licence.serialize_lite(),
                 "admin_person" : self.get_admin_person(),
                 "institution"  : self.get_institution()
        }


class Filename(db.Model):
    """
    class containing data on image and other external files (reproduction
    of iconographic ressources or cartographic ressources.
    """
    __tablename__ = "filename"

    id             : Mapped[int]                          = mapped_column(psql.INTEGER, nullable=False, primary_key=True)
    id_uuid        : Mapped[str]                          = mapped_column(Text, nullable=False)
    url            : Mapped[str]                          = mapped_column(Text, nullable=False)
    latlngbounds   : Mapped[t.List[t.List[float]] | None] = mapped_column(psql.ARRAY(Float, dimensions=2), nullable=True)  # [ [<float>,<float>], [<float>,<float>] ]
    id_licence     : Mapped[int]                          = mapped_column(psql.INTEGER, ForeignKey("licence.id"), nullable=True)
    id_iconography : Mapped[int]                          = mapped_column(psql.INTEGER, ForeignKey("iconography.id"), nullable=True)
    id_cartography : Mapped[int]                          = mapped_column(psql.INTEGER, ForeignKey("cartography.id"), nullable=True)

    licence     : Mapped["Licence"]     = relationship("Licence", back_populates="filename")
    iconography : Mapped["Iconography"] = relationship("Iconography", back_populates="filename")
    cartography : Mapped["Cartography"] = relationship("Cartography", back_populates="filename")

    @validates("id_uuid", include_backrefs=False)
    def validate_uuid(self, key, _uuid):
        return _validate_uuid(_uuid, self.__tablename__)

    def serialize_lite(self):
        return { "url": self.url,                     # str
                 "latlngbounds": self.latlngbounds }  # t.List[t.List[float]]

    def get_cartography(self):
        return self.cartography.serialize_lite() if self.cartography is not None else None

    def get_iconography(self):
        return self.iconography.serialize_lite() if self.iconography is not None else None

    def serialize_full(self):
        return { "url": self.url,                                 # str
                 "latlngbounds" : self.latlngbounds,              # t.Dict
                 "licence"      : self.licence.serialize_lite(),  # t.Dict
                 "iconography"  : self.get_cartography(),         # t.Dict | None
                 "cartography"  : self.get_iconography()          # t.Dict | None
        }


