/**
 * URL building functions
 */


/**
 * create an URL to an image on the remote server
 * from the cartography/iconography table.
 * @param {str} fn : the filename to the image
 * @returns {URL}  : the URL to that image
 */
export const urlToCartographyFile = (fn) =>
  new URL(`cartography/${fn}`, __STATICS_URL__);

export const urlToIconographyFile = (fn) =>
  new URL(`iconography/${fn}`, __STATICS_URL__);

/**
 * prefix URL to the openseadragon icons
 */
export const urlToOsdIcons = () =>
  new URL("openseadragon-icons/", __STATICS_URL__);

/**
 * build an URL to a theme category.
 * @param {string} categorySlug: theme.category_slug
 * @returns {URL}
 */
export const urlToFrontendThemeCategory = (categorySlug) =>
  new URL(`/theme/${ encodeURIComponent(categorySlug) }`, window.location.origin);

/**
 * build an URL to a frontend page on a theme, based on this theme's UUID and category_slug.
 * @param {string} categorySlug: the category_slug of the theme.
 * @param {string} themeIdUuid: the UUID of the theme
 * @returns {URL}
 */
export const urlToFrontendTheme = (categorySlug, themeIdUuid) =>
  new URL( `/theme/${ encodeURIComponent(categorySlug) }/${ themeIdUuid }`
         , window.location.origin);

         /**
 * build an URL to a frontend page on a theme, based on its UUID.
 * to be used when the category of the theme is not known.
 * basically this works exactly the same as sending an uuid instead of a category_slug
 * to `urlToFrontendThemeCategory`.
 * @param {string} themeIdUuid: the UUID of the theme
 * @returns {URL}
 */
export const urlToFrontendThemeNoCategory = (themeIdUuid) =>
  new URL( `/theme/${ themeIdUuid }`
         , window.location.origin);

/**
 * build an URL to a named entity category.
 * @param {string} categorySlug: the named_entity.category_slug
 * @returns {URL}
 */
export const urlToFrontendNamedEntityCategory = (categorySlug) =>
  new URL( `/entite-nommee/${ encodeURIComponent(categorySlug) }`
         , window.location.origin);

/**
 * build an URL to a frontend page on a named entity, based on this NE's UUID and category
 * @param {string} categorySlug: the named_entity.category_slug
 * @param {string} namedEntityIdUuid: the UUID of the named entity
 * @returns {URL}
 */
export const urlToFrontendNamedEntity = (categorySlug, namedEntityIdUuid) =>
  new URL( `/entite-nommee/${ encodeURIComponent(categorySlug) }/${ namedEntityIdUuid }`
         , window.location.origin);

/**
 * build an URL to a frontend page on a named entity, based on this NE's UUID.
 * to be used when the category of the named entity is not known.
 * basically this works exactly the same as sending an uuid instead of a category_slug
 * to `urlToFrontendNamedEntityCategory`.
 * @param {string} namedEntityIdUuid: the UUID of the named entity
 * @returns {URL}
 */
export const urlToFrontendNamedEntityNoCategory = (namedEntityIdUuid) =>
  new URL( `/entite-nommee/${ namedEntityIdUuid }`
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


/**
 * build an URL to a main article. articleSlug si the slug that
 * allows us to point to a specific article: $root/article/$articleSlug
 *
 * @example: urlToArticleMain(bourse) returns an URL
 *   pointing to localhost:5173/article/bourse
 */
export const urlToArticleMain = articleSlug =>
  new URL(`/article/${articleSlug}`, window.location.origin);


