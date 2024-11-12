<!-- CartographyPlaceInfo.vue

     information on a place, displayed in `CartographyView.vue`,
     when clicking on a place feature on the map, in a sidebar.

     it contains:
     - the address
     - a list of the 5 places that are the most frequently
       associated to this place.
     - an index of iconography resources related to a place,
       to be displayed on the cartographic interface when
       clicking on a geojson feature

     props:
     - placeIdUuid (string)
        the place.id_uuid of the place we want to display data on
     - associatedPlaces (object)
        an array of the places most often associated with the current place.
        structure:
        [ { id_uuid : <string:place.id_uuid>,
            count   : <int:number of relations between input place and related places>
          }
        ]

     emits:
     - closePlaceInfo:
        emitting this event will trigger the unmounting of this component
-->

<template>
  <div class="cpi-outer-wrapper negative-default"
       :id="`cpi-${ placeIdUuid }`"
  >  <!-- cpi = CartographyPlaceInfo -->
    <div class="cpi-closer-wrapper">
      <UiButtonCross @click="emit('closePlaceInfo')"
                     @touchend="emit('closePlaceInfo')"
      ></UiButtonCross>
    </div>
    <div class="cpi-inner-wrapper">
      <h2 v-if="loadStateAddress === 'loaded'">
        {{ capitalizeFirstChar(address.address) }}</h2>

      <UiLoader v-if="loadStatePlace === 'loading'">
      </UiLoader>
      <div v-if="loadStatePlace === 'loaded'"
           class="iconography-index-outer-wrapper"
      >
        <p>Voir <RouterLink :to="`/lieu/${placeIdUuid}`">
          la page principale de ce lieu</RouterLink>.</p>

        <p v-if="place.iconography.length > 1">
          <strong>{{ place.iconography.length }} ressources iconographiques</strong>
          sont associées à ce lieu.</p>
        <p v-else-if="place.iconography.length === 1">
          <strong>{{ place.iconography.length }} ressource iconographique</strong>
          est associée à ce lieu.</p>
        <p v-else-if="place.iconography.length === 0">
          <strong>Aucune ressource iconographique</strong>
          n'est associée à ce lieu.</p>

        <IndexAssociationRedirects fromTable="place"
                                   toTable="place"
                                   :from="{ entry_name: address, id_uuid: placeIdUuid }"
                                   :to="associatedPlaces"
        ></IndexAssociationRedirects>

        <div class="iconography-index-wrapper">
          <IndexBase :data="iconographyDataFilter"
                     :itemsPerRow="1"
                     display="resource"
          ></IndexBase>
        </div>
      </div>
    </div>
  </div>
</template>


<script setup>
import { onMounted, ref, onUnmounted, watch } from "vue";

import axios from "axios";
import $ from "jquery";

import UiLoader from "@components/UiLoader.vue";
import UiButtonCross from "@components/UiButtonCross.vue";
import IndexBase from "@components/IndexBase.vue";
import IndexAssociationRedirects from "@components/IndexAssociationRedirects.vue";

import { indexDataFormatterIconography } from "@utils/indexDataFormatter";
import { sortAddressBySource } from "@utils/array.js";
import { capitalizeFirstChar } from "@utils/strings";

/***************************************/

const props                 = defineProps(["placeIdUuid", "associatedPlaces"]);
const emit                  = defineEmits(["closePlaceInfo"]);

const placeIdUuid           = ref("");
const associatedPlaces      = ref([]);
const place                 = ref();
const address               = ref()
const iconographyDataFilter = ref([]);
const loadStateAddress      = ref("loading");  // loading/loaded/error
const loadStatePlace        = ref("loading");  // loading/loaded/error

/***************************************/

/**
 * emit an event to close this component on pressing `keydown.escape`
 */
const escHandler = (e) => e.key === "Escape" ? emit("closePlaceInfo") : "";

/**
 * UNUSED: it also closes the component when dragging the map around.
 * emit an event to close this component when clicking outside of it
 */
// const clickHandler = (e) => {
//   $(e.target).closest($(`#cpi-${ placeIdUuid }`)).length === 0
//   ? emit("close")
//   : "";
// };

function resetData() {
  placeIdUuid.value           = "";
  place.value                 = undefined;
  associatedPlaces.value      = undefined;
  address.value               = undefined;
  iconographyDataFilter.value = [];
  loadStateAddress.value      = "loading";
  loadStatePlace.value        = "loading";
}

function getData() {
  axios.get(new URL(`/i/place/${placeIdUuid.value}`, __API_URL__))
  .then(r => r.data[0])
  .then(data => {
    place.value = data;
    iconographyDataFilter.value = indexDataFormatterIconography(place.value.iconography);
    loadStatePlace.value = "loaded";
  })
  .catch(e => { console.error(e); loadStatePlace.value = "error" });

  axios.get(new URL(`/i/place-address/${placeIdUuid.value}`, __API_URL__))
  .then(r => r.data)
  .then(sortAddressBySource)
  .then(r => { address.value = r[0];
               loadStateAddress.value = "loaded" })
  .catch(e => { console.error(e); loadStateAddress.value = "error" })
}

/****************************************/

/**
 * on the map, when clicking on a feature while a `CartographyPlaceInfo`
 * is open, update the data to be displayed in `CartographyPlaceInfo` so
 * that it matches the newly clicked feature.
 */
watch(props, (newProps, oldProps) => {
  resetData();
  placeIdUuid.value = newProps.placeIdUuid;
  associatedPlaces.value = newProps.associatedPlaces;
  getData();
})

onMounted(() => {
  placeIdUuid.value = props.placeIdUuid;
  getData();
  $(document).on("keydown", escHandler);
             // .on("click", clickHandler),

})

onUnmounted(() =>
  $(document).off("keydown", escHandler)
             //.off("click", clickHandler)
);
</script>


<style scoped>
/*
.iconography-index-wrapper {
  overflow: scroll;
  max-height: 100vh;
}
*/
.cpi-outer-wrapper {
  max-height: calc(100vh - var(--cs-navbar-height));
  height: calc(100vh - var(--cs-navbar-height));
  overflow: scroll;
  border-left: var(--cs-negative-border);
}
.cpi-closer-wrapper {
  display: flex;
  justify-content: flex-end;
  margin: 1vh 1vh 0 1vh;

}
.cpi-closer-wrapper > button {
  height: 5vh;
  width: 5vh;
}
.cpi-inner-wrapper {
  height: 100%;
  margin: 0 3vh;
}
h2 {
  margin-top: 0;
}

</style>