<!--  IndexBase.vue

      a basic index to display an array of data: Iconography, Named Entity, Themes.
      the parent sends an array of objects from which to build an item.
        IndexBase
          handles the array-level
        IndexItem
          handles the object-level, aka the display of each individual
          item in this array.

      props:
        display:
          one of "resource"|"concept".
          passed to `IndexItem` to determine the style used.
        data:
          the array of data to display. the structure is the same
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
        itemsPerRow: int|undefined
          the maximum number of items to display per row. so far it's only used
          by `CartographyPlaceInfo`
-->

<template>
  <div class="index-outer-wrapper">
    <div class="index-filter-wrapper">
      <FormKit type="search"
               placeholder="..."
               label="Filtrer"
               :delay="1000"
               @input="textFilter"
      ></FormKit>
    </div>
    <div class="index-inner-wrapper animate__animated animate__slideInLeft"
         :style="computedStyle"
    >
      <!-- without paging -->
      <!--
      <IndexItem v-for="d in dataFilter"
                 :item="d"
                 :display="display"
      ></IndexItem>
      -->

      <!-- with infinite scrolling -->
      <div v-for="d in pageRenderer(pageNumber, pageSize)"
           class="index-item-wrapper"
      >
        <IndexItem :item="d"
                   :display="display"
        ></IndexItem>
      </div>

    </div>
  </div>
</template>

<script setup>
import { onMounted, onUnmounted, ref, computed } from "vue";

import $ from "jquery";

import IndexItem from "@components/IndexItem.vue";

/*******************************************************/

const props = defineProps([ "display"      // which component to use for rendering a component: `resource` => `IndexItem.vue`, `concept` => `IndexItem.vue`
                          , "data"         // data to display
                          , "itemsPerRow"  // (optional) number of items to display for each row
                          ])  // the data to display.
const dataFull   = ref([]);   // all items of the index
const dataFilter = ref([]);   // index items filtered in `.index-filter-wrapper`

const pageNumber = ref(0);    // which page we're on: offset
const pageSize   = 20;        // number of new items to add to the "page"

/**
 * if there is a props.itemsPerRow, set the grid-template-columns.
 * else, just go with what's aldready defined in the css
 */
const computedStyle = computed(() =>
  (props.itemsPerRow)
  ? `grid-template-columns: repeat(${props.itemsPerRow}, calc(100%/${props.itemsPerRow})`
  : '')

/*******************************************************/

/**
 * this function defines the items to display in an infinite scroll.
 * @param {Number} pNumber: the page number
 * @param {Number} pSize  : the number of items per page (aka, the number
 *    of items to display next)
 */
const pageRenderer = (pNumber, pSize) =>
   dataFilter.value.slice(0, (pNumber+1) * pSize);

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
 * @param {string} filterBy
 */
function textFilter(filterBy) {
  filterBy = simplifyString( stripHtml(filterBy) );
  dataFilter.value = dataFull.value.filter(x =>
    simplifyString( stripHtml(x.text) ).includes(filterBy) );

}

/*******************************************************/


onMounted(() => {
  dataFull.value = props.data;
  dataFilter.value = dataFull.value;

  // infinite scroll:
  // if you've scrolled to the end of page, increment pageNumber.
  $("main").on("scroll", (e) => {
    const t = e.target;
    if ( t.scrollTop === t.scrollHeight - t.offsetHeight ) {
      pageNumber.value++
    }
  })
})
onUnmounted(() =>
  $("main").off("scroll")
)
</script>

<style>
/**
 * 3 viewports are defined:
 * - mobile/portrait with small screen/default: only
 *    1 IndexItem per row
 * - mobile/portrait with large screen: 3 items per row
 *    (else, the image quality is too low)
 * - landscape: 3 items per row
 */
.index-outer-wrapper {
  width: 100%;
}
.index-inner-wrapper {
  margin: 0 15px;
  width: auto;
  display: grid;
  grid-auto-rows: 40vh;
  grid-template-columns: 50% 50%;
}
@media ( orientation:portrait ) and ( max-width: 600px ) {
  .index-inner-wrapper {
    grid-template-columns: 100%;
    padding: 0 3% 0 3%;
  }
}
@media ( orientation:landscape ) {
  .index-inner-wrapper {
    grid-template-columns: repeat(3, calc(100%/3));
  }
}
.index-item-wrapper {
  padding: 7px;
}
</style>