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


/**
 * check that an object is kind of empty.
 * this is a generic function that works for scalars
 * (string, float, int) and complex types (arrays, dicts)
 * @param {any} obj
 * @returns {bool}
 */
export const isKindaEmpty = (obj) =>
  Array.isArray(obj)                        // for Arrays: contains no elements or only null or undefined elts
  ? !obj.filter(o => o != null  ).length
  : typeof(obj)==="object" && obj !== null  // for Objects (dict-like): contains no keys
  ? !Object.keys(obj).length
  : typeof(obj)==="string"                  // for strings: has no length
  ? obj.length === 0
  : obj == null;                            // else: is null or undefined


/**
 * a scalar (undefined, null, string or number) contains no data
 * @param {undefined | null | String | Number} s: the scalar we want to test
 * @returns {bool}
 */
export const isEmptyScalar = s =>
  s === undefined || s === null || s === "" || s.length === 0;


/**
 * an array is empty, or it contains only elements with no data
 * @param {Array} s: the array we want to test
 * @returns {bool}
 */
export const isEmptyArray = a => a.length === 0 || a.every(x => isEmptyScalar(x));


/**
 * assert that `num` can be contained in the array `numRange`
 * @param {string|undefined} num: a string that must be serializable as a number
 * @param {Array<Number>} rangeArray: the array into which `num` must be comprised. length=2
 */
export const isNumberInRange = (num, rangeArray) =>
  !isNaN(num)
  && Number(num) >= rangeArray[0]
  && Number(num) <= rangeArray[1];

/**
 * check `numRange` is an array of 2 strings that can be represented
 * as numbers, with `numRange[0] <= numRange[1]`
 * @param {Array<string>} numRange: an array of 2 strings that are expected to be numbers
 */
export const isValidNumberRange = numRange =>
  numRange.every(x => !isNaN(x))
  && Number(numRange[0]) <= Number(numRange[1]);

