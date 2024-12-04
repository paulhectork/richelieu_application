<!-- TheQuickSearchBar.vue

  a search bar placed in the navbar to run a quick search
  (on the website and on backend data)

-->

<template>
  <div class="qsb-outer-wrapper">
    <!-- the search qsbInput -->
    <div class="qsb-form-wrapper" style="position: relative;">
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
    <div class="qsb-output-wrapper" v-if="searchResults.length">
      <div class="qsb-output-inner">
        <ul class="qsb-result-list list-invisible">
          <li v-for="result in searchResults"
              class="qsb-result"
          >
            <RouterLink v-html="result.entryName"
                       :to="result.entryUrl.pathname"
            ></RouterLink>
          </li>
          <li class="qsb-result see-more">
            <RouterLink :to="{ path: 'recherche-rapide',
                               query: { queryString: queryString } }"
            ><strong>Afficher plus de résultats</strong></RouterLink>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>


<script setup>
import { ref, watch } from "vue";
import { useRoute } from "vue-router";

import { FormKitMessages, FormKitIcon } from '@formkit/vue';

import { quickSearch } from "@modules/quickSearchInternals.js";
import "@typedefs";
import { pushScopeId } from "vue";

/**********************************/

const route = useRoute();

const qsbInput = ref();
const queryString = ref();  /** @type {String?}: the user inputted query string */
const searchResults = ref([]);  /** @type {typedefs.QuickSearchResultFlatArray} */

/**********************************/

/**
 * flatten the search results returned by quickSearchInternals.
 * @param {typedefs.QuickSearchResultGroupArray} theSearchResults: the search results returned by `quickSearchInternals`
 * @returns {typedefs.QuickSearchResultFlatArray}
 */
const flattenSearchResults = (theSearchResults) =>
  Array.from(...theSearchResults.map(group => group.entries));

/**
 * when submitting data, run the query
 */
function onSubmit(e) {
  queryString.value = e.qsbInput;
  quickSearch(queryString.value).then(data => {
    searchResults.value = flattenSearchResults(data);
    console.log(searchResults.value);
  });
}

/**********************************/

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
}
.qsb-output-inner {
  position: absolute;
  top: 0;
  left: 0;
  background-color: var(--cs-main-default-bg);
  border: var(--cs-main-border);
}
.qsb-result {
  border-bottom: var(--cs-main-border);
  display: grid;
  grid-template-rows: 100%;
  transition: background-color .3s;
}
.qsb-result:last-child {
  border-bottom: none;
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


</style>