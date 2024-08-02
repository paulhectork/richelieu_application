from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from sqlalchemy.dialects import postgresql as psql
from sqlalchemy import ForeignKey, Text
from sqlalchemy import select, and_
import typing as t
import intervals

from ..utils.converters import int4range2list
from ..utils.strings import _validate_uuid
from ..app import db


# -----------------------------------------------------------------
# tables concerning the place and georeferencement of our corpus
#
# contains
# ~~~~~~~~
# * `Place`: the main table on a `place`, that is, a spatial
#   unit at a point in time
# * `Address`: addresses connected to places
# -----------------------------------------------------------------


class Place(db.Model):
    """
    class describing a place, that is, a certain spatial unit
    that exists at a given moment (for example, the footprint of
    a building that existed between 1830 et 1850).
    if there is no footprint (a polygon, or a shape), a place must
    be defined at least by geographical coordinates.

    * `centroid` is stored as a JSON (GeoJSON geometry point)
    * `vector` is the shape of the place on a cartographic space. it
      is stored as a JSON (the structure is a GeoJSON geometry multipolygon)
    """
    __tablename__ = "place"

    id             : Mapped[int]                   = mapped_column(psql.INTEGER, nullable=False, primary_key=True)
    id_uuid        : Mapped[str]                   = mapped_column(Text, nullable=False)
    id_richelieu   : Mapped[str]                   = mapped_column(Text, nullable=False)
    date           : Mapped[intervals.IntInterval] = mapped_column(psql.INT4RANGE, nullable=False)
    centroid       : Mapped[t.Dict]                = mapped_column(psql.JSON, nullable=True)
    vector         : Mapped[t.Dict]                = mapped_column(psql.JSON, nullable=True)
    vector_source  : Mapped[str]                   = mapped_column(Text, nullable=False)
    crs_epsg       : Mapped[int]                   = mapped_column(psql.INTEGER, nullable=False)
    id_place_group : Mapped[int]                   = mapped_column(psql.INTEGER, ForeignKey("place_group.id"), nullable=True)

    place_group         : Mapped["PlaceGroup"]                 = relationship("PlaceGroup", back_populates="place")
    r_address_place     : Mapped[t.List["R_AddressPlace"]]     = relationship("R_AddressPlace", back_populates="place")
    r_iconography_place : Mapped[t.List["R_IconographyPlace"]] = relationship("R_IconographyPlace", back_populates="place")
    r_cartography_place : Mapped[t.List["R_CartographyPlace"]] = relationship("R_CartographyPlace", back_populates="place")

    @validates("id_uuid", include_backrefs=False)
    def validate_uuid(self, key, _uuid):
        return _validate_uuid(_uuid, self.__tablename__)

    def get_address(self):
        return [ r.address.serialize_lite()
                 for r in self.r_address_place ]

    def get_iconography(self):
        return [ r.iconography.serialize_lite()
                 for r in self.r_iconography_place ]

    def get_cartography(self):
        return [ r.cartography.serialize_lite()
                 for r in self.r_cartography_place ]

    def get_place_group(self) -> t.Dict:
        return self.place_group.serialize_lite() if self.place_group is not None else None

    def get_filename_index(self) -> t.List[str]:
        cartography_objs = [ r.cartography for r in self.r_cartography_place
                             if r.cartography.map_source == self.vector_source ]
        return [ f.serialize_lite()
                 for c in cartography_objs
                 for f in c.filename ]

    def get_address_index(self) -> t.List[t.Dict]:
        address_objs = [ r.address for r in self.r_address_place
                         if r.address.source == self.vector_source ]
        return [ a.serialize_lite()
                 for a in address_objs ]

    # def serialize_lite(self) -> t.Dict:
    #     return { "id_uuid"  : self.id_uuid,      # str
    #              "vector"   : self.vector,       # t.Dict
    #              "centroid" : self.centroid,     # t.Dict
    #     }

    def serialize_lite(self) -> t.Dict:
        """object representation of `Place` for the Place index page"""
        return { "id_uuid"  : self.id_uuid,               # str
                 "date"     : int4range2list(self.date),  # t.List[int]
                 "filename" : self.get_filename_index(),  # t.List[t.Dict]
                 "address"  : self.get_address_index(),   # t.List[t.Dict]
                 "vector"   : self.vector,                # t.Dict
                 "centroid" : self.centroid               # t.Dict
        }

    def serialize_full(self) -> t.Dict:
        return { "id_uuid"       : self.id_uuid,               # str
                 "id_richelieu"  : self.id_richelieu,          # str
                 "date"          : int4range2list(self.date),  # t.List[int]
                 "centroid"      : self.centroid,              # t.Dict
                 "vector"        : self.vector,                # t.Dict
                 "vector_source" : self.vector_source,         # str

                 "place_group"   : self.get_place_group(),     # t.List[t.Dict]
                 "address"       : self.get_address(),         # t.List[str]
                 "iconography"   : self.get_iconography(),     # t.List[t.Dict]
                 "cartography"   : self.get_iconography()      # t.List[t.Dict]
        }


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

    def serialize_full(self):
        return { "id_uuid": self.id_uuid,
                 "entry_name": self.entry_name,
                 "description": self.description,
                 "place": self.get_place() }


class Address(db.Model):
    """
    postal addresses connected to a place and to the bottins & annuaires.
    a postal address is defined temporally: just like places change with
    time, a postal address evolves with time.

    it is possible to see a diachronic evolution of addresses pointing to a
    single place by doing a `GROUP BY` query on the `PlaceGroup` table
    """
    __tablename__ = "address"

    id      : Mapped[int]                   = mapped_column(psql.INTEGER, nullable=False, primary_key=True)
    id_uuid : Mapped[str]                   = mapped_column(Text, nullable=False)
    address : Mapped[str]                   = mapped_column(Text, nullable=False)
    city    : Mapped[str]                   = mapped_column(Text, nullable=False)
    country : Mapped[str]                   = mapped_column(Text, nullable=False)
    source  : Mapped[str]                   = mapped_column(Text, nullable=False)
    date    : Mapped[intervals.IntInterval] = mapped_column(psql.INT4RANGE, nullable=False)

    r_address_place : Mapped[t.List["R_AddressPlace"]] = relationship("R_AddressPlace", back_populates="address")
    directory       : Mapped[t.List["Directory"]]      = relationship("Directory", back_populates="address")

    @validates("id_uuid", include_backrefs=False)
    def validate_uuid(self, key, _uuid):
        return _validate_uuid(_uuid, self.__tablename__)

    # def to_string(self):
    #     """
    #     string representation of an address
    #     """
    #     return f"{self.number} {self.street}, {self.city} ({self.date})"

    def get_place(self):
        return [ r.place.serialize_lite()
                 for r in self.r_address_place ]

    # PERFORMANCE WARNING: THIS **WILL** CAUSE SIGNIFICANT
    # OVERHEAD, ESPECIALLY WITH THE 4.000.000 ENTRIES.
    def get_directory(self):
        return [ d.serialize_lite()
                 for d in self.directory ]

    def serialize_lite(self):
        return { "id_uuid" : self.id_uuid,            # str
                 "address" : self.address,              # str
                 "city"    : self.city,                  # str
                 "country" : self.country,            # str
        }


    def serialize_full(self):
        return { "id_uuid" : self.id_uuid,            # str
                 "address" : self.address,              # str
                 "city"    : self.city,                  # str
                 "country" : self.country,            # str
                 "source"  : self.source,              # str
                 "date"    : int4range2list(self.date),  # t.List[int]

                 # "as_string": self.to_string(),    # str

                 "place": self.get_place(),          # t.List[t.Dict]
                 "directory": self.get_directory()   # t.List[t.Dict]
        }


from .data_sources import Cartography
from .relationships import R_CartographyPlace


