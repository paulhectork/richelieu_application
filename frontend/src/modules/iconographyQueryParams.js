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

import _ from "lodash";

import { isEmptyArray, isEmptyScalar, isNumberInRange, isValidNumberRange } from "@utils/functions";


export class IconographyQueryParams {
  /**
   * our data fields, undefined by default
   */
  // actual data inputs
  title                = [];         // Array<String> || []
  author               = [];         // Array<String> || []
  publisher            = [];         // Array<String> || []
  theme                = [];         // Array<string> || []
  namedEntity          = [];         // Array<string> || []
  institution          = [];         // Array<string> || []
  dateFilter           = undefined;  // Array<string> || undefined
  date                 = [];         // Array<Number> || []. we prefer our types to always stay the same. `date` will thus always be an array, of length 0 if no data is submitted.
  // boolean operators for each input
  titleBooleanOp       = "and";  // "and"|"or"|"not"
  authorBooleanOp      = "and";  // "and"|"or"|"not"
  publisherBooleanOp   = "and";  // "and"|"or"|"not"
  themeBooleanOp       = "and";  // "and"|"or"|"not"
  namedEntityBooleanOp = "and";  // "and"|"or"|"not"
  institutionBooleanOp = "and";  // "and"|"or"|"not"
  dateBooleanOp        = "and";  // "and"|"or"|"not"

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
   * simplifying the raw, user-inputted values.
   * basically, the processing is:
   * - the boolean operators are left as is
   * - retyping every actual input field to list
   * - cleaning the free text inputs
   * @param {Object} data: the JSON
   */
  fromJson(data) {

    // boolean ops should always be defined in the form.
    // if for some reasonthey aren't, reverd to the default value
    this.titleBooleanOp       = this.booleanOpCleaner(data.titleBooleanOp);
    this.authorBooleanOp      = this.booleanOpCleaner(data.authorBooleanOp);
    this.publisherBooleanOp   = this.booleanOpCleaner(data.publisherBooleanOp);
    this.themeBooleanOp       = this.booleanOpCleaner(data.themeBooleanOp);
    this.namedEntityBooleanOp = this.booleanOpCleaner(data.namedEntityBooleanOp);
    this.institutionBooleanOp = this.booleanOpCleaner(data.institutionBooleanOp);
    this.dateBooleanOp        = this.booleanOpCleaner(data.dateBooleanOp);
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
    this.date = this.extractCleanDate(data.date)
  }
  /**
   * serialize an instance of `IconographyQueryParams` to JSON.
   * using `JSON.parse(JSON.stringify(...))` ensures we end up with a
   * JSON, not a weird proxy object
   * @returns {Object}: the json. the structure is always the
   *  same. if there is no data for a field, it is `undefined`
   */
  toJson() {
    return JSON.parse(JSON.stringify(
      { title                : this.title,
        author               : this.author,
        publisher            : this.publisher,
        theme                : this.theme,
        namedEntity          : this.namedEntity,
        institution          : this.institution,
        dateFilter           : this.dateFilter,
        date                 : this.date,

        titleBooleanOp       : this.titleBooleanOp,
        authorBooleanOp      : this.authorBooleanOp,
        publisherBooleanOp   : this.publisherBooleanOp,
        themeBooleanOp       : this.themeBooleanOp,
        namedEntityBooleanOp : this.namedEntityBooleanOp,
        institutionBooleanOp : this.institutionBooleanOp,
        dateBooleanOp        : this.dateBooleanOp
      }
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

    // booleanOps are pretty easy
    this.titleBooleanOp       = this.booleanOpCleaner(data.titleBooleanOp);
    this.authorBooleanOp      = this.booleanOpCleaner(data.authorBooleanOp);
    this.publisherBooleanOp   = this.booleanOpCleaner(data.publisherBooleanOp);
    this.themeBooleanOp       = this.booleanOpCleaner(data.themeBooleanOp);
    this.namedEntityBooleanOp = this.booleanOpCleaner(data.namedEntityBooleanOp);
    this.institutionBooleanOp = this.booleanOpCleaner(data.institutionBooleanOp);
    this.dateBooleanOp        = this.booleanOpCleaner(data.dateBooleanOp);
    // repeatable text fields are of type Array<String>, with simplified values
    this.title     = this.stringArrayCleanerSimplifier(data.title) || [],
    this.author    = this.stringArrayCleanerSimplifier(data.author) || [],
    this.publisher = this.stringArrayCleanerSimplifier(data.publisher) || [],
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
                  .filter(k =>  k !== "dateFilter" && !k.match(/BooleanOp/g))  // dateFilter and boolean ops have default values but are useless if extra data isn't submitted => remove them
                  .map(k => Array.isArray(data[k])
                            ? isEmptyArray(data[k])
                            : data[k] === undefined )
    ).every(x => x===true)
  }

  /*********************************************/
  /* helper functions */

  /**
   * extract a clean date from what is sent by the form.
   * `FormRepeatableDate` is quite complex: it's a repeatable block of 2 inputs.
   * formDate's structure is:
   * {
   *   <uuid>-date-filter: "dateRange",
   *   <uuid>-date: {
   *     <uuid>-date-dateStart: <1st date of the range>,
   *     <uuid>-date-dateEnd: <2nd date of the range
   *   }
   * }
   * or:
   * {
   *   <uuid>-date-filter: "dateExact|dateBefore|dateAfter",
   *   <uuid>-date: <the date>
   * }
   * retype it to:
   * [ { filter: <the date filter>, data: <the date, as an array of 1 or 2 numbers> }  # 1st date filter
   * , { filter: <the date filter>, data: <the date, as an array of 1 or 2 numbers> }  # 2nd date filter and so on.
   * ]
   * Array<{ filter: string, data: Array<number> }>
   * the output contains no elts with
   * @param {*} formDate: the date, as returned by FormRepeatableDate.vue
   * @returns { Array<{ filter: string, data: Array<number> }> }: the clean date
   */
  extractCleanDate = (formDate) => {
    // the output date object
    let dateOut = [];
    // unique UUIDs, with 1 uuid per date search.
    let dateUuidArray =
      [... new Set(Object.keys(formDate)
                         .map(x => x.replaceAll(/-date-filter$/g, "")
                                    .replaceAll(/-date$/g, "")) )];

    // extract the `date-filter` part of `formDate`.
    const extractDateFilter = (_uuid, _formDate) =>
    _formDate[`${_uuid}-date-filter`];
    const extractDateData = (_uuid, _formDate) =>
      _formDate[`${_uuid}-date-filter`] === "dateRange"
      ? Object.values(_formDate[`${_uuid}-date`])  // if it's a range, then the date is a dict => extract the values
      : [ _formDate[`${_uuid}-date`] ];            // else, it's a (possibly empty) string.

    // build the basic dateOut
    dateUuidArray.map(x => dateOut.push({ filter: extractDateFilter(x, formDate),
                                          data  : extractDateData(x, formDate) }) );

    // find which entries are empty (the `data` key contains only undefined elts, aka there is no inputted date)
    let toDelete = [];  // array of indexes of `dateOut` that we must remove
    dateOut.map((x, idx) => isEmptyArray(x.data) ? toDelete.push(idx) : false );

    // delete the empty entries ; retype `data` in non-empty entries to `Number`
    dateOut = dateOut.filter((x,idx) => !toDelete.includes(idx))
                     .map(x => { return { filter: x.filter, data: x.data.map(Number) } })
    return dateOut;
  }
  /**
   * clean a booleanOp parameter. if it's not valid, revert to the default "and"
   */
  booleanOpCleaner = x => ["and","or","not"].includes(x) ? x : "and";
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
