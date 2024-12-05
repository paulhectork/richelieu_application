from typing import Optional
from enum import Enum
from functools import cached_property

from flask import jsonify
from flask_openapi3 import Tag

from pydantic import BaseModel, Field

from sqlalchemy.orm import class_mapper
from sqlalchemy.exc import NoResultFound

from ..app import db
from ..api import api

from ..orm.data_sources import (
    Iconography,
    Cartography,
    Directory,
    Filename,
)

from ..orm.qualifiers import (
    Title,
    Annotation,
    Theme,
    NamedEntity,
    Actor,
)

from ..orm.places import (
    Place,
    Address,
)

from ..orm.admin import (
    Institution,
    Licence,
    AdminPerson,
)


from .to_pydantic import sqlalchemy_to_pydantic, RelatedEntity

from ..search.search_iconography import make_query, sanitize_params


# *************************************************
# routes for the public API
# basepath: `<APP URL>/api/v1`
# *************************************************


class PaginationParameters(BaseModel):
    """Paramètres pour les routes fournisant de la pagination"""
    page: Optional[int] | None = Field(default=1, description="numéro de la page à consulter")
    limit: Optional[int] | None = Field(default=20, description="nombre maximum de resources décrites par page")


class EntityParameters(BaseModel):
    """Paramètres pour la récupération d'une resource à partir de son identifiant"""
    id_uuid: str = Field("identifiant unique de la resource à récupérer")


class BooleanEnum(str, Enum):
    and_selection = 'and'
    or_selection  = 'or'
    not_selection  = 'not'


class SearchParameters(BaseModel):
    """Paramètres pour la recherche des iconographies"""
    title: Optional[str] | None = Field(default="", description="chaîne de caractères à rechercher dans tous les titres des iconographies")
    title_boolean_op: BooleanEnum = Field(default=BooleanEnum.and_selection, description="opérateur de sélection pour les titres")
    author: Optional[str] | None = Field(default="", description="chaîne de caractères à rechercher dans tous les noms des auteurs/autrices")
    author_boolean_op: BooleanEnum = Field(default=BooleanEnum.and_selection, description="opérateur de sélection pour les auteurs/autrices")
    publisher: Optional[str] | None = Field(default="", description="chaîne de caractères à rechercher dans tous les noms des éditeurs/éditrices")
    publisher_boolean_op: BooleanEnum = Field(default=BooleanEnum.and_selection, description="opérateur de sélection pour les éditeurs/éditrices")
    theme: Optional[str] | None = Field(default="", description="sélection des iconographies correspondant à un ou plusieurs thème")
    theme_boolean_op: BooleanEnum = Field(default=BooleanEnum.and_selection, description="opérateur de sélection pour les thèmes")
    named_entity: Optional[str] | None = Field(default="", description="sélection des iconographies correspondant à une ou plusieurs entités nommées")
    named_entity_boolean_op: BooleanEnum = Field(default=BooleanEnum.and_selection, description="opérateur de sélection pour les entités nommées")
    institution: Optional[str] | None = Field(default="", description="sélection des iconographies correspondant à une ou plusieurs institutions")
    institution_boolean_op: BooleanEnum = Field(default=BooleanEnum.and_selection, description="opérateur de sélection pour les institutions")
    date: Optional[str] | None = Field(default="", description="sélection d'une date ou d'un intervalle de date")
    date_boolean_op: BooleanEnum = Field(default=BooleanEnum.and_selection, description="opérateur de sélection des dates")


class ResourceNotFoundResponse(BaseModel):
    code: int = Field(-1, description="Status Code")
    message: str = Field("Resource not found!", description="Exception Information")


class Resource:
    orm_model = None
    tag = None
    columns = None
    relationships = None
    join_relations = None
    ui_name = None

    def __init__(self):
        self.columns = class_mapper(self.orm_model).columns
        self.relationships = class_mapper(self.orm_model).relationships
        self.join_relations = {}
        for relation in self.relationships:
            if "r_" in relation.key:
                for c in relation.mapper.relationships:
                    if c.mapper.entity.__name__ != self.orm_type:
                        attr_name = c.mapper.mapped_table.key
                        target_type = c.mapper.entity.__name__
                        target_route = target_type.lower()
                        self.join_relations[relation.key] = (attr_name, target_route)

    @property
    def name(self):
        return self.orm_model.__name__.lower()

    @property
    def summary(self):
        return f"Récupération des resources correspondant aux {self.ui_name}"

    @property
    def summary_id_uuid(self):
        return f"Récupération d'une ressource de type {self.ui_name[:-1]} à partir de son identifiant unique"

    @property
    def summary_lite(self):
        return f"Récupération des resources correspondant aux {self.ui_name} sans les resources liées"

    @cached_property
    def orm_type(self):
        return self.orm_model.__name__

    @cached_property
    def api_model(self):
        return sqlalchemy_to_pydantic(self.orm_model, self.ui_name)

    @cached_property
    def api_model_lite(self):
        return sqlalchemy_to_pydantic(self.orm_model, self.ui_name, lite=True)

    def _add_linked_entity(self, target_route, target):
        return {
            "api_route": f"/api/v1/{target_route}",
            "id_uuid": target.id_uuid,
            "label": target.label,
        }

    def _serialize_relationships(self, obj, output):
        for relation in self.relationships:
            rel_name = relation.key
            attr_name, target_route = self.join_relations.get(rel_name, (rel_name, rel_name))
            if relation.uselist:
                output[rel_name] = []
                for target in getattr(obj, rel_name):
                    if target:
                        if rel_name in self.join_relations:
                            second_target = getattr(target, attr_name)
                            if second_target is None:
                                continue
                            output[rel_name].append(
                                self._add_linked_entity(target_route, second_target)
                            )
                        else:
                            output[rel_name].append(
                                self._add_linked_entity(target_route, target)
                            )
            else:
                target = getattr(obj, attr_name)
                if target:
                    output[rel_name] = self._add_linked_entity(target_route, target)

    def serialize(self, obj, lite=False):
        output = {}
        api_model = self.api_model_lite
        for attr in self.columns:
            if str(attr.type) == "INT4RANGE":
                date_range = getattr(obj, attr.key)

                if date_range:
                    output[attr.key] = {
                        "lower": date_range.lower,
                        "upper": date_range.upper,
                        "bounds": date_range.bounds,
                        "empty": date_range.empty,
                    }
                else:
                    output[attr.key] = None

            else:
                output[attr.key] = getattr(obj, attr.key)

        if not lite:
            self._serialize_relationships(obj, output)
            api_model = self.api_model

        obj = api_model(**output)  # output format validation
        return obj.dict()

    def serialize_as_link(self, obj):
        link = RelatedEntity(api_route=f"/api/v1/{self.name}", id_uuid=obj.id_uuid, label=obj.label)
        return link.dict()

    def get_paginate(self, query: PaginationParameters):
        page = db.paginate(self.orm_model.query, page=query.page, per_page=query.limit)
        return jsonify([self.serialize(obj) for obj in page])

    def get_entity(self, query: EntityParameters):
        r = db.session.execute(
            self.orm_model.query.filter(self.orm_model.id_uuid == query.id_uuid)
        )
        return jsonify(self.serialize(r.one()[0]))

    def get_entity_lite(self, query: PaginationParameters):
        page = db.paginate(self.orm_model.query, page=query.page, per_page=query.limit)
        return jsonify([self.serialize(obj, lite=True) for obj in page])


class IconographyResource(Resource):
    orm_model = Iconography
    tag = Tag(
        name="Iconographies", description="Récupération des données iconographiques"
    )
    ui_name = "iconographies"


class CartographyResource(Resource):
    orm_model = Cartography
    tag = Tag(
        name="Cartographies", description="Récupération des données cartographiques"
    )
    ui_name = "cartographies"


class DirectoryResource(Resource):
    orm_model = Directory
    tag = Tag(
        name="Répertoire",
        description="Récupération des données répertoires de fichiers",
    )
    ui_name = "répertoires de fichiers"


class FilenameResource(Resource):
    orm_model = Filename
    tag = Tag(name="Fichiers", description="Récupération des fichiers")
    ui_name = "fichiers"


class TitleResource(Resource):
    orm_model = Title
    tag = Tag(name="Titres", description="Récupération des titres des iconographies")
    ui_name = "titres des iconographies"


class AnnotationResource(Resource):
    orm_model = Annotation
    tag = Tag(
        name="Annotations", description="Récupération des annotations des iconographies"
    )
    ui_name = "annotations"


class ThemeResource(Resource):
    orm_model = Theme
    tag = Tag(name="Thèmes", description="Récupération des thèmes")
    ui_name = "thèmes"


class NamedEntityResource(Resource):
    orm_model = NamedEntity
    tag = Tag(name="Entités nommées", description="Récupération des entités nommées")
    ui_name = "entités nommées"


class ActorResource(Resource):
    orm_model = Actor
    tag = Tag(name="Acteurs", description="Récupération des acteurs")
    ui_name = "acteurs"


class PlaceResource(Resource):
    orm_model = Place
    tag = Tag(name="Lieux", description="Récupération des lieux")
    ui_name = "lieux"


class AddressResource(Resource):
    orm_model = Address
    tag = Tag(name="Adresses", description="Récupération des adresses")
    ui_name = "adresses"


class InstitutionResource(Resource):
    orm_model = Institution
    tag = Tag(name="Institutions", description="Récupération des institutions")
    ui_name = "institutions"


class LicenceResource(Resource):
    orm_model = Licence
    tag = Tag(name="Licences", description="Récupération des licences")
    ui_name = "licences"


class AdminPersonResource(Resource):
    orm_model = AdminPerson
    tag = Tag(
        name="AdminPerson", description="Récupération des personnes administrateur"
    )
    ui_name = "administrateurs"


def make_get_paginate(resource):
    def get_paginate(query: PaginationParameters):
        return resource.get_paginate(query)

    get_paginate.__name__ = f"get_{resource.name}_list"
    return get_paginate


def make_get_entity(resource):
    def get_entity(path: EntityParameters):
        try:
            return resource.get_entity(path)
        except NoResultFound:
            return ResourceNotFoundResponse().dict(), 404


    get_entity.__name__ = f"get_{resource.name}"
    return get_entity


def make_get_entity_lite(resource):
    def get_entity_lite(query: PaginationParameters):
        return resource.get_entity_lite(query)

    get_entity_lite.__name__ = f"get_{resource.name}_lite"
    return get_entity_lite


def sanitize_search_query(query):
    prepare_query = {}
    col_sep = ","
    for key, val in query.items():
        if "op" in key:
            prepare_query[key] = val
        elif "date" in key and val:
            dates = val.split(col_sep)
            if len(dates) == 1:
                prepare_query[key] = [{'filter': 'dateExact', 'data': [int(dates[0])]}]
            elif len(dates) == 2:
                prepare_query[key] = [{'filter': 'dateRange', 'data': [int(d) for d in dates]}]
            else:
                raise ValueError("more than 2 dates is not allowed")
        elif col_sep in val:
            prepare_query[key] = val.split(col_sep)
        else:
            if val:
                prepare_query[key] = [val]
            else:
                prepare_query[key] = []
    return sanitize_params(prepare_query)[0]


ICONOGRAPHY_RESOURCE = IconographyResource()


@api.get("/search",
         summary="Recherche des iconographies",
         tags=[IconographyResource.tag],
         doc_ui=True,
         responses={200: RelatedEntity})
def search(query: SearchParameters):
    """
    search resource.
    """
    query_dump = sanitize_search_query(query.model_dump())
    results = make_query(query_dump).all()
    data = [ICONOGRAPHY_RESOURCE.serialize_as_link(r[0]) for r in results]
    return jsonify(data)


alls = globals()

for resource in [
    CartographyResource(),
    ICONOGRAPHY_RESOURCE,
    DirectoryResource(),
    FilenameResource(),
    TitleResource(),
    AnnotationResource(),
    ThemeResource(),
    NamedEntityResource(),
    ActorResource(),
    PlaceResource(),
    AddressResource(),
    InstitutionResource(),
    LicenceResource(),
    AdminPersonResource(),
]:
    route = f"/{resource.name}"

    get_paginate = make_get_paginate(resource)
    alls[get_paginate.__name__] = api.get(
        route,
        summary=resource.summary,
        tags=[resource.tag],
        doc_ui=True,
        responses={200: resource.api_model},
    )(get_paginate)

    get_entity = make_get_entity(resource)
    alls[get_entity.__name__] = api.get(
        f"{route}/<string:id_uuid>",
        summary=resource.summary_id_uuid,
        tags=[resource.tag],
        doc_ui=True,
        responses={200: resource.api_model, 404: ResourceNotFoundResponse},
    )(get_entity)

    get_entity_lite = make_get_entity_lite(resource)
    alls[get_entity_lite.__name__] = api.get(
        f"{route}/lite",
        summary=resource.summary_lite,
        tags=[resource.tag],
        doc_ui=True,
        responses={200: resource.api_model_lite},
    )(get_entity_lite)
