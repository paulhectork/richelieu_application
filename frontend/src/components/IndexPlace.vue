<!-- a special type of index for our places:
     left, a list of places. right, a map that can display
     vectors and rasters for the selected place. -->

<template>
  <div class="index-place">

    <div class="index-container">
      <table>
        <tr v-for="d in data" class="animate__animated animate__bounceInUp">
          <td>
            <button class="text-container" v-html="d.text" :value="d.href"></button>
            <a :href="d.href" class="button-arrow-container">
              <ButtonArrow orient="right"></ButtonArrow>
            </a>
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
import axios from "axios";
import { onMounted, onUpdated, onBeforeUnmount, ref } from "vue";
import $ from "jquery";
import "leaflet";

import "leaflet/dist/leaflet.css";

import ButtonArrow from "@components/ui/ButtonArrow.vue";
import { globalDefineMap } from "@utils/leafletUtils.js";
import { clickOrTouchEvent } from "@globals";


const props = defineProps(["display", "data"])
const map = ref();  // will be defined in `onMounted`


/**
 * when clicking a place, display it on the map
 * @param {HTML Event} e: the click or touchend event
 */
function displayVector(e) {
  const placeUrl = $(e.target).val();
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
            mouseover: (e) => {
              e.target.setStyle({ fillOpacity: 1 });
            },
            mouseout: (e) => {
              e.target.setStyle({ fillOpacity: 0.5 });
            },
            // redirect to PlaceMainView when clicking on the geojson
            click: () => { window.location.href = placeUrl },
            touchend: () => { window.location.href = placeUrl }
          })
        }
    });
    gjPlace.addTo(_map);
    _map.fitBounds(gjPlace.getBounds());
  })
  map.value = _map

}


onMounted(() => {
  map.value = globalDefineMap("place-map");

  console.log(clickOrTouchEvent);
  $(".text-container").on(clickOrTouchEvent, displayVector);
})

// the index has been added
onUpdated(() => {
  /**
   * option1
   * on hover, show the vector.
   * on click, redirect to the main place page.
   * advantages    : no need for two buttons;
   * disadvantages : doesn't work on mobile
   */
  // $(".text-container").on("mouseover", displayVector);

  /**
   * option2
   * on click of the place name, show the vector
   * on click of the button, redirect to the main place page
   * advantages    : this logic works on mobile and desktop
   * disadvantages : the two button system will be confusing
   */
  // onUpdated isn't fired, so i put the thing in `onMounted`.
  $(".text-container").on(clickOrTouchEvent, displayVector);

})

onBeforeUnmount(() => {
  document.querySelector(".text-container")
          .removeEventListener(clickOrTouchEvent, displayVector)
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
  border-top: var(--cs-border);
}

/******************************/

.index-container {
  overflow: scroll;
}
table {
  /*border-collapse: collapse;*/
  border-right: var(--cs-border);
  border-left: var(--cs-border);
}

td {
  padding: 0;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
}

td>button {
  flex-grow: 3;
  flex-shrink: 1;
}

.button-arrow-container {
  flex-shrink: 2;
}

.button-arrow-container>button {
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