<!-- FormKit plugin with fancier select.

     FormKit only offers basic selects.
     this custom component offers a fancier select
     based on `select2`.

     the parent can pass 2 props to this component:
     * `placeholder`: a placeholder value. otherwise,
                      a default value is given
     * `options`    : the different options for this select.
                      defaults to an empty array.
                      options must be an array of objects,
                      following the structure:
                      https://formkit.com/inputs/select#array-of-objects,
                      with a `value` key containing the form data and a
                      `label` key containing the displayed data.
                      (of course, `label` and `value` can be the same)

     style notes:
     according to the docs, it's best to set sizes
     using inline CSS.

     see:
     https://select2.org/
     https://formkit.com/guides/create-a-custom-input
     https://formkit.com/api-reference/context

     usage example:
     ```
     <FormKit type="formSelectBasic"
              name="namedEntity"
              label="Sujet"
              placeholder="Sélectionner un sujet"
              :options="[{ value: 'a', label: 'Sujet 1' },
                         { value: 'b', label: 'Sujet 2' },
                         { value: 'c', label: 'Sujet 3' }]"
     /><FormKit>
     ```
-->

<template>
  <div class="form-select-basic-wrapper">
    <select :id="selectId"
            class="form-select-basic"
            style="width: 100%;
                   border-radius: 0;"
    >
      <option v-html="placeholder"
              value=""
              selected disabled hidden
      ></option>
      <option v-for="o in optionsArray"
              :value="o.value">{{ o.label }}</option>
    </select>
  </div>
</template>


<script setup>
import { onMounted } from "vue";

import select2 from "select2";
import "select2/dist/css/select2.css";
import $ from "jquery";

// hook the select2 plugin to jquery.
// not shown in the doc, see: https://stackoverflow.com/a/49722514/17915803
select2($);

/****************************************/

const selectId     = `form-select-basic-${window.crypto.randomUUID()}`;  // HTML ID of this select
const props        = defineProps([ "context" ]);
const optionsArray = props.context.options || [];       // array of all the possible options
const placeholder  = props.context.placeholder != null
                     ? props.context.placeholder
                     : "Sélectionner une valeur";

/****************************************/

onMounted(() => {
  $(`#${selectId}`).select2();
})
</script>


<style scoped>

</style>