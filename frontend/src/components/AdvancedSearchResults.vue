<template>
  <!-- AdvancedSearchResults
    display the results of an advanced search query in an index.

    props:
      - queryResults (Array<Object>)
          the array of Iconography objects.

  -->

  <h2>Résultats de la recherche</h2>

  <p v-if="dataFull.length > 1">{{ dataFull.length }}
    résultats correspondent à votre recherche.</p>
  <p v-else-if="dataFull.length === 1">{{ dataFull.length }}
    résultat correspond à votre recherche.</p>
  <p v-else>Aucun résultat de correspond à votre recherche.</p>

  <div v-if="dataFull.length">
    <IndexIconography :data="dataFull"></IndexIconography>
  </div>
</template>


<script setup>
import { ref, onMounted } from "vue";

import IndexIconography from "@components/IndexIconography.vue";

/******************************************/

const props = defineProps(["queryResults"]);
const dataFull   = ref([]);

/******************************************/

onMounted(() => {
  dataFull.value   = props.queryResults;
})
</script>


<style scoped>

</style>