<template>
  <div class="qsv-wrapper">
    <div class="qsv-title-wrapper">
      <h1>Recherche rapide</h1>
      <h2>Votre recherche&nbsp;: <q>&nbsp;{{ queryString }}&nbsp;</q>
        ({{ computedResultCount }})</h2>
    </div>
  </div>
  <div class="qsv-results-wrapper">
    <!--
    <ul v-if="queryResults.length"
        class="list-invisible"
    >
      <li v-for="group in queryResults"></li>
    </ul>
    -->
    <ul class="tree-category list-invisible"
    >
      <li v-for="group in queryResults"
          class="category-wrapper"
          :class="{ 'category-expanded':
            expandedTreeCategories.includes(group.groupName) }"
      >
        <span class="category-title-wrapper">
          <UiButtonPlus @click="() => expandOrCollapseTreeCategory(group.groupName)"
          ></UiButtonPlus>
          <span class="category-title">
            {{ group.groupName }} ({{ group.entries.length }}
            {{ group.entries.length != 1 ? "entrées" : "entrée" }})
          </span>
        </span>
        <div class="category-entries-wrapper">
        <ul class="category-entries">
          <li v-for="item in group.entries"
              class="category-entry">
            <RouterLink :to="item.entryUrl"
                        v-html="item.entryName"
            ></RouterLink>
          </li>
        </ul>
        </div>
      </li>
    </ul>

  </div>

</template>

<script setup>
import { ref, onMounted, watch, computed } from "vue";
import { useRoute } from "vue-router";

import UiButtonPlus from "@components/UiButtonPlus.vue";

import { quickSearch } from "@modules/quickSearchInternals.js";

/*******************************************/

const route = useRoute();

const queryString = ref();  /** @type {String?}  */
const queryResults = ref([]);  /** @type {typedefs.QuickSearchResultGroupArray} */
const expandedTreeCategories = ref([]);  /** @type { string[] } */

/** @type {string} */
const computedResultCount = computed(() => {
  const count = queryResults.value
                            .map(group => group.entries.length)
                            .reduce((partialSum, a) => partialSum + a, 0);
  return count > 1
         ? `${count} résultats`
         : count === 1
         ? `${count} résultat`
         : "aucun résultat";
})

/*******************************************/

function expandOrCollapseTreeCategory() {

}

/**
 * run the query and set the necessary refs.
 */
function initHook() {
  queryString.value = route.query.queryString;
  quickSearch(queryString.value).then(results => {
    queryResults.value = results;
  });
}

/*******************************************/

watch(() => route.query.queryString, (newQ, oldQ) =>
  initHook()
)

onMounted(() => {
  initHook();
})
</script>


<style scoped>

</style>