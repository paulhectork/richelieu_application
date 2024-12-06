<!-- FormKitSlider
  a custom formkit slider that supports 2-input slider (min,max)
  instead of just 1 input, done using jQuery plugin noUiSlider.

  props: as with all formkit inputs, the props are all contained
  within `context` object.
  - number (string)
      one of "float"|"integer", wether we accept float inputs
      or only integer inputs
  - step (number)
      the slider's step (distance between 2 possible values: .1, 0.01...)
  - minVal (number)
      the minimum value for the slider
  - maxVal (number)
      the maximum value for the slider

  usage example:
    <FormKit type="fkSlider"
             name="iconographyCount"
             id="iconography-count"
             label="Nombre de ressources iconographiques"
             help="Filtrer par nombre de ressources iconographiques"
             number="integer"
             :step="1"
             :minVal="0"
             :maxVal="800"
    ></FormKit>

-->

<template>
  <div class="form-field-slider-wrapper">
    <div class="form-field-slider">
      <div :id="htmlId"></div>
    </div>
    <div class="form-field-info"
         v-if="context"
    >
      <div class="form-field-minmax">
        <span>{{ allowedMin }}</span>
        <span>{{ allowedMax }}</span>
      </div>
      <div class="form-field-selection">
        <span><i>Sélection&nbsp;: entre {{ selectedMin }}
          et {{ selectedMax }}</i></span>
      </div>
    </div>

  </div>
</template>


<script setup>
import { onMounted, onUnmounted, ref, watch } from "vue";

import $ from "jquery";
import noUiSlider from '@plugins/nouislider.min.mjs';  // imported as plugin because else there are import bugs
import '@plugins/nouislider.min.css';

/**********************************************/

const htmlId      = `formkit-slider-${window.crypto.randomUUID()}`;
const props       = defineProps(["context"]);  /** @type { { minVal: Number?, maxVal: Number?, step: Number?, number: ("integer"|"float") } } */
const slider      = ref();
const context     = ref();
const allowedMin  = ref();  /** @type {Number} allowed minimum value */
const allowedMax  = ref();  /** @type {Number} allowed maximum value */
const selectedMin = ref();  /** @type {Number} currently selected minimum value */
const selectedMax = ref();  /** @type {Number} currently selected maximum value */
// const showPopup   = ref(false);

/**********************************************/

/**
 * define the slider.
 */
function createSlider() {
  slider.value = noUiSlider.create(document.getElementById(htmlId), {
    start: [ allowedMin.value, allowedMax.value ],
    step: context.value.step,
    connect: true,
    range: { min: allowedMin.value, max: allowedMax.value }
  });
  // add the events
  slider.value.on("update", () => {
    [ selectedMin.value, selectedMax.value ] = slider.value.get().map(parseFloat);
  });
  slider.value.on("set", () => {
    context.value.node.input([ selectedMin.value, selectedMax.value ]) });
}

function setRefs(theContext) {
  context.value     = theContext;
  allowedMin.value  = theContext.minVal;  // allowed minimum/maximum values
  allowedMax.value  = theContext.maxVal;
  selectedMin.value = theContext.minVal;  // currently selected mimumums / maximums
  selectedMax.value = theContext.maxVal;
}

/**********************************************/

/**
 * for when new data is sent without the slider being unmounted:
 * destroy the slider, create a new one
 */
watch(props, (newP, oldP) => {
  // the watcher is triggered several times,
  // even without an actual update of the props
  // => check if there's actually been a change in values
  if ( newP.minVal !== oldP.minVal
    || newP.maxVal !== oldP.maxVal
    || newP.number !== oldP.number
    || newP.step   !== oldP.step
  ) {
    setRefs(newP.context);
    if ( slider.value ) {
      slider.value.destroy();
      createSlider();
    }
  }
})

onMounted(() => {
  setRefs(props.context);
  createSlider();
})

onUnmounted(() => {
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
  width: 100%;
  margin: 5px 0;
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
