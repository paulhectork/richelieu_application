/**
 * a class for handling query parameters to the `Iconography`
 * table, especially useful for the `AdvancedSearch*.vue`
 * components. the point of this class is to centralize
 * processing of the user inputted data, and reformatting
 * from and to other useful structures.
 *
 * basically this is a boosted JSON of the form query.
 * there are helper functions to:
 * * read and write `IconographyQueryParams` objects
 *   to and from JSON
 * * read and write `IconographyQueryParams` objects
 *   to and from and from URL parameters.
 * * clean the data user inputted data
 * * check if the user inputted data is empty
 */

import { isEmptyArray, isEmptyScalar, isNumberInRange, isValidNumberRange } from "@utils/functions";


export class IconographyQueryParams {
  /**
   * our data fields, undefined by default
   */
  title       = undefined;
  author      = undefined;
  publisher   = undefined;
  theme       = undefined;
  namedEntity = undefined;
  institution = undefined;
  dateFilter  = undefined;
  date        = [];  // we prefer our types to always stay the same. `date` will thus always be an array, of length 0 if no data is submitted.

  /**
   * create the `IconographyQueryParams`
   * @param {string|Object} data: the data to populate
   *  `IconographyQueryParams` from, either:
   *  * if `from === 'form'`, a JSON returned by
   *    `AdvancedSearchQuery`'s submit event.
   *  * if `from === 'route'`, the route query,
   *    as obtained by vue-router's `useRoute().query`
   * @param {string} from: "form"|"route": create the object
   *  from a JSON string or from a URL.
   */
  constructor(data, from) {
    const allowed = ["form","route"];
    if ( !allowed.includes(from) ) {
      throw new Error(`iconographyQueryData.constructor: invalid value for 'from'.
                       expected one of ${allowed}, got ${from}`)
    }
    if ( from==="form" ) { this.fromJson(data) }
    else                 { this.fromRouteParams(data)  };
  }
  /**
   * populate the object from a JSON sent from the
   * `AdvancedSearchQuery` form. this includes
   * simplifying the raw, user-inputted values
   * @param {Object} data: the JSON
   */
  fromJson(data) {
    // simplify a string
    const simplifyString = s =>
      s !== undefined
      ? s.toLowerCase().trim().replaceAll(/\s+/g, " ")
      : s;

    // all null-ish values are converted to undefined.
    // raw text fields are simplified
    this.title     = simplifyString( this.scalar2undefined(data.title) ),
    this.author    = simplifyString( this.scalar2undefined(data.author) ),
    this.publisher = simplifyString( this.scalar2undefined(data.publisher) ),
    // select and radio fields don't need simplification
    this.theme       = this.scalar2undefined(data.theme),
    this.namedEntity = this.scalar2undefined(data.namedEntity),
    this.institution = this.scalar2undefined(data.institution),
    this.dateFilter  = data.dateFilter,
    // dates are converted to numbers. we remove `undefined` items.
    this.date = (data.dateFilter === "dateRange"
                ? [ data.date.dateStart, data.date.dateEnd ]
                : [ data.date ]
                ).map(this.scalar2undefined)
                 .filter(x => x !== undefined)
                 .map(this.string2number)
                 // .map(x => console.log(x, x === "string" && !isNaN(x)) && x);
  }
  /**
   * serialize an instance of `IconographyQueryParams` to JSON
   * @returns {object}: the json. the structure is always the
   *  same. if there is no data for a field, it is `undefined`
   */
  toJson() {
    return { title       : this.title,
             author      : this.author,
             publisher   : this.publisher,
             theme       : this.theme,
             namedEntity : this.namedEntity,
             institution : this.institution,
             dateFilter  : this.dateFilter,
             date        : this.date }
  }
  /**
   * populate the object from a route's query params.
   *
   * this is quite similar to `fromJson()`, except that:
   * * we're fetching data from the route, and not from a form
   * * the keys in `data` we're looking for may be undefined
   * * the URL data is aldready clean (it's created from
   *   from data, that has passed through `fromJson()` ),
   *   so there's no need to simplify the values.
   *
   * @param {object} data: the query params returned by
   *  vue-router's `useRoute().query`.
   */
  fromRouteParams(data) {
    data.date = Array.isArray(data.date) ? data.date : [ data.date ];  // retype date to array

    this.title       = this.scalar2undefined(data.title) || undefined,
    this.author      = this.scalar2undefined(data.author) || undefined,
    this.publisher   = this.scalar2undefined(data.publisher) || undefined,
    // select and radio fields don't need simplification
    this.theme       = this.scalar2undefined(data.theme) || undefined,
    this.namedEntity = this.scalar2undefined(data.namedEntity) || undefined,
    this.institution = this.scalar2undefined(data.institution) || undefined,
    this.dateFilter  = data.dateFilter,
    // dates are converted to numbers. we remove `undefined` items.
    this.date = data.date.map(this.string2number) || [];
  }
  /**
   * return an object of query parameters to update the router
   * @returns {object}
   */
  toRouteParams() {
    return this.toJson();
  }
  /**
   * check if all data fields are empty.
   * @returns {bool}: `true` if all fields are empty
   */
  allEmpty() {
    const data = this.toJson();
    return (Object.keys(data)
                  .filter(k =>  k !== "dateFilter")  // dateFilter has a default value but is useless if a date isn't submitted => remove it
                  .map(k => Array.isArray(data[k])
                            ? isEmptyArray(data[k])
                            : data[k] === undefined )
    ).every(x => x===true)
  }
  /**
   * replace scalar `s` by `undefined` if the scalar `s` contains no data.
   */
  scalar2undefined = s => isEmptyScalar(s) ? undefined : s ;
  /**
   * retype a string-representation of a number to a number
   */
  string2number = s => typeof s === "string" && !isNaN(s) ? Number(s) : s;
}
