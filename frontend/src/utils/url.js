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
  new URL(`/statics/cartography/${fn}`, __STATICS_URL__);

export const fnToIconographyFile = (fn) =>
  new URL(`/statics/iconography/${fn}`, __STATICS_URL__);

/**
 * build an URL to a theme category.
 * @param {string} categoryName: the name of the category (as is in the database)
 * @returns {URL}
 */
export const urlToFrontendThemeCategory = (categoryName) =>
  new URL(`/theme/${ encodeURIComponent(categoryName) }`, window.location.origin);

/**
 * build an URL to a frontend page on a theme, based on this theme's UUID
 * @param {string} themeIdUuid: the UUID of the theme
 * @returns {URL}
 */
export const urlToFrontendTheme = (categoryName, themeIdUuid) =>
  new URL( `/theme/${ encodeURIComponent(categoryName) }/${ themeIdUuid }`
         , window.location.origin);


/**
 * build an URL to a named entity category.
 * @param {string} categoryName: the name of the category (as is in the database)
 * @returns {URL}
 */
export const urlToFrontendNamedEntityCategory = (categoryName) =>
  new URL( `/entite-nommee/${ encodeURIComponent(categoryName) }`
         , window.location.origin);

/**
 * build an URL to a frontend page on a named entity, based on this NE's UUID
 * @param {string} namedEntityIdUuid: the UUID of the named entity
 * @returns {URL}
 */
export const urlToFrontendNamedEntity = (categoryName, namedEntityIdUuid) =>
  new URL( `/entite-nommee/${ encodeURIComponent(categoryName) }/${ namedEntityIdUuid }`
         , window.location.origin);

/**
 * the same for other frontend pages.
 */
export const urlToFrontendPlace = placeIdUuid =>
  new URL(`/lieu/${placeIdUuid}`, window.location.origin);

export const urlToFrontendIconography = iconographyIdUuid =>
  new URL(`/iconographie/${iconographyIdUuid}`, window.location.origin);

export const urlToFrontendActor = actorIdUuid =>
  new URL(`/acteur/${actorIdUuid}`, window.location.origin);

export const urlToFrontendInstitution = institutionIdUuid =>
  new URL(`/institution/${institutionIdUuid}`, window.location.origin);


