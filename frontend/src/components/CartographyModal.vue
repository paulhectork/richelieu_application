<!-- CartographyModal.vue
     a modal that shows info in @views/CartographyMain.vue

     emits:
        closeCartographyModal: a flag that will cause
          @views/CartographyMain.vue to remove this
          component.
 -->

<template>
  <div v-if="displayModal"
       class="c-modal-outer-wrapper"
  >
    <div class="c-modal-inner-wrapper negative-default">
      <div class="c-modal-title-wrapper">
        <h1>Cartographie du Quartier</h1>
        <span><UiButtonCross @click="emit('closeCartographyModal')">
        </UiButtonCross></span>
      </div>
      <div class="c-modal-text-wrapper">
        <div class="c-modal-text">
          <p>Cette carte présente l'évolution du parcellaire du quartier
            et permet d'explorer les représentations du quartier de la fin
            du XVIII<sup>e</sup> au début du XX<sup>e</sup> siècle.
            Voici comment l'utiliser&nbsp:</p>
          <ul>
            <li>Dans la carte, cliquer sur une parcelle permettra d'obtenir plus
              d'information sur celle-ci:
              <ul>
                <li>Une interface s'ouvrira pour explorer toutes les ressources
                  iconographiques associées à la parcelle sélectionnée.</li>
                <li>Sur la carte, la parcelle cliquée s'affichera en
                  <span class="ui-button-demo bg-color"
                        style="background-color: var(--cs-duck)"
                        aria-label="couleur de fond d'une parcelle: vert sombre"></span>.
                  Les parcelles associées s'afficheront en
                  <span class="ui-button-demo bg-color"
                        style="background-color: var(--cs-seagreen)"
                        aria-label="couleur de fond d'une parcelle: vert clair"></span>.
                </li>
              </ul>
            </li>
            <li>Le bouton <span class="ui-button-demo"><UiButtonFilter>
              </UiButtonFilter></span> permet d'afficher une barre contenant
              des filtres pour sélectionner les parcelles à afficher.
              <ul>
                <li><code>Adresse</code> permet de sélectionner les adresses
                  à afficher sur la carte.</li>
                <li><code>Nombre de ressources iconographiques</code> permet
                  de n'afficher les parcelles qui ne contiennent qu'un certain nombre
                  de ressources iconographiques.</li>
                <li><code>Granularité</code> permet de sélectionner les parcelles
                  à afficher en fonction de leur échelle de précision, selon qu'elles
                  représentent un bâtiment entier ou juste une partie. Par défault, un
                  mélange est affiché.</li>
                <li><code>Source cartographique</code> permet de changer de fond de carte
                  et d'afficher la parcelle correspondant à ce fond. Cela permet de voir
                  l'évolution parcellaire sur différentes sources historiques.</li>
              </ul>
            </li>
            <li>Le bouton <span class="ui-button-demo"><UiButtonQuestion>
              </UiButtonQuestion></span> permet d'afficher ce texte de
              présentation.</li>
          </ul>
        </div>
      </div>
    </div>
  </div>

</template>


<script setup>
import { ref, onMounted, onUnmounted } from "vue";

import $ from "jquery";

import UiButtonCross from "@components/UiButtonCross.vue";
import UiButtonFilter from "@components/UiButtonFilter.vue";
import UiButtonQuestion from "@components/UiButtonQuestion.vue";

import { clickOutside } from "@utils/ui.js";

/************************************/

const emit = defineEmits(["closeCartographyModal"]);

const displayModal = ref(true);  // when true, display an explanatory modal

onMounted(() => {
  // emit an order to close the modal when pressing escape
  $(document).on("keyup", (e) => {
    if (e.originalEvent.code==="Escape") {
      emit("closeCartographyModal");
      $(document).off("keyup");
    }
  })
  // close when clicking outside of the modal
  $(document).on("click", (e) => {
    if ( clickOutside(e, ".c-modal-inner-wrapper")
       && clickOutside(e, ".leaflet-control .button-question")  // without that, clicking on the button to open the modal will emit "closeCartographyModal"
    ) {
      emit("closeCartographyModal");
      $(document).off("click");
    }
  })
})

onUnmounted(() => {
  $(document).off("click");
  $(document).off("keyup");
})

</script>

<style scoped>
.c-modal-outer-wrapper {
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  width: 100%;
  transform: translateX(100%);
  z-index: 1000;

  display: flex;
  align-items: center;
  justify-content: center;

  /*background-color: RGBA(113, 5, 81, .5);*/ /* var(--cs-plum) in rgba with .3 opacity */
}

.c-modal-inner-wrapper {
  height: 90%;
  width: 80%;
  border: var(--cs-negative-border);

  display: grid;
  grid-template-columns: 100%;
  grid-template-rows: auto 2fr;

  box-shadow: 8px 8px var(--cs-plum);
  overflow: auto;
}
.c-modal-title-wrapper {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  padding: 3% 3%;
  border-bottom: var(--cs-negative-border);
}
.c-modal-title-wrapper > h1 {
  margin: 0;
}
.c-modal-title-wrapper :deep(.button-cross) {
  height: 5vh;
  width: 5vh;
}
.c-modal-text-wrapper {
  margin: 1% 5%;
  max-height: 100%;
  overflow: scroll;
  max-height: 100%;
}
.ui-button-demo {
  display: inline-block;
  height: 25px;
  width: 25px;
  transform: translateY(15%) translateX(-15%);
  margin: 0 3px;
}

.ui-button-demo button {
  height: 100%;
  width: 100%;
}

.ui-button-demo.bg-color {
  border: var(--cs-negative-border);
  height: 20px;
}

li > ul > li {
  margin: 5px 0;
}
code {
  background-color: var(--cs-main-default-bg);
  color: var(--cs-main-default);
  font-size: 90%;
  padding: 0 2px;
}

@media ( orientation:landscape ) {
  .c-modal-outer-wrapper {
    height: 100%;
    width: calc(100vw - var(--cs-sidebar-landscape-width));
    transform: translateX(30%);
  }
  .c-modal-inner-wrapper {
    height: 70%;
    width: 70%;
  }
}

.c-modal-text-wrapper {
  overflow: auto !important;
  scrollbar-width: thin;
  scrollbar-color: var(--cs-darkplum) white;
}
</style>
