/**********************************************
 *        generally useful functions          *
 **********************************************/

import $ from "jquery";
import { domStore } from "@stores/dom.js";
import { hasTouch } from "@globals";


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
    return ! obj.filter(o => o != null  ).length;
  // for Objects: contains only
  } else if ( typeof(obj)==="object" && obj !== null ) {
    return ! Object.keys(obj).length;
  // for scalars: is == null
  } else {
    return obj == null;
  }
}


/**
 * on touchscreen devices, "when the user touches
 * the screen both touch and click events will occur".
 * this means that, if `hasTouch`, 2 events are fired
 * and we need to make it so that only a single event
 * is processed, using `preventDefault()`.
 *
 * see: https://web.dev/articles/mobile-touchandmouse
 * and: https://web.dev/articles/mobile-touchandmouse#1_-_clicking_and_tapping_-_the_natural_order_of_things
 */
export function cleanClickOrTouchend(event) {
  if ( hasTouch ) {
    event.stopPropagation()
    event.preventDefault();
  }
  return event
}
