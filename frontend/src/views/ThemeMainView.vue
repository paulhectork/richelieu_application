<!-- ThemeMainView.vue

     the main page of a theme, or an index of all
     iconographic resources associated to that theme.

     the code and logic are pretty much the same as in
     NamedEntityMainView.vue
-->


<template>
  <h1>{{ formattedThemeName }}</h1>
  <H2IndexCount :indexCount="theme.iconography.length"
                dataType="iconography"
                v-if="backendLoaded"
  ></H2IndexCount>

  <UiLoader v-if="!backendLoaded"></UiLoader>
  <div v-else>
    <div class="index-headtext-wrapper">
      <div>
        <p>Ce thème appartient à la catégorie
          <RouterLink :to="urlToFrontendThemeCategory(theme.category_slug)"
                      v-html="theme.category_name"
          ></RouterLink>.</p>
        <IndexAssociationRedirects v-if="associatedThemes.length"
                                   fromTable="theme"
                                   toTable="theme"
                                   :to="associatedThemes"
                                   :from="{ entry_name: theme.entry_name
                                          , id_uuid: theme.id_uuid }"
        ></IndexAssociationRedirects>
        <IndexAssociationRedirects v-if="associatedNamedEntities.length"
                                   fromTable="theme"
                                   toTable="named_entity"
                                   :to="associatedNamedEntities"
                                   :from="{ entry_name: theme.entry_name
                                          , id_uuid: theme.id_uuid }"
        ></IndexAssociationRedirects>
      </div>
    </div>

    <IndexIconography :data="theme.iconography"></IndexIconography>
  </div>
</template>


<script setup>
import { onMounted, ref, watch, computed } from "vue";
import { useRoute } from "vue-router";
import axios from "axios";

import UiLoader from "@components/UiLoader.vue";
import H2IndexCount from "@components/H2IndexCount.vue";
import IndexIconography from "@components/IndexIconography.vue";
import IndexAssociationRedirects from "@components/IndexAssociationRedirects.vue";

import { urlToFrontendThemeCategory } from "@utils/url.js";
import { capitalizeWords } from "@utils/strings";
import "@typedefs";

/**************************************************/

const route         = useRoute();
const theme         = ref({});                   /** @type {typedefs.ThemeOrNamedEntityItemFull}: the theme object sent from the backend */
const themeName     = ref("");                   /** @type {String} */
const backendLoaded = ref(false);                /** @type {bool} when swittched to true, the loader is removed */
const idUuid        = ref(route.params.idUuid);  /** @type {String} */

const associatedThemes        = ref([]); /** @type { { count: Number, id_uuid: String, entry_name: string }[] } themes most frequently associated with the current theme */
const associatedNamedEntities = ref([]); /** @type { { count: Number, id_uuid: String, entry_name: string }[] } named entites most frequently associated with the current theme  */

/** @type {computed<URL>} the backend URLs, defined as `computed` to handle reactivity */
const apiTargetThemeName = computed(() =>
  new URL(`/i/theme/name/${idUuid?.value}`, __API_URL__));
const apiTargetTheme  = computed(() =>
  new URL(`/i/theme/${idUuid?.value}`, __API_URL__) );

/** @type {String} */
const formattedThemeName = computed(() =>
  themeName.value ? capitalizeWords(themeName.value) : themeName.value );

/***************************************************/

/**
 * get all backend data from an UUID. we divide the fetching
 * of data in 2 queries because the second query, `apiTargetTheme`,
 * can take time to run
 */
function getData() {
  axios.get(apiTargetThemeName.getter().href).then(r => {
    themeName.value = r.data.length ? r.data[0] : undefined;
  })
  axios.get(apiTargetTheme.getter().href).then(r => {
    backendLoaded.value = true;
    if ( r.data.length ) {
      theme.value      = r.data[0];
    }
  })
}

/**
 * get the named entities and themes associated to the current theme.
 * for example: the NEs which are the most often used to tag images
 * which are also tagged with the current theme.
 */
function getAssociated() {
  axios.get( new URL(`/i/association/theme-from-theme/${idUuid.value}`, __API_URL__).href )
       .then(r => { associatedThemes.value = r.data; });
  axios.get( new URL(`/i/association/named-entity-from-theme/${idUuid.value}`, __API_URL__).href )
       .then(r => { associatedNamedEntities.value = r.data });
}

/***************************************************/

// see @views/NamedEntityMainView.vue about my doubts on these watchers...
watch(route, (newRoute, oldRoute) => {
  idUuid.value = newRoute.params.idUuid;
  getData();
  getAssociated();
})

onMounted(() => {
  getData();
  getAssociated();
})

</script>


<style scoped>

</style>


