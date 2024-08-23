<!-- ThemeView.vue
     an index page for all of our themes -->

<template>
  <h1>Index des sujets</h1>
  <p>Les sujets sont des points d'intérêt découverts dans chacune des images.</p>

  <UiLoaderComponent v-if="!isLoaded"></UiLoaderComponent>
  <IndexBase v-else
         :display="display"
         :data="dataFilter"
  ></IndexBase>

</template>

<script setup>
import { onMounted, ref } from "vue";
import axios from "axios";

// import { stringifyThemeOrNamedEntityResource } from "@utils/stringifiers";
// import { fnToIconographyFile } from "@utils/url";
import { indexDataFormatterNamedEntity } from "@utils/indexDataFormatter";
import UiLoaderComponent from "@components/UiLoaderComponent.vue";
import IndexBase from "@components/IndexBase.vue";

const apiTarget  = new URL("/i/named-entity", __API_URL__);
const dataFull   = ref([]);     // the full index, independent of user filters
const dataFilter = ref([]);     // the data to pass to `IndexBase.vue`. this can depend on user-defined filters. an array of { href: <url to redirect to when clicking on an item>, img: <url to the background img to display>, text, <text to display> }
const display    = "concept";   // define the view to use in `IndexItem`
const isLoaded   = ref(false);  // toggled to true once data has loaded. will hide the loader and show the index


onMounted(() => {
  axios.get(apiTarget).then((r) => {
    dataFull.value   = JSON.parse(r.request.response);
    dataFilter.value = indexDataFormatterNamedEntity(dataFull.value);
    isLoaded.value = true;
  })
})


</script>

<style scoped>

</style>