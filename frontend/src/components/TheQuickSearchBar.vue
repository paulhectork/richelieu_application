<template>

  <!-- TheQuickSearchBar.vue
  
    a search bar placed in the navbar to run a quick search
    (on the website and on backend data)
  
  -->


  <div class="qsb-outer-wrapper">
    <!-- the search qsbInput -->
    <div class="qsb-form-wrapper">
      <FormKit type="form"
               id="qsb-form"
               name="qsbForm"
               :actions="false /** disable submit button : we add our custom one */"
               @submit="onSubmit"
               aria-description="Recherche rapide à partir d'un mot clé"
      >
        <FormKit type="text"
                 id="qsb-input"
                 name="qsbInput"
                 ref="qsbInput"
                 outer-class="qsb-input-wrapper"
                 placeholder="Recherche"
                 value=""
                 validation="textValidatorNoEmpty"
        ></FormKit>
        <!-- if qsbInput has no input or the input is shorter than 3 chars, then
             - qsbSubmit is disabled (can't submit the form)
             - the `svg-valid` class is added, which changes the submit's color
        -->
        <FormKit type="submit"
                 id="qsb-submit"
                 name="qsbSubmit"
                 outer-class="qsb-submit-wrapper"
                 value=""
                 :disabled="qsbInput?.node.value
                            && qsbInput?.node.value.length
                            && qsbInput?.node.context.state.valid===false"
                 :wrapper-class="{
                    'svg-valid': qsbInput?.node.context.state.valid===true || false }"
        >
          <FormKitIcon icon="search"
                       aria-label="Lancer la recherche rapide"
          ></FormKitIcon>
        </FormKit>

      </FormKit>

      <!-- error messages are hidden  by moving
        them to a `FormKitMessages` with `display:none` -->
      <FormKitMessages :node="qsbInput?.node"
                       style="display: none"
      ></FormKitMessages>
    </div>

    <!-- the search results -->
    <div class="qsb-output-wrapper">
      <div v-if="searchResults.length"
           class="qsb-output-inner animate__animated animate__slideInDown"
           style="overflow-y: hidden;">
        <ul class="qsb-result-list list-invisible">
          <li v-for="result in searchResults"
              class="qsb-result"
          >
            <RouterLink v-html="result.entryName"
                       :to="result.entryUrl.pathname"
            ></RouterLink>
          </li>
        </ul>
        <span class="qsb-result result-special negative-default">
          <RouterLink :to="{ path: '/recherche-rapide',
                             query: { queryString: queryString } }"
          ><strong>Afficher plus de résultats</strong></RouterLink>
        </span>
      </div>
      <div v-else-if="queryString != null
                      && queryString != ''
                      && !searchResults.length
                      && loadState !== 'loading'"
           class="qsb-output-inner animate__animated animate__slideInDown"
      >
        <span class="no-result qsb-result result-special negative-default"
        >Pas de résultat</span>
      </div>
    </div>
  </div>
</template>


<script setup>
import { ref, watch } from "vue";
import { useRoute } from "vue-router";

import { FormKitMessages, FormKitIcon } from '@formkit/vue';
import $ from "jquery";

import { quickSearch } from "@modules/quickSearchInternals.js";
import { clickOutside } from "@utils/ui.js";
import "@typedefs";

/**********************************/

const route = useRoute();

const qsbInput      = ref();
const queryString   = ref();    /** @type {String?}: the user inputted query string */
const searchResults = ref([]);  /** @type {typedefs.QuickSearchResultFlatArray} */
const loadState     = ref();    /** @type {typedefs.AsyncRequestState?} */

/**********************************/

/**
 * set the refs to their start state (empty the query string and results)
 */
function resetRefs() {
  queryString.value = "";
  searchResults.value = [];
}

/**
 * flatten the search results returned by quickSearchInternals.
 * @param {typedefs.QuickSearchResultGroupArray} theSearchResults: the search results returned by `quickSearchInternals`
 * @returns {typedefs.QuickSearchResultFlatArray}
 */
const flattenSearchResults = (theSearchResults) =>
  theSearchResults.map(group => group.entries).flat();

/**
 * when submitting data, run the query
 */
function onSubmit(e) {
  loadState.value = "loading";
  queryString.value = e.qsbInput;
  quickSearch(queryString.value).then(data => {
    searchResults.value = flattenSearchResults(data);
    loadState.value = "loaded";
  }).catch((e) => {
    // if there's an error, log it + set `searchResults` to display "pas de résultats"
    console.error("TheQuickSearchBar.onSubmit() : ", e);
    loadState.value = "error";
    searchResults.value = [];
  });
}

/**
 * events to close the results: click outside of `.qsb-outer-wrapper` or press escape
 */
function registerCloseEvents() {
  $(document).on("click", (e) => {
    if ( clickOutside(e, ".qsb-outer-wrapper") ) resetRefs();
  });
  $(document).on("keydown", (e) => {
    if ( e.key==="Escape" ) resetRefs();
  })
}
/**
 * remove the event listeners registered in `registerCloseEvents()`
 */
function unRegisterCloseEvents() {
  $(document).off("click");
}

/**********************************/

watch(() => queryString.value?.length, (newLength, oldLength) => {
  newLength > 0 ? registerCloseEvents() : unRegisterCloseEvents();
})

/** reset the search bar on redirect */
watch(route, (newR, oldR) => {
  queryString.value = "";
  searchResults.value = [];
  qsbInput.value.node.input("");
})

</script>


<style scoped>
.qsb-outer-wrapper {
  height: 100%;
  display: grid;
  align-items: center;
  justify-content: center;
}
@media ( max-width: 400px ) {
  .qsb-outer-wrapper {
    max-width: 130px;
  }
}
@media ( orientation:landscape ) {
  .qsb-outer-wrapper {
    min-width: 200px;
  }
}
.qsb-form-wrapper {
  z-index: 2; /** for the results display animation */
}
.formkit-outer {
  margin: 0;
}
.qsb-outer-wrapper :deep(#qsb-form) {
  border: var(--cs-main-border);
  display: grid;
  grid-template-columns: 1fr auto;
  grid-template-rows: 100%;
  height: calc(var(--cs-navbar-height) - 20px);  /** same height as the burger button */

}
.qsb-outer-wrapper :deep(.formkit-wrapper),
.qsb-outer-wrapper :deep(.formkit-inner),
.qsb-outer-wrapper :deep(#qsb-input) {
  height: 100%;
}
.qsb-outer-wrapper :deep(#qsb-input),
.qsb-outer-wrapper :deep(#qsb-submit)  {
  border: none;
}

/******************************/

.qsb-submit-wrapper {
  border-left: var(--cs-main-border);
  margin: 0;
  padding: 0;
  min-width: 4vh;
}
.qsb-submit-wrapper > :deep(.formkit-wrapper) {
  height: 100%;
  margin: 0;
  padding: 0;
}

:deep(#qsb-submit) {
  height:90%;
  width: 90%;
  display: flex;
  align-items: center;
  justify-content: center;
  border-left: var(--cs-main-border);
}
:deep(#qsb-submit svg) {
  width: 4vh;
  height: 4vh;
}
:deep(#qsb-submit svg > path) {
  stroke: var(--cs-main-second-bg);
}
:deep(.svg-valid #qsb-submit svg > path) {  /** yes this terrible selector is needed else the `id` of the rule above takes precedence */
  stroke: var(--cs-main-default);
}

/******************************/

.qsb-output-wrapper {
  position: relative;
  width: 100%;
}
.qsb-output-inner {
  width: 100%;
  position: absolute;
  top: 0px;
  left: 0px;
  background-color: var(--cs-main-default-bg);
  border: var(--cs-main-border);

  max-height: 50vh;
  height: auto;
  display: grid;
  grid-template-rows: 2fr 50px;
  grid-template-columns: 100%;
  box-shadow: 5px 5px 0 var(--cs-plum);
}
@media ( orientation:portrait ) {
  .qsb-output-inner {
    /** in portrait mode, `.qsb-output-inner` is much wider
     and is aligned to the right end of `qsb-outer-wrapper`.
    positionning is hacky but it works. */
    top: 0;
    left: -100%;
    width: 200%;
    max-height: 80vh;
  }
}
.qsb-result-list {
  overflow: scroll;
}
.qsb-result {
  border-bottom: var(--cs-main-border);
  display: grid;
  grid-template-rows: 100%;
  transition: background-color .3s;
}
.qsb-result:hover {
  background-color: var(--cs-main-second-bg);
  color: var(--cs-main-second);
}
.qsb-result a {
  padding: 5px;
  text-decoration: none;
  color: var(--cs-main-default);
  width: 100%;
}
.qsb-result.result-special {
  width: 100%;
  height: max(10%, 50px);
  position: absolute;
  bottom: 0;
  left: 0;
  border-top: var(--cs-main-border);
  border-bottom: none;
  display: flex;
  align-items: center;
}
.qsb-result.result-special a {
  color: var(--cs-negative-default);
}

</style>
