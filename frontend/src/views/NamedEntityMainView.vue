<!-- NamedEntityMainView.vue

     the main page of a named entity, or an index of all
     iconographic resources associated to that entity.

     the code and logic are pretty much the same as in
     ThemeMainView.vue
-->

<template>
  <h1>{{ namedEntityName }}</h1>

  <UiLoader v-if="loadState === 'loading'"></UiLoader>

  <div v-else-if="loadState === 'loaded'">
    <p><strong>{{ namedEntity.iconography_count }}
      <span v-if="namedEntity.iconography_count > 1"> ressources iconographiques</span>
      <span v-else>ressource iconographique</span>
    </strong> sont associées à cette entité nommée.</p>

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

    <IndexBase :data="dataFilter"
               display="resource"
    ></IndexBase>
  </div>

  <ErrNotFound v-else-if="loadState === 'error'"></ErrNotFound>
</template>


<script setup>
import { onMounted, ref, watch, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import axios from "axios";

import ErrNotFound from "@components/ErrNotFound.vue";
import IndexBase from "@components/IndexBase.vue";
import UiLoader from "@components/UiLoader.vue";
import IndexAssociationRedirects from "@components/IndexAssociationRedirects.vue";
import { indexDataFormatterIconography } from "@utils/indexDataFormatter";

/**************************************************/

const route           = useRoute();
const namedEntity     = ref({});    // the namedEntity object sent from the backend
const namedEntityName = ref("");    // the name of the namedEntity.
const dataFull        = ref([]);    // the complete iconography  data, set from a watcher
const dataFilter      = ref([]);    // the user-filtered iconography data, set from a watcher
const idUuid          = ref(route.params.idUuid);
const loadState       = ref("loading");  // loading/loaded/error

const associatedThemes      = ref([]); // themes most frequently associated with the current named entity
const associatedNamedEntities = ref([]); // named entites most frequently associated with the current named entity

// the backend URLs, defined as `computed` to handle reactivity
const apiTargetNamedEntity = computed(() =>
  new URL(`/i/named-entity-name/${idUuid?.value}`, __API_URL__))
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
    if ( r.data.length ) { namedEntity.value = r.data[0]; loadState.value = 'loaded'; }
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

watch(namedEntity, (newNamedEntity, oldNamedEntity) => {
  dataFull.value   = newNamedEntity.iconography;
  dataFilter.value = indexDataFormatterIconography(dataFull.value);
  console.log(dataFilter.value);
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
