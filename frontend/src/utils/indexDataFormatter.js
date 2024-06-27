/**
 * format data coming from the backend to match what is
 * required by `IndexItem.vue`.
 *
 * indexes are used on a lot of pages (for example, an
 * icongraphy index is used by `IconographyView.vue`,
 * `ThemeMainView.vue`, `NamedEntityMain.vue`). the data
 * for indexes sent from the backend has to be reformatted
 * before being passed to `Index.vue` and `IndexItem.vue`.
 * this module centralizes this reformatting, with one
 * formatting function per data source (Iconography,
 * NamedEntity, Theme...)
 */

import { fnToIconographyFile, fnToCartographyFile } from "@utils/functions";
import { stringifyIconographyResource
       , stringifyAddressResource
       , stringifyThemeOrNamedEntityResource } from "@utils/stringifiers";


/**
 * all functions format data for an index from a specific data source
 * @param {Array} dataArr: the array of data to format.
 */

export function indexDataFormatterIconography(dataArr) {
  return dataArr.map((c) => {
   return { idUuid : c.id_uuid,
            href   : new URL(`/iconographie/${c.id_uuid}`, window.location.href).href,
            iiif   : c.iiif_url != null ? new URL(c.iiif_url) : c.iiif_url,
            img    : c.thumbnail.length ? fnToIconographyFile(c.thumbnail[0].url).href : null,
            text   : stringifyIconographyResource(c) };
  })
}

export function indexDataFormatterCartography(dataArr) {
  return dataArr.map((c) => {
    return { idUuid : c.id_uuid,
             href   : new URL(`/lieu/${c.id_uuid}`, window.location.href).href,
             iiif   : c.iiif_url != null ? new URL(c.iiif_url) : c.iiif_url,
             img    : c.filename.length ? fnToCartographyFile(c.filename[0].url).href : null,
             text   : c.address.length ? stringifyAddressResource(c.address[0]) : "Addresse inconnue" };
  })
}

export function indexDataFormatterTheme(dataArr) {
  return dataArr.map((c) => {
    return { idUuid : c.id_uuid,
             href   : new URL(`/theme/${c.id_uuid}`, window.location.href).href,
             iiif   : c.iiif_url != null ? new URL(c.iiif_url) : c.iiif_url,
             img    : c.thumbnail.length ? fnToIconographyFile(c.thumbnail[0]).href : null,
             text   : stringifyThemeOrNamedEntityResource(c)

    }
  })
}

export function indexDataFormatterNamedEntity(dataArr) {
  return dataArr.map((c) => {
    return { idUuid : c.id_uuid,
             href   : new URL(`/sujet/${c.id_uuid}`, window.location.href).href,
             iiif   : c.iiif_url != null ? new URL(c.iiif_url) : c.iiif_url,
             img    : c.thumbnail.length ? fnToIconographyFile(c.thumbnail[0]).href : null,
             text   : stringifyThemeOrNamedEntityResource(c)
    }
  })
}