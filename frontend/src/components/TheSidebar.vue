<!-- TheSidebar.vue

     a decorative sidebar incorporating a IIIF viewer.
     the viewer is panned depending on the % of page scrolling.
     if there's an error, a static image is displayed.

     logic:
     1) create an openseadragon IIIF viewer. if there's no error,
        assign the osd viewer to the ref `viewer`. if there is an error,
        the ref `viewer` is `false` and the Openseadragon-specific
        behaviours are disabled.
     2) if there's no error: on page scrolling, the viewport is be
        panned from left to right.
        > `viewportPan()` handles the panning, depending on the % of
          the page that has been scrolled.
        > the Osd viewer can be manipulated by hand (clicked, pinched etc.),
          which can zoom/move the image around and mess up our scrolling.
          to prevent that, we use
          > `viewportRevert()` to go back to the expected panning/zooming levels
          > `viewportReset()` to go back to the original position and zooming level on page change.

     x-axis scrolling is ponly allowed within a certain range, defined
     by setting min-max values in a `viewportConfig` object:

     X = non-scrollable zone
     V = scrollable zone
     ______________________________
     |   |                    |   |
     |   |                    |   |
     | X |         V          | X |
     |   |                    |   |
     |   |                    |   |
     ______________________________

-->

<template>
  <div class="sidebar-wrapper">
    <!-- <img :src="menuCropPath"> -->
    <div class="sidebar-iiif-wrapper">
      <IiifViewer :osdId="htmlId"
                  :iiifUrl="iiifUrl"
                  :backupImgUrl="imgUrl"
                  backupImgDisplay="cover"
                  @osd-viewer="defineViewer"
      ></IiifViewer>
    </div>
  </div>
</template>


<script setup>
import { ref, onMounted, onUnmounted, watch } from "vue";
import { useRoute } from "vue-router";

import $ from "jquery";
import OpenSeadragon from "openseadragon";

import IiifViewer from "@components/IiifViewer.vue";
import { fnToIconographyFile } from "@utils/url";

/****************************************/

// wrong URL to test error handling
// const iiifUrl           = "https://example.com";
const iiifUrl           = "https://apicollections.parismusees.paris.fr/iiif/320057446/manifest";
const imgUrl            = "qr16080c31522fa44a3b238cb3790054d1c.jpg";
const htmlId            = "sidebar-iiif-viewer";
const idUuidIconography = "qr11679c39145004726a591f2b7086234e5";

const route    = useRoute();
const viewer   = ref(); // Openseadragon.viewer: the IIIF viewer
const panPoint = ref(); // Openseadragon.Point : the point on which the viewer is centered

/**
 * viewport config and coordinates.
 *
 * `xStartPos` is the left-minimum point the viewport can panned to.
 * `xEndPoint` is the right-maximum point the viewport can be panned to.
 * `yPos`      is the center of the viewport (we only do vertical scrolling).
 * `zoom`      is the zoom level. it is redefined in `defineViewer()`.
 *
 * a reminder, an openseadraon viewport's are defined by
 * an (x,y) tuple, with x and y in the range 0..1.
 * the center of the viewport is (0.5 , 0.5),
 * the top-left point is         (0   , 0  ),
 * the bottom-right point is     (1   , 1  ).
 */
 const viewportConfig = { xStartPos:0.3, xEndPos:0.7, yPos:0.5, zoom:30 };

/****************************************/

/////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////
/** TODO
 * - error handling if the IIIF viewer doesn't load
 * - see if there are other events on the OSD viewer
 *   that should trigger viewportRevert
 */
/////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////

/**
 * get the scroll ratio of "main":
 * 0 = hasn't been scrolled at all,
 * 1 = has completely been scrolled
 * @returns {Number}: 0..1
 */
function getScrollRatio() {
  var s = $("main").scrollTop(),     // number of pixels to scroll back to top
      f = $("main")[0].scrollHeight, // full height of overflow: scroll element.
      m = $("main").height() / 2;    // half the height of "main" on the client (without the overflow: scroll stuff)

  return (s+m)/f;
}

/**
 * calculate the point to pan the viewer to, optionnally
 * depending on the scrolling % of "main":
 *
 * the y-coordinate of the point returned is defined by `y`
 * the x-coordinate of that point is within a range of (`xStart`,`xEnd`),
 * and its precise poisition depends on the % of main that has been scrolled.
 * at the top of the page, `x` == `xStart`, at the end, it is closer to `xEnd`.
 *
 * @param {Number} xStart       : the X minimum to pan to
 * @param {Number} xEnd         : the X maximum to pan to
 * @param {Number} y            : the y positon (0.5 to center).
 * @param {Number} xScrollRatio : the ratio of scrolling, contained in 0..1.
 */
function makePanPoint(xStart, xEnd, y, xScrollRatio=0) {
  let x = xStart + xScrollRatio * (xEnd-xStart);
  return new OpenSeadragon.Point(x,y)
}

/**
 * pan the viewport horizontally depending on the vertical scroll
 * of the `main` html element. see `makePanPoint` for details.
 * if `init===false`, add an x-offset defined by the % of page
 * scrolled. else, there is no offset.
 */
function viewportPan(init=false) {
  if ( viewer.value && viewer.value.viewport && viewer.value.viewport !== false ) {
    let scrollRatio = !init ? getScrollRatio() : 0,
        p = makePanPoint( viewportConfig.xStartPos
                        , viewportConfig.xEndPos
                        , viewportConfig.yPos
                        , scrollRatio);
    viewer.value.viewport.panTo(p, false)
    panPoint.value = p;
  }
}

/**
 * zoom on the viewport based on what has been
 * defined in `viewportConfig.zoom`
 */
function viewportZoom() {
  if ( viewer.value && viewer.value.viewport && viewer.value.viewport !== false ) {
    viewer.value.viewport.zoomTo( viewportConfig.zoom, null, true );
  }
}

/**
 * revert the viewport's zoom and pan to its last
 * scroll-defined position.
 * a user can interact with the OSD viewer and thus
 * change the pan/zoom of the viewer. in that case,
 * we wait a while before returning to the "normal"
 * position.
 */
function viewportRevert() {
  setTimeout(() => {
    viewportZoom();
    viewportPan();
  }, 2000);
}

/**
 * reset a viewport's pannong/zoom to its position
 * on initial page load. to be used when the user
 * changes page.
 */
function viewportReset() {
  viewportZoom();
  viewportPan();
}

function defineViewer(newViewer) {

  if ( newViewer === false ) {
    viewer.value = false;

  } else {
    // update the global viewer handler
    viewer.value = newViewer.value;

    // hide the navigation buttons
    $(`#${htmlId}`).find(".openseadragon-container > div:nth-child(2)")
                   .hide();
    $(`#${htmlId}`).find(".openseadragon-container .navigator").hide();

    // set the zoom level so that the image fills its container
    // see: https://codepen.io/iangilman/pen/RZxEWZ
    const viewport = viewer.value.viewport;
    const tiledImage = viewer.value.world.getItemAt(0);
    viewportConfig.zoom = tiledImage.source.dimensions.x / viewport.getContainerSize().x;
    viewportZoom();

    // define the default center of the viewport
    viewportPan();

    // on scroll, update the viewport's center.
    $("main").on("scroll", () => {
      setTimeout(() => {
        viewportPan();
      }, 50)
    })

    //TODO see if there are other events that should be added here.
    // the viewport can be panned or zoomed by the user, but after some inactivity,
    // switch the view back to what it is supposed to be based on the scrolling level.
    viewer.value.addHandler("canvas-release", viewportRevert);
    viewer.value.addHandler("canvas-scroll", viewportRevert);

  }
}

/****************************************/

// reposition the viewport to its original position when user changes page
watch(route, () => { if (viewer.value !== false) { viewportReset() } });

onUnmounted(() => {
  $("main").off("scroll");
})
</script>


<style>
.sidebar-wrapper {
  width: 100%;
  height: 100%;
  overflow: scroll;
  border-top: var(--cs-border);
  border-left: none;
  padding: 5px;
}
.sidebar-iiif-wrapper {
  border:var(--cs-border);
  height: 100%;
}
@media ( orientation: landscape ) {
  .sidebar-wrapper {
    border-top: none;
    border-left: var(--cs-border);
  }
}
</style>