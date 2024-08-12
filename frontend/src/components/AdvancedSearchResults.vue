<template>
  <h2>Résultats de la recherche</h2>

  <p v-if="dataFilter.length">{{ dataFilter.length }}
    résultats correspondent à votre recherche.</p>
  <p v-else>Aucun résultat de correspond à votre recherche.</p>

  <IndexBase v-if="dataFilter.length"
         :data="dataFilter"
         display="resource"
  ></IndexBase>
</template>


<script setup>
import { ref, onMounted, watch } from "vue";

import IndexBase from "@components/IndexBase.vue";
import { indexDataFormatterIconography } from "@utils/indexDataFormatter";

/******************************************/

const props = defineProps(["queryResults"]);
const dataFull = ref([]);
const dataFilter = ref([]);
// const

/******************************************/
/******************************************/

/******************************************/
onMounted(() => {
  console.log("hello");
  dataFull.value   = props.queryResults;
  dataFilter.value = indexDataFormatterIconography(dataFull.value);
})
</script>


<style scoped>

</style>