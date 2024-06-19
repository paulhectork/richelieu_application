<!-- FormKit plugin with tabs-like selection

    the parent can pass 2 props to this component:
    * `options`: the different options for this select.
                 defaults to an empty array.
                 options must be an array of objects,
                 following the structure:
                 https://formkit.com/inputs/select#array-of-objects,
                 with a `value` key containing the form data and a
                 `label` key containing the displayed data.
                 (of course, `label` and `value` can be the same)

    see:
    https://formkit.com/guides/create-a-custom-input
    https://formkit.com/api-reference/context

    usage example:
    ```
    ```
-->

<template>
  <div class="form-radio-tabs-wrapper"
       :id="htmlId">
    <fieldset>
      <div v-for="o in optionsArray"
           class="form-radio-option"
           :class="{ 'form-radio-option-selected': checkedInput===o.value }"
      >
        <input type="radio"
               :value="o.value"
               :name="`fieldset-${htmlId}`"
               :id="`form-radio-tabs-${o.value}`"
               v-model="checkedInput"

        ></input>
        <label :for="`form-radio-tabs-${o.value}`"
               v-html="o.label"
        ></label>
      </div>
    </fieldset>
  </div>

</template>

<script setup>
import { onMounted, ref } from "vue";

import $ from "jquery";

import { clickOrTouchEvent } from "@globals";

/*******************************************/

const props = defineProps([ "context" ]);
const optionsArray = props.context.options || [];
const defaultValue = props.context.value
                     ? props.context.value
                     : optionsArray.length
                     ? optionsArray[0].value
                     : undefined;
const htmlId = `form-radio-tabs-${window.crypto.randomUUID()}`;
const checkedInput = ref(defaultValue);  // `v-model` on the `input`, that helps us to track the currently checked item

/*******************************************/


/*******************************************/
onMounted(() => {

})
</script>


<style scoped>
.form-radio-tabs-wrapper fieldset {
  width: 100%;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  padding-left: 0;
  margin: 0;
}
.form-radio-option {
  flex-grow: 1;
  margin: 3px;
  border: var(--cs-border);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2px;
  font-family: var(--cs-font-sans-serif);

  transition: background-color var(--cs-color-transition)
              , color var(--cs-color-transition);
}
.form-radio-option:hover {
  background-color: var(--cs-main-second-bg);
  color: var(--cs-main-second)
}
.form-radio-option-selected {
  background-color: var(--cs-contrast-default-bg);
  color: var(--cs-contrast-default);
}
.form-radio-option:checked {
  background-color: var(--cs-main-second-bg);
  color: var(--cs-main-second)
}
.form-radio-option, .form-radio-option * {
  cursor: grab;
}
.form-radio-option > input {
  visibility: hidden;
  width: 0;
  padding: 0;
  margin: 0;
}
ul.formkit-options {
  display: flex;
}
</style>