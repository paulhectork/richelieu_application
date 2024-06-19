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
  <!--
    <button v-for="o in optionsArray"
            :value="o.value"
            v-html="o.label"
            @click="selectHandler"
            @touchend="selectHandler"
    ></button>
  -->

    <FormKit type="radio"
             name=""
             :options="optionsArray"
             :sections-schema="{ wrapper: { $el: 'button' },
                                 input  : { $el: 'span' }      // block the display of the radio button
                               }"
    ></FormKit>

  </div>

</template>

<script setup>
import { onMounted } from "vue";

import $ from "jquery";

import { clickOrTouchEvent } from "@globals";

/*******************************************/

const props        = defineProps([ "context" ]);
const optionsArray = props.context.options || []; // array of all the values
console.log(optionsArray);

/*******************************************/

onMounted(() => {
  // style. we need to use JS because FormKit
  // overwrites basic CSS stylings
  $("ul.formkit-options").css({ listStyle     : "none",
                                paddingLeft   : 0,
                                margin        : 0,
                                display       : "flex",
                                flexDirection : "row",
                                justifyContent: "space-between",
                                alignItems    : "center" });
  $("ul.formkit-options li").css({ flexGrow: 1, margin: "3px" });
  $("ul.formkit-options button").css({ width: "100%" });

  // events
  $("ul.formkit-options button").on(clickOrTouchEvent, (e) => {
    e.preventDefault();
    // color the selected button
    $("button.formkit-wrapper").removeClass("contrast-default");
    $(e.currentTarget).addClass("contrast-default");
  })

})

/*******************************************/
</script>

<style scoped>
.form-select-tabs-wrapper ul {
  width: 100%;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
}
.form-select-tabs-wrapper button {
  flex-grow: 1;
}
ul.formkit-options {
  display: flex;
}
</style>