<!-- TheHomeModal.vue
    a small modal displaying basic info on the project and 2 videos.
    2 buttons allow to switch between videos and to hide/display info
    on the video.

    emits:
    - closeHomeModal
        an emit that is received by @/App.vue
        which in turn unmounts this component.
-->

<template>
  <div class="hm-outer-wrapper">
    <div class="hm-inner-wrapper main-default">

      <div class="hm-left">

        <div class="hm-left-header">
          <div class="hm-left-title-wrapper">
            <img src="@/assets/icons/logo-text.svg"
                 alt="logo du projet Richelieu"
            >
            <span style="visibility: hidden; height: 0; width: 0;"
            >Quartier Richelieu</span>
          </div>
          <div class="hm-left-redirect-wrapper">
            <div class="hm-left-redirect">
              <span>En savoir plus</span>
              <RouterLink to="/a-propos/projet"><UiButtonLink></UiButtonLink></RouterLink>
            </div>
          </div>

        </div>

        <div class="hm-left-content">
          <p>Le projet de recherche <i>Richelieu. Histoire du quartier</i> (1750-1950)
            est né de la collaboration de plusieurs institutions publiques situées au cœur
            du II<sup>e</sup> arrondissement de Paris. Ce projet étudie le quartier communément
            désigné sous le nom de <q>&nbsp;Richelieu&nbsp;</q>, à travers ses dynamiques
            architecturales, humaines et économiques et en croisant des sources
            iconographiques et cartographiques, à l'échelle du long XIX<sup>e</sup> siècle.
          </p>

          <div class="video-outer-wrapper">
            <div class="video-controller-wrapper">
              <button @click="showCredit"
                      :class="{ 'button-activated': displayCredit }"
              >Crédits</button>
              <button @click="switchVideo">Changer de vidéo</button>
            </div>
            <!--
            <div class="video-controller-credits-wrapper">
              <div v-if=""
            </div>
            -->
            <div class="video-inner-wrapper">
              <div class="video-loader-wrapper"
                   v-if="videoLoading"
              >
                <UiLoader></UiLoader>
              </div>
              <figure :class="{ 'video-loading': videoLoading }">
                <video v-if="currentVideoIndex !== undefined"
                       id="video-container"
                       :alt="promoVideoArray[currentVideoIndex].credit"
                       autoplay
                       controls
                       playsinline
                       muted
                >
                  <source id="video-source"
                          :src="promoVideoArray[currentVideoIndex].source"
                          type="video/mp4"
                  ></source>
                </video>
                <figcaption v-if="displayCredit">
                  <span v-html="promoVideoArray[currentVideoIndex].credit"></span>
                </figcaption>
              </figure>
            </div>
          </div>

        </div>

        <div class="hm-left-logos">
          <LogoBanner></LogoBanner>
        </div>
      </div>

      <div class="hm-right">
        <div class="hm-right-video-wrapper">
          <!--
          <img src="@/assets/media/home_modal_map_noborder.jpg"
               alt="Dessin de carte du centre de Paris"
          >
          -->
        </div>
        <UiButtonCross @click="emit('closeHomeModal')"></UiButtonCross>
      </div>
    </div>
  </div>

</template>


<script setup>
import { onMounted, ref } from "vue";

import $ from "jquery";

import UiButtonCross from "@components/UiButtonCross.vue";
import UiButtonLink from "@components/UiButtonLink.vue";
import LogoBanner from "@components/LogoBanner.vue";
import UiLoader from "@components/UiLoader.vue";

import { clickOutside } from "@utils/ui.js";
import { promoVideoArray } from "@globals";

/*******************************************************/

const emit = defineEmits(["closeHomeModal"]);

const currentVideoIndex = ref();
const displayCredit     = ref();
const videoLoading      = ref(false);

/*******************************************************/

function showCredit() {
  displayCredit.value = !displayCredit.value;
}

/**
 * switch the video: update `currentVideoIndex` and trigger a reload.
 * see:
 *   https://tomelliott.com/html-5/changing-html5-video-javascript-jquery
 */
function switchVideo() {
  videoLoading.value = true;
  setTimeout(() => videoLoading.value = false, 1000);

  let vContainer = document.querySelector("#video-container");
  vContainer.pause();
  currentVideoIndex.value = currentVideoIndex.value === 0 ? 1 : 0;
  vContainer.load();
  vContainer.play();
}

onMounted(() => {
  currentVideoIndex.value = 0;
  displayCredit.value = false;

  // close on pressing Escape
  $(document).on("keyup", (e) => {
    if ( e.key === "Escape" ) {
      emit('closeHomeModal');
      $(document).off("keyup");
    };
  });
  // close when clicking outside of the modal
  $(document).on("click", (e) => {
    if ( clickOutside(e, ".hm-inner-wrapper") ) {
      $(document).off("click");
      emit('closeHomeModal');
    }
  });

})

</script>


<style scoped>
.hm-outer-wrapper {
  position: fixed;
  top: 0;
  left: 0;
  height: 100vh;
  width: 100vw;
  background: rgba(0,0,0,0.3);

  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}
.hm-inner-wrapper {
  width: max(300px, 80%);
  height: max(80%, 500px);
  display: grid;
  grid-template-columns: max(45%, 300px) calc(100% - max(45%, 300px));
  grid-template-rows: 100%;
  border: var(--cs-main-border);
  box-shadow: 8px 8px var(--cs-plum);
}
.hm-left, .hm-right {
  height: 100%;
}

/**********************************************/

.hm-left {
  display: grid;
  grid-template-columns: 100%;
  grid-template-rows: 20% auto 20%;
  border-right: var(--cs-main-border);
}
.hm-left > :not(:last-child) {
  border-bottom: var(--cs-main-border);
}
.hm-left-header {
  display: grid;
  grid-template-rows: 100%;
  grid-template-columns: 60% 40%;
  height: 100%;
  width: 100%;
}
.hm-left-title-wrapper {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: center;
}
.hm-left-title-wrapper > img {
  object-fit: contain;
  max-width: 90%;
  height: 90%;
  margin-left: 5px;
}
.hm-left-redirect-wrapper {
  display: flex;
  flex-direction: column;
  align-items: end;
  justify-content: center;
}
.hm-left-redirect {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  border: var(--cs-main-border);
  margin: 5px;
}
.hm-left-redirect > span {
  margin: 3px;
}
.hm-left-redirect :deep(button) {
  height: max(5vh, 40px);
  width: max(5vh, 40px);
}

.hm-left-content {
  overflow: scroll;
  overflow: auto !important;
  scrollbar-width: thin;
  scrollbar-color: var(--cs-darkplum) white;
}

.video-outer-wrapper {
  border-top: var(--cs-main-border);
  width: 100%;
}
.video-controller-wrapper {
  border-bottom: var(--cs-main-border);
  display: flex;
  justify-content: space-between;
}
.video-inner-wrapper {
  height: 100%;
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 5px;
  position: relative;
}
.video-inner-wrapper > * {
  position: absolute;
  top: 0;
  left: 0;
}
.video-inner-wrapper > .video-loader-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  margin-top: 25%;
}
.video-inner-wrapper > figure {
  margin: 0;
  padding: 0;
  transition: opacity .3s;
}
.video-inner-wrapper > figure.video-loading {
  opacity: 0.5;
}
.video-inner-wrapper video {
  width: 100%;
}

/**********************************************/

.hm-right {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
}
.hm-right-video-wrapper {
  height: calc(100% - 20px);
  width: calc(100% - 20px);
  margin: 10px;
  overflow: hidden;
  background-image: url("@/assets/media/home_modal_map_noborder.jpg");
  background-size: cover;

  display: flex;
  flex-direction: row;
  align-items: end;
}
.hm-right :deep(.button-cross) {
  position: absolute;
  top: 0;
  right: 0;
  height: max(5vh, 50px);
  width: max(5vh, 50px);
}

/**********************************************/

/* hide the right block + change title display on small portrait viewports */
@media ( orientation:portrait ) and ( max-width: 600px ) {
  .hm-inner-wrapper {
    grid-template-columns: 100% 0%;
    overflow: hidden;
  }
  .hm-left {
    border-right: none;
  }
  .hm-left-header {
    padding-top: 6vh;  /** vertical space for the .button-cross */
  }
  .hm-left-title-wrapper {
    transform: translateY(-3vh);  /** recenter the logo. yes it's hacky. */
  }
  .hm-right-video-wrapper {
    display: none;
  }
}
</style>