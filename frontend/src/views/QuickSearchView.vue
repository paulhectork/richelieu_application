<template>

  <!-- QuickSearchView.vue
    displays the results of a quick search in a tree.
  -->


  <div class="qsv-wrapper">
    <div class="qsv-title-wrapper">
      <h1>Recherche rapide</h1>
      <h2>Votre recherche&nbsp;: <q>&nbsp;{{ queryString }}&nbsp;</q>
        ({{ computedResultCount }})</h2>
    </div>
    <div class="qsv-results-wrapper">
      <TreeComponent :data="queryResultsTree"
                     v-if="queryResultsTree.length"
      ></TreeComponent>
    </div>
  </div>

</template>


<script setup>
import { ref, onMounted, watch, computed } from "vue";
import { useRoute } from "vue-router";

import TreeComponent from "@components/TreeComponent.vue";

import { quickSearch } from "@modules/quickSearchInternals.js";
import { capitalizeFirstChar } from "@utils/strings";
import "@typedefs";

/*******************************************/

const route = useRoute();

const queryString = ref();  /** @type {String?}  */
const queryResults = ref([]);  /** @type {typedefs.QuickSearchResultGroupArray} */

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

const queryResultsTree = computed(() => restructureToTree(queryResults.value))

/*******************************************/

/**
 * restructure data to be used by `TreeComponent`
 * @param {typedefs.QuickSearchResultGroupArray} data
 * @returns {typedefs.treeData}
 */
function restructureToTree(data) {
  const restructureGroupEntries = (x) => {
    return { nodeLabel: x.entryName,
             nodeUrl: x.entryUrl,
             nodeChildren: undefined } };
  const humanReadableGroupName = {
    "iconography"  : "ressources iconographiques",
    "named_entity" : "entités nommées",
    "theme"        : "thèmes",
    "place"        : "lieux",
    "article"      : "articles sur le quartier",
    "institution"  : "institutions",
    "cartography"  : "cartographie du quartier"
  }
  const restructureGroupName = (x) =>
    `${capitalizeFirstChar(humanReadableGroupName[x.groupName])}
    (${x.entries.length}  ${ x.entries.length > 1 ? 'résultats' : 'résultat'})`;

  return data.map(group => {
    return { nodeLabel: restructureGroupName(group),
             nodeUrl: group.groupUrl,
             nodeChildren: group.entries.map(restructureGroupEntries)  } });
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
