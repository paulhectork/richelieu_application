<!-- CartographyController.vue
     a sidebar containing a form in which the user can define
     filters to change the data displayed on the map.

     @props:
      * places {Object}:
          the default `places` geoJson (corresponds to
          a geoJson representation of the `Place` database table)
      * currentFeatureCount {Integer}:
          the number of features currently displayed on the map,
          after the user filters have been applied

     @emits:
      * closeCartographyController {undefined}:
          an emit that triggers the closing of this component.
      * filterUpdate {Object}:
          on input inside the form, emit the fitler data to the parent
          CartographyView, which will trigger filtering data and updating
          the map.
-->

<template>
  <!-- cc = cartographyController -->
  <div class="cc-outer-wrapper">
    <div class="cc-closer-wrapper">
      <UiButtonCross @click="emit('closeCartographyController')"
                     @touchend="emit('closeCartographyController')"
      ></UiButtonCross>
    </div>

    <div v-if="places == null"
         class="cc-inner-wrapper"
    >
      <UiLoader></UiLoader>
    </div>
    <div class="cc-inner-wrapper"
         v-else
    >
      <h2>Filtrer les données</h2>
      <h3>
        <span v-if="props.currentFeatureCount>1">{{ currentFeatureCount }}
          parcelles correspondent</span>
        <span v-else-if="props.currentFeatureCount===1">{{ currentFeatureCount }}
          parcelle correspond</span>
        <span v-else>Aucune parcelle ne correspond</span>
        à la sélection.
      </h3>

      <div class="cc-form-wrapper">
        <FormKit type="form"
                 name="cartographyController"
                 id="cartography-controller"
                 submit-label="Lancer la recherche"
                 :submit-attrs="{ inputClass   : 'form-submit-input',
                                  wrapperClass : 'form-submit-wrapper',
                                  outerClass   : 'form-submit-outer' }"
                 @submit="''/*onSubmit*/"
                 :actions="false"
                 @input="emitFilterUpdate"
        >
          <FormKit type="fkSelect"
                   placeholder="Sélectionner une adresse"
                   name="address"
                   label="Adresse"
                   help="Sélectionner une ou plusieurs adresses"
                   :options="places.features.map(x => {
                    return { label : x.properties.address[0].address,
                             value : x.properties.address[0].id_uuid  }})"
          ></FormKit>

          <FormKit type="fkSlider"
                   outer-class="fk-range"
                   name="iconographyCount"
                   id="iconography-count"
                   label="Nombre de ressources iconographiques"
                   help="Filtrer par nombre de ressources iconographiques"
                   number="integer"
                   :step="1"
                   :minVal="Math.min.apply(null,
                     places.features.map(x => x.properties.iconography_count))"
                   :maxVal="Math.max.apply(null,
                     places.features.map(x => x.properties.iconography_count))"
          ></FormKit>

          <FormKit v-if="cartographyGranularities.length"
                   type="fkSelect"
                   name="cartographyGranularity"
                   id="cartography-granularity"
                   label="Granularité"
                   help="Sélectionner une échelle de précision pour les parcelles"
                   :options="cartographyGranularities"
                   :multiple="false"
          ></FormKit>

          <FormKit v-if="cartographySources.length"
                   type="fkSelect"
                   name="cartographySource"
                   id="cartography-source"
                   label="Source cartographique"
                   help="Sélectionner une autre source cartographique"
                   :options="cartographySources"
                   :multiple="false"
          ></FormKit>

        </FormKit>
      </div>
    </div>

  </div>
</template>


<script setup>
import { onMounted, onUnmounted, ref } from "vue";

import axios from "axios";
import $ from "jquery";
import _ from "lodash";

import UiButtonCross from "@components/UiButtonCross.vue";
import UiLoader from "@components/UiLoader.vue";

import { cartographySourceMapper } from "@globals";
import { sortCartographyBySource } from "@utils/array";

/***************************************/

const emit   = defineEmits(["closeCartographyController"
                           , "filterUpdate"
                           ]);
const props  = defineProps([ "places"
                           , "currentFeatureCount" ]);
const places = props.places;  // the whole place geoJson
const cartographySources = ref([]);  // [{ value: "...", label: "..." }]
const cartographyGranularities = ref([]);

/***************************************/

/**
 * emit an event to close this component on pressing `keydown.escape`
 */
const escHandler = (e) =>
  e.key === "Escape" ? emit("closeCartographyController") : "";

function getSources() {
  axios.get(new URL("/i/cartography-main/cartography/source", __API_URL__))
  .then(r => r.data)
  .then(data => sortCartographyBySource(data))
  .then(data => data.map(x => {
    return { label: cartographySourceMapper[x], value: x }}))
  .then(data => [{ label: "Fonds par défaut", value: "default" }].concat(data))  // add the default value as the first element of `data`
  .then(data => { cartographySources.value = data; });
}

function getGranularities() {
  let sorter = ["parcelle", "point", "galerie", "aile", "ensemble"];
  axios.get(new URL("/i/cartography-main/cartography/granularity", __API_URL__))
  .then(r => r.data)
  .then(data => data.sort((a,b) =>
    sorter.indexOf(a) - sorter.indexOf(b)))
  .then(data => data.map(x => { return {label:x, value:x} }))
  .then(data => [{ label: "Par défault", value: "default" }].concat(data))
  .then(data => { cartographyGranularities.value = data; });
}

function emitFilterUpdate(inputData) {
  inputData = _.cloneDeep(inputData);  // transform proxies into normal objects
  const newFilter = {
    address: inputData.address || [],                      // Array<String?> | Proxy<Array<String?>>
    iconographyCount: inputData.iconographyCount || [],    // Array<Number?> | Proxy<Array<Number?>>
    cartographySource:                                     // String | Undefined. if inputData.cartographySource is a string, then a source has been selected, and return it. otherwise, return undefined
      typeof inputData.cartographySource === 'string' || inputData.cartographySource instanceof String
      ? inputData.cartographySource
      : undefined,
    cartographyGranularity:
      typeof inputData.cartographyGranularity === 'string' || inputData.cartographyGranularity instanceof String
      ? inputData.cartographyGranularity
      : undefined
  }
  emit("filterUpdate", newFilter);
}


const onSubmit = () => {};

/***************************************/

onMounted(() => {
  getSources();
  getGranularities();
  $(document).on("keydown", escHandler);

})
onUnmounted(() => {
  $(document).off("keydown", escHandler);
})

</script>


<style scoped>
.cc-outer-wrapper {
  max-height: 100%;
  width: 100%;
  overflow: scroll;
}
.cc-closer-wrapper {
  display: flex;
  justify-content: flex-end;
  margin: 1vh 1vh 0 1vh;
}
.cc-closer-wrapper button {
  height: 5vh;
  width: 5vh;
}
.cc-inner-wrapper {
  margin: 0 3vh;
  max-height: 100%;
  display: grid;
  grid-template-columns: 100%;
  grid-template-rows: 5% 2fr;

}
h2 {
  margin: 0 auto;
}
h3 {
  margin: 0 auto;
  height: fit-content;
}

/**************************************/

.cc-form-wrapper > #cartography-controller {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  overflow-x: scroll;
  padding: 2%;
}
:deep(.formkit-outer) {
  margin: 5% 0;
}
.fk-range :deep(.formkit-inner) {
  display: flex;
  flex-direction: row;
  align-items: center;
}
/** avoid overflow in the noUi slider */
:deep(.noUi-target) {
  width: 90%;
  margin: 5px;
}
</style>