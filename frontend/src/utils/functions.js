/**********************************************
 *         globally useful functions          *
 **********************************************/

/**
 * create an URL to an image on the remote server
 * from the cartography table.
 * @param {str} fn : the filename to the image
 * @returns        : the URL to that image
 */
export function fnToCartographyFile(fn) {
  return new URL(`/richelieu/imagefiles/cartography/${fn}`, __SERVER_URL__);
}


/**
 * check that an object is kind of empty.
 * this is a generic function that works for scalars
 * (string, float, int) and complex types (arrays, dicts)
 * @param {any} obj
 * @returns {bool}
 */
export function isKindaEmpty(obj) {
  // for Arrays: contains no elements or only null or undefined elts
  if ( Array.isArray(obj) ) {
    return obj.filter((o) => { return o != null }).length === 0;
  // for Objects: contains only
  } else if ( typeof(obj)==="object" && obj !== null ) {
    return Object.keys(obj).length === 0;
  // for scalars: is == null
  } else {
    return obj == null;
  }
}
