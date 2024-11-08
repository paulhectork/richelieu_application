<!-- TheHomeModal.vue
    a small modal displaying basic info on the project.

    emits:
    - closeHomeModal
        an emit that is received by @/App.vue
        which in turn unmounts this component.
-->

<template>
  <div class="hm-outer-wrapper">
    <div class="hm-inner-wrapper main-default">

      <div class="hm-left">

        <div class="hm-left-title">
          <img src="@/assets/icons/logo-text.svg"
               alt="logo du projet Richelieu"
          >
          <span style="visibility: hidden">Quartier Richelieu</span>

        </div>

        <div class="hm-left-content">
          <p>Le projet de recherche <i>Richelieu. Histoire du quartier</i> (1750-1950)
            est né de la collaboration de plusieurs institutions publiques situées au cœur
            du II<sup>e</sup> arrondissement de Paris. Ce projet étudie le quartier communément
            désigné sous le nom de <q>&nbsp;Richelieu&nbsp;</q>,à travers ses dynamiques
            architecturales, humaines et économiques et en croisant des sources
            iconographiques et cartographiques, à l'échelle du long XIX<sup>e</sup> siècle.
          </p>
          <div class="hm-left-redirect-wrapper">
            <div class="hm-left-redirect">
              <span>En savoir plus</span>
              <RouterLink to="/a-propos/projet"><UiButtonLink></UiButtonLink></RouterLink>

            </div>
          </div>
        </div>

        <div class="hm-left-logos">
          <LogoBanner></LogoBanner>
        </div>
      </div>

      <div class="hm-right">
        <div class="hm-right-img-wrapper">
          <img src="@/assets/media/home_modal_map_noborder.jpg"
               alt="Dessin de carte du centre de Paris"
          >
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

import { clickOutside } from "@utils/ui.js";

/*******************************************************/

const emit = defineEmits(["closeHomeModal"]);

onMounted(() => {
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
.hm-left-title {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  height: 100%;
}
.hm-left-title > img {
  object-fit: contain;
  max-width: 90%;
  height: 90%;
  margin: 5%;
}
.hm-left-content {
  overflow: scroll;
}
.hm-left-redirect-wrapper {
  display: flex;
  flex-direction: column;
  align-items: end;
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

/**********************************************/

.hm-right {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
}
.hm-right-img-wrapper {
  height: calc(100% - 20px);
  width: calc(100% - 20px);
  margin: 10px;
  overflow: hidden;
}
.hm-right img {
  object-fit: cover;
  min-width: 100%;
  height: 140%;
}
.hm-right :deep(.button-cross) {
  position: absolute;
  top: 0;
  right: 0;
  height: max(5vh, 50px);
  width: max(5vh, 50px);
}

/* hide the right block on small portrait viewports */
@media ( orientation:portrait ) and ( max-width: 600px ) {
  .hm-inner-wrapper {
    grid-template-columns: 100% 0%;
    overflow: hidden;
  }
  .hm-left {
    border-right: none;
  }
  .hm-right-img-wrapper {
    display: none;
  }
}
</style>