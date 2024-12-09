/**
 * the backend for `@components/TheQuickSearchBar` and `@views/QuickSearchViews`
 */
import axios from "axios";

import { articles } from "@globals";
import { urlToArticleMain
       , urlToFrontendNamedEntityNoCategory
       , urlToFrontendThemeNoCategory
       , urlToFrontendInstitution
       , urlToFrontendPlace
       , urlToFrontendIconography } from "@utils/url.js";
import { simplifyString
       , simplifyAndUnaccentString } from "@utils/strings.js";
import "@typedefs";

/**************************************/

/**
 * @typedef backendDataArray: the data received from the backend
 * @type {backendDataItem[]}
 */

/**
 * @typedef backendDataItem: a single entry in `backendDataArray`
 * @type {object}
 * @property {string} table_name: the name of the table in which the entry is
 * @property {string} id_uuid   : the id_uuid of the entry_
 * @property {string} entry_name: the text to display to the user
 */

/**************************************/

/**
 *
 * @param {backendDataItem} item
 * @returns {URL?}
 */
function itemToUrl(item) {
  let itemUrl = item.table_name === "iconography"
      ? urlToFrontendIconography(item.id_uuid)
      : item.table_name === "place"
      ? urlToFrontendPlace(item.id_uuid)
      : item.table_name === "theme"
      ? urlToFrontendThemeNoCategory(item.id_uuid)
      : item.table_name === "named_entity"
      ? urlToFrontendNamedEntityNoCategory(item.id_uuid)
      : item.table_name === "institution"
      ? urlToFrontendInstitution(item.id_uuid)
      : () => { console.error("quickSearchInternals.itemToUrl: unexpected value for `item.table_name` : ", item.table_name);
                return undefined }
  return itemUrl
}

/**
 *
 * @param {backendDataArray} data
 * @returns { typedefs.QuickSearchResultGroup[] }
 */
function restructureBackendData(data) {
  /** @type { string[] } */
  let dataGroupNames = [ ...new Set(data.map(item => item.table_name)) ];
  /** @type { typedefs.QuickSearchResultGroup[] } */
  let out = [];

  console.log("restructureBackendData in  :", data);
  dataGroupNames.forEach((groupName) => {
    let entries = data.filter(item => item.table_name === groupName)
                      .map((item) => { return { entryName: item.entry_name,
                                                entryUrl: itemToUrl(item) } })
    out.push({ groupName: groupName, entries: entries })
  })
  console.log("restructureBackendData out :", out);
}

/**
 * match sections of the website and return them as a
 * typedefs.QuickSearchResultGroup[].
 *
 * site sections are represented by `appSections`, which contains an
 * array of app sections each section is represented by
 * - `searchKeys`, a string[] of keywords
 * - `searchResult` (an object to build the redirection html).
 * if `queryString` is contained in an item of `searchKeys`, then `searchResults`
 * is added to the output.
 * @param {String} queryString
 * @returns {typedefs.QuickSearchResultGroup[]}
 */
function matchAppSections(queryString) {
  /**
   * an array of [`search terms`, `QuickSearchResultItem (search result)`]
   * * @type { { searchKeys: string[], searchResult: typedefs.QuickSearchResultItem }[] }
   */
  const appSections =
    [ { searchKeys  : ["iconographie", "iconographies", "iconographique"],
        searchResult: { groupName: "iconography",
                        entries: [{ entryName: "Toutes les ressources iconographiques", entryUrl: new URL("/iconographie", window.origin) }] } }
    , { searchKeys  : ["theme", "themes", "thématique"],
        searchResult: { groupName: "theme",
                        entries: [ { entryName: "Tous les thèmes", entryUrl: new URL("/theme", window.origin)} ] } }
    , { searchKeys  : ["entite nommee", "entites nommees", "sujet", "sujets"],
        searchResult: { groupName: "namedEntity",
                        entries: [{ entryName: "Toutes les entités nommées", entryUrl: new URL("/entite-nommee", window.origin) }] } }
    , { searchKeys  : ["lieu", "lieux", "adresse", "adresses"],
        searchResult: { groupName: "place",
                        entries: [{ entryName: "Tous les lieux", entryUrl: new URL("/lieu", window.origin)}] } }
    , { searchKeys  : ["institution", "institutions", "musées", "archives"],
        searchResult: { groupName: "institution",
                        entries: [{ entryName: "Toutes les institutions", entryUrl: new URL("/institution", window.origin) }] } }
    , { searchKeys  : ["carte", "cartographie"],
        searchResult: { groupName: "cartography",
                        entries: [{ entryName: "Cartographie du quartier", entryUrl: new URL("/cartographie", window.origin) }] } }
    , { searchKeys  : ["article", "articles"],
        searchResult: { groupName: "article",
                        entries: [{ entryName: "Tous les articles", entryUrl: new URL("/article", window.origin) }] } }
    ];
  queryString = simplifyAndUnaccentString(queryString);

  // return QuickSearchResultItem[] where queryString is included in any of the strings in `item.searchKeys`
  return appSections.filter((item) =>
    item.searchKeys.some(key => key.includes(queryString))
  ).map((item) => item.searchResult);
}

/**
 * match articles to `queryString` and reformat
 * the selected articles to fit the return's data model.
 * @param {String} queryString
 * @returns {typedefs.QuickSearchResultGroup}
 */
function matchArticles(queryString) {
  /** @type {typedefs.QuickSearchResultGroup} */
  const out = { groupName: "article", entries: [] };
  let matchedArticles = [];

  // do an extra cleaning on the query string
  queryString = simplifyAndUnaccentString(queryString);

  // extract the items from `articles` where `title` or `subtitle` contains `queryString`
  matchedArticles = articles.filter(a =>
    simplifyAndUnaccentString(a.title).includes(queryString)
    || simplifyAndUnaccentString(a.subtitle).includes(queryString) )

  // reformat `matchedArticles` to fit the data model of `typedefs.QuickSearchResultGroup`
  out.entries.push(...matchedArticles.map(article => {
    return { entryName: article.title,
             entryUrl: urlToArticleMain(article.urlSlug) } }));
  return out;
}

/**
 * return data that matches `queryString` from the database
 * @async
 * @param {String} queryString
 * @returns {typedefs.QuickSearchResultGroup[]}
 */
async function matchData(queryString) {
  const apiTarget = new URL(`/i/search/quicksearch/${queryString}`, __API_URL__);

  queryString = simplifyString(queryString);
  return axios.get( apiTarget )
         .then(r => r.data)
         .then(data => { return restructureBackendData })
         .catch(e => {
          console.error("quickSearchInternals.matchData() : error", e);
          return []
        })

}

/**************************************/

/**
 *
 * @async
 * @param {String} input: the user input
 * @returns {typedefs.QuickSearchResultGroupArray}: an array of results.
 *    structure: [ { groupName: "...", entries: [ { entryName: "...", entryUrl: URL } ] } ]
 */
export async function quickSearch(queryString) {
  /** @type {typedefs.QuickSearchResultGroupArray} */
  const results = [];

  matchData(queryString).then(data => results.push(...data));

  // results.push( matchArticles(queryString) );
  // results.push( ...matchAppSections(queryString) );
  // console.log("from : ", results);

  return results
}