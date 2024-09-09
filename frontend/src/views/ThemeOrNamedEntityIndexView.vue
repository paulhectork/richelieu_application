<!--  ThemeViewOrNamedEntityIndexView.vue
      an index page for all themes or named entities in a category

      see the documentation of ThemeOrNamedEntityCategoryIndexView.vue
      for a more global outlook on the logic.

      props and refs:
        tableName (prop):
        categoryName (props):
        apiTarget (computed property):
-->

<template>
  <div v-if="loadState === 'error'">
    <ErrNotFound></ErrNotFound>
  </div>
  <div v-else>

    <h1>Index des
      {{ tableName === "theme" ? "thèmes" : "entités nommées" }}&nbsp;:
      {{ capitalizeString(categoryName) }}</h1>

    <UiLoaderComponent v-if="loadState === 'loading'"></UiLoaderComponent>
    <IndexBase v-else
           :display="display"
           :data="dataFilter"
    ></IndexBase>

  </div>

</template>

<script setup>
import { onMounted, ref, computed, watch } from "vue";
import { useRoute } from "vue-router";
import axios from "axios";

import { indexDataFormatterTheme
       , indexDataFormatterNamedEntity } from "@utils/indexDataFormatter";
import {capitalizeString} from "@utils/stringifiers";

import UiLoaderComponent from "@components/UiLoaderComponent.vue";
import ErrNotFound from "@components/ErrNotFound.vue";
import IndexBase from "@components/IndexBase.vue";

/*************************************************************/

const route        = useRoute();
const props        = defineProps(["tableName"]);

const tableName    = ref(props.tableName);
const categoryName = ref(decodeURIComponent(route.params.categoryName));
const dataFull     = ref([]);         // the full index, independent of user filters
const dataFilter   = ref([]);         // the data to pass to `IndexBase.vue`. this can depend on user-defined filters. an array of { href: <url to redirect to when clicking on an item>, img: <url to the background img to display>, text, <text to display> }
const loadState    = ref("loading");  // toggled to true when data has loaded, hides the loader
const display      = "concept";       // define the view to use in `IndexItem`

const apiTarget = computed(() =>  // defined as a computed property to avoid manually updating the url on tableName.value's change.
  tableName.value === "theme"
  ? new URL("/i/theme", __API_URL__)
  : new URL("/i/named-entity", __API_URL__));

/*************************************************************/

/**
 * reset all global variables when changing page without reloading
 */
function resetView() {
  tableName          = props.tableName;
  dataFull.value     = [];
  dataFilter.value   = [];
  categoryName.value = route.params.categoryName;
}

/**
 * get backend data: fetch all theme or iconography
 * resources for a single category
 */
function getData() {
  axios.get(apiTarget.getter().href, { params: {category:categoryName.value} })
  .then(r => r.data)
  .then(data => { dataFull.value = data;
                  dataFilter.value = tableName.value === "theme"
                                     ? indexDataFormatterTheme(data)
                                     : indexDataFormatterNamedEntity(data);
                  loadState.value = "loaded";
                })
  .catch(e => { console.error(e);
                loadState.value = "error"
              });
}

/*************************************************************/

watch(props, (oldProps, newProps) => {
  resetView();
  getData();
})

onMounted(() => {
  getData();
})
</script>

<style scoped>

</style>