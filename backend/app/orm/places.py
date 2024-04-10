from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from sqlalchemy.dialects import postgresql as psql
from sqlalchemy import ForeignKey, Text
import typing as t
import intervals

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
    number  : Mapped[str]                   = mapped_column(Text, nullable=True)
    street  : Mapped[str]                   = mapped_column(Text, nullable=False)
    city    : Mapped[str]                   = mapped_column(Text, nullable=False)
    country : Mapped[str]                   = mapped_column(Text, nullable=False)
    source  : Mapped[str]                   = mapped_column(Text, nullable=False)
    date    : Mapped[intervals.IntInterval] = mapped_column(psql.INT4RANGE, nullable=False)

    r_address_place : Mapped[t.List["R_AddressPlace"]] = relationship("R_AddressPlace", back_populates="address")
    directory       : Mapped[t.List["Directory"]]      = relationship("Directory", back_populates="address")

    @validates("id_uuid", include_backrefs=False)
    def validate_uuid(self, key, _uuid):
        return _validate_uuid(_uuid, self.__tablename__)

    def to_string(self):
        """
        string representation of an address
        """
        return f"{self.number} {self.street}, {self.city} ({self.date})"



