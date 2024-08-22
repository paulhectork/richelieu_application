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
            "idUuid" : <uuid of the resource>,
            "href"   : <relative url to redirect to on click (without the url origin)>,
            "img"    : <url to the background image>,
            "text"   : <text to display in the `IndexItem`>
          },
          // other objects
          {...}
        ]
        ```
-->

<template>
  <div class="index-wrapper">
    <div class="index-filter-wrapper">
      <FormKit type="search"
               placeholder="..."
               label="Filtrer"
               :delay="1000"
               @input="textFilter"
      ></FormKit>
    </div>
    <div class="index-inner-wrapper animate__animated animate__slideInLeft">
      <IndexItem v-for="d in dataFilter"
                 :item="d"
                 :display="display"
      ></IndexItem>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from "vue";

import IndexItem from "@components/IndexItem.vue";

/*******************************************************/

const props = defineProps([ "display"  // which component to use for rendering a component: `resource` => `IndexItem.vue`, `concept` => `IndexItem.vue`
                          , "data" ])  // the data to display.
const dataFull = ref([]);    // all items of the index
const dataFilter = ref([]);  // index items filtered in `.index-filter-wrapper`

/*******************************************************/

/**
 * simplify the string `s`
 */
const simplifyString = s =>
  s !== undefined
  ? s.toLowerCase().trim().replaceAll(/\s+/g, " ")
  : s;


/**
 * remove html tags from the string `_string`
 */
const stripHtml = _string => _string.replace(/<[^>]*>?/gm, '');

/**
 *
 * @param {string} filterBy
 */
function textFilter(filterBy) {
  filterBy = simplifyString( stripHtml(filterBy) );
  dataFilter.value = dataFull.value.filter(x =>
    simplifyString( stripHtml(x.text) ).includes(filterBy)
  );
  console.log(dataFilter.value)

}

/*******************************************************/


onMounted(() => {
  dataFull.value = props.data;
  dataFilter.value = dataFull.value;
})
</script>

<style>
.index-inner-wrapper {
  width: 100%;
  display: grid;
  grid-auto-rows: 40vh;
  grid-template-columns: repeat(3, 33%);
}
</style>