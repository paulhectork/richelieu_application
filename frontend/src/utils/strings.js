/**
 * generally useful operations on strings
 */

/**
 * capitalize the first letter of string `s`
 * (all other letters kept as is)
 * @param {string|Any} s: the string to capitalize
 * @returns s if we sent a string, else the input unchanged
 */
export const capitalizeFirstChar = (s) =>
  s != null && typeof s === "string"
  ? s.charAt(0).toUpperCase() + s.slice(1)
  : s;

/**
 * same as above, but all words are capitalized,
 * instead of just the first letter of the string
 */
export const capitalizeWords = (s) =>
  s != null && typeof s === "string"
  ? s.split(" ").map(s =>
      s.charAt(0).toUpperCase() + s.slice(1).toLowerCase()).join(" ")
  : s;

/**
 * simplify the string `s`
 */
export const simplifyString = s =>
  s !== undefined
  ? s.toLowerCase().trim().replaceAll(/\s+/g, " ")
  : s;

/**
 * same as the above, but on top of that we also normalize all accented characters
 */
export const simplifyAndUnaccentString = s =>
  s != null && typeof s === "string"
  ? s.toLowerCase()
     .replaceAll(/\s+/g, " ")
     .normalize("NFD")
     .replace(/[\u0300-\u036f]/g, "")
     .trim()
  : s;


/**
 * remove html tags from the string `_string`
 */
export const stripHtml = s => s.replace(/<[^>]*>?/gm, '');

