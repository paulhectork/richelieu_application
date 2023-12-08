from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from sqlalchemy.dialects import postgresql
from sqlalchemy import ForeignKey, Text, Float, Boolean
import typing as t
import intervals

from ..utils.strings import validate_uuid, int4range2list
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
    date                 : Mapped[t.List[int]] = mapped_column(postgresql.INT4RANGE, nullable=True)
    # date                 : Mapped[t.List[int]] = mapped_column(postgresql.INT4RANGE, nullable=False)
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
    
    title                      : Mapped[t.List["Title"]]                    = relationship("Title"
                                                                                         , back_populates="iconography")
    annotation                 : Mapped[t.List["Annotation"]]               = relationship("Annotation"
                                                                                         , back_populates="iconography")
    file                       : Mapped[t.List["File"]]                     = relationship("File"
                                                                                         , back_populates="iconography")
    license                    : Mapped["License"]                        = relationship("License"
                                                                                         , back_populates="iconography")
    r_iconography_theme        : Mapped[t.List["R_IconographyTheme"]]       = relationship("R_IconographyTheme"
                                                                                         , back_populates="iconography")
    r_iconography_actor        : Mapped[t.List["R_IconographyActor"]]       = relationship("R_IconographyActor"
                                                                                         , back_populates="iconography")
    r_iconography_location     : Mapped[t.List["R_IconographyLocation"]]    = relationship("R_IconographyLocation"
                                                                                         , back_populates="iconography")
    r_iconography_named_entity : Mapped[t.List["R_IconographyNamedEntity"]] = relationship("R_IconographyNamedEntity"
                                                                                         , back_populates="iconography")
    r_admin_person             : Mapped[t.List["R_AdminPerson"]]            = relationship("R_AdminPerson"
                                                                                         , back_populates="iconography")
    r_institution              : Mapped[t.List["R_Institution"]]              = relationship("R_Institution"
                                                                                           , back_populates="iconography")
    
    @validates("uuid", include_backrefs=False)
    def validate_uuid(self, key, _uuid):
        return validate_uuid(_uuid, self.__tablename__)
    
    def get_author(self) -> t.List[t.Dict]:
        """
        return a t.list of authors, with the main author first
        """
        l = [ [r.actor.serialize_lite(), r.ismain ]
              for r in self.r_iconography_actor
              if r.role == "author" ]
        print(l)
        l = [ a[0] for a in sorted(l, key=lambda x: x[1]) ]  # reorder + remove the `ismain` flag. the first item is the main author
        return l
    
    def get_title(self) -> t.List[str]:
        """
        get the title(s) for a ressource and return them as a list of strings.
        """
        l = [ [t.name, t.ismain] for t in self.title ]
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

    def serialize_lite(self) -> t.Dict:
        return { "uuid"         : self.uuid,                  # str
                 "url_manifest" : self.url_manifest,          # str
                 "date"         : int4range2list(self.date),  # t.List[int]
                 "authors"      : self.get_author(),          # t.List[str]
                 "title"        : self.get_title()            # str ; 1st title
        }
    
    def serialize_full(self) -> t.Dict:
        return { "uuid"                 : self.uuid,                         # str
                 "url_manifest"         : self.url_manifest,                 # str
                 "url_source"           : self.source,                       # str
                 "date"                 : int4range2list(self.date),         # t.List[int]
                 "date_source"          : int4range2list(self.date_source),  # t.List[int]
                 "technique"            : self.technique,                    # str
                 "corpus"               : self.corpus,                       # str
                 "inventory_number"     : self.inventory_number,             # str
                 "produced_richelieu"   : self.produced_richelieu,           # bool
                 "represents_richelieu" : self.represents_richelieu,         # bool
                 
                 "author"               : self.get_author(),                 # t.List[t.Dict]
                 "title"                : self.get_title(),                  # str ; 1st title
                 "license"              : self.license.serialize_light(),    # t.Dict
                 "publisher"            : self.get_publisher(),              # t.List[t.Dict]
                 "theme"                : self.get_theme(),                  # t.List[t.Dict]
                 "named_entity"         : self.get_named_entity(),           # t.List[t.Dict]
                 "admin_person"         : self.get_admin_person()            # t.List[t.Dict]
        }
        

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
    vector            : Mapped[t.Dict]                  = mapped_column(postgresql.JSON)  # MAYBE DELETE ?
    id_license        : Mapped[int]                   = mapped_column(postgresql.INTEGER, ForeignKey("license.id"), nullable=False)
    
    r_cartography_location : Mapped[t.List["R_CartographyLocation"]] = relationship("R_CartographyLocation"
                                                                                 , back_populates="cartography")
    r_admin_person         : Mapped[t.List["R_AdminPerson"]]         = relationship("R_AdminPerson"
                                                                                 , back_populates="cartography")
    r_institution          : Mapped[t.List["R_Institution"]]         = relationship("R_Institution"
                                                                                 , back_populates="cartography")
    file                   : Mapped[t.List["File"]]                  = relationship("File"
                                                                                 , back_populates="cartography")
    license                : Mapped["License"]                       = relationship("License"
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
    tags         : Mapped[t.List[str]] = mapped_column(postgresql.ARRAY(Text, dimensions=1), nullable=True)
    id_address   : Mapped[int]       = mapped_column(postgresql.INTEGER, ForeignKey("address.id"), nullable=False)
    id_license   : Mapped[int]       = mapped_column(postgresql.INTEGER, ForeignKey("license.id"), nullable=False)
    
    address        : Mapped["Address"]             = relationship("Address", back_populates="directory")
    license        : Mapped["License"]             = relationship("License", back_populates="directory")
    r_admin_person : Mapped[t.List["R_AdminPerson"]] = relationship("R_AdminPerson", back_populates="directory")
    r_institution  : Mapped[t.List["R_Institution"]] = relationship("R_Institution", back_populates="directory")

    @validates("uuid", include_backrefs=False)
    def validate_uuid(self, key, _uuid):
        return validate_uuid(_uuid, self.__tablename__)
    
    def serialize_lite(self) -> t.Dict:
        return { "uuid"       : self.uuid,
                 "name"       : self.name,
                 "occupation" : self.occupation,
                 "date"       : self.date,
                 "address"    : self.address.to_string() }
    
    def serialize_full(self):
        return { "uuid"       : self.uuid,
                 "name"       : self.name,
                 "occupation" : self.occupation,
                 "date"       : self.date,
                 "license"    : self.license.t.dict_lite(),
                 "address"    : self.license.t.dict_lite(),
                 # "r_admin_person": #TODO,
                 # r_institution: # TODO        
        }
        

class File(db.Model):
    """
    class containing data on image and other external files (reproduction 
    of iconographic ressources or cartographic ressources.
    """
    __tablename__ = "file"
    
    id             : Mapped[int]                      = mapped_column(postgresql.INTEGER, nullable=False, primary_key=True)
    uuid           : Mapped[str]                      = mapped_column(Text, nullable=False)
    url            : Mapped[str]                      = mapped_column(Text, nullable=False)
    latlngbounds   : Mapped[t.List[t.List[float]] | None] = mapped_column(postgresql.ARRAY(Float, dimensions=2), nullable=True)  # [ [<float>,<float>], [<float>,<float>] ]
    id_license     : Mapped[int]                      = mapped_column(postgresql.INTEGER, ForeignKey("license.id"), nullable=True)
    id_iconography : Mapped[int]                      = mapped_column(postgresql.INTEGER, ForeignKey("iconography.id"), nullable=True)
    id_cartography : Mapped[int]                      = mapped_column(postgresql.INTEGER, ForeignKey("cartography.id"), nullable=True)

    license     : Mapped["License"]     = relationship("License", back_populates="file")
    iconography : Mapped["Iconography"] = relationship("Iconography", back_populates="file")
    cartography : Mapped["Cartography"] = relationship("Cartography", back_populates="file")
    
    @validates("id", include_backrefs=False)
    def validate_uuid(self, key, _uuid):
        return validate_uuid(_uuid, self.__tablename__)


