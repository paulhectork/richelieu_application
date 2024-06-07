import typing as t


# **************************************************
# helpers for spatial data and spatial operations
# see: https://geojson.org/
#      https://fr.wikipedia.org/wiki/GeoJSON
# **************************************************


GEOJSON_GEOMETRY_TYPES = [ "Point", "LineString", "Polygon", "MultiPoint"
                         , "MultiLineString", "MultiPolygon" ]


def geometry_to_feature(geometry:t.Dict, custom_properties:t.Dict=None) -> t.Dict:
    """
    our database stores spatial data as geoJson geometry objects.
    here, we transform them into geoJson features. using `custom_properties`,
    we add custom data into the feature's `properties` object.

    :param geometry: a valid geoJson geometry object
    :param custom_properties: a dict containing extra data that will be useful.
                              this is a good place to store an UUID
    """
    # check that our data is valid
    if not isinstance(custom_properties, dict):
        raise TypeError(f"`custom_properties` must be of type `dict`, got `{type(custom_properties)}`")
    if not isinstance(geometry, dict):
        raise TypeError(f"`geometry` must be of type `dict`, got `{type(geometry)}`")
    if ( "type" not in list(geometry.keys())
         or geometry["type"] not in GEOJSON_GEOMETRY_TYPES ):
        raise ValueError(f"`geometry` is not a valid GeoJSON geometry: got {geometry}")

    # create the feature
    return { "type": "Feature",
             "geometry": geometry,
             "properties": custom_properties
    }


def featurelist_to_featurecollection(featurelist:t.List[t.Dict]) -> t.Dict:
    """
    transform a list of geojson features into a geojson featurecollection
    """
    # check that our data is valid
    if not isinstance(featurelist, list):
        raise TypeError(f"`featurelist` must be of type `list`, got `{type(featurelist)}`")
    if not all( ("type" in list(f.keys()) and f["type"] == "Feature") for f in featurelist ):
        print("`featurelist` contains invalid geojson features")

    # create the feature collection
    return { "type": "FeatureCollection",
             "features": featurelist }