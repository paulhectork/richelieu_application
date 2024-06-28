<!-- NamedEntityMainView.vue

     the main page of a named entity, or an index of all
     iconographic resources associated to that entity.

     the code and logic are pretty much the same as in
     ThemeMainView.vue
-->

<template>
  <h1>Sujet: {{ formattedNamedEntityName }}</h1>

  <LoaderComponent v-if="!backendLoaded"></LoaderComponent>
  <div v-else>
    <p><strong>{{ namedEntity.iconography_count }}</strong>
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

const route           = useRoute();
const namedEntity     = ref({});    // the namedEntity object sent from the backend
const namedEntityName = ref("");    // the name of the namedEntity.
const dataFull        = ref([]);    // the complete iconography  data, set from a watcher
const dataFilter      = ref([]);    // the user-filtered iconography data, set from a watcher
const idUuid          = ref(route.params.idUuid);
const backendLoaded   = ref(false);  // when swittched to true, the loader is removed

// the backend URLs, defined as `computed` to handle reactivity
const apiTargetNamedEntity = computed(() =>
  new URL(`/i/named-entity-name/${idUuid?.value}`, __API_URL__))
const apiTargetIconography  = computed(() =>
  new URL(`/i/named-entity/${idUuid?.value}`, __API_URL__) );
// the namedEntity name
const formattedNamedEntityName = computed(() =>
  namedEntityName.value ? capitalizeWords(namedEntityName.value) : namedEntityName.value );

/***************************************************/

/**
 * get all backend data from an UUID. we divide the fetching
 * of data in 2 queries because the second query, `apiTargetIconography`,
 * can take time to run
 * @param {string} namedEntityIdUuid: the UUID of this namedEntity
 */
function getData(namedEntityIdUuid) {
  axios.get(apiTargetNamedEntity.getter().href).then(r => {
    namedEntityName.value = r.data.length ? r.data[0] : undefined;
  })
  axios.get(apiTargetIconography.getter().href).then(r => {
    backendLoaded.value = true;
    if ( r.data.length ) {
      namedEntity.value = r.data[0]
    }
  })
}

watch(namedEntity, (newNamedEntity, oldNamedEntity) => {
  dataFull.value   = newNamedEntity.iconography;
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
