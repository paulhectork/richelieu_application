<!-- IndexPlace.vue

     a special type of index for our places:
     left, a list of places. right, a map that can display
     vectors and rasters for the selected place.

      props:
      * `display`: one of "resource"|"concept".
          passed to `IndexItem` to determine the style used.
      * `data`   : the array of data to display. the structure is the same
          no matter the parent which calls IndexBase, or the kind of object
          to display (Icono, Named Entity...):
        ```
        [
          // 1st object
          {
            "idUuid" : <uuid of the resource>,
            "href"   : <relative url to redirect to on click (without the url origin)>,
            "img"    : <url to the background image>,
            "text"   : <text to display in the `IndexItem`>
          },
          // other objects
          {...}
        ]
        ```

-->

<template>
  <div class="index-place">

    <div class="index-container">
      <table>
        <tr v-for="d in data" class="animate__animated animate__bounceInUp">
          <td>
            <span class="place-text"
                  v-html="capitalizeFirstChar(d.text)"
            ></span>
            <div class="buttons-outer-wrapper">
              <div class="button-wrapper">
                <UiButtonMap :value="d.href"
                             @click="displayVector"
                ></UiButtonMap>
              </div>
              <RouterLink :to="d.href"
                          class="button-wrapper"
              >
                <UiButtonLink></UiButtonLink>
              </RouterLink>

            </div>
          </td>
        </tr>
      </table>
    </div>

    <div class="map-container">
      <div id="place-map"></div>
    </div>

  </div>
</template>

<script setup>
import { onMounted, onUpdated, onBeforeUnmount, ref } from "vue";

import axios from "axios";
import $ from "jquery";
import "leaflet";
import "leaflet/dist/leaflet.css";

import UiButtonLink from "@components/UiButtonLink.vue";
import UiButtonMap from "@components/UiButtonMap.vue";
import { globalDefineMap } from "@utils/leaflet.js";
import { clickOrTouchEvent } from "@globals";
import { capitalizeFirstChar } from "@utils/strings";

/******************************************************/

const props = defineProps(["display", "data"])
const map = ref();  // will be defined in `onMounted`

/******************************************************/

/**
 * when clicking a place, display it on the map
 * @param {Event} e: the click or touchend event
 */
function displayVector(e) {
  const placeUrl = e.currentTarget.value;
  const placeUuid = placeUrl.split(/\//g).at(-1);  // extract the place's UUID from the URL
  const placeUuidTarget = new URL(`/i/place-lite/${placeUuid}`, __API_URL__);

  let _map = map.value;

  // remove the previous geojson
  _map.eachLayer((layer) => {
    layer.toRemove ? _map.removeLayer(layer) : false;
  })

  // load the geoJson and add it to the map
  axios
  .get(placeUuidTarget)
  .then((r) => {
    const gjPlace = L.geoJSON(
      JSON.parse(r.request.response)[0].vector,  // données geojson
      {
        style: { className: "place-gj" },
        onEachFeature: (feature, layer) => {
          // the layer will be removed
          layer.toRemove = true;
          // events
          layer.on({
            // interactive style
            mouseover: (e) => e.target.setStyle({ fillOpacity: 1 }),
            mouseout : (e) => e.target.setStyle({ fillOpacity: 0.5 }),
            // redirect to PlaceMainView when clicking on the geojson
            click   : () => { window.location.href = placeUrl },
            touchend: () => { window.location.href = placeUrl }
          })
        }
    });
    gjPlace.addTo(_map);
    _map.fitBounds(gjPlace.getBounds());
  })
  map.value = _map

}

/******************************************************/

onMounted(() => {
  map.value = globalDefineMap("place-map");
})
</script>

<style scoped>
.index-place {
  height: 100%;
  width: 100%;
  display: grid;
  overflow: scroll;
  grid-template-rows: 100%;
  grid-template-columns: 50% 50%;
  border-top: var(--cs-main-border);
}

/******************************/

.index-container {
  overflow: scroll;
}
table {
  /*border-collapse: collapse;*/
  border-right: var(--cs-main-border);
  border-left: var(--cs-main-border);
}
td {
  padding: 0;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
}
td > .buttons-outer-wrapper {
  display: flex;
  flex-direction: row;
}
.place-text {
  font-variant-caps: small-caps;
  font-family: var(--cs-font-sans-serif-accentuate);
}
.button-wrapper {
  flex-shrink: 2;
}
.button-wrapper > button {
  display: block;
  height: 5vh;
  width: 5vh;
}

/******************************/

.map-container {
  width: 100%;
  height: 100%;
  background-color: blue;
  align-self: start;
  position: sticky;
  top: 0;
}
#place-map {
  height: 100%;
  width: 100%;
}
.place-gj {
  transition: fill-opacity .2s;
}
</style>