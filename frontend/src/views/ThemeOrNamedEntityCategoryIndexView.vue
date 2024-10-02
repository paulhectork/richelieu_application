<!--  ThemeOrNamedEntityCategoryIndexView.vue
      an index of categories fo the Themes or Named Entities.

      this component handles two indexes:
         $rootUrl/theme         : the "Theme" category index
         $rootUrl/entite-nommee : the "Named Entity" category index.
      those are two different pages on the website, but their
      functionning is centralized in this view: themes and named entities
      work them same way, and have the same data structure. they are
      different concepts (hence the 2 different tables), but the underlying
      logic is the same.
      if we're on a theme or named entity index is determined by `props.tableName`.
      this is a static prop defined in `@router/index.js` which tells the view
      wether it is a named entity or a theme, and loads the relevant variables
      (like the backend url to query).

      the user's path through themes and named entities has 3 steps:
        1) ThemeOrNamedEntityCategoryIndexView.vue:
          a category index (the current view). categories are broad
          groups in which individual themes/named entities are
          classified, and correspond to theme.category or
          named_entity.category, in the SQL DB.
        2) ThemeOrNamedEntityIndexView.vue:
          an index of themes/named entities for a single category.
          this gives access to individual themes / named entities.
        3) the index of iconography ressources describing this
          theme or named entities.

      props and global variables:
        tableName (prop) : the name of the table we're querying, which
          determines relevant info to display and backend urls.
        apiTarget (computed) : the URL where to get backend data,
          defined as a computed property to avoid manually having
          to update it
        dataFull (ref) : all the data fetched from the backend
        dataFilter (ref) : data fetched from the backend, reformatted
          and possibly filtered to be passed to IndexBase.vue

      lifecycle:
        1) first page load: based on the URL (theme/entite-nommee),
          define relevant variables and fetch data from the proper
          backend routes.
        2) page change without reload: manually reset the variables
          based on the new URL, fetch data again. this happens when
          we're on $root/theme and, using the menu, click on
          $root/entite-nommee to see the named entity reload.
-->

<template>
  <div v-if="loadState !== 'error'">

    <h1>Index des {{ tableName === "theme" ? "thèmes" : "entités nommées" }}</h1>

    <UiLoader v-if="loadState === 'loading'"></UiLoader>
    <IndexBase v-else
               :display="display"
               :data="dataFilter"
    ></IndexBase>

  </div>

  <div v-else>
    <ErrNotFound></ErrNotFound>
  </div>

</template>


<script setup>
import { onMounted, ref, watch, computed } from "vue";

import axios from "axios";

import { indexDataFormatterThemeCategory
       , indexDataFormatterNamedEntityCategory } from "@utils/indexDataFormatter";
import UiLoader from "@components/UiLoader.vue";
import ErrNotFound from "@components/ErrNotFound.vue";
import IndexBase from "@components/IndexBase.vue";

/*************************************************************/

const props      = defineProps([ "tableName" ]);

const tableName  = ref(props.tableName);
const loadState  = ref("loading");  // "loading"/"loaded"/"error"
const dataFull   = ref([]);
const dataFilter = ref([]);
const display    = "concept";

const apiTarget  = computed(() =>  // defined as computed to be able to dynamically switch URL when `tableName` changes.
  tableName.value === "theme"
  ? new URL("/i/theme", __API_URL__)
  : new URL("/i/named-entity", __API_URL__));

/*************************************************************/

/**
 * reset the global variables for this view based on `props.tableName`.
 * else, when switching from "/theme" to "/named-entity" (and back),
 * the `ref`s won't be updated: the view will keep thinking that
 * we're on page "Theme", while we'll want to be on "Entités nommées".
 */
function resetView() {
  if ( !["theme", "namedEntity"].includes(props.tableName) ) {
    throw new Error(`ThemeOrNamedEntityCategoryView: "tableName" props must be one of ["theme", "namedEntity"], got "${tableName.value}"`);
  }
  tableName.value  = props.tableName;
  dataFull.value   = [];
  dataFilter.value = [];
  loadState.value  = "loading";
}

/**
 * fetch data from the backend.
 */
function getData() {
  axios.get(apiTarget.getter().href)
  .then(r => r.data)
  .then(data => { dataFull.value   = data;
                  dataFilter.value = tableName.value === "theme"
                                     ? indexDataFormatterThemeCategory(data)
                                     : indexDataFormatterNamedEntityCategory(data);
                  loadState.value = "loaded";
                })
  .catch(e => { console.error(e);
                loadState.value = "error"
              })
  ;

}

/*************************************************************/

// trigger the whole reset/reload cycle when going from
// "/theme" to "/entite-nommee" without reloading.
watch(props, (newProps, oldProps) => {
  resetView();
  getData();
})

onMounted(() => {
  if ( !["theme", "namedEntity"].includes(tableName.value) ) {
    throw new Error(`ThemeOrNamedEntityCategoryView: "tableName" props must be one of ["theme", "namedEntity"], got "${tableName.value}"`);
  }
  getData();
})


</script>


<style scoped>

</style>
