<!-- advanced search page for the Iconography table

     this route uses 2 components, `AvancedSearchQuery`
     and `AdvancedSearchResults`

     `AdvancedSearchQuery` is a form that creates a JSON of
     valid query data, and returns it to this componennt.
     here, the frontend URL is updated based on this query
     data, and a query is run to the backend to fetch results.
     after a query has been started, if an error occurs, an
     error message is displayed by this component.

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
     on page load
        => are there query params in the page URL?
          => yes: update `queryParams` ref
          => no: when a valid form is submitted in
             `AdvancedSearchQuery.vue`, `queryParams is updated.
     when queryParams changes
        => the watcher is triggered
        => the route URL is updated and a backend query is run
        => results from the backend query are passed to
           AdvancedSearchResults.vue``
-->

<template>
  <h1>Recherche avancée</h1>

  <Transition name="slideInOut">
  <div class="query-container"
       v-show="displayQuery">
    <AdvancedSearchQuery @query-params="updateQueryParamsFromForm"
                         :query-error="queryError"
    ></AdvancedSearchQuery>
  </div>
  </Transition>

  <div class="show-hide">
    <button @click="hideOrShowQuery"
    >{{ displayQuery ? "Masquer" : "Afficher" }} la recherche</button>
  </div>

  <LoaderComponent v-if="displayResults==='loading'"
                   class="results-loader"
  ></LoaderComponent>

  <div class="results-container"
       v-if="displayResults === 'yes'">
    <AdvancedSearchResults :query-results="queryResults"
    ></AdvancedSearchResults>
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
import LoaderComponent from "@components/ui/LoaderComponent.vue";


/***************************************/

const targetUrl = new URL("/i/iconography/search", __API_URL__);

const route          = useRoute();  // the current route
const router         = useRouter(); // the full router
const queryParams    = ref();       // an IconographyQueryParams object with query params defined by the user in `AdvancedSearchQuery`, or query params visible in the URL
const queryResults   = ref([]);     // results of a query to the server
const queryError     = ref(false);  // switched to true if a backend internal server error occurs
const displayResults = ref("no");   // `no|loading|yes`. controls the display of `AdvancedSearchResults` and `LoaderComponent`. when the value is 'no', neither are shown. when it is 'loading', `LoaderComponent` is shown. when 'yes', `LoaderComponent` is not shown and `AdvancedSearchResults` is shown.
const displayQuery   = ref(true);   // when switched to false, the AdvancedSearchQuery block is hidden using the `slideInOut` transition

/***************************************/

/**
 * when clicking on `.hide-show`, toggle the visiblity of the query
 */
function hideOrShowQuery() {
  displayQuery.value = !displayQuery.value;
}

/**
 * when receiving new query parameters from
 * `AdvancedSearchQuery`, update `queryParams`.
 * `_.isEqual()` performs deep comparison and allows us
 * to only update `queryParams` if the new query parameters
 * are different from the previous oness
 * @param {Object} newQueryParams: a dict of query parameters.
 *   see AdvancedSearchQuery.onSubmit() for its structure.
 */
 function updateQueryParamsFromForm(newQueryParams) {
  if ( !_.isEqual(newQueryParams.toJson(), queryParams.value?.toJson()) ) {
    queryParams.value = newQueryParams;
    displayQuery.value = false;  // to hide the query and show only the results
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
  const routeParams = new IconographyQueryParams(routeQueryParams, "route");
  queryParams.value = routeParams.allEmpty() ? queryParams.value : routeParams;  // only update `queryParams` if `routeParams` is not empty
}


/**
 * when `queryParams` is updated, update the route,
 * run a new query on the server and update `queryResults`
 */
watch(queryParams, async (newParams, oldParams) => {
  console.log("AdvancedSearchView.watch(queryParams): query params changed", newParams.toRouteParams(), newParams.toJson());
  router
  .push({ path:"/recherche", query: newParams.toRouteParams() })
  .then(() => {

    console.log("AdvancedSearchView.watch(queryParams): going out !", { params: newParams.toJson() });
    displayResults.value = "loading";

    axios
    .post(targetUrl.href, newParams.toJson() )
    .then(r => { queryResults.value = r.data;
                 displayResults.value = "yes"; })
    .catch(e => { queryError.value = true;
                  displayResults.value = "no";
                  displayQuery.value = true;
                  console.error( `AdvancedSearchView.watch(queryParams): backend error (${e.response.data})`
                               , "on query:"
                               , newParams.toJson()
                               , "error dump:"
                               , e);
    });
  });
})

/***************************************/

onMounted(() => {
  updateQueryParamsFromRoute(route.query);
})

</script>


<style scoped>
.query-container {
  height: auto;
}
.show-hide {
  margin: 3vh 5%;
  border-top: var(--cs-border);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
.show-hide > button {
  transform: translateY(-60%);
}
.results-loader {
  height: 10vh;
}

</style>