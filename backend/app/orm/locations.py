from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from sqlalchemy import ForeignKey, Integer, Text
from sqlalchemy.dialects import postgresql 
from typing import List, Dict
import intervals

from ..utils.strings import validate_uuid
from ..app import db 


# -----------------------------------------------------------------
# tables concerning the location and georeferencement of our corpus
#
# contains
# ~~~~~~~~
# * `Location`: the main table on a `place`, that is, a spatial
#   unit at a point in time
# * `Address`: addresses connected to locations
# -----------------------------------------------------------------


class Location(db.Model):
    """
    class describing a location, that is, a certain spatial unit 
    that exists at a given moment (for example, the footprint of
    a building that existed between 1830 et 1850).
    if there is no footprint (a polygon, or a shape), a place must 
    be defined at least by geographical coordinates.
    
    * `coordinates` is stored as an array of 2 floats [x, y]: SQLAlchemy 
      doesn't support Postgre's geometry types.
    * `shape` is the shape of the location on a cartographic space. it
      is stored as 
    """
    __tablename__ = "location"
    
    id                : Mapped[int]                   = mapped_column(postgresql.INTEGER, nullable=False, primary_key=True)
    uuid              : Mapped[str]                   = mapped_column(Text, nullable=False)
    # centroid          : Mapped[List[float]]           = mapped_column(postgresql.ARRAY(Integer, dimensions=1), nullable=False)
    centroid          : Mapped[List[float]]           = mapped_column(postgresql.ARRAY(Integer, dimensions=1), nullable=True)
    # vector            : Mapped[Dict]                  = mapped_column(postgresql.JSON, nullable=False)
    vector            : Mapped[Dict]                  = mapped_column(postgresql.JSON, nullable=True)
    date              : Mapped[intervals.IntInterval] = mapped_column(postgresql.INT4RANGE, nullable=False)
    id_location_group : Mapped[int]                   = mapped_column(postgresql.INTEGER, ForeignKey("location_group.id"), nullable=True)
    
    location_group         : Mapped["LocationGroup"]               = relationship("LocationGroup"
                                                                                 , back_populates="location")
    r_address_location     : Mapped[List["R_AddressLocation"]]     = relationship("R_AddressLocation"
                                                                                 , back_populates="location")
    r_iconography_location : Mapped[List["R_IconographyLocation"]] = relationship("R_IconographyLocation"
                                                                                 , back_populates="location")
    r_cartography_location : Mapped[List["R_CartographyLocation"]] = relationship("R_CartographyLocation"
                                                                                 , back_populates="location")
    
    @validates("uuid", include_backrefs=False)
    def validate_uuid(self, key, _uuid):
        return validate_uuid(_uuid, self.__tablename__)


class Address(db.Model):
    """
    postal addresses connected to a location and to the bottins & annuaires.
    a postal address is defined temporally: just like locations change with
    time, a postal address evolves with time. 
    
    it is possible to see a diachronic evolution of addresses pointing to a 
    single location by doing a `GROUP BY` query on the `LocationGroup` table
    """
    __tablename__ = "address"
    
    id      : Mapped[int]                   = mapped_column(postgresql.INTEGER, nullable=False, primary_key=True)
    uuid    : Mapped[str]                   = mapped_column(Text, nullable=False)
    number  : Mapped[str]                   = mapped_column(Text, nullable=True)
    street  : Mapped[str]                   = mapped_column(Text, nullable=False)
    city    : Mapped[str]                   = mapped_column(Text, nullable=False)
    country : Mapped[str]                   = mapped_column(Text, nullable=False)
    source  : Mapped[str]                   = mapped_column(Text, nullable=False)
    date    : Mapped[intervals.IntInterval] = mapped_column(postgresql.INT4RANGE, nullable=False)
    
    r_address_location : Mapped[List["R_AddressLocation"]] = relationship("R_AddressLocation"
                                                                         , back_populates="address")
    directory          : Mapped[List["Directory"]]         = relationship("Directory"
                                                                         , back_populates="address")

    @validates("uuid", include_backrefs=False)
    def validate_uuid(self, key, _uuid):
        return validate_uuid(_uuid, self.__tablename__)
    
    def to_string(self):
        """
        string representation of an address
        """
        return f"{self.number} {self.street}, {self.city} ({self.date})"
