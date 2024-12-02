<!-- PlaceMainView.vue

     the main view for a single place, to see it on a map
     and view all of its related iconography
-->

<template>
  <div v-if="loadStatePlace==='error' || loadStateAddress==='error'">
    <ErrNotFound></ErrNotFound>
  </div>
  <div v-else>
    <h1>{{ computedAddress }}</h1>
    <H2IndexCount :indexCount="dataFull.length"
                dataType="iconography"
                v-if="loadStatePlace === 'loaded'"
    ></H2IndexCount>

    <UiLoader v-if="loadStatePlace==='loading'"></UiLoader>

    <div v-else-if="loadStatePlace==='loaded'">
      <div class="map-block-wrapper">
        <MapPlaceMain :place="place"></MapPlaceMain>
      </div>

      <div class="icono-block-wrapper">

        <div class="index-headtext-wrapper">
          <div>
            <IndexAssociationRedirects v-if="loadStateAssociated === 'loaded'"
                                       from-table="place"
                                       to-table="place"
                                       :from="{ entry_name: computedAddress, id_uuid: idUuid }"
                                       :to="associatedPlaces"
            ></IndexAssociationRedirects>
          </div>
        </div>

        <IndexIconography :data="dataFull"></IndexIconography>
      </div>
    </div>
  </div>
</template>


<script setup>
import { onMounted, ref, computed } from "vue";
import { useRoute } from "vue-router";

import axios from "axios";

import UiLoader from "@components/UiLoader.vue";
import MapPlaceMain from "@components/MapPlaceMain.vue";
import ErrNotFound from "@components/ErrNotFound.vue";
import IndexAssociationRedirects from "@components/IndexAssociationRedirects.vue";
import H2IndexCount from "@components/H2IndexCount.vue";
import IndexIconography from "@components/IndexIconography.vue";

import { cartographySourcePriority } from "@globals";
import { sortAddressBySource } from "@utils/array.js";

/******************************************************************/

const route = useRoute();
const idUuid = route.params.idUuid;
const address = ref([]);  // array of addresses related to that place. fetched from backend
const source = ref("");   // currently used `source` for `Place.vector_source`, `Address.source` and `Cartography.map_source`
const place = ref({});    // fetched from backend
const dataFull = ref([]);   // iconography data. fetched from backend
const associatedPlaces = ref([]);  // places most frequently tagged together with the current place

// loading/loaded/error
const loadStatePlace = ref("loading");
const loadStateAddress = ref("loading");
const loadStateAssociated = ref("loading");

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
 * all backend communication goes on here.
 */
async function getData() {
  axios.get(new URL(`/i/place/${idUuid}`, __API_URL__))
  .then(r => r.data)
  .then(data => {
    place.value = data[0];
    dataFull.value = place.value.iconography;
    loadStatePlace.value = "loaded";
  })
  .catch(e => { console.error(e);
                loadStatePlace.value = "error"
  });

  axios.get(new URL(`/i/place/address/${idUuid}`, __API_URL__))
  .then(r => r.data)
  .then(data => { address.value = sortAddressBySource(data);
                  loadStateAddress.value = "loaded";
  })
  .catch(e => { console.error(e);
                loadStateAddress.value = "error";
  })

  axios.get(new URL(`/i/association/place-from-place/${idUuid}`, __API_URL__))
  .then(r => r.data)
  .then(data => { associatedPlaces.value = data;
                  loadStateAssociated.value = "loaded";
  })
  .catch(e => { console.error(e);
                loadStateAssociated.value = "error" });
}

/******************************************************************/

onMounted(() => {
  getData()
});
</script>


<style scoped>
.map-block-wrapper {
  min-height: 300px;
  height: 60vh;
  margin-bottom: 5vh;
}
@media ( orientation:landscape ) {
  .map-block-wrapper {
    height: 40vh;
    margin-bottom: 5vh;
  }

}
</style>