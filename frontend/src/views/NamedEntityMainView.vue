<!-- NamedEntityMainView.vue

     the main page of a named entity, or an index of all
     iconographic resources associated to that entity.

     the code and logic are pretty much the same as in
     ThemeMainView.vue
-->

<template>
  <h1>Sujet: {{ namedEntityName }}</h1>

  <LoaderComponent v-if="!backendLoaded"></LoaderComponent>
  <div v-else>
    <p><strong>{{ namedEntity.iconography_count }}</strong>
      ressources iconographiques sont associées à ce sujet.</p>

    <p v-if="associatedThemes.length && associatedThemes.length > 1"
       v-html="`Les <strong>${associatedThemes.length} thèmes</strong> les
                plus fréquemment associés au sujet <i>${ namedEntityName }</i> sont:
                ${ stringifyAssociated(associatedThemes, 'theme') }.`"
    ></p>
    <p v-else-if="associatedThemes.length===1"
       v-html="`<strong>Le thème</strong> le plus fréquemment associé
                au sujet <i>${ namedEntityName }</i> est:
                ${ stringifyAssociated(associatedThemes, 'theme') }.`"
    ></p>

    <p v-if="associatedNamedEntity.length && associatedNamedEntity.length > 1"
       v-html="`Les <strong>${associatedNamedEntity.length} sujets</strong> les
                plus fréquemment associés au sujet <i>${namedEntityName}</i> sont:
                ${ stringifyAssociated(associatedNamedEntity, 'namedEntity') }.`"
    ></p>
    <p v-else-if="associatedThemes.length===1"
       v-html="`<strong>Le sujet</strong> le plus fréquemment associé
                au sujet <i>${ namedEntityName }</i> est:
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
import LoaderComponent from "@components/ui/LoaderComponent.vue";
import { indexDataFormatterIconography } from "@utils/indexDataFormatter";
import { stringifyAssociated, capitalizeString, capitalizeWords } from "@utils/stringifiers";

/**************************************************/

const route           = useRoute();
const namedEntity     = ref({});    // the namedEntity object sent from the backend
const namedEntityName = ref("");    // the name of the namedEntity.
const dataFull        = ref([]);    // the complete iconography  data, set from a watcher
const dataFilter      = ref([]);    // the user-filtered iconography data, set from a watcher
const idUuid          = ref(route.params.idUuid);
const backendLoaded   = ref(false);  // when swittched to true, the loader is removed

const associatedThemes      = ref([]); // themes most frequently associated with the current named entity
const associatedNamedEntity = ref([]); // named entites most frequently associated with the current named entity

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
  axios.get(apiTargetIconography.getter().href).then(r => {
    backendLoaded.value = true;
    if ( r.data.length ) {
      namedEntity.value = r.data[0]
    }
  })
}

/**
 * get the named entities and themes associated to the current named entity.
 * for example: the named entites which are the most often used to tag images
 * which are also tagged with the current named entity.
 */
function getAssociated() {
  axios.get( new URL(`/i/associated-theme-from-named-entity/${idUuid.value}`, __API_URL__).href )
       .then(r => { associatedThemes.value = r.data });
  axios.get( new URL(`/i/associated-named-entity-from-named-entity/${idUuid.value}`, __API_URL__).href )
       .then(r => { associatedNamedEntity.value = r.data });
}

watch(namedEntity, (newNamedEntity, oldNamedEntity) => {
  dataFull.value   = newNamedEntity.iconography;
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
