<!-- IntroIiifView.vue

  a minimal introduction page. it contains 2 elements:
  - a modal with some info on the website
  - a iiif viewer in the background that moves based
    on the user's mouse movements.

  it's pretty neat :)
-->

<template>
<div class="intro-outer-wrapper">
  <div class="intro-inner-wrapper">
    <div class="intro-iiif-wrapper">
      <div class="intro-iiif-inner-wrapper">
        <IiifViewer :osdId="htmlId"
                    :iiifUrl="iiifUrl"
                    :backupImgUrl="imgUrl"
                    backupImgDisplay="cover"
                    @osd-viewer="onViewerMounted"
        ></IiifViewer>
      </div>
    </div>
    <div class="intro-modal-wrapper">
      <div id="intro-modal"
           class="negative-default"
      >
        <div class="title-block">
          <h1>
            <span class="title-text">Richelieu. Histoire du quartier</span>
            <img src="@/assets/icons/logo-text-invert-small.png"
                 alt="logo du projet Richelieu"
            >
          </h1>
          <h2>Plongez dans l'histoire du Paris du XIX<sup>e</sup> siècle</h2>
        </div>
        <div class="content-block">
          <div class="image-block">
            <!--
            <img :src="vasserotImgSrc"
                 alt="Relevé parcellaire du Palais-Royal sur l'atlas Vasserot (Archives de Paris)"
            >
            -->
            <!--
            <img src="@/assets/media/home_modal_map_noborder.jpg">
            -->
            <img :src="urlToIconographyFile('qr13f4af1da6eee4caabdc8e39f30ac92a6_compress.jpg')"
                 alt="Gravure représentant la section LePelletier en 1792, durant la révolution française, sur la rue ViVienne"
            >
          </div>
          <div class="info-block">
            <ul class="list-invisible count-block"
                v-if="loadStateCounts === 'loaded'"
            >
              <li v-if="showIconography === true"
                  class="animate__animated animate__lightSpeedInRight"
              ><span :style="{ color: customColors[0] }">
                {{ dbCounts.iconography }}</span> documents</li>
              <li v-if="showInstitution === true"
                  class="animate__animated animate__lightSpeedInRight"
              >Issus de <span :style="{ color: customColors[1] }">
                {{ dbCounts.institution }}</span> institutions</li>
              <li v-if="showNamedEntity === true"
                  class="animate__animated animate__lightSpeedInRight"
              >Représentant <span :style="{ color: customColors[2] }">
                {{ dbCounts.named_entity }}</span> points d'intérêt</li>
              <li v-if="showPlace === true"
                  class="animate__animated animate__lightSpeedInRight"
              >Dans <span :style="{ color: customColors[3] }">
                {{ dbCounts.place }}</span> lieux</li>
            </ul>

            <div class="button-wrapper">
              <button v-if="showEnter"
                      id="enter-website"
                      class="animate__animated animate__lightSpeedInRight"
                      @click="redirectToHome"
              >Entrer dans le site</button>
            </div>
          </div>
        </div>

      </div>
    </div>
  </div>
</div>

</template>


<script setup>
import { onMounted, onUnmounted, ref } from "vue";
import { useRouter } from "vue-router";

import OpenSeadragon from "openseadragon";
import axios from "axios";
import $ from "jquery";

import IiifViewer from "@components/IiifViewer.vue";

import { urlToIconographyFile } from "@utils/url";
import { randomColorLight } from "@utils/colors";

/****************************************************/

const router = useRouter();

const viewer = ref();
const iiifUrl           = "https://apicollections.parismusees.paris.fr/iiif/320057446/manifest";
const imgUrl            = "qr16080c31522fa44a3b238cb3790054d1c.jpg";
const htmlId            = "intro-iiif-viewer";
const idUuidIconography = "qr11679c39145004726a591f2b7086234e5";

const dbCounts = ref({});
const showIconography = ref(false)
const showInstitution = ref(false)
const showNamedEntity = ref(false)
const showTheme       = ref(false)
const showPlace       = ref(false)
const showEnter       = ref(false);

const customColors = [ randomColorLight(), randomColorLight()
                     , randomColorLight(), randomColorLight() ];

console.log(customColors);

const loadStateIiif   = ref("loading");  // "loading|loaded|error"
const loadStateCounts = ref("loading");  // "loading|loaded|error"

const vasserotImgSrc = new URL('/statics/other/adp_vasserot_crop.jpg', __STATICS_URL__);

const tileSource = [ { type: "image",
                       height: 1,
                       url: "https://apicollections.parismusees.paris.fr/sites/default/files/styles/4k/collections/atoms/images/CAR/aze_carg000679_001.jpg" } ]

/****************************************************/

/**
 * when the viewer is mounted, define the global `viewer` ref,
 * hide the viewer's navigators and controls and zoom in.
 * @param {OpenSeadragon.Viewer} theViewer
 */
function onViewerMounted(theViewer) {
  viewer.value = theViewer.value;
  console.log(viewer.value.options);
  $(`#${htmlId} .navigator,
     #${htmlId} .openseadragon-container > div:nth-child(2)`
  ).css({ display: "none" });
  setTimeout(() => viewer.value.viewport.zoomTo(2, undefined, false), 1000);
}

/**
 * move the iiif viewer based on the mouse movements.
 * @param {jQuery.event} e
 */
function panViewportOnMousemove(e) {
  let modalBounds = document.querySelector("#intro-modal").getBoundingClientRect(),
      pos = [ e.originalEvent.clientX, e.originalEvent.clientY ];   // mouse position
  // there's a viewer and the mouse is outside the modal
  if ( viewer.value && viewer.value.viewport
       && !( pos[0] >= modalBounds.left
          && pos[0] <= modalBounds.right
          && pos[1] <= modalBounds.bottom
          && pos[1] >= modalBounds.top )
  ) {
    let coef     = 10,  // >= 1. the higher the value, the slower the viewport will pan
        vpCenter = [ 0.5, 0.5 ], // viewport center. openseadragon viewers have x,y coordinates between 0 and 1.
        delta    = [ (pos[0] - window.innerWidth/2) / window.innerWidth    // how much to pan by, in comparison with the center. y and y are in the range -0.5..0.5.
                   , (pos[1] - window.innerHeight/2) / window.innerHeight ],
        toCenter = [ vpCenter[0] - (delta[0]/coef)                         // where to pan to, in coordinates 0..1.
                   , vpCenter[1] - (delta[1]/coef) ]
    viewer.value.viewport.panTo({ x: toCenter[0], y: toCenter[1] });
  }
}

/**
 * when clicking on `#enter-website`, redirect to TheHomeView.vue.
 * @param {jQuery.event} e
 */
function redirectToHome(e) {
  if ( viewer.value && viewer.value.viewport ) {
    let currentZoom = viewer.value.viewport.getZoom();
    console.log(currentZoom);
    viewer.value.viewport.zoomTo(currentZoom + 5, undefined, false);

  }
  setTimeout(() => router.push({ path: "/accueil" }), 600);
}

/**
 * by setting all these refs to `true`, we'll progressively
 * display all the children of `.info-block`.
 */
function animateInfos() {
  setTimeout(() => showIconography.value=true, 0);
  setTimeout(() => showInstitution.value=true, 500);
  setTimeout(() => showNamedEntity.value=true, 1000);
  setTimeout(() => showTheme.value=true, 1500);
  setTimeout(() => showPlace.value=true, 2000);
  setTimeout(() => showEnter.value=true, 2500);
}

/**
 * fetch data from the backend, and when receiving it, trigger `animateInfos()`.
 */
function getData() {
  axios.get(new URL("/i/database-counts", __API_URL__))
  .then(r => r.data)
  .then(data => {
    dbCounts.value = data;
    loadStateCounts.value = "loaded";
    animateInfos();
  })
  .catch(err => {
    console.error(err);
    loadStateCounts.value = "error";
  });
}

/****************************************************/

onMounted(() => {
  getData();
  $(document).on("mousemove", panViewportOnMousemove);
})

onUnmounted(() => {
  $(document).off("mousemove");
})
</script>


<style scoped>
.intro-outer-wrapper {
  position: fixed;
  height: 100vh;
  width: 100vw;
  top: 0;
  z-index: 100;
}
.intro-inner-wrapper {
  position: relative;
  height: 100%;
  width: 100%;
  background-color: white;
  display: grid;
}

/************************/

.intro-modal-wrapper {
  grid-row: 1;
  grid-column: 1;
  height: 100%;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}
#intro-modal {
  /*
  height: 70%;
  width: 80%;
  max-width: 1000px;
  min-height: 350px;
  */
  height: max(350px, 70%);
  width: min(1000px, 80%);
  z-index: 199;
  position: absolute;
  border: var(--cs-negative-border);
  display: grid;
  grid-template-rows: 30% 70%;
  grid-template-columns: 100%;
}
@media ( orientation:landscape ) {
  #intro-modal {
    width: min(1000px, 80%);
  }
}
#intro-modal > .title-block {
  display: grid;
  grid-template-rows: 60% 40%;
  grid-template-columns: 100%;
  margin: max(3%, 10px);
}
h1 {
  height : 100%;
  width: 100%;
  margin: 0;
}
h1 > .title-text {
  position: absolute;
  visibility: hidden;
  height: 0;
  width: 0;
}
h1 > img {
  max-height: 90%;
  max-width: 90%;
  object-fit: contain;
}
h2 {
  margin: 0;
}
.content-block {
  display: grid;
  grid-template-rows: 40% 60%;
  grid-template-columns: 100%;
}
@media ( orientation:landscape ) {
  .content-block {
    grid-template-rows: 100%;
    grid-template-columns: 60% 40%;
  }
}
.content-block > * {
  margin: max(3%, 10px);
}
.image-block {
  border: var(--cs-negative-border);
  max-height: 100%;
  max-width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}
.image-block > img {
  object-fit: cover;
  width:  200%;
  height: 200%;
}
.info-block {
  font-family: var(--cs-font-serif);
  font-size: 140%;
  display: grid;
  grid-template-rows: 2fr 1fr;
  grid-template-columns: 100%;
}
.count-block {
}
.button-wrapper {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  justify-content: center;
}
.button-wrapper > button {
  max-width: 200px;
  max-height: 90px;
  height: 90%;
  width: 90%;
  margin: 5px;
  font-size: 80%;
  background-color: var(--cs-darkplum);
  transition: background-color var(--animate-duration);
}
.button-wrapper > button:hover {
  background-color: var(--cs-plum);
}
.button-wrapper > button:active {
  background-color: var(--cs-lightplum);
}

/************************/

.intro-iiif-wrapper {
  grid-row: 1;
  grid-column: 1;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}
.intro-iiif-inner-wrapper {
  height: calc(100% - 2vh);
  width: calc(100% - 2vh);
  border: var(--cs-main-border);
  z-index: 0 !important;

}
</style>