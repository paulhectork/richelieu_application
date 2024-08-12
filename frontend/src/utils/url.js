/********************************************
 *                                          *
 * URL building functions                   *
 *                                          *
 ********************************************/


/**
 * create an URL to an image on the remote server
 * from the cartography/iconography table.
 * @param {str} fn : the filename to the image
 * @returns {URL}  : the URL to that image
 */
export const fnToCartographyFile = (fn) =>
  new URL(`/statics/cartography/${fn}`, __SERVER_URL__);

export const fnToIconographyFile = (fn) =>
  new URL(`/statics/iconography/${fn}`, __SERVER_URL__);


/**
 * build an URL to a frontend page on a theme, based on this theme's UUID
 * @param {string} themeIduuid: the UUID of the theme
 * @returns {URL}
 */
export const urlToFrontendTheme = (themeIduuid) =>
  new URL(`/theme/${themeIduuid}`, window.location.origin);


/**
 * build an URL to a frontend page on a named entity, based on this NE's UUID
 * @param {string} namedEntityIduuid: the UUID of the named entity
 * @returns {URL}
 */
export const urlToFrontendNamedEntity = (namedEntityIduuid) =>
  new URL(`/sujet/${namedEntityIduuid}`, window.location.origin);

/**
 * the same for other frontend pages.
 */
export const urlToFrontendPlace = placeIduuid =>
  new URL(`/lieu/${placeIduuid}`, window.location.origin);

export const urlToFrontendIconography = iconographyIduuid =>
  new URL(`/iconographie/${iconographyIduuid}`, window.location.origin);

export const urlToFrontendActor = actorIduuid =>
  new URL(`/acteur/${actorIduuid}`, window.location.origin);

export const urlToFrontendInstitution = institutionIduuid =>
  new URL(`/institution/${institutionIduuid}`, window.location.origin);


