/*******************************************
 * custom formkit validation rules,
 * helper functions and validation messages
 *
 * see:
 * https://formkit.com/essentials/validation#defining-custom-rule-behaviors
 * https://formkit.com/essentials/validation#custom-messages
 *******************************************/

import { isEmptyArray
       , isEmptyScalar
       , isNumberInRange
       , isValidNumberRange } from "@utils/functions";

/*******************************************/
// the rules

/**
 * date validation in a nutshell:
 *
 * a date must be in format 'AAAA' and within a date
 * range specified in the formkit element using the
 * HTML attribute `data-allowedDateRange`. if we are
 * validating a date range (2 formkit inputs of type
 * number), then the second date input must be higher
 * than the first one.
 */

/**
 * fetch the allowed date range from a formkit node.
 * it is expected to contain an attribute `data-allowedDateRange`
 * with the date range to validate. if the node does not contain
 * this attribute, a default range is returned
 *
 * @param {FormKitNode} node: the HTML node to validate.
 * @returns {Array<int>}: the allowed date range
 */
export function getAllowedDateRange(node) {
  if ( Object.keys(node.context.attrs).includes("data-allowedDateRange")
     && node.context.attrs["data-allowedDateRange"].length
  ) {
    return node.context.attrs["data-allowedDateRange"];
  } else {
    console.warn("formValidationRules.dateRangeValidator: `data-allowedDateRange` attribute not provided in FormKit element, reverting to default allowed range [1700,2100].")
    return [1700,2100];
  }
}


/**
 * validate a single date
 * @param {FormKitNode} node: the node to validate
 * @returns {boolean}
 */
export function dateValidator(node) {
  let allowedDateRange = getAllowedDateRange(node);
  return isNumberInRange(node.value, allowedDateRange)
}


/**
 * validate a date range. a date range is made of two
 * FormKit elements with @type="number", and this validator
 * is placed on both elements. it checks the validity of both
 * number fields by comparing their values:
 * if at least one field is filled, we check that our range is valid
   else, both our fields are empty, so it's valid
 * @param {FormKitNode} node: the formkit date node to validate
 * @returns {boolean}
 */
export function dateRangeValidator(node) {
  let allowedDateRange = getAllowedDateRange(node);
  let parent = node.at("$parent");

  if ( parent.value ) {
    let dateRange = [ parent.value.dateStart, parent.value.dateEnd ];
    return dateRange.some(x => x!=null)
           ? dateRange.every(x => isNumberInRange(x, allowedDateRange) )  // every number is in the allowed range
             && isValidNumberRange(dateRange)                             // dateStart < dateEnd
           : true;
  }
  return true;
}

/**
 * text validation in a nutshell:
 *
 * all text elements must be either empty or have a length of 3+
 */
const validateText = (txt) =>
  isEmptyScalar(txt) || typeof txt === "string" && txt.length >= 3;

/**
 * validate a single text element
 * @param {FormKitNode} node : the node to validate
 * @returns {boolean}
 */
export function textValidator(node) {
  return validateText(node.value);
}
/**
 * validate a repeatable text element
 * @param {FormKitNode} node: the node to validate
 * @returns {boolean}
 */
export function textArrayValidator(node) {
  return node.value.every(validateText);
}


/*******************************************/
// the messages

// for a text element, or a repeatable text element.
export const textValidatorMessage = "La valeur entrée doit comporter au moins 3 caractères."

// for a single date
export const dateValidatorMessage = ([name, args, node]) => {
  let allowedDateRange = getAllowedDateRange(node);
  return `La date doit être au format 'AAAA' et comprise entre
          ${allowedDateRange[0]} et ${allowedDateRange[1]}`};

// for a date range
export const dateRangeValidatorMessage = ([name, args, node]) => {
  let allowedDateRange = getAllowedDateRange(node);
  return `La tranche de dates doit composée de deux dates au format 'AAAA',
          comprises entre ${allowedDateRange[0]} et ${allowedDateRange[1]}` };
