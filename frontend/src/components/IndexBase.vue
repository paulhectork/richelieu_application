<!--  IndexBase.vue

      a basic index to display an array of data: Iconography, Named Entity, Themes.
      the parent sends an array of objects from which to build an item.
      * `IndexBase` handles the array-level
      * `IndexItem` handles the object-level, aka the display of each individual
        item in this array.

      props:
      * `display`: one of "resource"|"concept".
          passed to `IndexItem` to determine the style used.
      * `data`   : the array of data to display. the structure is the same
          no matter the parent which calls IndexBase, or the kind of object
          to display (Icono, Named Entity...):
        ```
        [
          // 1st object
          {
            "href" : <url to redirect to on click>,
            "img"  : <url to the background image>,
            "text" : <text to display in the `IndexItem`>
          },
          // other objects
          {...}
        ]
        ```
-->

<template>
  <div class="index-container animate__animated animate__slideInLeft">
    <IndexItem v-for="d in data"
               :item="d"
               :display="display"
    ></IndexItem>
  </div>
</template>

<script setup>
import { onMounted } from "vue";

import IndexItem from "@components/IndexItem.vue";

const props = defineProps([ "display"  // which component to use for rendering a component: `resource` => `IndexItem.vue`, `concept` => `IndexItem.vue`
                          , "data" ])  // the data to display.
</script>

<style>
.index-container {
  width: 100%;
  display: grid;
  grid-auto-rows: 40vh;
  grid-template-columns: repeat(3, 33%);
}
</style>