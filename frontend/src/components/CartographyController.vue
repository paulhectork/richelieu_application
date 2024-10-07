<template>
  <!-- cc = cartographyController -->
  <div class="cc-outer-wrapper">
    <div class="cc-closer-wrapper">
      <UiButtonCross @click="emit('closeCartographyController')"
                     @touchend="emit('closeCartographyController')"
      ></UiButtonCross>
    </div>

    <div class="cc-inner-wrapper">
      <h2>Filtrer les données</h2>
    </div>

  </div>
</template>


<script setup>
import { onMounted, onUnmounted, ref } from "vue";

import $ from "jquery";

import UiButtonCross from "@components/UiButtonCross.vue";

/***************************************/

const emit = defineEmits(["closeCartographyController", "filter"]);

/***************************************/

/**
 * emit an event to close this component on pressing `keydown.escape`
 */
 const escHandler = (e) => e.key === "Escape" ? emit("closeCartographyController") : "";

/***************************************/

onMounted(() => {

  $(document).on("keydown", escHandler);
})
onUnmounted(() => {
  $(document).off("keydown", escHandler);
})

</script>


<style scoped>
.cc-outer-wrapper {
  height: 100%;
  width: 100%;
}
.cc-closer-wrapper {
  display: flex;
  justify-content: flex-end;
  margin: 1vh 1vh 0 1vh;
}
.cc-closer-wrapper button {
  height: 5vh;
  width: 5vh;
}
.cc-inner-wrapper {
  margin: 0 3vh;
}
h2 {
  margin: 0 auto;
}
</style>