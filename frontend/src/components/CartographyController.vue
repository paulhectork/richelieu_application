<template>
  <!-- cc = cartographyController -->
  <div class="cc-outer-wrapper">
    <div class="cc-closer-wrapper">
      <UiButtonCross @click="emit('closeCartographyController')"
                     @touchend="emit('closeCartographyController')"
      ></UiButtonCross>
    </div>

    <div class="cc-inner-wrapper">
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
                   placeholder="Sélectionner une addresse"
                   name="address"
                   label="Addresse"
                   help="Sélectionner une ou plusieurs addresses"
                   :options="places.features.map(x => {
                    return { label : x.properties.address[0].address,
                             value : x.properties.address[0].id_uuid  }})"
                   @input="''/*data => emit('filterAddress', data)*/"
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
                   @input="''/*data => emit('filterIconographyCount', data)*/"
          ></FormKit>

          <FormKit v-if="cartographySources.length"
                   type="fkSelect"
                   name="cartographySource"
                   id="cartography-source"
                   label="Changer de source cartographique"
                   help="Sélectionner une autre source cartographique"
                   :options="cartographySources"
                   :multiple="false"
                   @input="''/*data => emit('filterCartographySource', data)*/"
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

/***************************************/

/**
 * emit an event to close this component on pressing `keydown.escape`
 */
const escHandler = (e) => e.key === "Escape" ? emit("closeCartographyController") : "";

function getData() {
  axios.get(new URL("/i/cartography-main/cartography-sources", __API_URL__))
  .then(r => r.data)
  .then(data => sortCartographyBySource(data))
  .then(data => data.map(x => {
    return { label: cartographySourceMapper[x], value: x }}))
  .then(data => [{ label: "Fonds par défaut", value: "default" }].concat(data))  // add the default value as the first element of `data`
  .then(data => { cartographySources.value = data; });
}

function emitFilterUpdate(inputData) {
  inputData = _.cloneDeep(inputData);  // transform proxies into normal objects
  const newFilter = {
    address: inputData.address || [],                      // Array<String?> | Proxy<Array<String?>>
    iconographyCount: inputData.iconographyCount || [],    // Array<Number?> | Proxy<Array<Number?>>
    cartographySource:                                     // String | Undefined. if inputData.cartographySource is a string, then a source has been selected, and return it. otherwise, return undefined
      typeof inputData.cartographySource === 'string' || inputData.cartographySource instanceof String
      ? inputData.cartographySource
      : undefined
  }
  emit("filterUpdate", newFilter);
}

const onSubmit = () => {};

/***************************************/

onMounted(() => {
  getData();
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
</style>