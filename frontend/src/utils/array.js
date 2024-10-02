/**
 * globally useful array-processing functions
 */

import { cartographySourcePriority } from "@globals";


/**
 * reorder an array of `address` objects by the order specified in `cartographySourcePriority`
 * @param {Array<Object>} arr: the array of `address` objects
 * @returns {Array<Object}
 */
export const sortAddressBySource = (arr) =>
  arr.sort((a,b) =>
    arr.indexOf(a.source) - cartographySourcePriority.indexOf(b.source));

/**
 * reorder an array of `cartography` objects by the order specified in `cartographySourcePriority`
 * @param {Array<Object>} arr: the array of `cartography` objects
 * @returns {Array<Object}
 */
export const sortCartographyBySource = (arr) =>
  arr.sort((a,b) =>
    cartographySourcePriority.indexOf(a) - cartographySourcePriority.indexOf(b))
