from pydantic import BaseModel, create_model
from sqlalchemy.orm import class_mapper
from typing import Type, Dict, Any, List


class RelatedEntity(BaseModel):
    api_route: str
    identifier: str


def sqlalchemy_to_pydantic(model: Type[BaseModel]) -> Type[BaseModel]:
    """
    Convert a SQLAlchemy model to Pydantic for API
    Args:
        model (Type[Base]): SQLAlchemy model.

    Returns:
        Type[BaseModel]: generated Pydantic model.
    """

    columns = class_mapper(model).columns
    relationships = class_mapper(model).relationships

    pydantic_fields: Dict[str, Any] = {}

    for column in columns:
        try:
            field_type = column.type.python_type
        except Exception:
            field_type = int
        if column.nullable is True:
            field_type = field_type | None
        pydantic_fields[column.name] = (field_type, ...)

    for rel_name, rel in relationships.items():
        if rel.is_property:
            if rel.uselist:
                pydantic_fields[rel_name] = (List[RelatedEntity], ...)
            else:
                pydantic_fields[rel_name] = (RelatedEntity, ...)
    return create_model(f"{model.__name__}Model", **pydantic_fields)
