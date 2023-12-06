from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from sqlalchemy.dialects import postgresql
from sqlalchemy import ForeignKey, Text, Boolean

from ..utils.strings import validate_uuid
from ..app import db


# ----------------------------------------------------------------------
# relationship tables
#
# contains
# ~~~~~~~~
# * `R_IconographyActor`: relation between Iconography and Actor
# * `R_IconographyLocation`: relationship between `Iconography`
#   and `Location
# * `R_CartographyLocation`: relationship between `Cartography`
#   and `Location`
# * `R_AddressLocation`: relationship between `Address`
#   and `Location`
# * `R_IconographyNamedEntity`: relationship between `Iconography`
#   and `NamedEntity`
# * `R_IconographyTheme`: relationship between `Iconography`
#   and `Theme`
#
# docs
# ~~~~
# the relationship pattern used is `Association Object`,
# see: https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html
#
# ----------------------------------------------------------------------


class R_IconographyActor(db.Model):
    """
    relationship between the tables `iconography`, `actor` and `role`
    """
    __tablename__: str = "r_iconography_actor"
    
    id             : Mapped[int]  = mapped_column(postgresql.INTEGER, nullable=False, primary_key=True)
    uuid           : Mapped[str]  = mapped_column(Text, nullable=False)
    id_iconography : Mapped[int]  = mapped_column(postgresql.INTEGER, ForeignKey("iconography.id"), nullable=False)
    id_actor       : Mapped[int]  = mapped_column(postgresql.INTEGER, ForeignKey("actor.id"), nullable=False)
    role           : Mapped[str]  = mapped_column(Text, nullable=False)
    ismain         : Mapped[bool] = mapped_column(Boolean, nullable=False)
    
    iconography : Mapped["Iconography"] = relationship("Iconography"
                                                       , back_populates="r_iconography_actor")
    actor       : Mapped["Actor"]       = relationship("Actor"
                                                       , back_populates="r_iconography_actor")
    
    @validates("uuid", include_backrefs=False)
    def validate_uuid(self, key, _uuid):
        return validate_uuid(_uuid, self.__tablename__)



    
class R_IconographyLocation(db.Model):
    """
    relationship between tables `Iconography` and `Location`
    """
    __tablename__ = "r_iconography_location"
    
    id             : Mapped[int] = mapped_column(postgresql.INTEGER, nullable=False, primary_key=True)
    uuid           : Mapped[str] = mapped_column(Text, nullable=False)
    id_iconography : Mapped[int] = mapped_column(postgresql.INTEGER, ForeignKey("iconography.id"), nullable=False)
    id_location    : Mapped[int] = mapped_column(postgresql.INTEGER, ForeignKey("location.id"), nullable=False)

    iconography : Mapped["Iconography"] = relationship("Iconography"
                                                       , back_populates="r_iconography_location")
    location    : Mapped["Location"]    = relationship("Location"
                                                       , back_populates="r_iconography_location")

    @validates("uuid", include_backrefs=False)
    def validate_uuid(self, key, _uuid):
        return validate_uuid(_uuid, self.__tablename__)


class R_CartographyLocation(db.Model):
    """
    relationship between tables `Cartography` and `Location`
    """
    __tablename__ = "r_cartography_location"
    
    id             : Mapped[int] = mapped_column(postgresql.INTEGER, nullable=False, primary_key=True)
    uuid           : Mapped[str] = mapped_column(Text, nullable=False)
    id_cartography : Mapped[int] = mapped_column(postgresql.INTEGER, ForeignKey("cartography.id"), nullable=False)
    id_location    : Mapped[int] = mapped_column(postgresql.INTEGER, ForeignKey("location.id"), nullable=False)

    cartography : Mapped["Cartography"] = relationship("Cartography"
                                                       , back_populates="r_cartography_location")
    location    : Mapped["Location"]    = relationship("Location"
                                                       , back_populates="r_cartography_location")

    @validates("uuid", include_backrefs=False)
    def validate_uuid(self, key, _uuid):
        return validate_uuid(_uuid, self.__tablename__)


class R_AddressLocation(db.Model):
    """
    relationship between the tables `Address` and `Location`
    """
    __tablename__ = "r_address_location"
    
    id          : Mapped[int] = mapped_column(postgresql.INTEGER, nullable=False, primary_key=True)
    uuid        : Mapped[str] = mapped_column(Text, nullable=False)
    id_address  : Mapped[int] = mapped_column(postgresql.INTEGER, ForeignKey("address.id"), nullable=False)
    id_location : Mapped[int] = mapped_column(postgresql.INTEGER, ForeignKey("location.id"), nullable=False)

    address  : Mapped["Address"]  = relationship("Address"
                                                 , back_populates="r_address_location")
    location : Mapped["Location"] = relationship("Location"
                                                 , back_populates="r_address_location")

    @validates("uuid", include_backrefs=False)
    def validate_uuid(self, key, _uuid):
        return validate_uuid(_uuid, self.__tablename__)


class R_IconographyNamedEntity(db.Model):
    """
    relationship between `iconography` and `named_entity` tables
    """
    __tablename__: str = "r_iconography_named_entity"
    
    id              : Mapped[int] = mapped_column(postgresql.INTEGER, nullable=False, primary_key=True)
    uuid            : Mapped[str] = mapped_column(Text, nullable=False)
    id_iconography  : Mapped[int] = mapped_column(postgresql.INTEGER, ForeignKey("iconography.id"), nullable=False)
    id_named_entity : Mapped[int] = mapped_column(postgresql.INTEGER, ForeignKey("named_entity.id"), nullable=False)
    
    iconography  : Mapped["Iconography"] = relationship("Iconography"
                                                        , back_populates="r_iconography_named_entity")
    named_entity : Mapped["NamedEntity"] = relationship("NamedEntity"
                                                        , back_populates="r_iconography_named_entity")
    
    @validates("uuid", include_backrefs=False)
    def validate_uuid(self, key, _uuid):
        return validate_uuid(_uuid, self.__tablename__)

   
class R_IconographyTheme(db.Model):
    """
    relationship between `iconography` and `theme` tables
    """
    __tablename__: str = "r_iconography_theme"
    
    id             : Mapped[int] = mapped_column(postgresql.INTEGER, nullable=False, primary_key=True)
    uuid           : Mapped[str] = mapped_column(Text, nullable=False)
    id_iconography : Mapped[int] = mapped_column(postgresql.INTEGER, ForeignKey("iconography.id"), nullable=False)
    id_theme       : Mapped[int] = mapped_column(postgresql.INTEGER, ForeignKey("theme.id"), nullable=False)
    
    iconography : Mapped["Iconography"] = relationship("Iconography"
                                                       , back_populates="r_iconography_theme")
    theme       : Mapped["Theme"] = relationship("Theme"
                                                 , back_populates="r_iconography_theme")
    
    @validates("uuid", include_backrefs=False)
    def validate_uuid(self, key, _uuid):
        return validate_uuid(_uuid, self.__tablename__)


class R_AdminPerson(db.Model):
    """
    relationship between `admin_person` and the
    `iconography`, `cartography` and `directory` tables
    
    see: https://stackoverflow.com/questions/57040784/sqlalchemy-foreign-key-to-multiple-tables
    """
    __tablename__: str = "r_admin_person"

    id              : Mapped[int] = mapped_column(postgresql.INTEGER, nullable=False, primary_key=True)
    uuid            : Mapped[str] = mapped_column(Text, nullable=False)
    id_iconography  : Mapped[int] = mapped_column(postgresql.INTEGER, ForeignKey("iconography.id"), nullable=True)
    id_cartography  : Mapped[int] = mapped_column(postgresql.INTEGER, ForeignKey("cartography.id"), nullable=True)
    id_directory    : Mapped[int] = mapped_column(postgresql.INTEGER, ForeignKey("directory.id"), nullable=True)
    id_admin_person : Mapped[int] = mapped_column(postgresql.INTEGER, ForeignKey("admin_person.id"), nullable=False)
    
    iconography  : Mapped["Iconography"] = relationship("Iconography"
                                                        , back_populates="r_admin_person")
    cartography  : Mapped["Cartography"] = relationship("Cartography"
                                                        , back_populates="r_admin_person")
    directory    : Mapped["Directory"]   = relationship("Directory"
                                                        , back_populates="r_admin_person")
    admin_person : Mapped["AdminPerson"] = relationship("AdminPerson"
                                                        , back_populates="r_admin_person")
    
    @validates("uuid", include_backrefs=False)
    def validate_uuid(self, key, _uuid):
        return validate_uuid(_uuid, self.__tablename__)
    

class R_Institution(db.Model):
    """
    relationship between `institution`, `directory`,
    `cartography`, `filename` and `iconography`
    """
    __tablename__: str = "r_institution"

    id             : Mapped[int] = mapped_column(postgresql.INTEGER, nullable=False, primary_key=True)
    uuid           : Mapped[str] = mapped_column(Text, nullable=False)
    id_iconography : Mapped[int] = mapped_column(postgresql.INTEGER, ForeignKey("iconography.id"), nullable=True)
    id_cartography : Mapped[int] = mapped_column(postgresql.INTEGER, ForeignKey("cartography.id"), nullable=True)
    id_directory   : Mapped[int] = mapped_column(postgresql.INTEGER, ForeignKey("directory.id"), nullable=True)
    id_institution : Mapped[int] = mapped_column(postgresql.INTEGER, ForeignKey("institution.id"), nullable=False)

    iconography : Mapped["Iconography"] = relationship("Iconography"
                                                       , back_populates="r_institution")
    cartography : Mapped["Cartography"] = relationship("Cartography"
                                                       , back_populates="r_institution")
    directory   : Mapped["Directory"]   = relationship("Directory"
                                                       , back_populates="r_institution")
    institution : Mapped["AdminPerson"] = relationship("Institution"
                                                       , back_populates="r_institution")
    
    @validates("uuid", include_backrefs=False)
    def validate_uuid(self, key, _uuid):
        return validate_uuid(_uuid, self.__tablename__)
    



