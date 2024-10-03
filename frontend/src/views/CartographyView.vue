<template>
  <div class="cartography-wrapper">
    <div id="map-main"></div>
  </div>
</template>


<script setup>
import { onMounted, ref } from "vue";

import axios from "axios";
import L from "leaflet";

import WaitingToComeToLife from "@components/WaitingToComeToLife.vue";
import { globalDefineMap } from "@utils/leafletUtils";

/************************************************************/

const map    = ref();  // defined in onMounted
const places = ref([]);
const loadState = ref("loading");  // loading/loaded/error

// [ [min,max], color ]
const colorScales = [ [ [161, 320], '#000000' ]
                    , [ [81, 160], '#4b0082']
                    , [ [41, 80], '#800080']
                    , [ [21, 40], '#ff0000']
                    , [ [11, 20], '#ff4500']
                    , [ [5, 10], '#ff7f50']
                    , [ [0, 5], '#ffddc1']
                    ];

/************************************************************/

function getData() {
  return Promise.all([
    axios.get(new URL("/i/cartography-main/places", __API_URL__))
    .then(r => r.data)
    .then(data => { places.value = data; })
  ])
}

function addPlacesToMap(_map, _places) {
  let countArr = _places.features.map(p => p.properties.iconography_count),  // array of number of iconography_counts
      countMax = Math.max.apply(null, countArr),
      countMin = Math.min.apply(null, countArr);

  const opacityCalc = (c, _max) => .5 + c / (_max * 2);
  const gjPlaces = L.geoJSON(places.value, {
    style: (feature) => {
      // option1: continuous scale opacity variant
      // return { fillOpacity: opacityCalc(feature.properties.iconography_count, countMax) }},

      // option2: discrete colors
      let iconographyCount = feature.properties.iconography_count;
      return { fillColor: colorScales.find((c) =>
        iconographyCount >= c[0][0] && iconographyCount <= c[0][1] )[1] }},  // is undefined

    onEachFeature: (feature, layer) =>
      layer.on("click", (e) =>
        console.log(feature.properties.id_uuid,
                    layer.feature.properties.iconography_count,
                    opacityCalc(feature.properties.iconography_count, countMax)))
  });
  gjPlaces.addTo(_map);
  return _map;
}

/************************************************************/

onMounted(() => {
  map.value = globalDefineMap("map-main");  // synchronous
  getData().then(() => { map.value = addPlacesToMap( map.value, places.value ) });
})
</script>


<style scoped>
.cartography-viewer {
  height: calc(100vh - var(--cs-navbar-height));
  width: 100%;
}
#map-main {
  height: calc(100vh - var(--cs-navbar-height));
  width: 100%;
}
</style>