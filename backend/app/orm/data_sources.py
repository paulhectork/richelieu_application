from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from sqlalchemy.dialects import postgresql
from sqlalchemy import ForeignKey, Text, Float, Boolean
from typing import List, Dict
import intervals

from ..utils.strings import validate_uuid
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
# * `File`: external files, especially images of iconographic 
#   and cartographic ressources
# * `Directory`: the Bottins et Annuaires.
# -----------------------------------------------------------------


class Iconography(db.Model):
    """
    main class for the iconography, describing image and documents
    presented on the website.
    """
    __tablename__: str = "iconography"
    
    id                   : Mapped[int]       = mapped_column(postgresql.INTEGER, nullable=False, primary_key=True)
    uuid                 : Mapped[str]       = mapped_column(Text, nullable=False)
    # url_manifest         : Mapped[str]       = mapped_column(Text, nullable=False)
    # url_source           : Mapped[str]       = mapped_column(Text, nullable=False)
    url_manifest         : Mapped[str]       = mapped_column(Text, nullable=True)
    url_source           : Mapped[str]       = mapped_column(Text, nullable=True)
    # date_source          : Mapped[str]       = mapped_column(Text, nullable=False)
    date_source          : Mapped[str]       = mapped_column(Text, nullable=True)
    date_corr            : Mapped[str]       = mapped_column(Text, nullable=True)
    date                 : Mapped[List[int]] = mapped_column(postgresql.INT4RANGE, nullable=True)
    # date                 : Mapped[List[int]] = mapped_column(postgresql.INT4RANGE, nullable=False)
    technique            : Mapped[str]       = mapped_column(Text, nullable=True)
    description          : Mapped[str]       = mapped_column(Text, nullable=True)
    inscription          : Mapped[str]       = mapped_column(Text, nullable=True)
    corpus               : Mapped[str]       = mapped_column(Text, nullable=True)
    inventory_number     : Mapped[str]       = mapped_column(Text, nullable=True)
    # produced_richelieu   : Mapped[bool]      = mapped_column(Boolean, nullable=False)
    produced_richelieu   : Mapped[bool]      = mapped_column(Boolean, nullable=True)
    # represents_richelieu : Mapped[bool]      = mapped_column(Boolean, nullable=False)    
    represents_richelieu : Mapped[bool]      = mapped_column(Boolean, nullable=True)    
    id_license           : Mapped[int]       = mapped_column(postgresql.INTEGER, ForeignKey("license.id"), nullable=False)
    
    title                      : Mapped[List["Title"]]                    = relationship("Title"
                                                                                         , back_populates="iconography")
    annotation                 : Mapped[List["Annotation"]]               = relationship("Annotation"
                                                                                         , back_populates="iconography")
    file                       : Mapped[List["File"]]                     = relationship("File"
                                                                                         , back_populates="iconography")
    license                    : Mapped["License"]                        = relationship("License"
                                                                                         , back_populates="iconography")
    r_iconography_theme        : Mapped[List["R_IconographyTheme"]]       = relationship("R_IconographyTheme"
                                                                                         , back_populates="iconography")
    r_iconography_actor        : Mapped[List["R_IconographyActor"]]       = relationship("R_IconographyActor"
                                                                                         , back_populates="iconography")
    r_iconography_location     : Mapped[List["R_IconographyLocation"]]    = relationship("R_IconographyLocation"
                                                                                         , back_populates="iconography")
    r_iconography_named_entity : Mapped[List["R_IconographyNamedEntity"]] = relationship("R_IconographyNamedEntity"
                                                                                         , back_populates="iconography")
    r_admin_person             : Mapped[List["R_AdminPerson"]]            = relationship("R_AdminPerson"
                                                                                         , back_populates="iconography")
    r_institution              : Mapped[List["R_Institution"]]              = relationship("R_Institution"
                                                                                           , back_populates="iconography")
    
    @validates("uuid", include_backrefs=False)
    def validate_uuid(self, key, _uuid):
        return validate_uuid(_uuid, self.__tablename__)
        

class Cartography(db.Model):
    """
    class describing our cartographic ressources
    """
    __tablename__: str = "cartography"
    
    id                : Mapped[int]                   = mapped_column(postgresql.INTEGER, nullable=False, primary_key=True)
    uuid              : Mapped[str]                   = mapped_column(Text, nullable=False)
    # url_source        : Mapped[str]                   = mapped_column(Text, nullable=False)
    url_source        : Mapped[str]                   = mapped_column(Text, nullable=True)
    # url_image         : Mapped[str]                   = mapped_column(Text, nullable=False)
    url_image         : Mapped[str]                   = mapped_column(Text, nullable=True)
    description       : Mapped[str]                   = mapped_column(Text, nullable=True)
    date_source       : Mapped[str]                   = mapped_column(Text, nullable=True)
    inventory_number  : Mapped[str]                   = mapped_column(Text, nullable=True)
    isfullstreet      : Mapped[bool]                  = mapped_column(Boolean, nullable=False)
    # date              : Mapped[intervals.IntInterval] = mapped_column(postgresql.INT4RANGE)
    date              : Mapped[intervals.IntInterval] = mapped_column(postgresql.INT4RANGE, nullable=True)
    vector            : Mapped[Dict]                  = mapped_column(postgresql.JSON)  # MAYBE DELETE ?
    id_license        : Mapped[int]                   = mapped_column(postgresql.INTEGER, ForeignKey("license.id"), nullable=False)
    
    r_cartography_location : Mapped[List["R_CartographyLocation"]] = relationship("R_CartographyLocation"
                                                                                 , back_populates="cartography")
    r_admin_person         : Mapped[List["R_AdminPerson"]]         = relationship("R_AdminPerson"
                                                                                 , back_populates="cartography")
    r_institution          : Mapped[List["R_Institution"]]         = relationship("R_Institution"
                                                                                 , back_populates="cartography")
    file                  : Mapped[List["File"]]                   = relationship("File"
                                                                                 , back_populates="cartography")
    license                : Mapped["License"]                     = relationship("License"
                                                                                 , back_populates="cartography")
    
    @validates("uuid", include_backrefs=False)
    def validate_uuid(self, key, _uuid):
        return validate_uuid(_uuid, self.__tablename__)


class Directory(db.Model):
    """
    the third data source: directory (Bottins et Annuaires),
    mapping persons to an address and to the activity they
    practiced there. the Bottins were extracted from Gallica.
    """
    __tablename__ = "directory"
    
    id           : Mapped[int]       = mapped_column(postgresql.INTEGER, nullable=False, primary_key=True)
    uuid         : Mapped[str]       = mapped_column(Text, nullable=False)
    gallica_ark  : Mapped[str]       = mapped_column(Text, nullable=False)
    gallica_page : Mapped[str]       = mapped_column(Text, nullable=False)  # the page on the directory
    gallica_row  : Mapped[str]       = mapped_column(Text, nullable=False)  # the page row in the directory
    name         : Mapped[str]       = mapped_column(Text, nullable=False)
    occupation   : Mapped[str]       = mapped_column(Text, nullable=False)
    date         : Mapped[str]       = mapped_column(Text, nullable=False)
    tags         : Mapped[List[str]] = mapped_column(postgresql.ARRAY(Text, dimensions=1), nullable=True)
    id_address   : Mapped[int]       = mapped_column(postgresql.INTEGER, ForeignKey("address.id"), nullable=False)
    id_license   : Mapped[int]       = mapped_column(postgresql.INTEGER, ForeignKey("license.id"), nullable=False)
    
    address        : Mapped["Address"]             = relationship("Address", back_populates="directory")
    license        : Mapped["License"]             = relationship("License", back_populates="directory")
    r_admin_person : Mapped[List["R_AdminPerson"]] = relationship("R_AdminPerson", back_populates="directory")
    r_institution  : Mapped[List["R_Institution"]] = relationship("R_Institution", back_populates="directory")

    @validates("uuid", include_backrefs=False)
    def validate_uuid(self, key, _uuid):
        return validate_uuid(_uuid, self.__tablename__)
        

class File(db.Model):
    """
    class containing data on image and other external files (reproduction 
    of iconographic ressources or cartographic ressources.
    """
    __tablename__ = "file"
    
    id             : Mapped[int]                      = mapped_column(postgresql.INTEGER, nullable=False, primary_key=True)
    uuid           : Mapped[str]                      = mapped_column(Text, nullable=False)
    url            : Mapped[str]                      = mapped_column(Text, nullable=False)
    latlngbounds   : Mapped[List[List[float]] | None] = mapped_column(postgresql.ARRAY(Float, dimensions=2), nullable=True)  # [ [<float>,<float>], [<float>,<float>] ]
    id_license     : Mapped[int]                      = mapped_column(postgresql.INTEGER, ForeignKey("license.id"), nullable=True)
    id_iconography : Mapped[int]                      = mapped_column(postgresql.INTEGER, ForeignKey("iconography.id"), nullable=True)
    id_cartography : Mapped[int]                      = mapped_column(postgresql.INTEGER, ForeignKey("cartography.id"), nullable=True)

    license     : Mapped["License"]     = relationship("License", back_populates="file")
    iconography : Mapped["Iconography"] = relationship("Iconography", back_populates="file")
    cartography : Mapped["Cartography"] = relationship("Cartography", back_populates="file")
    
    @validates("id", include_backrefs=False)
    def validate_uuid(self, key, _uuid):
        return validate_uuid(_uuid, self.__tablename__)


