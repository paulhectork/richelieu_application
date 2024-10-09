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

      <div class="cc-form-wrapper">
        <FormKit type="form"
                 name="cartographyController"
                 :actions="true"
                 id="cartography-controller"
                 submit-label="Lancer la recherche"
                 :submit-attrs="{ inputClass   : 'form-submit-input',
                                  wrapperClass : 'form-submit-wrapper',
                                  outerClass   : 'form-submit-outer' }"
            @submit="''/*onSubmit*/"
        >
          <FormKit type="fkSelect"
                   placeholder="Sélectionner une addresse"
                   name="address"
                   label="Addresse"
                   help="Sélectionner une ou plusieurs addresses"
                   :options="places.features.map(x => {
                    return { label : x.properties.address[0].address,
                             value : x.properties.address[0].id_uuid  }})"
                   @input="handleAddress"
          ></FormKit>

          <FormKit type="fkSlider"
                   outer-class="fk-range"
                   name="iconography-count"
                   id="iconography-count"
                   label="Nombre de ressources iconographiques"
                   help="Filtrer par nombre de ressources iconographiques"
                   number="integer"
                   :step="1"
                   :minVal="Math.min.apply(null,
                     places.features.map(x => x.properties.iconography_count))"
                   :maxVal="Math.max.apply(null,
                     places.features.map(x => x.properties.iconography_count))"
                   @input="handleIconographyCount"
          ></FormKit>

          <FormKit v-if="cartographySources.length"
                   type="fkSelect"
                   name="cartography-source"
                   id="cartography-source"
                   label="Changer de source cartographique"
                   help="Sélectionner une autre source cartographique"
                   :options="cartographySources"
                   :multiple="false"
                   @input="handleCartographySource"
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

import UiButtonCross from "@components/UiButtonCross.vue";

import { cartographySourceMapper } from "@globals";
import { sortCartographyBySource } from "@utils/array";

/***************************************/

const emit               = defineEmits(["closeCartographyController"
                                       , "filterAddress"
                                       , "filterIconographyCount"
                                       , "filterCartographySource" ]);
const props              = defineProps(["places"]);
const places             = props.places;  // the whole place geoJson
const cartographySources = ref([]);  // [{ value: "...", label: "..." }]


const currentFilters = {
  address           : [],        // Array<string>: the selected addresses. display all if empty
  iconographyCount  : [],        // Array<integer>: the min/max range of iconographies to display
  cartographySource : "default"  // string: which cartography source to use. if "default", show all that's in the `Place` database, regardless of source
}

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
  .then(data => { cartographySources.value = data; });
}

/**
 * handle an address selection filter change in `CartographyController`
 */
function handleAddress() {
  console.log(1)
}

/**
 * handle an iconography count filter change in `CartographyController`
 */
function handleIconographyCount() {
  console.log(2)
}

/**
 * handle a cartography source change in `CartographyController`
 */
function handleCartographySource() {
  console.log(3)
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
  height: 100%;
  width: 100%;
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
}
h2 {
  margin: 0 auto;
}

/**************************************/

.fk-range :deep(.formkit-inner) {
  display: flex;
  flex-direction: row;
  align-items: center;
}
</style>