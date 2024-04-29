/**********************************************
 *         globally useful functions          *
 **********************************************/

import $ from "jquery";


/**
 * create an URL to an image on the remote server
 * from the cartography/iconography table.
 * @param {str} fn : the filename to the image
 * @returns        : the URL to that image
 */
export function fnToCartographyFile(fn) {
  return new URL(`/statics/cartography/${fn}`, __SERVER_URL__);
}
export function fnToIconographyFile(fn) {
  return new URL(`/statics/iconography/${fn}`, __SERVER_URL__);
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


/**
 * this function avoids the double firing of the `click touchend` event,
 * used to detect click on both mobile and desktop.
 *
 * on touch screens, `touchend` is an equivalent for the `click`
 * DOM event => we target click on mobile+desktop by listening
 * to "click touchend" event. however, this can cause a
 * click-like event to be fired twice (once for click, once
 * for touchend).
 *
 * WARNING: can cause bugs and cancel other click events being fired.
 * see: https://stackoverflow.com/questions/25572070/javascript-touchend-versus-click-dilemma
 */
export function cleanClickOrTouchend(event) {
  event.stopPropagation();
  event.preventDefault();
  return event
}