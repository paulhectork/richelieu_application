<!-- AdvancedSearchResults

  display the results of an advanced search query in an index.
  an `IndexIconographyFilter` allows to do extra filtering on
  the items.

  if i'm not mistaken, no need for a watcher here. the parent
  (AdvancedSearchView) destroys this component when running a
  new query, receives the results, re-mounts this component
  with new data.

  props:
    - queryResults (Array<Object>)
        the array of Iconography objects.

-->
<template>
  <h2>Résultats de la recherche</h2>

  <p v-if="dataFull.length > 1">{{ dataFull.length }}
    résultats correspondent à votre recherche.</p>
  <p v-else-if="dataFull.length === 1">{{ dataFull.length }}
    résultat correspond à votre recherche.</p>
  <p v-else>Aucun résultat de correspond à votre recherche.</p>

  <div v-if="dataFull.length">
    <IndexIconographyFilter :data="dataFull"
                            @iconography-filter="handleIconographyFilter"
    ></IndexIconographyFilter>
    <IndexBase :data="dataFilter"
               display="resource"
    ></IndexBase>
  </div>
</template>


<script setup>
import { ref, onMounted, watch } from "vue";

import IndexBase from "@components/IndexBase.vue";
import IndexIconographyFilter from "@components/IndexIconographyFilter.vue";

import { indexDataFormatterIconography } from "@utils/indexDataFormatter";

/******************************************/

const props = defineProps(["queryResults"]);
const dataFull   = ref([]);
const dataFilter = ref([]);

/******************************************/

/**
 * when IndexIconographyFilter returns the filtered array
 * of Iconography objects, update `dataFilter`, which will
 * trigger the updating of `IndexBase`.
 * @param {Array<Object>} iconographyData
 */
 function handleIconographyFilter(iconographyData) {
  dataFilter.value = indexDataFormatterIconography(iconographyData);
}

/******************************************/
onMounted(() => {
  dataFull.value   = props.queryResults;
  dataFilter.value = indexDataFormatterIconography(dataFull.value);
})
</script>


<style scoped>

</style>