/**
 * useful type definitions, especially defining
 * what's sent fom the background
 */

/**
 * @namespace typedefs
 */


/** frontend-specific objects */

/**
 * @typedef AsyncRequestState
 *    a string describing the state of an async http request.
 *    only 3 values are allowed, as seen below.
 * @type {("loading"|"loaded"|"error")}
 *
 */

/**
 * @typedef QuickSearchResultGroupArray
 *    the results of a quick search
 *    (initiated in `@components/TheQuickSeachBar`
 *    and processed in `@modules/quickSearchInternals`),
 *    grouped by page type (article, named entity, place...)
 * @type {QuickSearchResultGroup[]}
 */

/**
 * @typedef QuickSearchResultFlatArray
 *    the results of a quick search, but without
 *    group hierarchy and only result items.
 * @type {QuickSearchResultItem[]}
 */

/**
 * @typedef QuickSearchResultGroup
 *    a group of results in a quick search. a `group`
 *    is defined for a certain page type: theme, icono, articles...
 * @type {Object}
 * @property {("iconography"|"theme"|"named_entity"|"place"|"institution"|"article")} groupName
 *    1 result type per data type + 1 for the articles, which are also queried
 * @property { QuickSearchResultItem[] } entries
 *    an array of all the results for that group
 */

/**
 * @typedef QuickSearchResultItem
 *    an individual result in a quick search. this contains
 *    enough data to display a "result title" to the user and to
 *    redirect to another page of the website.
 * @type {Object}
 * @property {String} entryName : the "name" of the result displayed to the user
 * @property {String | URL | RouteLocationAsRelativeGeneric | RouteLocationAsPathGeneric} entryUrl
 *    the URL to redirect to, either as a string, a URL or a vue-router object.
 */

/**
 * @typedef QuickSearchResultItemEntries
 *    the individidual search results.
 */

/**
 * @typedef IndexBaseItem
 *    data structure expected by `@components/IndexBase.vue`
 * @type {object}
 * @property {String} idUuid
 * @property {String} text       : text to display in the @component/IndexItem
 * @property {(String|URL)} href : relative url to redirect to on click
 * @property {(String|URL)} img  : url to the image displayed on the IndexItem
 */

/**
 * @typedef HomeItemPreviewItem
 *    data model used by @components/HomeItemPreview
 * @type {String} title_main
 * @type {String} title_second
 * @type {String} title_sub
 * @type {(String|URL)} href
 * @type {String[]} thumbnail
 */

/** formkit stuff */

/**
 * @typedef FormKitOptionSingle
 *    structure of the "options" prop used by formkit
 *    see: https://formkit.com/inputs/select#array-of-objects.
 * @type {object}
 * @property {String} value: the "backend" (value that will be transmitted to the code when selected)
 * @property {String} label: "frontend" (the text displayed to the user)
 */

/**
 * @typedef FormKitOptionArray
 *    an array of `FormKitOptionSingle`, passed to the formkit `options` prop.
 * @type {FormKitOptionSingle[]}
 */

/** backend responses */
/** iconography */

/**
 * @typedef IconographyItemLite
 *    lite view of an iconography ressource
 * @type {object}
 * @property {String} id_uuid
 * @property {String} iiif_url
 * @property {String[]} title
 * @property {Number[]} date : the date of the work, always defined as a date range. @utils/stringifiers.stringifyDate can stringify this array
 * @property {ActorItemLite[]} authors: the creators of the resource
 * @property {FileNameItem[]} thumbnail
 */

/**
 * @typedef IconographyItemFull
 *    full view of an iconography ressource
 * @type {object}
 * @property {String}    id_uuid
 * @property {String}    source_url : url pointing to the document on the institution's website.
 * @property {String}    iiif_url
 * @property {Number[]?} iiif_folio : array of index numbers to select only specific views in IIIF manifests
 * @property {String[]}  title
 * @property {String[]}  technique
 * @property {String}    corpus : the corpus a rasource belongs to
 * @property {Number[]}  date
 * @property {String}    date_source : the date as specified in the source document
 * @property {boolean}   produced : if True, the resource was produced in the neighbourhood
 * @property {boolean}   represents : if True, the resource represents the neighbourhood
 * @property {ActorItemLite[]} author: the persons who created the document
 * @property {ActorItemLite[]} publisher: the publishers of the resource
 * @property {ThemeOrNamedEntityItemLite[]} named_entity
 * @property {ThemeOrNamedEntityItemLite[]} theme
 * @property {PlaceItemLite[]} place : the places related to the ressource
 * @property {FileNameItem[]}  filename: all static image files related to the resource
 * @property {LicenceItem} licence
 */

/** theme and named entities (they have the same structure) */

/**
 * @typedef ThemeOrNamedEntityItemLite
 *    "light" representation of a theme or named entity,
 *    used in collection/index views.
 * @type {object}
 * @property {String} id_uuid
 * @property {string} entry_name
 * @property {String} category_name
 * @property {String} category_slug
 * @property {Number} icononography_count: number of associated iconography ressources
 * @property {String[]} thumbnail: 1 item array with a filename
 */

/**
 * @typedef ThemeOrNamedEntityItemFull
 *    "full" representation of a theme or named entity.
 *    importantly, it contains an array of Iconography
 *    objects related to the theme or named entity.
 * @type {object}
 * @property {String} id_uuid
 * @property {string} entry_name
 * @property {String} category_name
 * @property {String} category_slug
 * @property {String?} description: an optional string describing the theme or named entity
 * @property {Number} icononography_count: number of associated iconography ressources
 * @property {IconographyItemLite[]}: the iconography items related to the theme or named entity
 */

/**
 * @typedef ThemeOrNamedEntityTree
 *    a tree view for themes or named entities,
 *    grouped together by category
 * @type {object}
 * @property {String} category_name: the name of the category
 * @property {String} category_slug: the URL slug for the category
 * @property { { entry_name: String, id_uuid: String }[] } entries: the themes or named entities for the current category
 */

/**
 * @typedef ThemeOrNamedEntityCategoryItem
 *    very light view of a category
 * @type {object}
 * @property {String} category_name
 * @property {String} category_slug
 */

/**
 * @typedef ThemeOrNamedEntityCategoryItemFull
 *    full view for a category of themes or named entitiess
 * @type {object}
 * @property {String} category_name : "<category name, to display on the page>",
 * @property {String} category_slug : "<category slug, to build urls>",
 * @property {Number} count         : <number of associated themes or named entities>,
 * @property {String[]?} preview    : optional key. [ <Array<string> of a few themes or named entities of that resource> ],
 * @property {String[]} thumbnail   : [ <filename> ]

/** place */

/**
 * @typedef PlaceItemLite
 *    lite view for a place, with minimal metadata and a geometry
 * @type {object}
 * @property {String} id_uuid
 * @property {Number} icononography_count
 * @property {Number[]} date : the date range for which a place exists
 * @property {Object} vector : a GeoJSON geometry (usually polygon, sometimes point)
 * @property {Object} centroid :  a GeoJson Poin: the centroid of the vector
 * @property {AddressItemFull[]} address : the human-readable address for this place.
 * @property {FileNameItem[]?} filename : an optional filename to display an image for the place
 */

/**
 * @typedef PlaceItemFull
 *    full view of a place. where the lite view restricts
 *    `address` and `place` to just 1, here we have all addresses
 *    and a `cartography` field with all vectors + an `iconography`
 *    column containing an array of related iconography resource
 * @type {object}
 * @property {String}   id_uuid
 * @property {String}   id_richelieu
 * @property {Number}   icononography_count
 * @property {Number[]} date : the date range for which a place exists
 * @property {String}   vector_source : where the vector comes from
 * @property {Object}   vector : a GeoJSON geometry (usually polygon, sometimes point)
 * @property {Object}   centroid :  a GeoJson Poin: the centroid of the vector
 * @property {Object?}  place_group : not yet implemented
 * @property {AddressItemFull[]}         address : the human-readable address for this place.
 * @property {FileNameItem[]?}       filename : an optional filename to display an image for the place
 * @property {IconographyItemLite[]} iconography
 * @property {CartographyItemLite[]} cartography
 */

/** cartography */

/**
 * @typedef CartographyItemLite
 *    lite view of an item in the cartography table.
 *    where the table Place is "source-agnostic" (not dependant on a
 *    historical source), a cartography item is a representation of a place
 *    in a single historical source.
 * @type {object}
 * @property {String} id_uuid
 * @property {String} title: the name of this cartographic item
 * @property {String} map_source : which historical source does this item come from
 * @property {Object} vector : a GeoJson geometry.
 * @property {PlaceItemLite[]} place : the place this cartography item describes
 * @property {FileNameItem[]?} filename : raster files for this cartography ressource (the raster's source will fit `map_source`)
 */

/** institutions */

/**
 * @typedef InstitutionItemLite
 *    lite view for an institution
 * @type {object}
 * @property {String} id_uuid
 * @property {Number} icononography_count
 * @property {String} entry_name
 * @property {String[]} thumbnail : an image for this institution
 */

/**
 * @typedef InstitutionItemFull
 *    full view for an institution
 * @type {object}
 * @property {String} id_uuid
 * @property {Number} icononography_count
 * @property {String} entry_name
 * @property {String?} description
 * @property {String[]} thumbnail : an image for this institution
 * @property {IconographyItemLite[]} iconography
 * @property {CartographyItemLite[]} cartography
 * @property {Array} directory
 */

/** actors */

/**
 * @typedef ActorItemLite
 *    lite view of a row from the "Actor" table:
 *    either an author or a publisher
 * @type {object}
 * @property {String} entry_name: the name of the actor
 * @property {string} id_uuid: their id_uuid
 */

/** other: Address, Filename, Licence */
/**
 * @typedef AddressItemFull
 *    a view of the table Address
 * @type {object}
 * @property {String} id_uuid
 * @property {String} address : number and street
 * @property {String} city
 * @property {String} country
 * @property {String} source : which source does the address come from ?
 *
 */

/**
 * @typedef FileNameItem
 *    view of a row of the Filename table. used to build URLs to files.
 * @type {object}
 * @property {String} url: the filename itself, from which we'll build a url.
 * @property {Number[][]}: bounds of the file, to position it on a
 *    leaflet map. same structure as a leaflet L.LatLng
 */


/**
 * @typedef LicenceItem
 *    info on the license under which a resource is distributed
 * @type {object}
 * @property {String} id_uuid
 * @property {String} entry_name
 */


export {}  // https://stackoverflow.com/questions/43183450/jsdoc-typedef-in-a-separate-file