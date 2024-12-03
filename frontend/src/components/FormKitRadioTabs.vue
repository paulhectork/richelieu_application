<!-- FormKit custom component with tabs-like selection

    the parent can pass 2 props to this component:
    * `value`  (String)
        the default value in one of our options.
    * `options` (FormKitOptions)
        the different options for this select.
        defaults to an empty array.

    our custom input doesn't check all the things in the checklist
    as they're not needed by the project.

    help:
    the trick to getting the value of a custom input is to use
    the `@input` with an input handler, event, either `node.input(value)`
    or `context.handlers.DOMInput `, as described in the link below !!

    see:
    https://formkit.com/essentials/custom-inputs#global-custom-inputs
    https://formkit.com/essentials/custom-inputs#input-checklist#input-checklist
    https://formkit.com/guides/create-a-custom-input
    https://formkit.com/api-reference/context

    usage example:
    ```
    <FormKit type="fkRadioTabs"
             id="date-filter"
             name="dateFilter"
             label="Date"
             help="Choisir le type de filtre pour la date"
             value="dateRange"
             :options="[ { value: 'a', label: 'Entité nommée 1' },
                         { value: 'b', label: 'Entité nommée 2' },
                         { value: 'c', label: 'Entité nommée 3' }]"
    ></FormKit>
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
               :name="`${htmlId}-input-${o.value}`"
               :id="`${htmlId}-input-${o.value}`"
               :value="o.value"
               @input="context.handlers.DOMInput"
               v-model="checkedInput"
        ></input>
        <label :for="`${htmlId}-input-${o.value}`"
               v-html="o.label"
        ></label>
      </div>
    </fieldset>
  </div>

</template>


<script setup>
import { onMounted, ref } from "vue";

import "@typedefs";

/*******************************************/

const props = defineProps([ "context" ]);
const optionsArray = props.context.options || [];  /** @type {typedefs.FormKitOptionArray} */
const defaultValue = props.context.value           /** @type {String?} : if the "value" is passed from the parent in the context, use it; else, if options are provided, select the 1st value; else, `undefined` */
                     ? props.context.value
                     : optionsArray.length
                     ? optionsArray[0].value
                     : undefined;
const htmlId = `form-radio-tabs-${window.crypto.randomUUID()}`;
const checkedInput = ref(defaultValue);  // `v-model` on the `input`, that helps us to track the currently checked item

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
  margin: 0;
  border: var(--cs-main-border);
  padding: 0;
}
.form-radio-option {
  flex-grow: 1;
  margin: 3px;
  border: var(--cs-main-border);
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  padding: 2px 0px;
  font-family: var(--cs-font-sans-serif);

  transition: background-color var(--cs-color-transition)
              , color var(--cs-color-transition);
}
.form-radio-option:hover {
  background-color: var(--cs-main-second-bg);
  color: var(--cs-main-second)
}
.form-radio-option-selected {
  background-color: var(--cs-main-active-bg);
  color: var(--cs-main-active);
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
.form-radio-option label {
  width: 100%;
  text-align: center;
}
ul.formkit-options {
  display: flex;
}
</style>