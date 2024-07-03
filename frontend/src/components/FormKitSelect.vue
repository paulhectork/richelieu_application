<!-- FormKit custom input with fancier select.

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
     https://formkit.com/essentials/architecture#setting-values

     usage example:
     ```
     <FormKit type="fkSelect"
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

  <div class="form-field-input-wrapper">
    <select :id="selectId"
            class="form-select-basic"
            style="width: 100%;
                   border-radius: 0;"
    ></select>
  </div>

</template>


<script setup>
import { onMounted, ref } from "vue";

import select2 from "select2";
import "select2/dist/css/select2.css";
import $ from "jquery";

// hook the select2 plugin to jquery.
// not shown in the doc, see: https://stackoverflow.com/a/49722514/17915803
select2($);

/****************************************/

const props        = defineProps([ "context" ]);

const selectId     = `form-select-basic-${window.crypto.randomUUID()}`;  // HTML ID of this select
const selectNode   = props.context.node;                // formkit node for the current FormKit @type='fkSelect' input. see: https://formkit.com/essentials/architecture#node
const optionsArray = props.context.options || [];       // array of all the possible options
const placeholder  = props.context.placeholder != null
                     ? props.context.placeholder
                     : "Sélectionner une valeur";

/****************************************/

/****************************************/

onMounted(() => {
  $(`#${selectId}`).select2({
    multiple: true,
    placeholder: placeholder,
    data: optionsArray.map((o, idx) => { return { id: `${selectId}-data-${idx}`,
                                                  value: o.value,
                                                  text: o.label }
    }),
    // propagate the selected values to FormKit.
    // triggered when adding / removing an element from the selection
    // see: https://formkit.com/essentials/architecture#setting-values
    // and: https://select2.org/programmatic-control/retrieving-selections#using-the-data-method
    templateSelection: (data, container) => {
      selectNode.input( $(`#${selectId}`).select2("data")           // $(`#${selectId}`).select2("data") returns an array of selected values
                                         .filter(x => !x.disabled)  // placeholder is disabled => remove it
                                         .map(x => x.value) )       // retrieve the @value attribute of the selected options
      return data.text;
    }
  });
})
</script>


<style scoped>
</style>