<template>

  <!-- NamedEntityMainView.vue
  
       the main page of a named entity, or an index of all
       iconographic resources associated to that entity.
  
       the code and logic are pretty much the same as in
       ThemeMainView.vue
  -->


  <h1>{{ namedEntityName }}</h1>
  <H2IndexCount :indexCount="namedEntity.iconography.length"
              dataType="iconography"
              v-if="loadState === 'loaded'"
  ></H2IndexCount>

  <UiLoader v-if="loadState === 'loading'"></UiLoader>

  <div v-else-if="loadState === 'loaded'">

    <div class="index-headtext-wrapper">
      <div>
        <p>Cette entité nommée appartient à la catégorie
          <RouterLink :to="urlToFrontendNamedEntityCategory(namedEntity.category_slug)"
                      v-html="namedEntity.category_name"
          ></RouterLink>.</p>

        <IndexAssociationRedirects v-if="associatedThemes.length"
                                   fromTable="named_entity"
                                   toTable="theme"
                                   :to="associatedThemes"
                                   :from="{ entry_name: namedEntity.entry_name
                                          , id_uuid: namedEntity.id_uuid }"
        ></IndexAssociationRedirects>

        <IndexAssociationRedirects v-if="associatedNamedEntities.length"
                                   fromTable="named_entity"
                                   toTable="named_entity"
                                   :to="associatedNamedEntities"
                                   :from="{ entry_name: namedEntity.entry_name
                                          , id_uuid: namedEntity.id_uuid }"
        ></IndexAssociationRedirects>
      </div>
    </div>

    <IndexIconography :data="namedEntity.iconography"></IndexIconography>

  </div>

  <ErrNotFound v-else-if="loadState === 'error'"></ErrNotFound>
</template>


<script setup>
import { onMounted, ref, watch, computed } from "vue";
import { useRoute } from "vue-router";

import axios from "axios";

import ErrNotFound from "@components/ErrNotFound.vue";
import UiLoader from "@components/UiLoader.vue";
import IndexAssociationRedirects from "@components/IndexAssociationRedirects.vue";
import H2IndexCount from "@components/H2IndexCount.vue";
import IndexIconography from "@components/IndexIconography.vue";

import { urlToFrontendNamedEntityCategory } from "@utils/url.js";
import "@typedefs";

/**************************************************/

const route           = useRoute();
const namedEntity     = ref({});                   /** @type {typedefs.ThemeOrNamedEntityItemFull} the namedEntity object sent from the backend */
const namedEntityName = ref("");                   /** @type {string} the name of the namedEntity */
const idUuid          = ref(route.params.idUuid);  /** @type {string} */
const loadState       = ref("loading");            /** @type {typedefs.AsyncRequestState}: the loading state */

const associatedThemes        = ref([]);  /** @type { {id_uuid: string, entry_name: string, count: Number}[] } themes most frequently associated with the current named entity */
const associatedNamedEntities = ref([]);  /** @type { {id_uuid: string, entry_name: string, count: Number}[] } named entites most frequently associated with the current named entity */

// the backend URLs, defined as `computed` to handle reactivity
const apiTargetNamedEntity = computed(() =>
  new URL(`/i/named-entity/name/${idUuid?.value}`, __API_URL__))
const apiTargetIconography  = computed(() =>
  new URL(`/i/named-entity/${idUuid?.value}`, __API_URL__) );

/***************************************************/

/**
 * get all backend data from an UUID. we divide the fetching
 * of data in 2 queries because the second query, `apiTargetIconography`,
 * can take time to run
 */
function getData() {
  axios.get(apiTargetNamedEntity.getter().href).then(r => {
    namedEntityName.value = r.data.length ? r.data[0] : undefined;
  })
  .catch(e => { loadState.value = 'error'; console.error(e) });

  axios.get(apiTargetIconography.getter().href)
  .then(r => {
    if ( r.data.length ) {
      namedEntity.value = r.data[0];
      loadState.value  = 'loaded';
    }
  })
  .catch(e => { loadState.value = 'error'; console.error(e) });
}

/**
 * get the named entities and themes associated to the current named entity.
 * for example: the named entites which are the most often used to tag images
 * which are also tagged with the current named entity.
 */
function getAssociated() {
  axios.get( new URL(`/i/association/theme-from-named-entity/${idUuid.value}`, __API_URL__).href )
       .then(r => { associatedThemes.value = r.data });
  axios.get( new URL(`/i/association/named-entity-from-named-entity/${idUuid.value}`, __API_URL__).href )
       .then(r => { associatedNamedEntities.value = r.data });
}

/***************************************************/

// could i do without those watchers ? just setting all the variables
// in `getData` or `onMounted` seems enough but idk...
// it was useful before `AssociationIndexView`, when clicking on the
// related named entites redirected you to a new NamedEntityMain with
// another idUuid, but it's no longer the case so i guess we're fine...
// also `IndexIconographyFilter` doesn't handle data updates,
// so if this watcher here is useful, then we have a problem in `IndexIconographyFilter`
watch(route, (newRoute, oldRoute) => {
  idUuid.value = route.params.idUuid;
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
