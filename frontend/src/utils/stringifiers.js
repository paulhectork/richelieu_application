/******************************************************
 *        transform objects (`[]`, `{}`) into         *
 *        string representations                      *
 ******************************************************/


/**
 * generate a string representation of a single iconography object
 * (defined in the backend by: Iconography.serialize_lite())
 * @param {Object} i: the iconography object
 * @returns String
 */
export function stringifyIconographyResource(i) {
  let out = "";
  let authors = stringifyAuthorArray(i.authors);
  let date = stringifyDate(i.date);

  out += authors.length ? `${authors}, ` : " ";
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
 * transform an author array into a string
 * an author array has the structure:
 * (`[ {uuid: <uuid>, entry_name: <entry_name>}
 *   , {uuid: <uuid>, entry_name: <entry_name>}
 *   , ... ]`)
 * @param {Array} authorArray
 * @returns str (empty string if `authorArray.length === 0`)
 */
export function stringifyAuthorArray(authorArray) {
  let authorStr = "";
  authorArray.filter(a => a.entry_name != null).map((a, idx) => {
    switch ( idx ) {
      case authorArray.length - 1:  // `a` is the last entry in `authorArray`
        authorStr += a.entry_name;
        break;
      case authorArray.length - 2:  //`a` is the entry before the last in `authorArray`
        authorStr += `${a.entry_name} et `;
        break;
      default:                      // any other entry
        authorStr += `${a.entry_name}, `;
    }
  })
  return authorStr;
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