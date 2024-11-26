from pydantic import BaseModel, create_model
from sqlalchemy.orm import class_mapper
from typing import Type, Dict, Any, List


class RelatedEntity(BaseModel):
    api_route: str
    identifier: str
    label: str


class DateRange(BaseModel):
    lower: int
    upper: int
    bounds: str
    empty: bool


def sqlalchemy_to_pydantic(model: Type[BaseModel], lite: bool=False) -> Type[BaseModel]:
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

    model_name = f"{model.__name__}LiteModel"

    for column in columns:
        try:
            field_type = column.type.python_type
        except Exception:
            if str(column.type) == "INT4RANGE":
                field_type = DateRange
        if column.nullable is True:
            field_type = field_type | None
        pydantic_fields[column.name] = (field_type, ...)

    if not lite:
        model_name = f"{model.__name__}LiteModel"
        for rel_name, rel in relationships.items():
            if rel.is_property:
                if rel.uselist:
                    pydantic_fields[rel_name] = (List[RelatedEntity], ...)
                else:
                    pydantic_fields[rel_name] = (RelatedEntity, ...)
    return create_model(model_name, **pydantic_fields)
