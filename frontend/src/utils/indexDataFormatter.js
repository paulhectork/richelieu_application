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

import { urlToIconographyFile
       , urlToCartographyFile
       , urlToFrontendPlace
       , urlToFrontendIconography
       , urlToFrontendTheme
       , urlToFrontendNamedEntity
       , urlToFrontendNamedEntityCategory
       , urlToFrontendThemeCategory
       , urlToFrontendInstitution } from "@utils/url";
import { stringifyIconographyResource
       , stringifyThemeOrNamedEntityResource
       , stringifyThemeOrNamedEntityCategory
       , stringifyInstitutionResource } from "@utils/stringifiers";


/**
 * all functions format data for an index from a specific data source
 * @param {Array} dataArr: the array of data to format.
 */

export const indexDataFormatterIconography = (dataArr) =>
  dataArr.map((c) => {
    return { idUuid : c.id_uuid,
            href   : urlToFrontendIconography(c.id_uuid).pathname,
            iiif   : c.iiif_url != null ? new URL(c.iiif_url) : c.iiif_url,
            img    : c.thumbnail.length ? urlToIconographyFile(c.thumbnail[0].url).href : null,
            text   : stringifyIconographyResource(c, true) };
  })

export const indexDataFormatterPlace = (dataArr) =>
  dataArr.map((c) => {
    return { idUuid : c.id_uuid,
             href   : urlToFrontendPlace(c.id_uuid).pathname,
             iiif   : c.iiif_url != null ? new URL(c.iiif_url) : c.iiif_url,
             img    : c.filename.length ? urlToCartographyFile(c.filename[0].url).href : null,
             text   : c.address.length ? c.address[0].address : "Adresse inconnue" };
  })

export const indexDataFormatterThemeCategory = (dataArr) =>
  dataArr.map((c) => {
    return { idUuid : undefined,
             href   : urlToFrontendThemeCategory(c.category_name).pathname,
             iiif   : null,   // todo
             img    : c.thumbnail.length ? urlToIconographyFile(c.thumbnail[0]).href : null,   // todo
             text   : stringifyThemeOrNamedEntityCategory(c)
    }
  })

export const indexDataFormatterTheme = (dataArr) =>
  dataArr.map((c) => {
    return { idUuid : c.id_uuid,
             href   : urlToFrontendTheme(c.category, c.id_uuid).pathname,
             iiif   : c.iiif_url != null ? new URL(c.iiif_url) : c.iiif_url,
             img    : c.thumbnail.length ? urlToIconographyFile(c.thumbnail[0]).href : null,
             text   : stringifyThemeOrNamedEntityResource(c)

    }
  })

export const indexDataFormatterNamedEntityCategory = (dataArr) =>
  dataArr.map((c) => {
    return { idUuid : undefined,
             href   : urlToFrontendNamedEntityCategory(c.category_name).pathname,
             iiif   : null,   // todo
             img    : c.thumbnail.length ? urlToIconographyFile(c.thumbnail[0]).href : null,
             text   : stringifyThemeOrNamedEntityCategory(c)
    }
  })

export const indexDataFormatterNamedEntity = (dataArr) =>
  dataArr.map((c) => {
    return { idUuid : c.id_uuid,
             href   : urlToFrontendNamedEntity(c.category, c.id_uuid).pathname,
             iiif   : c.iiif_url != null ? new URL(c.iiif_url) : c.iiif_url,
             img    : c.thumbnail.length ? urlToIconographyFile(c.thumbnail[0]).href : null,
             text   : stringifyThemeOrNamedEntityResource(c)
    }
  })

export const indexDataFormatterInstitution = (dataArr) =>
  dataArr.map((c) => {
    return { idUuid : c.id_uuid,
             href   : urlToFrontendInstitution(c.id_uuid).pathname,
             iiif   : null,
             img    : c.thumbnail.length ? urlToIconographyFile(c.thumbnail[0]).href : null, //TODO
             text   : stringifyInstitutionResource(c)
    }
  })