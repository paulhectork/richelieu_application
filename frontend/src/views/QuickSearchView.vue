<template>
  <div class="qsv-wrapper">
    <div class="qsv-title-wrapper">
      <h1>Recherche rapide</h1>
      <h2>Votre recherche&nbsp;: <q>&nbsp;{{ queryString }}&nbsp;</q></h2>
    </div>
  </div>
  <div class="qsv-results-wrapper">
  </div>

</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";

/*******************************************/

const route = useRoute();

const queryString = ref();  /** @type {String?}  */
const queryResults = ref([]);  /** @type {typedefs.QuickSearchResultGroupArray} */

/*******************************************/

onMounted(() => {
  queryString.value = route.query.queryString;
})
</script>


<style scoped>

</style>