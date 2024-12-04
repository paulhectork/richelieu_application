/**
 * the backend for `@components/TheQuickSearchBar` and `@views/QuickSearchViews`
 */
import { articles } from "@globals";
import { urlToArticleMain
       , urlToFrontendNamedEntity
       , urlToFrontendTheme
       , urlToFrontendPlace
       , urlToFrontendIconography } from "@utils/url.js";
import { simplifyString
       , simplifyAndUnaccentString } from "@utils/strings.js";
import "@typedefs";

/**************************************/

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
  queryString = simplifyString(queryString);

  results.push( matchArticles(queryString) );

  return results
}