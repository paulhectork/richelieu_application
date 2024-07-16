/**
 * a class for handling query parameters to the `Iconography`
 * table, especially useful for the `AdvancedSearch*.vue`
 * components. the point of this class is to centralize
 * processing of the user inputted data, and reformatting
 * from and to other useful structures.
 *
 * this function defines 3 data structures:
 * * internal data structure, with data fields and
 *   helper functions. see below for types
 * * json: this is a jsonified version quite similar
 *   to the internal data structure, with only the data
 *   fields present (no functions...)
 * * URL route parameters: this is the same as the json,
 *   structure (only data, no functions), except that,
 *   for our route params to be compatible with vue-router,
 *   it must be an object that contains only primitives and
 *   arrays. so the dict-like object (like dates), must
 *   be flattened when converting from internal to route,
 *   and unflattened when converting from route to internal.
 *
 * there are helper functions to:
 * * read and write `IconographyQueryParams` objects
 *   to and from JSON
 * * read and write `IconographyQueryParams` objects
 *   to and from and from URL parameters.
 * * clean the data user inputted data
 * * check if the user inputted data is empty
 *
 */

import _ from "lodash";
import F from "futil-js";

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
  date                 = [];         // Array<{ filter: string, data: Array<number> }> || []. we prefer our types to always stay the same. `date` will thus always be an array, of length 0 if no data is submitted.
  // boolean operators for each input
  titleBooleanOp       = "and";      // "and"|"not"
  authorBooleanOp      = "and";      // "and"|"not"
  publisherBooleanOp   = "and";      // "and"|"not"
  themeBooleanOp       = "and";      // "and"|"not"
  namedEntityBooleanOp = "and";      // "and"|"not"
  institutionBooleanOp = "and";      // "and"|"not"
  dateBooleanOp        = "and";      // "and"|"not"

  // utils properties
  toFlatten = ["date"];  // the fields to flatten/unflatten when converting to/from URLs. (fields which contain objects are stringified to `[objectObject]` by `vue-router`, we need to flatten them so their value can be readable in the URL)


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
   * @example
   * INPUT:
   * => {
   * =>   "titleBooleanOp": "and",
   * =>   "title": [ "le moniteur de la mode" ],
   * =>   "authorBooleanOp": "and",
   * =>   "author": [ "atget", "daumier" ],
   * =>   "publisherBooleanOp": "and",
   * =>   "dateBooleanOp": "and",
   * =>   "date": {
   * =>     "form-repeatable-date-00c0ea0a-bb45-4af1-a9cf-82b4588d002b-date-filter": "dateRange",
   * =>     "form-repeatable-date-00c0ea0a-bb45-4af1-a9cf-82b4588d002b-date": {
   * =>       "form-repeatable-date-00c0ea0a-bb45-4af1-a9cf-82b4588d002b-dateStart": "1860",
   * =>       "form-repeatable-date-00c0ea0a-bb45-4af1-a9cf-82b4588d002b-dateEnd": "1900"
   * =>     },
   * =>     "form-repeatable-date-4f6f4b60-f607-461d-ab32-59c8011a304b-date-filter": "dateBefore",
   * =>     "form-repeatable-date-4f6f4b60-f607-461d-ab32-59c8011a304b-date": "1850"
   * =>   },
   * =>   "themeBooleanOp": "and",
   * =>   "theme": [ "actualité", "architecture" ],
   * =>   "namedEntityBooleanOp": "and",
   * =>   "namedEntity": [ "Ardit éditeur" ],
   * =>   "institutionBooleanOp": "and",
   * =>   "institution": [ "Musée Carnavalet" ]
   * => }
   * OUTPUT:
   * => {
   * =>   "title": [ "le moniteur de la mode" ],
   * =>   "author": [ "atget", "daumier" ],
   * =>   "publisher": [],
   * =>   "theme": [ "actualité", "architecture" ],
   * =>   "namedEntity": [ "Ardit éditeur" ],
   * =>   "institution": [ "Musée Carnavalet" ],
   * =>   "date": [
   * =>     {
   * =>       "filter": "dateRange",
   * =>       "data": [ 1860, 1900 ]
   * =>     },
   * =>     {
   * =>       "filter": "dateBefore",
   * =>       "data": [ 1850 ]
   * =>     }
   * =>   ],
   * =>   "titleBooleanOp": "and",
   * =>   "authorBooleanOp": "and",
   * =>   "publisherBooleanOp": "and",
   * =>   "themeBooleanOp": "and",
   * =>   "namedEntityBooleanOp": "and",
   * =>   "institutionBooleanOp": "and",
   * =>   "dateBooleanOp": "and",
   * => }
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
    this.title     = this.stringArrayCleanerSimplifier(data.title);
    this.author    = this.stringArrayCleanerSimplifier(data.author);
    this.publisher = this.stringArrayCleanerSimplifier(data.publisher);
    // select fields are of type Array<string>, without simplified values
    // (only the null-ish values are removed)
    this.theme       = this.stringArrayCleaner(data.theme);
    this.namedEntity = this.stringArrayCleaner(data.namedEntity);
    this.institution = this.stringArrayCleaner(data.institution);
    this.dateFilter  = data.dateFilter;
    // dates are converted to numbers. we remove `undefined` items.
    this.date = this.extractCleanDate(data.date);
  }
  /**
   * serialize an instance of `IconographyQueryParams` to JSON.
   * without using `lodash.cloneDeep`, all values are proxies.
   * using _.cloneDeep converts proxies to normal objects.
   *
   * @example
   * OUTPUT:
   * => {
   * =>   "title": [ "le moniteur de la mode" ],
   * =>   "author": [ "atget", "daumier" ],
   * =>   "publisher": [],
   * =>   "theme": [ "actualité", "architecture" ],
   * =>   "namedEntity": [ "Ardit éditeur" ],
   * =>   "institution": [ "Musée Carnavalet" ],
   * =>   "date": [
   * =>     {
   * =>       "filter": "dateRange",
   * =>       "data": [ 1860, 1900 ]
   * =>     },
   * =>     {
   * =>       "filter": "dateBefore",
   * =>       "data": [ 1850 ]
   * =>     }
   * =>   ],
   * =>   "titleBooleanOp": "and",
   * =>   "authorBooleanOp": "and",
   * =>   "publisherBooleanOp": "and",
   * =>   "themeBooleanOp": "and",
   * =>   "namedEntityBooleanOp": "and",
   * =>   "institutionBooleanOp": "and",
   * =>   "dateBooleanOp": "and"
   * => }
   *
   * @returns {Object}: the json. the structure is always the
   *  same. if there is no data for a field, it is `[]`
   */
  toJson() {
    return _.cloneDeep({ title                : this.title,
                         author               : this.author,
                         publisher            : this.publisher,
                         theme                : this.theme,
                         namedEntity          : this.namedEntity,
                         institution          : this.institution,
                         date                 : this.date,

                         titleBooleanOp       : this.titleBooleanOp,
                         authorBooleanOp      : this.authorBooleanOp,
                         publisherBooleanOp   : this.publisherBooleanOp,
                         themeBooleanOp       : this.themeBooleanOp,
                         namedEntityBooleanOp : this.namedEntityBooleanOp,
                         institutionBooleanOp : this.institutionBooleanOp,
                         dateBooleanOp        : this.dateBooleanOp
    });
  }
  /**
   * populate the object from a route's query params.
   *
   * this is quite similar to `fromJson()`, except that:
   * * we're fetching data from the route, and not from a form
   * * the keys in `data` we're looking for may be undefined
   * * we need to unflatten the objects that were flattened
   *
   * why re-clean data from RouteParams when it has aldready
   * been cleaned in `this.fromJson()` ?
   * hand-manipulation of a URL string can lead to incoherences:
   * we expect a field to be an array (like `date`), but a single
   * value is in the URL and vue-router interprets it as a scalar.
   * here, we enforce our types and clean our data
   * to avoid errors down the road
   *
   * @param {object} data: the query params returned by
   *  vue-router's `useRoute().query`.
   * @example
   * INPUT:
   * => {
   * =>   "title": [ "le moniteur de la mode" ],
   * =>   "author": [ "atget", "daumier" ],
   * =>   "publisher": [],
   * =>   "theme": [ "actualité", "architecture" ],
   * =>   "namedEntity": [ "Ardit éditeur" ],
   * =>   "institution": [ "Musée Carnavalet" ],
   * =>   "dateBooleanOp": "and",
   * =>   "date.0.filter": "dateRange",
   * =>   "date.0.data.0": "1860",
   * =>   "date.0.data.1": "1900",
   * =>   "date.1.filter": "dateBefore",
   * =>   "date.1.data.0": "1850",
   * =>   "titleBooleanOp": "and",
   * =>   "authorBooleanOp": "and",
   * =>   "publisherBooleanOp": "and",
   * =>   "themeBooleanOp": "and",
   * =>   "namedEntityBooleanOp": "and",
   * =>   "institutionBooleanOp": "and"
   * => }
   * OUTPUT (functions removed for clarity):
   * => {
   * =>   "title": [ "le moniteur de la mode" ],
   * =>   "author": [ "atget", "daumier" ],
   * =>   "publisher": [],
   * =>   "theme": [ "actualité", "architecture" ],
   * =>   "namedEntity": [ "Ardit éditeur" ],
   * =>   "institution": [ "Musée Carnavalet" ],
   * =>   "date": [
   * =>     {
   * =>       "filter": "dateRange",
   * =>       "data": [ 1860, 1900 ]
   * =>     },
   * =>     {
   * =>       "filter": "dateBefore",
   * =>       "data": [ 1850 ]
   * =>     }
   * =>   ],
   * =>   "titleBooleanOp": "and",
   * =>   "authorBooleanOp": "and",
   * =>   "publisherBooleanOp": "and",
   * =>   "themeBooleanOp": "and",
   * =>   "namedEntityBooleanOp": "and",
   * =>   "institutionBooleanOp": "and",
   * =>   "dateBooleanOp": "and",
   * =>   "toFlatten": [ "date" ]
   * => }
   */
  fromRouteParams(data) {
    // first, we need to extract the params in `data` which
    // were flattened using `F.flattenObject` and unflatten
    // them, so they can get back to their internal structure)
    let unflatObjs = {}  // output of unflattened objects
    this.toFlatten.forEach(t => {
      let r = new RegExp(`^${t}\\.`);
      let unflattenKeys = Object.keys(data).filter(k => k.match(r));
      let unflat = F.unflattenObject(_.pick( data, unflattenKeys ));
      _.merge(unflatObjs, unflat);
    })

    // function to process the date field. basically we just
    // retype items in the `data` array from strings to numbers
    const unflatDate = (_unflatObjs) => {
      if ( Object.keys(_unflatObjs).includes("date") ) {
        let d = _unflatObjs.date;
        return d.filter(x => x.data.length).map(x => {
          return { filter: x.filter, data: x.data.map(this.string2number) } })
      }
      return [];  // default output
    }

    // then, we populate `this` from `data`, using the unflattened objects.
    // booleanOps are pretty easy
    this.titleBooleanOp       = this.booleanOpCleaner(data.titleBooleanOp);
    this.authorBooleanOp      = this.booleanOpCleaner(data.authorBooleanOp);
    this.publisherBooleanOp   = this.booleanOpCleaner(data.publisherBooleanOp);
    this.themeBooleanOp       = this.booleanOpCleaner(data.themeBooleanOp);
    this.namedEntityBooleanOp = this.booleanOpCleaner(data.namedEntityBooleanOp);
    this.institutionBooleanOp = this.booleanOpCleaner(data.institutionBooleanOp);
    this.dateBooleanOp        = this.booleanOpCleaner(data.dateBooleanOp);
    // repeatable text fields are of type Array<String>, with simplified values
    this.title     = this.stringArrayCleanerSimplifier(data.title) || [];
    this.author    = this.stringArrayCleanerSimplifier(data.author) || [];
    this.publisher = this.stringArrayCleanerSimplifier(data.publisher) || [];
    // select fields are of type Array<string>, but don't need simplification
    this.theme       = this.stringArrayCleaner(data.theme) || [];
    this.namedEntity = this.stringArrayCleaner(data.namedEntity) || [];
    this.institution = this.stringArrayCleaner(data.institution) || [];
    // dates are converted to numbers. we remove `undefined` items.
    this.date        = unflatDate(unflatObjs);
  }
  /**
   * return an object of query parameters to update the router.
   * vue-router exepects params to be a flat object (that is, an
   * object that contains only primitives or arrays). so we need
   * to flatten the fields defined in `this.toFlatten`. else, the
   * objects are stringified to `[objectObject]`
   *
   * see: https://github.com/smartprocure/futil-js/tree/master?tab=readme-ov-file#flattenobject)
   *
   * @example
   * OUTPUT:
   * => {
   * =>   "title": [ "le moniteur de la mode" ],
   * =>   "author": [ "atget", "daumier" ],
   * =>   "publisher": [],
   * =>   "theme": [ "actualité", "architecture" ],
   * =>   "namedEntity": [ "Ardit éditeur" ],
   * =>   "institution": [ "Musée Carnavalet" ],
   * =>   "dateBooleanOp": "and",
   * =>   "date.0.filter": "dateRange",
   * =>   "date.0.data.0": 1860,
   * =>   "date.0.data.1": 1900,
   * =>   "date.1.filter": "dateBefore",
   * =>   "date.1.data.0": 1850,
   * =>   "titleBooleanOp": "and",
   * =>   "authorBooleanOp": "and",
   * =>   "publisherBooleanOp": "and",
   * =>   "themeBooleanOp": "and",
   * =>   "namedEntityBooleanOp": "and",
   * =>   "institutionBooleanOp": "and"
   * => }
   * @returns {object}
   */
  toRouteParams() {
    let out = _.omit(this.toJson(), this.toFlatten);  // _.omit removes the keys in `toFlatten` from our json.

    this.toFlatten.forEach(k => {
      let obj = {};
      obj[k] = this.toJson()[k];
      _.merge( out, F.flattenObject(obj) );  // merge adds fields from `obj` to `out`
    })

    return out;
  }

  /**
   * check if all data fields are empty.
   * @returns {bool}: `true` if all fields are empty
   */
  allEmpty() {
    const data = this.toJson();
    return Object.keys(data)
                  // dateFilter and boolean ops have default values but are useless if extra data isn't submitted => remove them
                  .filter(k =>  k !== "dateFilter" && !k.match(/BooleanOp/g))
                  // a field is empty if it's an empty array or if it's undefined
                  .every(k => Array.isArray(data[k])
                              ? isEmptyArray(data[k])
                              : data[k] === undefined )
  }

  /*********************************************/
  /* helper functions */

  /**
   * extract a clean date from what is sent by the form.
   * the date is sent from `FormRepeatableDate`, which is
   * quite complex: it's a repeatable block of 2 inputs,
   * the date filter and the date data.
   * its contents are passed here as the arg `formDate`.
   * a filter + data couple share the same base, an
   * unique id, identified below as `<uuid>`
   *
   * formDate's structure is:
   * => {
   * =>   <uuid>-date-filter: "dateRange",
   * =>   <uuid>-date: {
   * =>     <uuid>-date-dateStart: <1st date of the range>,
   * =>     <uuid>-date-dateEnd: <2nd date of the range
   * =>   }
   * => }
   * or:
   * => {
   * =>   <uuid>-date-filter: "dateExact"|"dateBefore"|"dateAfter",
   * =>   <uuid>-date: <the date>
   * => }
   *
   * this function transforms the date to:
   * => [ { filter: <the date filter>, data: <the date, as an array of 1 or 2 numbers> }  # 1st date filter
   * => , { filter: <the date filter>, data: <the date, as an array of 1 or 2 numbers> }  # 2nd date filter and so on.
   * => ]
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

    // helper functions.
    // extract the `date-filter` part of `formDate`.
    const extractDateFilter = (_uuid, _formDate) =>
    _formDate[`${_uuid}-date-filter`];
    // extract the `date` part of `formDate`.
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
   * if `x` is not in [and,or,not] but is undefined, just return "and" (by default,
   * boolean ops can be undefined). else, log an error message and return "and".
   */
  booleanOpCleaner = x =>
    // ["and","or","not"].includes(x)
    ["and","not"].includes(x)
    ? x
    : "and"
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
