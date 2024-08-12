<!-- a map for `IconographyMainView`
     `IconographyMainView` sens this component the following:
     > placeGeoJson: a geojson of places related to the
                     resource in `IconographyMainView`
     > lflId       : an HTML id for the leafet map container

     from this data, this compnent builds a leaflet map
-->

<template>
  <div :id="lflId"
       class="leaflet-viewer"
  ></div>
</template>


<script setup>
import axios from "axios";
import { ref, onMounted } from "vue";

import $ from "jquery";

import { globalDefineMap } from "@utils/leafletUtils";
import { urlToFrontendPlace } from "@utils/url";

/******************************************************/

const props = defineProps([ "lflId", "placeGeoJson" ]);
const map = ref();

/******************************************************/

async function buildPlacePopup(placeUuid) {
  const apiTarget = new URL(`/i/place-lite/${placeUuid}`, __API_URL__);
  return axios.get(apiTarget).then(r => {
    let address = r.data[0].address;
    address = address.length
              ? address[0].address
              : "Addresse inconnue";
    return `<a href="${urlToFrontendPlace(placeUuid).href}"
            >${address}</a>`
  })
}

async function buildMap() {
  const _map = await globalDefineMap(props.lflId);
  const gjPlace = L.geoJSON(props.placeGeoJson, {
    onEachFeature: (feature, layer) => {
      // fetch place info aynchronously and create a popup
      buildPlacePopup(feature.properties.id_uuid)
      .then((popupContent) => {
        layer.bindPopup(popupContent)
      })
    }
  });
  gjPlace.addTo(_map);
  _map.fitBounds(gjPlace.getBounds());
  map.value = _map;
}

/******************************************************/

onMounted(() => {
  buildMap()
})

</script>


<style scoped>
.leaflet-viewer {
  height: 100%;
}
</style>