<template>
  <h1>Recherche avancée</h1>

  <div class="query-container">
    <AdvancedSearchQuery></AdvancedSearchQuery>
  </div>

  <div class="results-container"
       v-if="displayResults"
  >
    <AdvancedSearchResults></AdvancedSearchResults>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from 'vue-router';


import AdvancedSearchQuery from "@components/AdvancedSearchQuery.vue";
import AdvancedSearchResults from "@components/AdvancedSearchResults.vue";


/***************************************/

const router         = useRouter()
const displayResults = ref(false);  // toggled to True once a query has been run

/***************************************/


// router.push({ path:"/recherche", query: { pop: "popopop" } });

/***************************************/

</script>


<style scoped>

</style>