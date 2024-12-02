from pydantic import BaseModel, create_model, Field
from sqlalchemy.orm import class_mapper
from typing import Type, Dict, Any, List

class RelatedEntity(BaseModel):
    api_route: str = Field(description="Route permettant de récupérer la resource liée")
    id_uuid: str = Field(description="Identitfiant unique la resource liée")
    label: str = Field(description="libellé de la resource liéz (le nom du champ retourné dépend de la resource)")


class DateRange(BaseModel):
    lower: int
    upper: int
    bounds: str
    empty: bool


def sqlalchemy_to_pydantic(model: Type[BaseModel], resource_type: str, lite: bool=False) -> Type[BaseModel]:
    """
    Convert a SQLAlchemy model to Pydantic for API
    Args:
        model (Type[Base]): SQLAlchemy model.
        resource_type: name of the resource associated to the model
        lite selector for model with or without relationships


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

        if column.comment:
            pydantic_fields[column.name] = (field_type, Field(description=column.comment))
        else:
            pydantic_fields[column.name] = (field_type, ...)

    if not lite:
        model_name = f"{model.__name__}LiteModel"
        for rel_name, rel in relationships.items():
            if rel.is_property:
                if rel.uselist:
                    pydantic_fields[rel_name] = (List[RelatedEntity], ...)
                else:
                    pydantic_fields[rel_name] = (RelatedEntity, ...)
    model = create_model(model_name, **pydantic_fields)

    doc = f"Schéma de données pour les resources de type {resource_type}"
    if lite:
        doc += " en version simplifiée sans les resources liées"
    model.__doc__ = doc
    return model
