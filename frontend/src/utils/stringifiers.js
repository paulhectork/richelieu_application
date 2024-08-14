/******************************************************
 *                                                    *
 *        transform objects (`[]`, `{}`) into         *
 *        string representations                      *
 *                                                    *
 ******************************************************/

import { urlToFrontendActor
       , urlToFrontendTheme
       , urlToFrontendNamedEntity
       , urlToFrontendInstitution } from "@utils/url";


/**
 * capitalize the first letter of string str
 * @param {string|Any} str: the string to capitalize
 * @returns str if we sent a string, else the input unchanged
 */
export const capitalizeString = (str) =>
  str != null && typeof str === "string"
  ? str.charAt(0).toUpperCase() + str.slice(1)
  : str;

/**
 * same as above, but all words are capitalized, instead of just the first letter
 */
export const capitalizeWords = (str) =>
  str != null && typeof str === "string"
  ? str.split(" ").map(s => s.charAt(0).toUpperCase() + s.slice(1)).join(" ")
  : str;


/**
 * generic function to create a string representation
 * from an array of values named `arr`. this works best
 * if the array is flat (no nested arrays) and contains
 * only strings, floats and ints.
 * @param {Array} arr: the array to represent as a string
 * @returns {String}
 */
export function stringifyGenericArray(arr) {
  let out = "";
  arr.filter(a => a != null).map((a, idx) => {
    switch ( idx ) {
      case arr.length - 1:  // `a` is the last entry in `arr`
        out += String(a);
        break;
      case arr.length - 2:  // `a` is the entry before the last in `arr`
        out += `${String(a)} et `;
        break;
      default:              // any other entry
        out += `${String(a)}, `;
        break;
    }
  })
  return out;
}

/**
 * transform a date range array into a human-readable string
 * @param {Array} a: a date, of shape `[YYYY, YYYY]`
 * @returns {str}: `YYYY` or `YYYY-YYYY`
 */
export function stringifyDate(d) {
  if ( d != null ) {
    return d[0] === d[1]
           ? `${d[0]}`
           : `${d[0]}-${d[1]}`
  } else {
    return "Date inconnue"
  }
}

/**
 * generate a string representation of a single iconography object
 * (defined in the backend by: Iconography.serialize_lite())
 * @param {Object} i: the iconography object
 * @returns String
 */
export function stringifyIconographyResource(i) {
  let out = "";
  let authors = stringifyActorArray(i.authors);
  let date = stringifyDate(i.date);

  out += authors.length ? `${authors}, ` : "";
  out += i.title.length ? `<i>${ i.title[0] }</i> ` : " ";
  out += date.length ? `(${date})` : "";
  return out;
}

/**
 * stringify a single `Theme` or `NamedEntity` object
 * @returns string
 */
export function stringifyThemeOrNamedEntityResource(x) {
  return `<span>${x.entry_name}</span><span>[${x.iconography_count}]</span>`
}


/**
 * all of the functions below are pretty much the same: take an
 * array of objects and transform them into an HTML string. if
 * `hyperlink` is true, create an `<a href="">` with an redirection
 * to the main page of each item  in the array (to redirect to a theme...)
 * @param {Array} tablenameArray : the array of objects
 * @param {bool} hyperlink: perform redirections
 * @returns str
 */
export function stringifyActorArray(actorArray, hyperlink=false) {
  const doHyperlink = actor =>
    `<a href="${ urlToFrontendActor(actor.id_uuid).href }"
    >${actor.entry_name}</a>`;

  let out = "";
  if ( actorArray != null && actorArray.length ) {
    actorArray.filter(a => a.entry_name != null).map((a, idx) => {
      switch ( idx ) {
        case actorArray.length - 1:  // `a` is the last entry in `actorArray`
          out += hyperlink ? doHyperlink(a) : a.entry_name;
          break;
        case actorArray.length - 2:  //`a` is the entry before the last in `actorArray`
          out += `${hyperlink ? doHyperlink(a) : a.entry_name} et `;
          break;
        default:                      // any other entry
          out += `${hyperlink ? doHyperlink(a) : a.entry_name}, `;
      }
    })
  } else {
    out = "Anonyme";
  }
  return out;
}

export function stringifyThemeArray(themeArray, hyperlink=false) {
  const doHyperlink = (theme) => `<a href="${ urlToFrontendTheme(theme.id_uuid).href }"
                                  >${theme.entry_name}</a>`;
  let out = "";
  if ( themeArray != null && themeArray.length ) {
    themeArray.filter(a => a.entry_name != null).map((a, idx) => {
      switch ( idx ) {
        case themeArray.length - 1:  // `a` is the last entry
          out += hyperlink ? doHyperlink(a) : a.entry_name;
          break;
        case themeArray.length - 2:  //`a` is the entry before the last
          out += `${hyperlink ? doHyperlink(a) : a.entry_name} et `;
          break;
        default:                     // any other entry
          out += `${hyperlink ? doHyperlink(a) : a.entry_name}, `;
      }
    })
  }
  return out;
}

export function stringifyNamedEntityArray(namedEntityArray, hyperlink=false) {
  const doHyperlink = (ne) => `<a href="${ urlToFrontendNamedEntity(ne.id_uuid).href }"
                               >${ne.entry_name}</a>`;
  let out = "";
  if ( namedEntityArray != null && namedEntityArray.length ) {
    namedEntityArray.filter(a => a.entry_name != null).map((a, idx) => {
      switch ( idx ) {
        case namedEntityArray.length - 1:  // `a` is the last entry `
          out += hyperlink ? doHyperlink(a) : a.entry_name;
          break;
        case namedEntityArray.length - 2:  // `a` is the entry before the last
          out += `${hyperlink ? doHyperlink(a) : a.entry_name} et `;
          break;
        default:                      // any other entry
          out += `${hyperlink ? doHyperlink(a) : a.entry_name}, `;
      }
    })
  }
  return out;
}

export function stringifyInstitutionArray(institutionArray, hyperlink=false) {
  const doHyperlink = (i) => `<a href="${ urlToFrontendInstitution(i.id_uuid).href }"
                               >${i.entry_name}</a>`;
  let out = "";
  if ( institutionArray != null && institutionArray.length ) {
    institutionArray.filter(a => a.entry_name != null).map((a, idx) => {
      switch ( idx ) {
        case institutionArray.length - 1:  // `a` is the last entry `
          out += hyperlink ? doHyperlink(a) : a.entry_name;
          break;
        case institutionArray.length - 2:  // `a` is the entry before the last
          out += `${hyperlink ? doHyperlink(a) : a.entry_name} et `;
          break;
        default:                      // any other entry
          out += `${hyperlink ? doHyperlink(a) : a.entry_name}, `;
      }
    })
  }
  return out;

}

/**
 * elements that are associated with a resource always have the same
 * structure. here, we centralize their stringification.
 *
 * elements associated, are, for example, named entities that co-occur
 * with a theme. they are fetched from the backend.
 *
 * all associated elements are included in an `<a>`, with a redirection
 * to their main page.
 *
 * @param {Array<Object>} associated: the array of associated objects.
 *  their structure is:
 *  ```
 *  [
 *     # 1st theme
 *     { "id_uuid"    : "<uuid for a theme>",
 *       "entry_name" : "<name of the theme>",
 *       "count"      : "<number of times a theme is associated with the theme on which we run a query>"
 *     },
 *     # other themes
 *     {...}
 *  ]
 *  ```
 * @param {*} targetKey : `targetKey` is a key to determine where
 *  the URL of each `associated` el will redirect to: named entity, theme...
 */
export function stringifyAssociated(associated, targetKey) {
  const urlBuilder = targetKey === "theme" ? urlToFrontendTheme : urlToFrontendNamedEntity;
  const processEl = (el) =>
    `<a href="${urlBuilder((el.id_uuid))}">${el.entry_name}</a>
     (${el.count} co-occurrence${ el.count > 1 ? 's' : '' }`;

  // validate arguments
  if ( ! ["theme", "namedEntity"].includes(targetKey) ) {
    console.error(`ThemeMainView.stringifyAssociated: param 'targetKey'
                   must be one of ["theme", "namedEntity"], got ${targetKey}`)
  }

  let out = "";
  associated.map((el, idx) => {
    switch ( idx ) {
      case associated.length - 1:  // `a` is the last entry in `associated`
        out += processEl(el);
        break;
      case associated.length - 2:  //`a` is the entry before the last in `associated`
        out += `${processEl(el)} et `;
        break;
      default:                     // any other entry
        out += `${processEl(el)}, `;
    }
  })
  return out;
}

