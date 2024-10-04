<!--

     based on: https://github.com/MapunaH/code-stage

     the displaying of the right block (CartographyPlaceInfo) is
     determined by the value of `displayRight` and `placeIdUuid`.
     - `placeIdUuid` controls the creation of `CartographyPlaceInfo`
     - `displayRight` (bool) changes the CSS display to allow the
       block to be visible.
 -->

<template>
  <h1 hidden>Cartographie</h1>
  <div class="cartography-outer-wrapper"
       :class="{ 'right-visible': displayRight }"
  >
    <div class="cartography-controller-wrapper"></div>

    <div class="cartography-wrapper">
      <div id="map-main"></div>
    </div>

    <!--<Transition name="slideInOut">-->
    <div class="cartography-place-wrapper"
         v-if="placeIdUuid !== undefined"
    >
      <CartographyPlaceInfo :placeIdUuid="placeIdUuid"
                            @close="closeCartographyPlaceInfo"
      ></CartographyPlaceInfo>
    </div>
    <!--</Transition>-->

  </div>
</template>


<script setup>
import { onMounted, ref, watch } from "vue";

import axios from "axios";
import L from "leaflet";

import CartographyPlaceInfo from "@components/CartographyPlaceInfo.vue";

import { globalDefineMap } from "@utils/leaflet";
import { colorScaleBlue, colorScaleRed } from "@utils/colors";

/************************************************************/

const map          = ref();  // defined in onMounted
const places       = ref([]);
const placeIdUuid  = ref();  // when this is set, an indx of iconography resources of the place with place.id_uuid == placeIdUuid will be displayed
const displayRight = ref(false);  // when true, the right block will be displayed
const loadState    = ref("loading");  // loading/loaded/error

const transDur     = 500;  // transition duration

// [ [min,max], color ]
const colorClasses = [ [ [321, Infinity], colorScaleRed(0/7) ] // marina's color scale: '#000000'
                     , [ [161, 320]     , colorScaleRed(1/7) ] // marina's color scale: '#4b0082'
                     , [ [81, 160]      , colorScaleRed(2/7) ] // marina's color scale: '#800080'
                     , [ [41, 80]       , colorScaleRed(3/7) ] // marina's color scale: '#ff0000'
                     , [ [21, 40]       , colorScaleRed(4/7) ] // marina's color scale: '#ff4500'
                     , [ [11, 20]       , colorScaleRed(5/7) ] // marina's color scale: '#ff7f50'
                     , [ [6, 10]        , colorScaleRed(6/7) ] // marina's color scale: '#ffddc1'
                     , [ [0, 5]         , colorScaleRed(7/7) ] // marina's color scale: '#ffffff'
                     ];

/************************************************************/

/**
 * when receiving a `close` event from CartographyPlaceInfo,
 * hide the `.cartography-place-wrapper` before unmounting
 * the `CartographyPlaceInfo`. the setTimeout allows to be
 * sure that `.cartography-place-wrapper` has been hidden before
 * unmounting
 */
function closeCartographyPlaceInfo() {
  displayRight.value = false;
  setTimeout(() => { placeIdUuid.value = undefined }, 500);
}

function getData() {
  return Promise.all([
    axios.get(new URL("/i/cartography-main/places", __API_URL__))
    .then(r => r.data)
    .then(data => { places.value = data; })
  ])
}

function addPlacesToMap(_map, _places) {


  const gjPlaces = L.geoJSON(places.value, {
    style: (feature) => {
      // option1: continuous scale opacity variant
      // let opacityCalc = (c, _max) => .5 + c / (_max * 2),
      //     countArr    = _places.features.map(p => p.properties.iconography_count),  // array of number of iconography_counts
      //     countMax    = Math.max.apply(null, countArr),
      //     countMin    = Math.min.apply(null, countArr);
      // return { fillOpacity: opacityCalc(feature.properties.iconography_count, countMax) }},

      // option2: discrete colors
      const iconographyCount = feature.properties.iconography_count,
            comparator = (range, num) => range[0] <= num && num <= range[1];
      return {
        fillColor: colorClasses.find( (c) => comparator(c[0], iconographyCount) )[1],  // if iconographyCount is in a range defined in `colorClasses`, select the color
        fillOpacity: .5,
      }
    },

    onEachFeature: (feature, layer) => {
      layer.on("click", (e) => {
        // set the data, which will trigger mounting/display of CartographyPlaceInfo
        placeIdUuid.value = undefined;
        displayRight.value = true;
        placeIdUuid.value = feature.properties.id_uuid;
        // set the style: opacity of 1 on the clicked layer
        gjPlaces.resetStyle();  // revert the opacity for all layers
        layer.setStyle({ fillOpacity:1 });
        // zoom to the clicked layer
        //TODO fix yank here ?
        setTimeout(() => {        // wait for the size animation to complete...
          _map.fitBounds(layer.getBounds())
        }, transDur);
      });
      // layer.on("mouseover", (e) =>
      //   layer.setStyle({ color: layer.options.fillColor })  // works sometimes but then bugs
      // );
      // layer.on("mouseout", (e) => {
      //   layer.resetStyle()}  // definitely doesn't work
      // )
    }
  });
  gjPlaces.addTo(_map);
  _map.fitBounds(gjPlaces.getBounds());
  return _map;
}

/************************************************************/

/**
 * when (un)mounting `CartographyPlaceInfo`, the size of the map changes.
 * leaflet doesn't take this into account. this causes:
 * - on mount: buggy zooms
 * - on unmount: data positionned where `CartographyPlaceInfo` used to be
 *   is not displayed.
 * so, when (un)mounting, call `map.invalidateSize()` to force the redraw.
 * it's supposed to be possible to use `map.on(resize)` to do this,
 * but it doesn't work.
 */
watch(placeIdUuid, (newId, oldId) =>
  oldId !== undefined && newId === undefined && map.value != undefined    // unmount
  ? map.value.invalidateSize()
  : oldId === undefined && newId !== undefined && map.value != undefined  // mount
  ? setTimeout(() => map.value.invalidateSize(), transDur)  // the setTimeout is to wait for the transition to complete
  : ''
)

onMounted(() => {
  map.value = globalDefineMap("map-main");  // synchronous
  getData().then(() => {
    map.value = addPlacesToMap( map.value, places.value ) });
})
</script>


<style scoped>
.cartography-outer-wrapper {
  height: calc(100vh - var(--cs-navbar-height));
  width: 100%;

  display: grid;
  grid-template-columns: 30% 100% 30%;

  transform: translateX(-30%);
  transition: grid-template-columns v-bind("transDur");
}

.cartography-outer-wrapper.right-visible {
  grid-template-columns: 30% 70% 30%;
}

.cartography-place-wrapper {
  z-index: 400;
  height: 100%;
  width: 100%;
}

/**************************************/

#map-main {
  height: calc(100vh - var(--cs-navbar-height));
  width: 100%;
}
</style>