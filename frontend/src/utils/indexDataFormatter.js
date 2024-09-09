/**
 * format data coming from the backend to match what is
 * required by `IndexItem.vue`.
 *
 * indexes are used on a lot of pages (for example, an
 * icongraphy index is used by `IconographyView.vue`,
 * `ThemeMainView.vue`, `NamedEntityMain.vue`). the data
 * for indexes sent from the backend has to be reformatted
 * before being passed to `IndexBase.vue` and `IndexItem.vue`.
 * this module centralizes this reformatting, with one
 * formatting function per data source (Iconography,
 * NamedEntity, Theme...)
 */

import { fnToIconographyFile
       , fnToCartographyFile
       , urlToFrontendPlace
       , urlToFrontendIconography
       , urlToFrontendTheme
       , urlToFrontendNamedEntity } from "@utils/url";
import { stringifyIconographyResource
       , stringifyThemeOrNamedEntityResource } from "@utils/stringifiers";


/**
 * all functions format data for an index from a specific data source
 * @param {Array} dataArr: the array of data to format.
 */

export function indexDataFormatterIconography(dataArr) {
  return dataArr.map((c) => {
    return { idUuid : c.id_uuid,
            href   : urlToFrontendIconography(c.id_uuid).pathname,
            iiif   : c.iiif_url != null ? new URL(c.iiif_url) : c.iiif_url,
            img    : c.thumbnail.length ? fnToIconographyFile(c.thumbnail[0].url).href : null,
            text   : stringifyIconographyResource(c) };
  })
}

export function indexDataFormatterPlace(dataArr) {
  return dataArr.map((c) => {
    if ( ! c.address.length ) console.log(c)
    return { idUuid : c.id_uuid,
             href   : urlToFrontendPlace(c.id_uuid).pathname,
             iiif   : c.iiif_url != null ? new URL(c.iiif_url) : c.iiif_url,
             img    : c.filename.length ? fnToCartographyFile(c.filename[0].url).href : null,
             text   : c.address.length ? c.address[0].address : "Addresse inconnue" };
  })
}

export function indexDataFormatterTheme(dataArr) {
  return dataArr.map((c) => {
    return { idUuid : c.id_uuid,
             href   : urlToFrontendTheme(c.id_uuid).pathname,
             iiif   : c.iiif_url != null ? new URL(c.iiif_url) : c.iiif_url,
             img    : c.thumbnail.length ? fnToIconographyFile(c.thumbnail[0]).href : null,
             text   : stringifyThemeOrNamedEntityResource(c)

    }
  })
}

export function indexDataFormatterNamedEntity(dataArr) {
  return dataArr.map((c) => {
    return { idUuid : c.id_uuid,
             href   : urlToFrontendNamedEntity(c.category, c.id_uuid).pathname,
             iiif   : c.iiif_url != null ? new URL(c.iiif_url) : c.iiif_url,
             img    : c.thumbnail.length ? fnToIconographyFile(c.thumbnail[0]).href : null,
             text   : stringifyThemeOrNamedEntityResource(c)
    }
  })
}