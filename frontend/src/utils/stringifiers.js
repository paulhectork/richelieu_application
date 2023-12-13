/******************************************************
 *        transform objects (`[]`, `{}`) into         *
 *        string representations                      *
 ******************************************************/

export function stringifyAuthor(a) {
    /**
     * stringify the author object `a` into
     * a human-readable author name
     * @param {Object} a: an author, of shape { "uuid": <uuid>,
     *                                          "first_name": <first_name>,
     *                                          "last_name": <last_name> }
     * @returns {string}: the human-reaable author name
     */
    return a.first_name == null
           ? a.last_name
           : `${a.first_name} ${a.last_name}`
}

export function stringifyDate(d) {
    /**
     * transform a date range array into a human-readable string
     * @param {Array} a: a date, of shape `[YYYY, YYYY]`
     * @returns {str}: `YYYY` or `YYYY-YYYY`
     */
    if ( d != null ) {
      return d[0] === d[1]
             ? `${d[0]}`
             : `${d[0]}-${d[1]}`
    } else {
      return "Date inconnue"
    }
}