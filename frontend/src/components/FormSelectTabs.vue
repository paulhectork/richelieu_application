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
  <div class="form-select-tabs-wrapper">
    <button v-for="o in optionsArray"
            :value="o.value"
            v-html="o.label"
            @click="selectHandler"
            @touchend="selectHandler"
    ></button>
  </div>

</template>

<script setup>
import { onMounted } from "vue";

import $ from "jquery";

/*******************************************/

const props        = defineProps([ "context" ]);
const optionsArray = props.context.options || []; // array of all the values
console.log(optionsArray);

/*******************************************/

function selectHandler(e) {
  e.preventDefault();
}

/*******************************************/
</script>

<style scoped>
.form-select-tabs-wrapper {
  width: 100%;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
}
.form-select-tabs-wrapper > button {
  flex-grow: 1;
}
</style>