from ..app import db
from ..api import api, icono_tag

from sqlalchemy import inspect
from ..orm.data_sources import Iconography

from flask import jsonify

from pydantic import BaseModel


# *************************************************
# routes for the public API
# basepath: `<APP URL>/api/v1`
# *************************************************


class IconographyParameters(BaseModel):
    page: int
    limit: int


def api_serializer(obj):
    output = {}
    iobj = inspect(obj)

    for attr in iobj.mapper.column_attrs:
        output[attr.key] = getattr(obj, attr.key)
    for relation in iobj.mapper.relationships:
        if relation.uselist:
            output[relation.key] = [
                target.id_uuid for target in getattr(obj, relation.key)
            ]
        else:
            output[relation.key] = getattr(obj, relation.key).id_uuid
    return output


@api.get("/iconography", summary="get all `iconography` ressources", tags=[icono_tag])
def index_iconography(query: IconographyParameters):
    """
    get `iconography` ressources.
    """
    page = db.paginate(Iconography.query, page=query.page, per_page=query.limit)
    return jsonify([api_serializer(obj) for obj in page])
