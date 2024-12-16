from flask_openapi3 import APIBlueprint, Tag


api = APIBlueprint(
    'Richelieu',
    __name__,
    url_prefix='/api/v1',
    doc_ui=True
)
