<!-- a special type of index for our places:
     left, a list of places. right, a map that can display
     vectors and rasters for the selected place. -->

<template>
  <div class="index-place">
    <div class="index-container">
      <table>
        <tr v-for="d in data"
        ><td>
          <a v-html="d.text"></a>
        </td></tr>
      </table>

    </div>
    <div class="map-container">
      <div id="place-map"></div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from "vue";
import "leaflet/dist/leaflet.css";
import "leaflet";

const props = defineProps([ "display"
                          , "data" ])

function defineMap() {
  return L.map("place-map", {
    center: [ 48.8687452, 2.3363674 ]
    , maxBounds: L.latLngBounds([ { lat: 48.8856701621242, lng: 2.3092982353700506 }
                                , { lat: 48.829997780023035, lng: 2.3845843750075915 }
    ])
    , inertia: false  // inertia does weird things with the geojson layer
    , maxBoundsViscosity: 1.0
    , scrollWheelZoom: false
    , zoomControl: false
    , minZoom: 13  // 11 for paris + region, 13 for the neighbourhood
    , zoom: 14.7
  });
}

onMounted(() => {
  const map = defineMap();
  L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);
})
</script>

<style>
.index-place {
  display: grid;
  overflow: scroll;
  grid-template-rows: 100%;
  grid-template-columns: 50% 50%;
}
.index-container {
  width: 100%;
}
table {
  table-layout: fixed;
  border-spacing: 0;
  border-collapse: collapse;
}
tr, td {
  border: var(--cs-border);
}

.map-container {
  width: 100%;
  background-color: blue;
}
#place-map {
  height: 50vh;
  width: 100%;
}
</style>