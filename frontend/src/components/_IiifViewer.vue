<template>
  <div :id="osdId"
       class="iiif-viewer"
  ></div>
</template>

<script setup>
import { onMounted, ref } from "vue";

import OpenSeadragon from "openseadragon";

import { manifestToTileSequence } from "@utils/iiif";


const props = defineProps(["osdId", "iiifUrl"]);
const viewer = ref();    // OSD viewer


/**
 * build an openseadragon viewer using `tileSequence`
 *
 * @param {Array} tileSequence: the tiles to display in the viewer
 * @param {string} osdId: the openseadragon id of the tile
 */
function buildOsdViewer(tileSequence, osdId) {
  viewer.value = OpenSeadragon({
    id: osdId,
    prefixUrl: `../assets/icons/openseadragon-icons/`,
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
    // navImages: globals.navImages
  });
}


onMounted(() => {
  manifestToTileSequence(props.iiifUrl)
  .then((tileSequence) => {
    buildOsdViewer(tileSequence, props.osdId)
  });
})
</script>

<style scoped>
.iiif-viewer {
  height: 100%;
  width: 100%;
}
</style>