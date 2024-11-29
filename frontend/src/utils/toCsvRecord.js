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
    places_address: place
      .map(
        ({ address: [address] }) =>
          `${address.address}, ${address.city}, ${address.country}`
      )
      .join("|"),
    places_geometry: place
      .map((place) => serializeGeometry(place.vector))
      .join("|"),
    places_uuids: place.map((place) => place.id_uuid).join("|"),
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
  category,
  entry_name,
}) {
  return {
    id_uuid,
    category,
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
