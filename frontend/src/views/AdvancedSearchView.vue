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

  <!--
  <div class="query-container"
       :class="queryHidden ? 'hidden' : 'shown'"
  >
  -->
  <div class="query-container">
    <AdvancedSearchQuery @query-params="updateQueryParamsFromForm"
                         :query-error="queryError"
    ></AdvancedSearchQuery>
  </div>

  <div class="show-hide">
    <button @click="hideOrShowQuery"
    >{{ queryHidden ? "Afficher" : "Masquer" }} la recherche</button>
  </div>

  <div class="results-container"
       v-if="displayResults"
  >
    <AdvancedSearchResults :query-results="queryResults"
    ></AdvancedSearchResults>
  </div>
</template>

<script setup>
import axios from "axios";
import { ref, onMounted, watch } from "vue";
import { useRouter, useRoute } from 'vue-router';

import $ from "jquery";
import _ from "lodash";

import { IconographyQueryParams } from "@modules/iconographyQueryParams";
import AdvancedSearchQuery from "@components/AdvancedSearchQuery.vue";
import AdvancedSearchResults from "@components/AdvancedSearchResults.vue";


/***************************************/

const targetUrl = new URL("/i/iconography/search", __API_URL__);

const route          = useRoute();  // the current route
const router         = useRouter(); // the full router
const queryParams    = ref();       // an IconographyQueryParams object with query params defined by the user in `AdvancedSearchQuery`, or query params visible in the URL
const queryResults   = ref([]);     // results of a query to the server
const displayResults = ref(false);  // INUTILE???? toggled to True once a query has been run
const queryError     = ref(false);  // switched to true if a backend internal server error occurs
const queryHidden    = ref(false);  // when switched to true, the AdvancedSearchQuery block is hidden

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

    hideQuery();  // to hide the query and show only the results
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
 * ON EST OÙ ??????????????????????????????????????
 * L'ANIMATION EST LÀ, ELLE MARCHE QUAND ON CLIQUE
 * LE BOUTON. LE PETIT +, CE SERAIT DE FERMER LA RECHERCHE
 * À FILTRES QUAND DES RÉSULTATS S'AFFICHENT (QUAND
 * LA REQUÊTE DANS LE watch RÉUSSIT), MAIS PAS QUAND ON
 * RÉCUPÈRE LES PARAMÈTRES DE L'URL.
 *
 * ESSAYER DE METTRE UN FLAG DE LOAD INITIAL DANS
 * updateQueryParamsFromRoute QUI SOIT VÉRIFIÉ DANS
 * LE WATCH ?
 */

/**
 * functions hideQuery and showQuery animate the sliding in
 * and out of `AdvancedSearchQuery`.
 *
 * hiding the query container:
 * 1 `.query-container` is visible: this is the default
 * 2 the content of `.query-container` slides out by adding `.animate__slideOutUp`
 * 3 the height of `.query-container` is animated from 100% to 0 by adding `.height-zero`
 * 4 `.query-container` is hidden and invisible by adding class `.hidden`
 *
 * showing the query container:
 * 1 `.query-container` is made invisible by removing `.hidden`
 * 2 the height of `.query-container` is animated from 0 to 100% by removing `.height-zero`
 * 3 the content of `.query-container` slides in by adding `.animate_slideInDown`
 * 4 `.query container` is visible at height 100%.
 *
 * the `setTimeout` allows to wait for one animation to finish before the other starts.
 */
function hideQuery() {
  queryHidden.value = true;
  $(".query-container").addClass("animate__animated animate__slideOutUp");
  setTimeout(() => {
    $(".query-container").removeClass( "animate__animated animate__slideOutUp")
                         .addClass("hidden height-zero");
    console.log(queryHidden.value);
  }, 200)
}
function showQuery() {
  queryHidden.value = false;
  // `.pre-slide-down` is a small helper that makes sure that
  // `.query-container` is invisible before sliding it in
  $(".query-container").addClass("pre-slide-down")
                       .removeClass("hidden height-zero")
  setTimeout(() => {
    $(".query-container").removeClass("pre-slide-down")
                         .addClass("animate__animated animate__slideInDown");
  }, 400)
  setTimeout(() => {
    $(".query-container").removeClass( "animate__animated animate__slideInDown");
    console.log(queryHidden.value);
  }, 1000)
}

/**
 * toggle the visibility of the `AdvancedSearchQuery` block
 */
function hideOrShowQuery() {
  queryHidden.value ? showQuery() : hideQuery();
}


/**
 * when `queryParams` is updated, update the route,
 * run a new query on the server and update `queryResults`
 */
watch(queryParams, async (newParams, oldParams) => {
  router
  .push({ path:"/recherche", query: newParams.toRouteParams() })
  .then(() => {
    // debug prints
    // console.log("watchQueryParams: params changed !");
    // console.log("watchQueryParams: params in route:", new IconographyQueryParams(route.query, "route"));
    // console.log("watchQueryParams: params in `queryParams`", queryParams.value);

    console.log("going out !", { params: newParams.toJson() });
    displayResults.value = false;

    axios
    .get(targetUrl.href, { params: newParams.toJson() })
    .then(r => { queryResults.value = r.data;
                 displayResults.value = true; })
    .catch(e => { console.log("AdvancedSearchView: backend error on query:", newParams.toJson());
                  console.log("AdvancedSearchView: error dump:", e);
                  queryError.value = true;
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
  visibility: visible;
  height: auto;
  max-height: 130%;  /* setting to to just 100% messes up the position of following siblings */
  transition: max-height var(--animate-duration);
  animation-duration: .2s;  /* animate.css duration! */
}
.query-container.height-zero {
  max-height: 0;
}
.query-container.pre-slide-down {
  transform: translateX(-100vh);
}
.query-container.hidden {
  visibility: hidden;
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

</style>