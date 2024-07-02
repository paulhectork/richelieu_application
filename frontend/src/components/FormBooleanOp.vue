<!-- FormBooleanOp.vue:
     a Select2 component to choose a boolean operator
     ("AND", "OR", "NOT"), defaulting to "AND".

     unlike other `Form*.vue` components, this one is
     not a FormKit input but a simple Vue Component.
 -->


<template>
  <div class="form-boolean-flag-wrapper">
    <label :for="htmlId" hidden>Type de relation</label>
    <select :id="htmlId"
            :name="htmlId"
            class="form-select-basic"
            style="width: 100%;
                   height: 100%;
                   border-radius: 0;"
    >
      <option value="and">ET</option>
      <option value="or">OU</option>
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

const emits = defineEmits(["boolean-op"]);
const props = defineProps(["htmlId"]);
const htmlId = props.htmlId || `form-boolean-flag-${window.crypto.randomUUID()}`;

/*****************************************/

onMounted(() => {
  $(`#${htmlId}`).select2({
    multiple: false,
    // propagate the change of values to formkit.
    templateSelection: (data, container) => {
      if ( ! data.disabled ) { emits("boolean-op", data.element.value) }
      return data.text  // the return is the displayed value.
    }
  })
})

</script>


<style scoped>

</style>