<!-- ThemeMainView.vue

     the main page of a theme, or an index of all
     iconographic resources associated to that theme.

     the code and logic are pretty much the same as in
     NamedEntityMainView.vue
-->


<template>
  <h1>Thème: {{ formattedThemeName }}</h1>

  <LoaderComponent v-if="!backendLoaded"></LoaderComponent>
  <div v-else>
    <p><strong>{{ theme.iconography_count }}</strong>
      ressources iconographiques sont associées à ce thème.</p>

    <Index :data="dataFilter"
           display="resource"
    ></Index>
  </div>
</template>


<script setup>
import { onMounted, ref, watch, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import axios from "axios";

import Index from "@components/Index.vue";
import LoaderComponent from "@components/ui/LoaderComponent.vue";
import { indexDataFormatterIconography } from "@utils/indexDataFormatter";
import { capitalizeString, capitalizeWords } from "@utils/stringifiers";

/**************************************************/

const route      = useRoute();
const theme      = ref({});    // the theme object sent from the backend
const themeName  = ref("");    // the name of the theme.
const dataFull   = ref([]);    // the complete iconography  data, set from a watcher
const dataFilter = ref([]);    // the user-filtered iconography data, set from a watcher
const idUuid     = ref(route.params.idUuid);
const backendLoaded = ref(false);  // when swittched to true, the loader is removed

// the backend URLs, defined as `computed` to handle reactivity
const apiTargetTheme = computed(() =>
  new URL(`/i/theme-name/${idUuid?.value}`, __API_URL__))
const apiTargetIconography  = computed(() =>
  new URL(`/i/theme/${idUuid?.value}`, __API_URL__) );
// the theme name
const formattedThemeName = computed(() =>
  themeName.value ? capitalizeWords(themeName.value) : themeName.value );

/***************************************************/

/**
 * get all backend data from an UUID. we divide the fetching
 * of data in 2 queries because the second query, `apiTargetIconography`,
 * can take time to run
 * @param {string} themeIdUuid: the UUID of this theme
 */
function getData(themeIdUuid) {
  axios.get(apiTargetTheme.getter().href).then(r => {
    themeName.value = r.data.length ? r.data[0] : undefined;
  })
  axios.get(apiTargetIconography.getter().href).then(r => {
    backendLoaded.value = true;
    if ( r.data.length ) {
      theme.value = r.data[0]
    }
  })
}

watch(theme, (newTheme, oldTheme) => {
  dataFull.value   = newTheme.iconography;
  dataFilter.value = indexDataFormatterIconography(dataFull.value);
})

watch(() => route.params.idUuid, (newIdUuid, oldIdUuid) => {
  idUuid.value = newIdUuid;
  getData(newIdUuid);
})


/***************************************************/

onMounted(() => {
  getData(idUuid.value);
})

</script>


<style scoped>

</style>


