<!-- TheVisualBar.vue

     a decorative bar that is on the side of the website
-->

<template>
  <div class="visual-bar-wrapper">
    <!-- <img :src="menuCropPath"> -->
    <div class="visual-bar-iiif-wrapper">
      <div :id="htmlId"></div>
      <!--
      <IiifViewer osdId="visual-bar-iiif-viewer"
                  :iiifUrl="manifestUrl"
                  @osd-viewer="assignOsdViewer"
      ></IiifViewer>
      -->
    </div>
  </div>
</template>


<script setup>
import { ref, onMounted } from "vue";

import $ from "jquery";
import OpenSeadragon from "openseadragon";

import IiifViewer from "@components/IiifViewer.vue";
import { manifestToTileSequence, osdNavImages } from "@utils/iiif";

/****************************************/

const menuCropPath = "../src/assets/media/menu_crop.jpg";
const iiifUrl = "https://apicollections.parismusees.paris.fr/iiif/320057446/manifest";
const htmlId = "visual-bar-iiif-viewer";
const idUuidIconography = "qr11679c39145004726a591f2b7086234e5";

const viewer = ref();

/****************************************/

/**
 * build an openseadragon viewer using `tileSequence`.
 * it is anync: we wait for the viewer to be rendered
 * before returning and switching `isLoaded` to false.
 *
 * @param {Array} tileSequence: the tiles to display in the viewer
 * @param {string} osdId      : the html ID for this openseadragon viewer
 */
async function buildOsdViewer(tileSequence, osdId) {
  console.log(osdId, tileSequence)
  viewer.value = OpenSeadragon({
    id: osdId,
    tileSources: tileSequence,
    sequenceMode: false,
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
    showSequenceControl: false,
    showRotationControl: false,
    showNavigator: false,
    navigatorAutoFade: true,
    minScrollDeltaTime: 200,
    prefixUrl: new URL("/statics/openseadragon-icons/", __SERVER_URL__).href,
    navImages: osdNavImages,

    /*
    panHorizontal: false,
    defaultZoomLevel: 20,
    minZoomLevel: 20,
    maxZoomLevel: 20,
    visibilityRatio: 1,
    */
  });
  return await viewer.value.addOnceHandler("open", () => {
    // see: https://codepen.io/iangilman/pen/RZxEWZ
    let tiledImage = viewer.value.world.getItemAt(0);
    let targetZoom = tiledImage.source.dimensions.x / viewer.value.viewport.getContainerSize().x;
    viewer.value.viewport.zoomTo(targetZoom, null, true);
    return; });  // await for loading to be ready to return
}

onMounted(() => {
  $(`#${htmlId}`).height("100%");
  manifestToTileSequence(iiifUrl)
  .then( ([tileSequence, success]) => {
    if ( tileSequence.length && success ) {
      buildOsdViewer(tileSequence, htmlId)
    }
  })
})
</script>


<style scoped>
.visual-bar-wrapper {
  width: 100%;
  height: 100%;
  overflow: hidden;
  border-top: var(--cs-border);
  border-left: none;
}
.visual-bar-iiif-wrapper {
  margin: 5px;
  border:var(--cs-border);
  height: 100%;

}
img {
  object-fit: center;
  min-height: 100%;
  min-width: 100%;

}

@media ( orientation: landscape ) {
  .visual-bar-wrapper {
    border-top: none;
    border-left: var(--cs-border);
  }
}
</style>