<!-- PlaceMainView.vue

     the main view for a single place, to see it on a map
     and view all of its related iconography
-->

<template>
  <div v-if="loadState==='error'">
    <ErrNotFound></ErrNotFound>
  </div>
  <div v-else>
    <h1>{{ computedAddress }}</h1>

    <UiLoaderComponent v-if="loadState==='loading'"></UiLoaderComponent>
    <div v-else-if="loadState==='loaded'">
      <div class="map-block-wrapper"></div>
      <div class="icono-block-wrapper">
        <IndexBase :data="dataFilter"
                   display="resource"
        ></IndexBase>
      </div>
    </div>
  </div>
</template>


<script setup>
import { onMounted, ref, computed } from "vue";
import { useRoute } from "vue-router";

import axios from "axios";

import { indexDataFormatterIconography } from "@utils/indexDataFormatter";
import UiLoaderComponent from "@components/UiLoaderComponent.vue";
import ErrNotFound from "@components/ErrNotFound.vue";
import IndexBase from "@components/IndexBase.vue";

/******************************************************************/

const route = useRoute();
const idUuid = route.params.idUuid;
const address = ref([]);  // array of addresses related to that place. fetched from backend
const source = ref("");   // currently used `source` for `Place.vector_source`, `Address.source` and `Cartography.map_source`
const place = ref({});    // fetched from backend
const dataFull = ref([]);   // iconography data. fetched from backend
const dataFilter = ref([]); // iconography data. fetched from backend
const loadState = ref("loading");

const apiTargetPlace = new URL(`/i/place/${idUuid}`, __API_URL__);
const apiTargetAddress = new URL(`/i/place-address/${idUuid}`, __API_URL__);
const sourcePriority = [ "parcellaire1900", "vasserot", "feuille", "contemporain" ];

/**
 * `address` as returned by the backend is an array of objects;
 * represent it as a string, or undefined.
 * if `source` is defined, then select address by its source;
 * else, by the order specified in `sourcePriority`
 */
const computedAddress = computed(() =>
  source.value && address.value?.filter(a => a.source === source.value).length
  ? address.value.filter(a => a.source === source.value)[0].address
  : address.value.length
  ? address.value[0].address
  : undefined
)

/******************************************************************/

/**
 * reorder the address array using the `source` of each address,
 * and in the order specified in `sourcePriority`.
*/
const reorderAddressArr = (addrArr) =>
  addrArr.sort((a,b) =>
    sourcePriority.indexOf(a.source) - sourcePriority.indexOf(b.source));

async function getData() {
  Promise.all([
    axios.get(apiTargetPlace.href)
    .then(r => r.data)
    .then(data => { place.value = data[0];
                    dataFull.value = place.value.iconography;
                    dataFilter.value = indexDataFormatterIconography(place.value.iconography);
     })
    ,
    axios.get(apiTargetAddress.href)
    .then(r => r.data)
    .then(data => { address.value = reorderAddressArr(data); })
  ])
  .then(r => loadState.value = "loaded")
  .catch(e => { console.error(e);
                loadState.value = "error" });
}

/******************************************************************/

onMounted(() => {
  getData()
});
</script>


<style scoped>

</style>