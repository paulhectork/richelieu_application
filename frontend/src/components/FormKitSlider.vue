<template>
  <div class="form-field-slider-wrapper">
    <!--
    <input :id="htmlId"
           type="range"
           :min="context.minVal"
           :max="context.maxVal"
           :step="context.step"
           :number="['integer', 'float'].includes(context.number)
                    ? context.number
                    : 'float'"
    ></input>
    -->
    <div class="form-field-slider">
      <div :id="htmlId"></div>
    </div>
    <div class="form-field-info">
      <div class="form-field-minmax">
        <span>{{ context.minVal }}</span>
        <span>{{ context.maxVal }}</span>
      </div>
      <div class="form-field-selection">
        <span><i>Sélection&nbsp;: entre {{ selectedMin }}
          et {{ selectedMax }}</i></span>
      </div>
    </div>

  </div>
</template>


<script setup>
import { onMounted, onUnmounted, ref } from "vue";

import $ from "jquery";
import noUiSlider from '@plugins/nouislider.min.mjs';  // imported as plugin because else there are import bugs
import '@plugins/nouislider.min.css';

/**********************************************/

const htmlId      = `formkit-slider-${window.crypto.randomUUID()}`;
const props       = defineProps(["context"]);  // "minVal", "maxVal", "step", "number" ("integer"|"float")
const context     = props.context;
const slider      = ref();
const selectedMin = ref(context.minVal);
const selectedMax = ref(context.maxVal);
// const showPopup   = ref(false);

/**********************************************/

/**********************************************/

onMounted(() => {
  slider.value = noUiSlider.create(document.getElementById(htmlId), {
    start: [ context.minVal, context.maxVal ],
    step: context.step,
    connect: true,
    range: { min: context.minVal, max: context.maxVal }
  });
  // add the events
  slider.value.on("update", () => {
    [ selectedMin.value, selectedMax.value ] = slider.value.get().map(parseFloat);
  });
  // $(`#${htmlId}`).on("mouseover", () => {/*showPopup.value = true*/})
  //                .on("mouseout", () => {/*showPopup.value = false */})
  slider.value.on("set", () => { context.node.input([selectedMin.value, selectedMax.value]) });
})

onUnmounted(() => {
  $(`#${htmlId}`).off("mouseover")
                 .off("mouseout");
  slider.value.off("update");
  slider.value.off("set");

})
</script>


<style scoped>
.form-field-slider-wrapper {
  width: 100%;
}
.form-field-info {
  color: var(--cs-main-alt-fontcolor);
}
.form-field-minmax {
  width: 100%;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}

/**********************************/

.noUi-target {
  width: 90%;
  margin: 5px;
}
:deep(.noUi-handle) {
  border-radius: 100%;
  width: 25px;
  height: 25px;
  background-color: var(--cs-main-default-bg);
  border: var(--cs-main-border);
}
:deep(.noUi-handle::before), :deep(.noUi-handle::after) {
  display: none;
}
:deep(.noUi-connect) {
  background-color: var(--cs-seagreen);
  border: var(--cs-main-border);
}

/**********************************/

/*
.popup-outer-wrapper {
  position: absolute;
  z-index: 1002;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: blue;
}
.popup-inner-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: paleturquoise;
}
.popup-body {
  border: var(--cs-main-border);
  background-color: var(--cs-main-default-bg);
  width: 80%;
  z-index: 1002;
}
.popup-body > p {
  width: 100%;
  text-align: center;
}
*/
</style>