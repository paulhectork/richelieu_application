from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from sqlalchemy.dialects import postgresql
from sqlalchemy import Text
from typing import List

from ..utils.strings import validate_uuid
from ..app import db


# -----------------------------------------------------------------
# tables relative to data administration
#
# contains
# ~~~~~~~~
# * `Institution`: the institution granting access to a digitized
#   ressource
# * `License`: licenses of the ressources we created and of the
#   digitized documents made available by other institutions
# * `AdminPerson`: researchers and members of the project
# -----------------------------------------------------------------


class Institution(db.Model):
    """
    the institutions that own and/or grant access to a digitized 
    ressource (Iconography, Cartography, Bottins).
    """
    __tablename__ = "institution"
    
    id             : Mapped[int] = mapped_column(postgresql.INTEGER, nullable=False, primary_key=True)
    uuid           : Mapped[str] = mapped_column(Text, nullable=False)
    name           : Mapped[str] = mapped_column(Text, nullable=False)
    description    : Mapped[str] = mapped_column(Text, nullable=True)
    
    r_institution : Mapped[List["R_Institution"]] = relationship("R_Institution"
                                                                 , back_populates="institution")

    @validates("uuid", include_backrefs=False)
    def validate_uuid(self, key, value):
        return validate_uuid(value, self.__tablename__)
    
    def get_iconography(self):
        return [ r.iconography.serialize_lite() 
                 for r in self.r_institution ]
    
    def get_cartography(self):
        return [ r.cartography.serialize_lite() 
                 for r in self.r_institution ]
    
    def get_directory(self):
        return [ r.directory.serialize_lite() 
                 for r in self.r_institution ]
    
    def serialize_lite(self):
        return { "uuid": self.uuid,   # str
                 "name": self.name }  # str
    
    def serialize_full(self):
        return { "uuid"        : self.uuid,               # str
                 "name"        : self.name,               # str
                 "description" : self.description,        # str
                 "iconography" : self.get_iconography(),  # t.Dict
                 "cartography" : self.get_cartography(),  # t.Dict
                 "dicterory"   : self.get_directory()     # t.Dict
        }
        
    
class License(db.Model):
    """
    license under which a ressource is made available.
    this table is used to describe both:
    * the license under which we make the data we produced available
    * the licenses under which the digitized documents (image of paintings,
      maps...) are provided by other institutions
    """
    __tablename__ = "license"
    
    id          : Mapped[int] = mapped_column(postgresql.INTEGER, nullable=False, primary_key=True)
    uuid        : Mapped[str] = mapped_column(Text, nullable=False)
    name        : Mapped[str] = mapped_column(Text, nullable=False)
    description : Mapped[str] = mapped_column(Text, nullable=True)
    
    file        : Mapped[List["File"]]        = relationship("File", back_populates="license")
    iconography : Mapped[List["Iconography"]] = relationship("Iconography", back_populates="license")
    cartography : Mapped[List["Cartography"]] = relationship("Cartography", back_populates="license")
    directory   : Mapped[List["Directory"]]   = relationship("Directory", back_populates="license")

    @validates("uuid", include_backrefs=False)
    def validate_uuid(self, key, _uuid):
        return validate_uuid(_uuid, self.__tablename__)
    
    def serialize_light(self):
        return { "uuid" : self.uuid,   # str
                 "name" : self.name }  # str
    
    def serialize_full(self):
        return { "uuid"        : self.uuid,        # str
                 "name"        : self.name,        # str
                 "description" : self.description  # str
        }


class AdminPerson(db.Model):
    """
    members of the Richelieu. Histoire du quartier research project.
    this table allows us to attribute authors to the ressources we 
    made available. keeping in line with open data objectives, each
    researcher is identified by a persistent identifier (ORCID...)
    """
    __tablename__ = "admin_person"
    
    id             : Mapped[int] = mapped_column(postgresql.INTEGER, nullable=False, primary_key=True)
    uuid           : Mapped[str] = mapped_column(Text, nullable=False)
    first_name     : Mapped[str] = mapped_column(Text, nullable=False)
    last_name      : Mapped[str] = mapped_column(Text, nullable=False)
    id_persistent  : Mapped[int] = mapped_column(Text, nullable=False)
    
    r_admin_person : Mapped[List["R_AdminPerson"]] = relationship("R_AdminPerson"
                                                                  , back_populates="admin_person")

    @validates("uuid", include_backrefs=False)
    def validate_uuid(self, key, _uuid):
        return validate_uuid(_uuid, self.__tablename__)
    
    def serialize_lite(self):
        return { "uuid"       : self.uuid,
                 "first_name" : self.first_name,
                 "last_name"  : self.last_name }

