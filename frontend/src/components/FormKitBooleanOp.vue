<!-- FormKitBooleanOp.vue:
     a Select2 component to choose a boolean operator
     ("AND", "OR", "NOT"), defaulting to "AND".

     props:
     * context: the FormKit context
     * id: the html ID and name of the current FormKitBooleanOp component
 -->


<template>
  <div class="form-field-boolean-op-wrapper">
    <label :for="htmlId" hidden>Type de relation</label>
    <select :id="htmlId"
            :name="htmlId"
            class="form-select-basic"
            style="width: 100%;
                   height: 100%;
                   border-radius: 0;"
    >
      <option value="and">ET</option>
      <!--<option value="or">OU</option>-->
      <option value="not">SAUF</option>
    </select>
  </div>
</template>


<script setup>
import { onMounted } from "vue";

import select2 from "select2";
import "select2/dist/css/select2.css";
import $ from "jquery";

select2($);

/*****************************************/

const props = defineProps(["context"]);
const htmlId = props.context.id || `form-boolean-op-${window.crypto.randomUUID()}`;

/*****************************************/

onMounted(() => {
  $(`#${htmlId}`).select2({
    multiple: false,
    // propagate the change of values to formkit.
    templateSelection: (data, container) => {
      if ( ! data.disabled ) { props.context.node.input(data.element.value) }
      return data.text  // the return is the displayed value.
    }
  })
  // set the margin-top of .form-field-boolean-op-wrapper,
  // so that they can be properly aligned with the other input contained
  // in the .form-field-outer-wrapper.
  // for some reason, depending on the type of main input
  // (select2 or text input), the calculated `baseMarginTop`
  // can be slightly wrong (+-3px). so we calculate an `adapter`
  // of values to add / remove to the marginTop, to position it better.
  let $booleanOpWrapper = $(".form-field-boolean-op-wrapper");
  let $outerWrapper     = $(".form-field-outer-wrapper");
  let $inputWrapper     = $(".form-field-input-wrapper");
  let baseMarginTop = $inputWrapper.offset().top - $outerWrapper.offset().top;
  $booleanOpWrapper.each((idx, el) => {
    let adapter = $(el).closest(".form-field-outer-wrapper").find("input").length
                  ? 0
                  : 3;
    $(el).css({ marginTop: baseMarginTop - adapter });
  })
  // let adapter = $booleanOpWrapper.closest(".form-field-outer-wrapper").find("input").length;
  // $booleanOpWrapper.css({ marginTop: baseMarginTop });

})

</script>


<style scoped>

</style>