<!-- ThemeView.vue
     an index page for all themes in a category -->

<template>
  <div v-if="loadState === 'error'">
    <ErrNotFound></ErrNotFound>
  </div>
  <div v-else>

    <h1>Index des thèmes: {{ capitalizeString(categoryName) }}</h1>
    <p>Les thèmes sont des catégories générales dans
      lesquelles notre iconographie est organisée.</p>

    <UiLoaderComponent v-if="loadState === 'loading'"></UiLoaderComponent>
    <IndexBase v-else
           :display="display"
           :data="dataFilter"
    ></IndexBase>

  </div>

</template>

<script setup>
import { onMounted, ref, computed } from "vue";
import { useRoute } from "vue-router";
import axios from "axios";

import { indexDataFormatterTheme } from "@utils/indexDataFormatter";
import {capitalizeString} from "@utils/stringifiers";

import UiLoaderComponent from "@components/UiLoaderComponent.vue";
import ErrNotFound from "@components/ErrNotFound.vue";
import IndexBase from "@components/IndexBase.vue";

/*************************************************************/

/**********************************************************
 **********************************************************
 **********************************************************
 * TODO
 * centraliser les pages `ThemeIndex.+`
 * et `NamedEntityIndex.+`!!!!!!!!!!!!!
 * c'est juste deux représentations différentes pour
 * EXACTEMENT LE MÊME TYPE DE RESSOURCES (même structure
 * backend, même représentation frontend). centraliser
 * fera des vues plus costaudes, mais ça facilitera
 * l'harmonisation, et surtout la création de microfiltres.
 ***********************************************************/

const route        = useRoute();
const categoryName = ref(route.params.categoryName);
const dataFull     = ref([]);         // the full index, independent of user filters
const dataFilter   = ref([]);         // the data to pass to `IndexBase.vue`. this can depend on user-defined filters. an array of { href: <url to redirect to when clicking on an item>, img: <url to the background img to display>, text, <text to display> }
const display      = "concept";       // define the view to use in `IndexItem`
const loadState    = ref("loading");  // toggled to true when data has loaded, hides the loader

const apiTarget    = computed(() =>
  new URL(`/i/theme/${categoryName.value}`, __API_URL__));

/*************************************************************/

onMounted(() => {
  axios.get(apiTarget.getter().href)
  .then(r => r.data)
  .then(data => { dataFull.value = data;
                  dataFilter.value = indexDataFormatterTheme(data);
                  loadState.value = "loaded";
                })
  .catch(e => { console.error(e);
                loadState.value = "error"
              });
})
</script>

<style scoped>

</style>