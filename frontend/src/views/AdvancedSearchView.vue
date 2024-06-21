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

     an extra fancy feature of this component is to read
     query parameters from the URL, to be able to re-run
     a query based on what's in the URL without having to
     fill the form again. usefull on page reload.
-->

<template>
  <h1>Recherche avancée</h1>

  <div class="query-container">
    <AdvancedSearchQuery @query-params="updateQueryParams"
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

import AdvancedSearchQuery from "@components/AdvancedSearchQuery.vue";
import AdvancedSearchResults from "@components/AdvancedSearchResults.vue";


/***************************************/

const targetUrl = new URL("/i/avanced-search-iconography/", __API_URL__);

const route          = useRoute();  // the current route
const router         = useRouter(); // the full router
const displayResults = ref(false);  // toggled to True once a query has been run
const queryParams    = ref({});     // query params defined by the user in `AdvancedSearchQuery`
const queryResults   = ref([]);     // results of a query to the server

/***************************************/

/**
 * when receiving from `AdvancedSearchQuery` new query
 * parameters, update `queryParams` and the router.
 * `_.isEqual` performs deep comparison and allows us
 * to only update `queryParams` if the new query parameters
 * are different from the previous oness
 * @param {Object} newQueryParams: a dict of query parameters.
 *   see AdvancedSearchQuery.onSubmit() for its structure.
 */
function updateQueryParams(newQueryParams) {
  if ( !_.isEqual(newQueryParams, queryParams.value) ) {
    queryParams.value = newQueryParams;
    router.push({ path:"/recherche", query: queryParams.value });
  }
}


/**
 * when reloading the page, the query params are still in the URL
 * but `queryParams` is empty, and no results are displayed. repopulate
 * `queryParams` based on the query params in the URL, which will trigger
 * to rerun the query.
 * @param {Object} routeQueryParams: the query params, as specifiec by `route.query`
 */
function updateQueryParamsFromRoute(routeQueryParams) {
  console.log(routeQueryParams);
  queryParams.value = { title: routeQueryParams.title || undefined,
                        author: routeQueryParams.author || undefined,
                        publisher: routeQueryParams.publisher || undefined,
                        theme: routeQueryParams.theme || undefined,
                        namedEntity: routeQueryParams.namedEntity || undefined,
                        institution: routeQueryParams.institution || undefined,
                        dateFilter: routeQueryParams.dateFilter || undefined,  // dateFilter even if no date is set?
                        date: routeQueryParams.date?.filter(x => x!=null) || []
  };
}

/**
 * when `queryParams` is updated, run a new query
 * on the server and update `queryResults`
 */
watch(queryParams, (newParams, oldParams) => {
  console.log("params changed !");
  console.log(newParams);

  axios.get(targetUrl, { params: newParams.value });


})

//
/***************************************/

onMounted(() => {
  updateQueryParamsFromRoute(route.query);
})

</script>


<style scoped>

</style>