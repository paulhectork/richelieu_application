<!-- advanced search page.

     this route uses 2 components, `AvancedSearchQuery`
     and `AdvancedSearchResults`

     `AdvancedSearchQuery` is a form that creates a JSON of
     valid query data, and returns it to this componennt.
     here, the frontend URL is updated based on this query
     data, and a query is run to the backend to fetch results.

     `AdvancedSearchResults` displays all of the results for
     the current query parameters, once those results have
     been received.

     a reactive object `queryParams` stores the query parameters.
     changing it triggers a watcher that updates the route's query
     and sends a request to the backend in order to fetch relevant data.

     query parameters are read either:
     * from a form, using `updateQueryParamsFromForm()`,
       when a form is submitted in `AdvancedSearchQuery`
     * from a URL query, using `updateQueryParamsFromForm()`,
       which is useful when reloading a page with URL parameters,
       or to access the query results directly by loading a URL
     this is handled by transforming all our query data into an
     IconographyQueryData` object.

     lifecycle:
     **********

     page load
        => are there query params in the page URL?
          => yes: update `queryParams` ref
          => no: when a valid form is submitted in
             `AdvancedSearchQuery.vue`, `queryParams is updated.
     queryParams changes
        => the watcher is triggered
        => the route URL is updated and a backend query is run
        => results from the backend query are passed to
           AdvancedSearchResults.vue``

-->

<template>
  <h1>Recherche avancée</h1>

  <div class="query-container">
    <AdvancedSearchQuery @query-params="updateQueryParamsFromForm"
    ></AdvancedSearchQuery>
  </div>

  <div class="results-container"
       v-if="displayResults"
  >
    <AdvancedSearchResults></AdvancedSearchResults>
  </div>
</template>

<script setup>
import axios from "axios";
import { ref, onMounted, watch } from "vue";
import { useRouter, useRoute } from 'vue-router';

import _ from "lodash";

import { IconographyQueryParams } from "@modules/iconographyQueryParams";
import AdvancedSearchQuery from "@components/AdvancedSearchQuery.vue";
import AdvancedSearchResults from "@components/AdvancedSearchResults.vue";


/***************************************/

const targetUrl = new URL("/i/avanced-search-iconography/", __API_URL__);

const route          = useRoute();  // the current route
const router         = useRouter(); // the full router
const displayResults = ref(false);  // toggled to True once a query has been run
const queryParams    = ref();       // an IconographyQueryParams object with query params defined by the user in `AdvancedSearchQuery`, or query params visible in the URL
const queryResults   = ref([]);     // results of a query to the server

/***************************************/

/**
 * when receiving new query parameters from
 * `AdvancedSearchQuery`, update `queryParams`.
 * `_.isEqual` performs deep comparison and allows us
 * to only update `queryParams` if the new query parameters
 * are different from the previous oness
 * @param {Object} newQueryParams: a dict of query parameters.
 *   see AdvancedSearchQuery.onSubmit() for its structure.
 */
function updateQueryParamsFromForm(newQueryParams) {
  if ( !_.isEqual(newQueryParams.toJson(), queryParams.value?.toJson()) ) {
    queryParams.value = newQueryParams;
  }
}

/**
 * when reloading the page, the query params are still in
 * the URL but `queryParams` is empty, and no results are
 * displayed. repopulate `queryParams` based on the query
 * params in the URL, which will trigger to rerun the query.
 * @param {Object} routeQueryParams: the query params, as
 *  specified by `route.query`
 */
function updateQueryParamsFromRoute(routeQueryParams) {
  queryParams.value = new IconographyQueryParams(routeQueryParams, "route")
}

/**
 * when `queryParams` is updated, update the route,
 * run a new query on the server and update `queryResults`
 */
watch(queryParams, async (newParams, oldParams) => {
  router
  .push({ path:"/recherche", query: queryParams.value.toRouteParams() })
  .then(() => {
    // debug prints
    // console.log("watchQueryParams: params changed !");
    // console.log("watchQueryParams: params in route:", new IconographyQueryParams(route.query, "route"));
    // console.log("watchQueryParams: params in `queryParams`", queryParams.value);

    axios.get(targetUrl, { params: newParams.value });
  });
})

/***************************************/

onMounted(() => {
  updateQueryParamsFromRoute(route.query);
})

</script>


<style scoped>

</style>