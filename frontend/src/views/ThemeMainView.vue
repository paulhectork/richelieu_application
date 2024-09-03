<!-- ThemeMainView.vue

     the main page of a theme, or an index of all
     iconographic resources associated to that theme.

     the code and logic are pretty much the same as in
     NamedEntityMainView.vue
-->


<template>
  <h1>{{ formattedThemeName }}</h1>

  <UiLoaderComponent v-if="!backendLoaded"></UiLoaderComponent>
  <div v-else>
    <p><strong>{{ theme.iconography_count }} ressources iconographiques</strong>
      sont associées à ce thème.</p>

    <IndexAssociatedResources v-if="associatedThemes.length && associatedThemes.length > 1"
                              fromTable="theme"
                              toTable="theme"
                              :to="associatedThemes"
                              from=""
    ></IndexAssociatedResources>

    <p v-if="associatedThemes.length && associatedThemes.length > 1"
       v-html="`Les <strong>${associatedThemes.length} thèmes</strong> les
                plus fréquemment associés au thème <i>${themeName }</i> sont:
                ${ stringifyAssociated(associatedThemes, 'theme') }.`"
    ></p>
    <p v-else-if="associatedThemes.length===1"
       v-html="`<strong>Le thème</strong> le plus fréquemment associé
                au thème <i>${themeName }</i> est:
                ${ stringifyAssociated(associatedThemes, 'theme') }.`"
    ></p>

    <p v-if="associatedNamedEntity.length && associatedNamedEntity.length > 1"
       v-html="`Les <strong>${associatedNamedEntity.length} entités nommées</strong> les
                plus fréquemment associées au thème <i>${themeName}</i> sont:
                ${ stringifyAssociated(associatedNamedEntity, 'namedEntity') }.`"
    ></p>
    <p v-else-if="associatedThemes.length===1"
       v-html="`<strong>L'entité nommée</strong> la plus fréquemment associée
                au thème <i>${themeName }</i> est:
                ${ stringifyAssociated(associatedNamedEntity, 'namedEntity') }.`"
    ></p>


    <IndexBase :data="dataFilter"
               display="resource"
    ></IndexBase>
  </div>
</template>


<script setup>
import { onMounted, ref, watch, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import axios from "axios";

import IndexBase from "@components/IndexBase.vue";
import UiLoaderComponent from "@components/UiLoaderComponent.vue";
import IndexAssociatedResources from "@components/IndexAssociatedResources.vue";
import { indexDataFormatterIconography } from "@utils/indexDataFormatter";
import { stringifyAssociated, capitalizeString, capitalizeWords } from "@utils/stringifiers";

/**************************************************/

const route      = useRoute();
const theme      = ref({});    // the theme object sent from the backend
const themeName  = ref("");    // the name of the theme.
const dataFull   = ref([]);    // the complete iconography  data, set from a watcher
const dataFilter = ref([]);    // the user-filtered iconography data, set from a watcher
const idUuid     = ref(route.params.idUuid);
const backendLoaded = ref(false);  // when swittched to true, the loader is removed

const associatedThemes      = ref([]); // themes most frequently associated with the current theme
const associatedNamedEntity = ref([]); // named entites most frequently associated with the current theme

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
 */
function getData() {
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

/**
 * get the named entities and themes associated to the current theme.
 * for example: the NEs which are the most often used to tag images
 * which are also tagged with the current theme.
 */
function getAssociated() {
  axios.get( new URL(`/i/associated-theme-from-theme/${idUuid.value}`, __API_URL__).href )
       .then(r => { associatedThemes.value = r.data });
  axios.get( new URL(`/i/associated-named-entity-from-theme/${idUuid.value}`, __API_URL__).href )
       .then(r => { console.log(r.data); associatedNamedEntity.value = r.data });
}

watch(theme, (newTheme, oldTheme) => {
  dataFull.value   = newTheme.iconography;
  dataFilter.value = indexDataFormatterIconography(dataFull.value);
})

watch(() => route.params.idUuid, (newIdUuid, oldIdUuid) => {
  idUuid.value = newIdUuid;
  getData();
  getAssociated();
})


/***************************************************/

onMounted(() => {
  getData();
  getAssociated();
})

</script>


<style scoped>

</style>


