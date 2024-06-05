/******************************************************
 *        transform objects (`[]`, `{}`) into         *
 *        string representations                      *
 ******************************************************/


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
  console.log(authors);
  let date = stringifyDate(i.date);

  out += authors.length ? `${authors}, ` : "";
  out += i.title.length ? `<i>${ i.title[0] }</i> ` : " ";
  out += date.length ? `(${date})` : "";
  return out;
}

/**
 * stringify a single address object
 */
export function stringifyAddressResource(a) {
  let out = "";
  out += (a.number != null) ? `${a.number}, ` : "";
  out += a.street.length ? `${a.street} `  : "";
  out += "(Paris, France)"
  return out
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
  const doHyperlink = (actor) => `<a href="${ new URL(`/acteur/${actor.id_uuid}`, window.location.href).href }"
                                     >${actor.entry_name}</a>`
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
  const doHyperlink = (theme) => `<a href="${ new URL(`/theme/${theme.id_uuid}`, window.location.href).href }"
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
  const doHyperlink = (ne) => `<a href="${ new URL(`/sujet/${ne.id_uuid}`, window.location.href).href }"
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
  const doHyperlink = (i) => `<a href="${ new URL(`/institution/${i.id_uuid}`, window.location.href).href }"
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
