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
     * `multiple`   : (bool) : if `true`, then it's a multi-option select.
                      else, single option. defaults to true

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
              label="Entité nommée"
              placeholder="Sélectionner une entité nommée"
              :options="[{ value: 'a', label: 'Entité nommée 1' },
                         { value: 'b', label: '...2' },
                         { value: 'c', label: '...3' }]"
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
const multiple     = [ true, false, 0, 1 ].includes(props.context.multiple)  // is it a boolean ?
                     ? props.context.multiple
                     : true

/****************************************/

onMounted(() => {
  // single select select2 need an empty `html:option` as their 1st element
  // https://select2.org/placeholders#single-select-placeholders
  if ( !multiple ) { $(`#${selectId}`).prepend("<option></option>") };

  $(`#${selectId}`).select2({
    multiple: multiple,
    placeholder: placeholder,
    allowClear: true,
    data: optionsArray.map((o, idx) => {
      return { id    : `${selectId}-data-${idx}`,
               text  : o.label,
               value : o.value }
    }),
    //
    // `templateResult` and `templateSelection` must return jQuery objects
    // to ensure that HTML markup within `data.text` is not escaped.
    // see: https://select2.org/selections#built-in-escaping
    templateSelection: (data, container) => $(`<span>${data.text}</span>`),
    templateResult: (data) => $(`<span>${data.text}</span>`)
  });

  /**
   * propagate the selected values to FormKit.
   * "change.select2" is triggered when adding / removing an element
   * from the selection, or clearing the selection altogether
   *
   * for some reason, we must use a different way to retrieve data
   * on multi and single-input select2 elements.
   *    - `select2("data")` only works on multi-input.
   *    - for single input, we retrieve the HTML content of the
   *      clicked element and then use it to extract a `value` from
   *      `optionsArray`, which will be send to parent
   *
   * see: https://formkit.com/essentials/architecture#setting-values
   *      https://select2.org/programmatic-control/events
   *      retrieval of multi-input: https://select2.org/programmatic-control/retrieving-selections#using-the-data-method
   */
  $(`#${selectId}`).on("change.select2", (e) => {
    let newInput = [];
    if ( multiple === true ) {
        newInput = $(`#${selectId}`)
                   .select2("data")           // $(`#${selectId}`).select2("data") returns an array of selected values
                   .filter(x => !x.disabled)  // placeholder is disabled => remove it
                   .map(x => x.value)         // retrieve the @value attribute of the selected options
    } else {
      let label    = $(`#${selectId}`).find(":selected").text();  // html text of the clicked element
      if ( label && label.length ) {                              // don't run if what is selected is the empty placeholder
        newInput = optionsArray.filter(x => x.label === label)[0].value;
      }
    }
    selectNode.input(newInput);  // propagate the results to formkit

  });
})
</script>


<style scoped>
</style>