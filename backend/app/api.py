from flask_openapi3 import APIBlueprint, Tag


icono_tag = Tag(name='Iconography', description="Récupération des données iconographiques")


api = APIBlueprint(
    '/richelieu',
    __name__,
    url_prefix='/api/v1',
    abp_tags=[icono_tag],
    doc_ui=True
)
