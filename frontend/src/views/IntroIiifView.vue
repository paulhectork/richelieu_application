<template>
<div class="intro-outer-wrapper">
  <div class="intro-inner-wrapper">
    <div class="intro-iiif-wrapper">
      <div class="intro-iiif-inner-wrapper">
        <IiifViewer :osdId="htmlId"
                    :iiifUrl="iiifUrl"
                    :backupImgUrl="imgUrl"
                    backupImgDisplay="cover"
                    @osd-viewer="defineViewer"
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
            <img :src="vasserotImgSrc"
                 alt="Relevé parcellaire du Palais-Royal sur l'atlas Vasserot (Archives de Paris)"
            >
          </div>
          <div class="info-block">
            <ul class="list-invisible count-block"
                v-if="loadStateCounts === 'loaded'"
            >
              <li v-if="showIconography === true"
                  class="animate__animated animate__lightSpeedInRight"
              ><span :style="{ color: randomColorLight() }">
                {{ dbCounts.iconography }}</span> documents</li>
              <li v-if="showInstitution === true"
                  class="animate__animated animate__lightSpeedInRight"
              >Issus de <span :style="{ color: randomColorLight() }">
                {{ dbCounts.institution }}</span> institutions</li>
              <li v-if="showNamedEntity === true"
                  class="animate__animated animate__lightSpeedInRight"
              >Représentant <span :style="{ color: randomColorLight() }">
                {{ dbCounts.named_entity }}</span> sujets / activités</li>
              <li v-if="showPlace === true"
                  class="animate__animated animate__lightSpeedInRight"
              >Dans <span :style="{ color: randomColorLight() }">
                {{ dbCounts.place }}</span> lieux</li>
            </ul>

            <div class="button-wrapper">
              <button v-if="showEnter"
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
import { onMounted, ref, watch } from "vue";

import axios from "axios";

import IiifViewer from "@components/IiifViewer.vue";

import { randomColorLight, randomColorDark } from "@utils/colors";

/****************************************************/

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

const loadStateIiif   = ref("loading");  // "loading|loaded|error"
const loadStateCounts = ref("loading");  // "loading|loaded|error"

const vasserotImgSrc = new URL('/statics/other/adp_vasserot_crop.jpg', __STATICS_URL__);

/****************************************************/

const tileSource = [ { type: "image",
                       height: 1,
                       url: "https://apicollections.parismusees.paris.fr/sites/default/files/styles/4k/collections/atoms/images/CAR/aze_carg000679_001.jpg" } ]

/****************************************************/

function defineViewer(theViewer) {
  viewer.value = theViewer;
}

function redirectToHome(e) {
  console.log("omg hiiii");
  console.error("INTROIIIFVIEW: check that redirections are not broken")
}

function getData() {
  axios.get(new URL("/i/database-counts", __API_URL__))
  .then(r => r.data)
  .then(data => {
    dbCounts.value = data;
    loadStateCounts.value = "loaded";

    setTimeout(() => showIconography.value=true, 0);
    setTimeout(() => showInstitution.value=true, 500);
    setTimeout(() => showNamedEntity.value=true, 1000);
    setTimeout(() => showTheme.value=true, 1500);
    setTimeout(() => showPlace.value=true, 2000);
    setTimeout(() => showEnter.value=true, 2500);
  })
  .catch(err => {
    console.error(err);
    loadStateCounts.value = "error";
  });
}

/****************************************************/

onMounted(() => {
  getData();
})

/** without reusing IiifViewer.vue */
/*
import OpenSeadragon from "openseadragon";
import $ from "jquery";
import { osdNavImages } from "@utils/iiif";
import { urlToOsdIcons } from "@utils/url";

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
    prefixUrl: urlToOsdIcons().href,
    navImages: osdNavImages
  });
  return viewer.value.addOnceHandler("open", () => {
    $(`#${osdId} .openseadragon-canvas`).css("backgroundColor", "var(--cs-darkplum)");
    return
  });  // await for loading to be ready to return
}

onMounted(() => {
  buildOsdViewer(tileSource, "intro-iiif-viewer");
})
*/

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
}
.image-block > img {
  object-fit: cover;
  width: 100%;
  height: 100%;
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
  height: 98%;
  width: 98%;
  border: var(--cs-main-border);
  z-index: 0 !important;

}
</style>