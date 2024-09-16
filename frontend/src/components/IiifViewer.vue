<!-- a generic IIIF viewer.

     this components gets a IIIF manifest url, fetches it
     and builds an Openseadragon viewer using it. if there
     is an error, a static image can be provided to be displayed.

     the component viewer takes 4 inputs:
     * osdId            String        : the HTML id of the IIIF viewer
     * iiifUrl          String        : an URL to a IIIF presentation manifest
     * backupImgUrl     String        : the filename a backup static file,
                                        which is on our server. this will
                                        be displayed if an error is encountered
     * backupImgDisplay String        : "cover"|"contain": value for the backup
                                        static image <img>'s object-fit css property
     * folio            Array<Number> : an optional array of folio numbers,
                                        to select which canvases to show
                                        instead of the whole manfiest
-->

<template>
  <UiLoaderComponent v-if="!isLoaded"></UiLoaderComponent>

  <div v-if="loadingFailed !== true"
       :id="osdId"
       class="iiif-viewer"
  ></div>
  <img v-else
       :src="fnToIconographyFile(backupImgUrl)"
       :style="{ objectFit: backupImgDisplay === 'cover' ? 'cover' : 'contain'  }"
       class="static-viewer"
  >

</template>

<script setup>
import { onMounted, ref, watch } from "vue";

import $ from "jquery";
import OpenSeadragon from "openseadragon";

import { manifestToTileSequence, osdNavImages } from "@utils/iiif";
import { fnToIconographyFile } from "@utils/url";
import UiLoaderComponent from "@components/UiLoaderComponent.vue";

/********************************************/

const props         = defineProps([ "osdId"
                                  , "iiifUrl"
                                  , "backupImgUrl"
                                  , "backupImgDisplay"
                                  , "folio" ]);
const emit          = defineEmits(["osd-viewer"]);
const viewer        = ref();       // OSD viewer
const loadingFailed = ref(false);  // toggled in case of an error: will display a static image file instead of a IIIF tile sequence
const isLoaded      = ref(false);  // switched to true once a IIIF viewer has loaded. hides the loader, shows the viewer

/********************************************/

function viewerErrorHandler() {
  isLoaded.value      = true;
  loadingFailed.value = true;
  emit("osd-viewer", false);
}

/**
 * build an openseadragon viewer using `tileSequence`.
 * it is anync: we wait for the viewer to be rendered
 * before returning and switching `isLoaded` to false.
 *
 * @param {Array} tileSequence: the tiles to display in the viewer
 * @param {string} osdId      : the openseadragon id of the tile
 */
async function buildOsdViewer(tileSequence, osdId) {
  viewer.value = await OpenSeadragon({
    id: osdId,
    tileSources: tileSequence,
    sequenceMode: true,
    initialPage: 0,
    showHomeControl: true,
    autoHideControls: true,
    crossOriginPolicy: true,
    defaultZoomLevel: 1,
    viewportMargins: {
      top: 10,
      left: 10,
      right: 10,
      bottom: 10
    },
    gestureSettingsMouse: { scrollToZoom: false },
    showSequenceControl: ( typeof(tileSequence)===Array && tileSequence.length > 1 )  // show sequenceControl buttons only if tileSequence contains several tiles
                         ? tileSequence.length > 1
                         : false,
    showNavigator: true,
    navigatorAutoFade: true,
    showRotationControl: true,
    prefixUrl: new URL("openseadragon-icons/", __STATICS_URL__).href,
    navImages: osdNavImages
  });
  return viewer.value.addOnceHandler("open", () => {
    $(`#${osdId} .openseadragon-canvas`).css("backgroundColor", "var(--cs-darkplum)");
    emit("osd-viewer", viewer);
    return
  });  // await for loading to be ready to return
}

/**
 * switch all state variables back to their original state.
 * to use when the props change.
 */
function revertToStartState() {
  if (viewer.value) { viewer.value.destroy() };
  viewer.value        = undefined;
  isLoaded.value      = false;
  loadingFailed.value = false;
}

/**
 * create a new viewer from the values passed in `props`.
 * called in `onMounted` and `watch(props)`, when the
 * parent updates `props` without unmounting `IiifViewer`.
 */
async function initNewViewer() {
  if ( props.iiifUrl != null ) {
    manifestToTileSequence(props.iiifUrl)
    .then( ([tileSequence, success]) => {
      if ( tileSequence.length && success ) {
        buildOsdViewer(tileSequence, props.osdId)
        .then(isLoaded.value = true)
        .catch( viewerErrorHandler );

      } else {
        viewerErrorHandler();
      }
    })
    .catch( viewerErrorHandler );
  } else {
    console.warn( `IiifViewer.vue: no IIIF for resource: ${props.osdId}` )
    viewerErrorHandler();
  }
}

/**
 * triggered when the parent changes `props` without unmounting
 * this component (for example, when changing iiif viewer in `ArticleMainView`).
 */
watch(props, (newProps, oldProps) => {
  console.log("IiifViewer:watch(props)", newProps);

  revertToStartState();
  initNewViewer();
})

/********************************************/

onMounted(async () => {
  initNewViewer();
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
}
.openseadragon-canvas {
  background: var(--cs-darkplum) !important;
}
</style>