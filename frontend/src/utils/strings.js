/**
 * generally useful operations on strings
 */

/**
 * capitalize the first letter of string str (all other letters
 * kept as is)
 * @param {string|Any} str: the string to capitalize
 * @returns str if we sent a string, else the input unchanged
 */
export const capitalizeFirstChar = (str) =>
  str != null && typeof str === "string"
  ? str.charAt(0).toUpperCase() + str.slice(1)
  : str;

/**
 * same as above, but all words are capitalized, instead of just the first letter
 */
export const capitalizeWords = (str) =>
  str != null && typeof str === "string"
  ? str.split(" ").map(s =>
      s.charAt(0).toUpperCase() + s.slice(1).toLowerCase()).join(" ")
  : str;
