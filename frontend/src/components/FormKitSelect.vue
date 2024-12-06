<!-- FormKit custom input with fancier select.

  FormKit only offers basic selects.
  this custom component offers a fancier select
  based on `select2`.

  the parent can pass 2 props to this component:
  * `placeholder` (String?)
        a placeholder value. otherwise a default value is given
  * `options`(typedefs.FormKitOptionArray)
        the different options for this select. defaults to an empty array.
        options must be an array of objects, following the structure :
        https://formkit.com/inputs/select#array-of-objects,
        with a `value` key containing the form data and a `label` key
        containing the displayed data. (of course, `label` and `value` can
        be the same)
  * `multiple` (boolean)
        if `true`, then it's a multi-option select. else, single option.
        defaults to true
  * `disabled` (boolean)
        if `true`, then the select will be disabled. this option is THE ONLY
        ONE that can be dynamically switched using a watcher.

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
            :disabled="isDisabled"
    ></select>
  </div>

</template>


<script setup>
import { onMounted, ref, watch } from "vue";

import select2 from "select2";
import "select2/dist/css/select2.css";
import $ from "jquery";

import "@typedefs";

// hook the select2 plugin to jquery.
// not shown in the doc, see: https://stackoverflow.com/a/49722514/17915803
select2($);

/****************************************/

const props        = defineProps([ "context" ]);

const selectId     = `form-select-basic-${window.crypto.randomUUID()}`;  /** @type {String} HTML ID of this select */
const selectNode   = ref();                          /** @type {FormKitNode} formkit node for the current FormKit @type='fkSelect' input. see: https://formkit.com/essentials/architecture#node */
const optionsArray = ref([]);                        /** @type {typedefs.FormKitOptionArray} array of all the possible options */
const placeholder  = ref("Sélectionner une valeur"); /** @type {String} */
const multiple     = ref(true);                      /** @type {boolean} multi-select by default */

const isDisabled   = ref(false);    /** @type {boolean} */

/****************************************/

/**
 * define all the necessary refs
 */
function setRefs(theContext) {
  selectNode.value   = theContext.node;
  optionsArray.value = theContext.options || [];
  isDisabled.value   = theContext.disabled;
  placeholder.value  = theContext.placeholder != null
                       ? theContext.placeholder
                       : "Sélectionner une valeur";
  multiple.value     = [ true, false, 0, 1 ].includes(theContext.multiple)
                       ? theContext.multiple
                       : true
}

/**
 * define the select2 object
 */
function initSelect() {
  // single select2 need an empty `html:option` as their 1st element
  // https://select2.org/placeholders#single-select-placeholders
  if ( !multiple.value ) { $(`#${selectId}`).prepend("<option></option>") };

  $(`#${selectId}`).select2({
    multiple: multiple.value,
    placeholder: placeholder.value,
    allowClear: true,
    data: optionsArray.value.map((o, idx) => {
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

}

/**
 * event handler that, when a new value is selected,
 * emits values to the parent FormKit element.
 *
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
function emitOnChange() {
  $(`#${selectId}`).on("change.select2", (e) => {
    let newInput = [];
    if ( multiple.value === true ) {
        newInput = $(`#${selectId}`)
                   .select2("data")           // $(`#${selectId}`).select2("data") returns an array of selected values
                   .filter(x => !x.disabled)  // placeholder is disabled => remove it
                   .map(x => x.value)         // retrieve the @value attribute of the selected options
    } else {
      let label = $(`#${selectId}`).find(":selected").text();  // html text of the clicked element
      if ( label && label.length ) {                              // don't run if what is selected is the empty placeholder
        newInput = optionsArray.value.filter(x => x.label === label)[0].value;
      }
    }
    selectNode.value.input(newInput);  // propagate the results to formkit
  });
}

/****************************************/

/**
 * in some cases, the `disabled` attribute will be added/removed
 * to the input based on a dynamic value change: the parent has a
 * `ref` that enables/disables FormKitSelect` based on some data.
 * we implement a watcher that switches `isDisabled` based on the
 * `context.disabled`, in turn switching the `disabled` html
 * attribute on the `select`.
 *
 * WARNING: ONLY THE DISABLED PROPERTY IS WATCHED,
 * the select does not handle other data changes !!!!!!!!!!!!
 */
watch(props, (newP, oldP) => {
  isDisabled.value = newP.context.disabled || false;
})

onMounted(() => {
  setRefs(props.context);
  initSelect();
  emitOnChange();
})
</script>


<style scoped>
</style>