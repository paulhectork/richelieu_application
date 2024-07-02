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
  title       = [];         // Array<String> || []
  author      = [];         // Array<String> || []
  publisher   = [];         // Array<String> || []
  theme       = [];         // Array<string> || []
  namedEntity = [];         // Array<string> || []
  institution = [];         // Array<string> || []
  dateFilter  = undefined;  // Array<string> || undefined
  date        = [];         // Array<Number> || []. we prefer our types to always stay the same. `date` will thus always be an array, of length 0 if no data is submitted.

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
      throw new Error(`iconographyQueryParams.constructor: invalid value for 'from'.
                       expected one of ${allowed}, got ${from}`)
    }
    if ( from==="form" ) { this.fromJson(data) }
    else                 { this.fromRouteParams(data)  };
  }

  /*********************************************/
  /* main methods */

  /**
   * populate the object from a JSON sent from the
   * `AdvancedSearchQuery` form. this includes
   * simplifying the raw, user-inputted values
   * @param {Object} data: the JSON
   */
  fromJson(data) {
    // repeatable text fields are of type Array<String>, with simplified values
    // (no undefined or null-ish values, simplified strings)
    this.title     = this.stringArrayCleanerSimplifier(data.title),
    this.author    = this.stringArrayCleanerSimplifier(data.author),
    this.publisher = this.stringArrayCleanerSimplifier(data.publisher),
    // select fields are of type Array<string>, without simplified values
    // (only the null-ish values are removed)
    this.theme       = this.stringArrayCleaner(data.theme),
    this.namedEntity = this.stringArrayCleaner(data.namedEntity),
    this.institution = this.stringArrayCleaner(data.institution),
    this.dateFilter  = data.dateFilter,
    // dates are converted to numbers. we remove `undefined` items.
    this.date = (data.dateFilter === "dateRange"
                ? [ data.date.dateStart, data.date.dateEnd ]
                : [ data.date ]
                ).map(this.scalar2undefined)
                 .filter(x => x !== undefined)
                 .map(this.string2number)
  }
  /**
   * serialize an instance of `IconographyQueryParams` to JSON.
   * using `JSON.parse(JSON.stringify)` ensures we end up with a
   * JSON, not a weird proxy object
   * @returns {Object}: the json. the structure is always the
   *  same. if there is no data for a field, it is `undefined`
   */
  toJson() {
    return JSON.parse(JSON.stringify(
      { title       : this.title,
        author      : this.author,
        publisher   : this.publisher,
        theme       : this.theme,
        namedEntity : this.namedEntity,
        institution : this.institution,
        dateFilter  : this.dateFilter,
        date        : this.date }
    ))
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
    // why re-clean data from RouteParams when it has aldready
    // been cleaned in `this.fromJson()` ?
    // hand-manipulation of a URL string can lead to incoherences:
    // we expect a field to be an array (like `date`), but a single
    // value is in the URL and vue-router interprets it as a scalar.
    // here, we enforce our types and clean our data
    // to avoid errors down the road

    // repeatable text fields are of type Array<String>, with simplified values
    this.title       = this.stringArrayCleanerSimplifier(data.title) || [],
    this.author      = this.stringArrayCleanerSimplifier(data.author) || [],
    this.publisher   = this.stringArrayCleanerSimplifier(data.publisher) || [],
    // select fields are of type Array<string>, but don't need simplification
    this.theme       = this.stringArrayCleaner(data.theme) || [],
    this.namedEntity = this.stringArrayCleaner(data.namedEntity) || [],
    this.institution = this.stringArrayCleaner(data.institution) || [],
    // dateFilter does not need simplification either, and is a string
    this.dateFilter  = data.dateFilter,
    // dates are converted to numbers. we remove `undefined` items.
    this.date        = this.ensureIsArray(data.date)
                           .filter(x => x!=null)
                           .map(this.string2number) || [];
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

  /*********************************************/
  /* helper functions */

  /**
   * clean a flat string array (that is, an array made only
   * of scalars) by removing values that are null or undefined
   * AND simplifying the string values
   */
  stringArrayCleanerSimplifier = arr =>
    this.ensureIsArray(arr)
    .map(this.scalar2undefined)
    .filter(x => x !== undefined)
    .map(this.simplifyString);
  /**
   * clean a flat string array (that is, an array made only
   * of scalars) by removing values that are null or undefined
   * WITHOUT simplifying the string values
   */
  stringArrayCleaner = arr =>
    this.ensureIsArray(arr)
    .map(this.scalar2undefined)
    .filter(x => x !== undefined);
  /**
   * ensure `x` is a scalar. returns `undefined` if these is no `x[0]`
   */
  ensureIsScalar = x => Array.isArray(x) ? x[0] || undefined : x;
  /**
   * ensure `x` is an array.
   */
  ensureIsArray = x => Array.isArray(x) ? x : [x] ;
  /**
   * simplify the string `s`
   */
  simplifyString = s =>
    s !== undefined
    ? s.toLowerCase().trim().replaceAll(/\s+/g, " ")
    : s;
  /**
   * replace scalar `s` by `undefined` if the scalar `s` contains no data.
   */
  scalar2undefined = s => isEmptyScalar(s) ? undefined : s ;
  /**
   * retype a string-representation of a number to a number
   */
  string2number = s => typeof s === "string" && !isNaN(s) ? Number(s) : s;
}
