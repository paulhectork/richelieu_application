from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from sqlalchemy.dialects import postgresql as psql
from sqlalchemy import Text
import typing as t

from ..utils.strings import _validate_uuid
from ..app import db


# -----------------------------------------------------------------
# tables relative to data administration
#
# contains
# ~~~~~~~~
# * `Institution`: the institution granting access to a digitized
#   ressource
# * `Licence`: licences of the ressources we created and of the
#   digitized documents made available by other institutions
# * `AdminPerson`: researchers and members of the project
# -----------------------------------------------------------------


class Institution(db.Model):
    """
    the institutions that own and/or grant access to a digitized
    ressource (Iconography, Cartography, Bottins).
    """
    __tablename__ = "institution"

    id            : Mapped[int] = mapped_column(psql.INTEGER, nullable=False, primary_key=True, comment="identifiant interne")
    id_uuid       : Mapped[str] = mapped_column(Text, nullable=False, comment="identifiant unique")
    entry_name    : Mapped[str] = mapped_column(Text, nullable=False, comment="nom")
    description   : Mapped[str] = mapped_column(Text, nullable=True, comment="description")

    r_institution : Mapped[t.List["R_Institution"]] = relationship("R_Institution", back_populates="institution")

    @validates("id_uuid", include_backrefs=False)
    def validate_uuid(self, key, value):
        return _validate_uuid(value, self.__tablename__)

    @property
    def label(self) -> str:
        return self.entry_name

    def get_iconography(self):
        return [ r.iconography.serialize_lite()
                 for r in self.r_institution
                 if r.iconography is not None ]

    def get_cartography(self):
        return [ r.cartography.serialize_lite()
                 for r in self.r_institution
                 if r.cartography is not None ]

    def get_directory(self):
        return [ r.directory.serialize_lite()
                 for r in self.r_institution
                 if r.directory is not None ]

    def serialize_lite(self):
        return { "id_uuid"    : self.id_uuid,      # str
                 "entry_name" : self.entry_name }  # str

    def serialize_full(self):
        return { "id_uuid"     : self.id_uuid,            # str
                 "entry_name"  : self.entry_name,         # str
                 "description" : self.description,        # str
                 "iconography" : self.get_iconography(),  # t.Dict
                 "cartography" : self.get_cartography(),  # t.Dict
                 "directory"   : self.get_directory()     # t.Dict
        }



class Licence(db.Model):
    """
    licence under which a ressource is made available.
    this table is used to describe both:
    * the licence under which we make the data we produced available
    * the licences under which the digitized documents (image of paintings,
      maps...) are provided by other institutions
    """
    __tablename__ = "licence"

    id          : Mapped[int] = mapped_column(psql.INTEGER, nullable=False, primary_key=True, comment="identifiant interne")
    id_uuid     : Mapped[str] = mapped_column(Text, nullable=False, comment="identifiant unique")
    entry_name  : Mapped[str] = mapped_column(Text, nullable=False, comment="nom")
    description : Mapped[str] = mapped_column(Text, nullable=True, comment="description")

    filename    : Mapped[t.List["Filename"]]    = relationship("Filename", back_populates="licence")
    iconography : Mapped[t.List["Iconography"]] = relationship("Iconography", back_populates="licence")
    cartography : Mapped[t.List["Cartography"]] = relationship("Cartography", back_populates="licence")
    directory   : Mapped[t.List["Directory"]]   = relationship("Directory", back_populates="licence")

    @validates("id_uuid", include_backrefs=False)
    def validate_uuid(self, key, _uuid):
        return _validate_uuid(_uuid, self.__tablename__)

    @property
    def label(self) -> str:
        return self.entry_name

    def get_filename(self):
        return [ f.serialize_lite() for f in self.filename ]

    def get_iconography(self):
        return [ i.serialize_lite() for i in self.iconography ]

    def get_cartography(self):
        return [ c.serialize_lite() for c in self.cartography ]

    def serialize_lite(self):
        return { "id_uuid"    : self.id_uuid,      # str
                 "entry_name" : self.entry_name }  # str

    def serialize_full(self):
        return { "id_uuid"     : self.id_uuid,           # str
                 "entry_name"  : self.entry_name,        # str
                 "description" : self.description,       # str
                 "iconography" : self.get_iconography(), # t.Dict
                 "cartography" : self.get_cartography(), # t.Dict
                 "filename"    : self.get_filename()     # t.Dict
        }


class AdminPerson(db.Model):
    """
    members of the Richelieu. Histoire du quartier research project.
    this table allows us to attribute authors to the ressources we
    made available. keeping in line with open data objectives, each
    researcher is identified by a persistent identifier (ORCID...)
    """
    __tablename__ = "admin_person"

    id             : Mapped[int] = mapped_column(psql.INTEGER, nullable=False, primary_key=True, comment="identifiant interne")
    id_uuid        : Mapped[str] = mapped_column(Text, nullable=False, comment="identifiant unique")
    first_name     : Mapped[str] = mapped_column(Text, nullable=False, comment="nom")
    last_name      : Mapped[str] = mapped_column(Text, nullable=False, comment="prénom")
    id_persistent  : Mapped[int] = mapped_column(Text, nullable=True, comment="identifiant persitent")

    r_admin_person : Mapped[t.List["R_AdminPerson"]] = relationship("R_AdminPerson", back_populates="admin_person")

    @validates("id_uuid", include_backrefs=False)
    def validate_uuid(self, key, _uuid):
        return _validate_uuid(_uuid, self.__tablename__)

    @property
    def label(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def get_r_admin_person_iconography(self):
        return [ r.iconography.serialize_lite()
                 for r in self.r_admin_person
                 if r.iconography is not None ]

    def get_r_admin_person_cartography(self):
        return [ r.cartography.serialize_lite()
                 for r in self.r_admin_person
                 if r.cartography is not None ]

    def get_r_admin_person_directory(self):
        return [ r.directory.serialize_lite()
                 for r in self.r_admin_person
                 if r.directory is not None ]

    def serialize_lite(self):
        return { "id_uuid"    : self.id_uuid,      # str
                 "first_name" : self.first_name,   # str
                 "last_name"  : self.last_name }   # str

    def serialize_full(self):
        return { "id_uuid"       : self.id_uuid,                          # str
                 "first_name"    : self.first_name,                       # str
                 "last_name"     : self.last_name,                        # str
                 "id_persistent" : self.id_persistent,                    # str
                 "cartography"   : self.get_r_admin_person_cartography(), # t.List[t.Dict]
                 "iconography"   : self.get_r_admin_person_iconography(), # t.List[t.Dict]
                 "directory"     : self.get_r_admin_person_directory(),   # t.List[t.Dict]
        }


