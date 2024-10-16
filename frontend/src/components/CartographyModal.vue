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
          <p>Cette carte présente l'évolution du parcellaire du quartier permet
            d'explorer les représentations du quartier de la fin du XVIII<sup>e</sup>
            au début du XX<sup>e</sup> siècle. Voici comment l'utiliser&nbsp:</p>
          <ul>
            <li>Dans la carte, cliquer sur une parcelle ouvrira une une interface
              pour explorer toutes les ressources iconographiques qui y sont
              associées.</li>
            <li>Le bouton <span class="ui-button-demo"><UiButtonFilter>
              </UiButtonFilter></span> permet d'afficher une barre contenant
              des filtres pour sélectionner les parcelles à afficher.</li>
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
import { ref, onMounted } from "vue";

import $ from "jquery";

import UiButtonCross from "@components/UiButtonCross.vue";
import UiButtonFilter from "@components/UiButtonFilter.vue";
import UiButtonQuestion from "@components/UiButtonQuestion.vue";

/************************************/

const emit = defineEmits(["closeCartographyModal"]);

const displayModal = ref(true);  // when true, display an explanatory modal

onMounted(() =>

  // emit an order to close the modal when pressing escape
  $(document).on("keyup", (e) => {
    if (e.originalEvent.code==="Escape") {
      emit("closeCartographyModal");
      $(document).off("keyup");
    }
  })
)

</script>

<style scoped>
.c-modal-outer-wrapper {
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  width: 100%;
  transform: translateX(30%);
  z-index: 1000;

  display: flex;
  align-items: center;
  justify-content: center;

  background-color: RGBA(113, 5, 81, .5); /* var(--cs-plum) in rgba with .3 opacity */
}

.c-modal-inner-wrapper {
  height: 70%;
  width: 70%;
  border: var(--cs-negative-border);

  display: grid;
  grid-template-columns: 100%;
  grid-template-rows: 15% 85%;
}
.c-modal-title-wrapper {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  padding: 0 3%;
  border-bottom: var(--cs-negative-border);
}
.c-modal-title-wrapper > h1 {
  margin: 0px;
}
.c-modal-title-wrapper :deep(.button-cross) {
  height: 5vh;
  width: 5vh;
}
.c-modal-text-wrapper {
  margin: 5%;
  max-height: 100%;
  overflow: scroll;
  max-height: 100%;
}
.ui-button-demo button {
  display: inline-block;
  height: 25px;
  width: 25px;
  transform: translateY(15%);
}

</style>
