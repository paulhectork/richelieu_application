<!-- InstitutionMainView.vue
     displays all iconography related to an institution.
     that institution is targeted using its `id_uuid`.

    the small fun complexity of this component is that there
    are 2 kinds of institutions: "normal" ones and "consortiums"
    that regroup several institutions.
    for example, "Musée Carnavalet" is a member of the "Paris Musées" consortium.
    we do a 2-way binding between institutions that are member of a consortium
    and consortium.
    - on the consortium's page we list all institutions that belong to the consortium.
    - on the pages of institutions that are members of a consortium,
      we include a hyperlink to the consortium's page.
-->
<template>
  <div v-if="loadState === 'error'">
    <ErrNotFound></ErrNotFound>
  </div>

  <div v-else>
    <h1>{{ institutionName }}</h1>
    <IndexCount :indexCount="dataFull.length"
                dataType="iconography"
                v-if="loadState === 'loaded'"
    ></IndexCount>

    <UiLoader v-if="loadState==='loading'"></UiLoader>
    <div v-if="loadState==='loaded'"
         class="index-headtext-wrapper"
    >

      <p v-if="parisMusees.includes(institutionName)">Ce musée est membre du réseau
        <RouterLink to="/institution/qr1ea925dc913804199ac1c0576480da5aa">
          Paris Musées</RouterLink>.</p>

      <p v-if="bibliSpe.includes(institutionName)">Cette bibliothèque est membre
        du réseau des
        <RouterLink to="/institution/qr1882f452734fc4049ae13bab3ae018981">
          Bibliothèques spécialisées de la ville de Paris</RouterLink>.</p>

      <p v-if="institutionName==='Paris Musées'">Le réseau Paris Musées regroupe les
        institutions suivantes&nbsp;:
        <span v-html="stringifyInstitutionArray(parisMuseesIndex, true)"></span>.
      </p>

      <p v-if="institutionName === 'Bibliothèques spécialisées de la Ville de Paris'">
        Le réseau des Bibliothèques spécialisées de la Ville de Paris regroupe les
        institutions suivantes&nbsp;:
        <span v-html="stringifyInstitutionArray(bsvpIndex, true)"></span>.
      </p>
    </div>

    <div v-if="loadState === 'loaded'">
      <IndexIconography :data="dataFull"></IndexIconography>
    </div>

  </div>
</template>


<script setup>
import { onMounted, ref, computed } from "vue";
import { useRoute } from "vue-router";

import axios from "axios";

import ErrNotFound from "@components/ErrNotFound.vue";
import UiLoader from "@components/UiLoader.vue";
import IndexCount from "@components/IndexCount.vue";
import IndexIconography from "@components/IndexIconography.vue";

import { stringifyInstitutionArray } from "@utils/stringifiers";

/**************************************************/

const route                = useRoute();
const idUuid               = ref(route.params.idUuid);  // id_uuid of the current institution
const institution          = ref({});    // the institution object sent from the backend
const institutionIndex     = ref([]);    // index of all institutions. fetched from backend
const institutionName      = ref("");    // the name of the institution. fetched from backend
const dataFull             = ref([]);    // the complete iconography  data, set from a watcher

const apiTargetIndex       = new URL("/i/institution", __API_URL__);
const apiTargetInstitution = new URL(`/i/institution-name/${idUuid.value}`, __API_URL__);
const apiTargetIconography = new URL(`/i/institution/${idUuid.value}`, __API_URL__);
const loadState            = ref("loading");  // loaded/loading/error

// 2-way binding stuff
// institution names from `Paris Musées` and
// `Bibliothèques Spécialisées de la Ville de Paris`
const parisMusees = [ "Musée Carnavalet"
                    , "Palais Galliera"
                    , "Maison de Balzac"
                    , "Maison Victor Hugo"
                    , "Musée de la Vie Romantique"
                    , "Petit Palais. Musée des Beaux-Arts de la Ville de Paris"
                    , "Musée Bourdelle"
                    , "Musée de la Libération Leclerc Moulin"
                    ];
const bibliSpe = [ "Bibliothèque historique de la Ville de Paris"
                 , "Bibliothèque de l'Hôtel de Ville"
                 , "Bibliothèque Marguerite Durand"
                 , "Bibliothèque Forney"
                 , "Médiathèque musicale de Paris"
                 , "Bibliothèque des littératures policières"
                 , "Bibliothèque du tourisme et des voyages - Germaine Tillion"
                 ];

// indexes of all institutions in Paris Musées and
// Bibliothèques spécialisées de la ville de Paris
const parisMuseesIndex = computed(() =>
  institutionName.value === 'Paris Musées' && institutionIndex.value.length
  ? institutionIndex.value.filter(i => parisMusees.includes(i.entry_name))
  : []
)
const bsvpIndex = computed(() =>
  institutionName.value === "Bibliothèques spécialisées de la Ville de Paris"
  && institutionIndex.value.length
  ? institutionIndex.value.filter(i => bibliSpe.includes(i.entry_name))
  : []
)

/***************************************************/

/**
 * get all backend data from an UUID. we divide the fetching
 * of data in 2 queries because the second query, `apiTargetIconography`,
 * can take time to run
 */
async function getData() {
  Promise.all([
    axios.get(apiTargetInstitution.href)
    .then(r => r.data)
    .then(data => { institutionName.value = data.length ? data[0] : undefined; })
    ,
    axios.get(apiTargetIndex.href)
    .then(r => r.data)
    .then(data => { institutionIndex.value = data })
    ,
    axios.get(apiTargetIconography.href)
    .then(r => r.data)
    .then(data => {
      if ( data.length ) {
        institution.value = data[0];
        dataFull.value    = institution.value.iconography;
      }
    })
  ])
  .then(r => loadState.value = "loaded")
  .catch(e => { console.error(e);
                loadState.value = "error" })
}

/***************************************************/

onMounted(() => {
  getData();
})

</script>


<style scoped>

</style>


