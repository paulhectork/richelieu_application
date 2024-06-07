<!-- a generic IIIF viewer.

     this IIIF viewer takes 4 inputs:
     * osdId        : the HTML id of the IIIF viewer
     * iiifUrl      : an URL to a IIIF presentation manifest
     * backupImgUrl : the filename a backup static file,
                      which is on our server. this will
                      be displayed if an error is encountered
     * folio        : an optional array of folio numbers, to select which
                      canvases to show instead of the whole manfiest
-->

<template>
  <div v-if="loadingFailed !== true"
       :id="osdId"
       class="iiif-viewer"
  ></div>
  <img v-else
       :src="fnToIconographyFile(backupImgUrl)"
       class="static-viewer">
</template>

<script setup>
import { onMounted, ref } from "vue";

import OpenSeadragon from "openseadragon";

import { manifestToTileSequence, osdNavImages } from "@utils/iiif";
import { fnToIconographyFile } from "@utils/functions";


const props = defineProps(["osdId", "iiifUrl", "backupImgUrl", "folio"]);
const viewer = ref();              // OSD viewer
const loadingFailed = ref(false);  // toggled in case of an error: will display a static image file instead of a IIIF tile sequence


/**
 * build an openseadragon viewer using `tileSequence`
 *
 * @param {Array} tileSequence: the tiles to display in the viewer
 * @param {string} osdId: the openseadragon id of the tile
 */
function buildOsdViewer(tileSequence, osdId) {
  viewer.value = OpenSeadragon({
    id: osdId,
    tileSources: tileSequence,
    sequenceMode: true,
    initialPage: 0,
    showHomeControl: true,
    autoHideControls: true,
    crossOriginPolicy: true,
    viewportMargins: {
      top: 10,
      left: 10,
      right: 10,
      bottom: 10
    },
    gestureSettingsMouse: { scrollToZoom: false },
    showSequenceControl: ( typeof(tileSequence) === Array  // show sequenceControl buttons only if tileSequence contains several tiles
                           && tileSequence.length > 1 )
                         ? tileSequence.length > 1
                         : false,
    showNavigator: true,
    navigatorAutoFade: true,
    showRotationControl: true,
    prefixUrl: new URL("/statics/openseadragon-icons/", __SERVER_URL__).href,
    navImages: osdNavImages
  });
}


onMounted(() => {
  manifestToTileSequence(props.iiifUrl)
  .then(([tileSequence, success]) => {
    if ( tileSequence.length && success ) {
      buildOsdViewer(tileSequence, props.osdId)
    } else {
      loadingFailed.value = true;
    }
  });
})
</script>

<style scoped>
.iiif-viewer {
  height: 100%;
  width: 100%;
}
.static-viewer {
  width: 100%;
  height: 100%;
  object-fit: contain;
}
</style>