from ..app import db
from ..api import api

from flask_openapi3 import Tag

from sqlalchemy.orm import class_mapper

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

from flask import jsonify

from pydantic import BaseModel
from typing import Optional

from .to_pydantic import sqlalchemy_to_pydantic

from functools import cached_property


# *************************************************
# routes for the public API
# basepath: `<APP URL>/api/v1`
# *************************************************


class PaginationParameters(BaseModel):
    page: Optional[int] | None = 1
    limit: Optional[int] | None = 20


class EntityParameters(BaseModel):
    id_uuid: str


class Resource:
    orm_model = None
    tag = None
    columns = None
    relationships = None
    join_relations = None

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

    @cached_property
    def orm_type(self):
        return self.orm_model.__name__

    @cached_property
    def api_model(self):
        return sqlalchemy_to_pydantic(self.orm_model)

    def serialize(self, obj):
        output = {}
        for attr in self.columns:
            output[attr.key] = getattr(obj, attr.key)
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
                                {
                                    "api_route": f"/api/v1/{target_route}",
                                    "identifier": second_target.id_uuid,
                                }
                            )
                        else:
                            output[rel_name].append(
                                {
                                    "api_route": f"/api/v1/{target_route}",
                                    "identifier": target.id_uuid,
                                }
                            )
            else:
                target = getattr(obj, attr_name)
                if target:
                    output[rel_name] = {
                        "api_route": f"/api/v1/{target_route}",
                        "identifier": target.id_uuid,
                    }
        return output

    def get_paginate(self, query: PaginationParameters):
        page = db.paginate(self.orm_model.query, page=query.page, per_page=query.limit)
        return jsonify([self.serialize(obj) for obj in page])

    def get_entity(self, query: EntityParameters):
        r = db.session.execute(
            self.orm_model.query.filter(self.orm_model.id_uuid == query.id_uuid)
        )
        return jsonify(self.serialize(r.one()[0]))


class IconographyResource(Resource):
    orm_model = Iconography
    tag = Tag(
        name="Iconographies", description="Récupération des données iconographiques"
    )
    summary = "Les resources iconographiques"


class CartographyResource(Resource):
    orm_model = Cartography
    tag = Tag(
        name="Cartographies", description="Récupération des données cartographiques"
    )
    summary = "Les resources cartographiques"


class DirectoryResource(Resource):
    orm_model = Directory
    tag = Tag(
        name="Répertoire",
        description="Récupération des données répertoires de fichiers",
    )
    summary = "Les resources répertoires de fichiers"


class FilenameResource(Resource):
    orm_model = Filename
    tag = Tag(name="Fichiers", description="Récupération des fichiers")
    summary = "Les resources fichiers"


class TitleResource(Resource):
    orm_model = Title
    tag = Tag(name="Titres", description="Récupération des titres des iconographies")
    summary = "Les resources titre iconographique"


class AnnotationResource(Resource):
    orm_model = Annotation
    tag = Tag(
        name="Annotations", description="Récupération des annotations des iconographies"
    )
    summary = "Les resources annotations"


class ThemeResource(Resource):
    orm_model = Theme
    tag = Tag(name="Thèmes", description="Récupération des thèmes")
    summary = "Les resources thèmes"


class NamedEntityResource(Resource):
    orm_model = NamedEntity
    tag = Tag(name="Entités nommées", description="Récupération des entités nommées")
    summary = "Les resources entités nommées"


class ActorResource(Resource):
    orm_model = Actor
    tag = Tag(name="Acteurs", description="Récupération des acteurs")
    summary = "Les resources acteurs"


class PlaceResource(Resource):
    orm_model = Place
    tag = Tag(name="Lieux", description="Récupération des lieux")
    summary = "Les resources lieux"


class AddressResource(Resource):
    orm_model = Address
    tag = Tag(name="Adresses", description="Récupération des adresses")
    summary = "Les resources adresses"


class InstitutionResource(Resource):
    orm_model = Institution
    tag = Tag(name="Institutions", description="Récupération des institutions")
    summary = "Les resources institutions"


class LicenceResource(Resource):
    orm_model = Licence
    tag = Tag(name="Licences", description="Récupération des licences")
    summary = "Les resources licences"


class AdminPersonResource(Resource):
    orm_model = AdminPerson
    tag = Tag(
        name="AdminPerson", description="Récupération des personnes administrateur"
    )
    summary = "Les resources personnes administrateur"


def make_get_paginate(resource):
    def get_paginate(query: PaginationParameters):
        return resource.get_paginate(query)

    get_paginate.__name__ = f"get_{resource.name}_list"
    return get_paginate


def make_get_entity(resource):
    def get_entity(path: EntityParameters):
        return resource.get_entity(path)

    get_entity.__name__ = f"get_{resource.name}"
    return get_entity


alls = globals()

for resource in [
    CartographyResource(),
    IconographyResource(),
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
        f"{route}/<string:id_uuid>", summary=resource.summary, tags=[resource.tag]
    )(get_entity)
