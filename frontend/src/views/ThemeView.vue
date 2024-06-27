<!-- ThemeView.vue
     an index page for all of our themes -->

<template>
  <h1>Index des thèmes</h1>
  <p>Les thèmes sont des catégories générales dans
    lesquelles notre iconographie est organisée.</p>
  <Index :display="display"
         :data="dataFilter"
  ></Index>
</template>

<script setup>
import { onMounted, ref } from "vue";
import axios from "axios";

import { indexDataFormatterTheme } from "@utils/indexDataFormatter";
import Index from "@components/Index.vue";

const apiTarget = new URL("/i/theme", __API_URL__);
const dataFull = ref([]);   // the full index, independent of user filters
const dataFilter = ref([]); // the data to pass to `Index.vue`. this can depend on user-defined filters. an array of { href: <url to redirect to when clicking on an item>, img: <url to the background img to display>, text, <text to display> }
const display = "concept";  // define the view to use in `IndexItem`


onMounted(() => {
  axios.get(apiTarget).then((r) => {
    dataFull.value   = JSON.parse(r.request.response);
    dataFilter.value = indexDataFormatterTheme(dataFull.value)
  })
})
</script>

<style scoped>

</style>