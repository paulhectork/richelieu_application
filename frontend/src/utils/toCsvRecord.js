/**
 * Utilities function  used to transform json array items into CSV records.
 */

import { stringifyDate } from "@utils/stringifiers";

// GIS WKT converters

function serializePoint(point) {
  return `${point[0]} ${point[1]}`;
}

function serializeRing(polygonRing) {
  return polygonRing.map(serializePoint).join(";");
}

function serializeRings(rings) {
  return rings.map((ring) => `(${serializeRing(ring)})`).join(", ");
}

function serializeGeometry(geo) {
  if (geo.type === "Polygon") {
    return `POLYGON (${serializeRings(geo.coordinates)})`;
  } else if (geo.type === "Point") {
    return `POINT (${serializePoint(geo.coordinates)})`;
  } else {
    throw Error(`Unknown geometry type "${geo.type}".`);
  }
}

// Transform specific to entity types

/**
 * prepare an iconography object for export.
 * small subtelty here: `iconography` is serialized
 * slightly differently depending on if we're exporting an
 * iconography collection (from `IconographyIconography.vue`)
 * or a single item (from `IconographyMainView`):
 * - if collection view, `iconography.place` is an array of places
 *    (@typedefs.PlaceItemLite[]) with an UUID, an address and a geometry
 *    represented as a geoJson geometry.
 * - if main view, `iconography.place` is a geoJson featureCollection and
 *    each place is represented by a feature. we don't have an address
 *    in that case
 * => detect if `place` is an array or an object and use the proper
 *      transformation method. if place is an object (IconographyMainView),
 *      the address can't be exported since it's not available to the frontend.
 * @returns { {[string]:string} }
 *   the Iconography object as a key-value pair, where each
 *    value has been stringified
 */
export function iconographyToCsvRecord({
  id_uuid,
  title,
  iiif_url,
  author,
  date,
  theme,
  place,
  named_entity,
}) {
  return {
    id_uuid,
    title: title.join("|"),
    iiif_url: iiif_url,
    authors: author.map((author) => author.entry_name).join("|"),
    authors_uuids: author.map((author) => author.id_uuid).join("|"),
    date: stringifyDate(date),
    themes: theme.map((theme) => theme.entry_name).join("|"),
    themes_uuids: theme.map((theme) => theme.id_uuid).join("|"),
    named_entities: named_entity.map((entity) => entity.entry_name).join("|"),
    named_entities_uuids: named_entity
      .map((entity) => entity.id_uuid)
      .join("|"),
    places_address:
      Array.isArray(place)
      ? place
        .map(({ address: [address] }) =>
          `${address.address}, ${address.city}, ${address.country}`)
        .join("|")
      : [].join("|"),  // no address exported since it's not available
    places_geometry:
      Array.isArray(place)
      ? place
        .map((place) => serializeGeometry(place.vector))
        .join("|")
      : place.features
        .map((placeFeature) => serializeGeometry(placeFeature.geometry))
        .join("|"),
    places_uuids:
      Array.isArray(place)
      ? place.map((place) => place.id_uuid).join("|")
      : place.features
        .map((placeFeature) => placeFeature.properties.id_uuid).join("|"),
  };
}

export function placeToCsvRecord({
  address: [{ address, city, country, id_uuid: address_uuid, source }],
  centroid,
  date,
  id_uuid,
  vector,
}) {
  return {
    id_uuid,
    address,
    city,
    country,
    address_uuid,
    centroid: serializeGeometry(centroid),
    date: stringifyDate(date),
    vector: serializeGeometry(vector),
  };
}

export function themeOrNamedEntityToCsvRecord({
  id_uuid,
  category_name,
  category_slug,
  entry_name,
}) {
  return {
    id_uuid,
    category_name,
    category_slug,
    entry_name,
  };
}

export function institutionToCsvRecord({
  id_uuid,
  entry_name,
  iconography_count,
}) {
  return {
    id_uuid,
    iconography_count,
    entry_name,
  };
}
