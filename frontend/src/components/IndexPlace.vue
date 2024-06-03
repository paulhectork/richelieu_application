<!-- a special type of index for our places:
     left, a list of places. right, a map that can display
     vectors and rasters for the selected place. -->

<template>
  <div class="index-place">

    <div class="index-container">
      <table>
        <tr v-for="d in data"
        ><td>
          <button class="text-container"
                  v-html="d.text"
                  :value="d.href"
          ></button>
          <a :href="d.href" class="button-arrow-container">
            <ButtonArrow orient="right"></ButtonArrow>
          </a>
        </td></tr>
      </table>

    </div>
    <div class="map-container">
      <div id="place-map"></div>
    </div>
  </div>
</template>

<script setup>
import axios from "axios";
import { onMounted } from "vue";
import "leaflet/dist/leaflet.css";
import $ from "jquery"
import "leaflet";

import ButtonArrow from "@components/ui/ButtonArrow.vue";
import { globalDefineMap } from "@utils/leafletUtils.js";

const props = defineProps(["display", "data"])


/**
 * when clicking a place, display it on the map
 * @param {string} placeUrl: the URL to the place's main page.
 * @param {leaflet map} _map
 */
function displayVector(placeUrl, _map) {
  const placeUuid = placeUrl.split(/\//g).at(-1);  // extract the place's UUID from the URL
  const placeUuidTarget = new URL(`/i/place-lite/${placeUuid}`, __API_URL__);

  // remove the previous geojson
  _map.eachLayer((layer) => {
    layer.toRemove ? _map.removeLayer(layer) : false;
  })

  // load the geoJson and add it to the map
  axios.get(placeUuidTarget)
       .then((r) => {
        const gjPlace = L.geoJSON(
          JSON.parse(r.request.response)[0].vector, {
            onEachFeature: (feature, layer) => { layer.toRemove = true }  // will allow us to remove the geojson when another one is selected
          }
        );
        gjPlace.addTo(_map);
        _map.fitBounds(gjPlace.getBounds());
        console.log("bye");
       });

}

onMounted(() => {
  const map = globalDefineMap("place-map");

  $(".text-container").on("click", (e) => {
    const tgt = $(e.target);
    displayVector(tgt.val(), map);
  })
})
</script>

<style>
.index-place {
  height: 100%;
  width: 100%;
  display: grid;
  /*overflow: scroll;*/
  grid-template-rows: 100%;
  grid-template-columns: 50% 50%;
}

/******************************/

.index-container {
  width: 100%;
}
table {
  table-layout: fixed;
  border-spacing: 0;
  border-collapse: collapse;
  width: 100%;
}
tr, td {
  border: var(--cs-border);
  /*height: 5vh;*/
  width: 100%;
}
td {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
}
td > button {
  flex-grow: 3;
  flex-shrink: 1;
}
.button-arrow-container {
  flex-shrink: 2;
}
.button-arrow-container > button {
  display: block;
  height: 5vh;
  width: 5vh;
}

/******************************/

.map-container {
  width: 100%;
  background-color: blue;
}
#place-map {
  height: 50vh;
  width: 100%;
  /*
  position: fixed;
  top: 0;
  */

}
</style>