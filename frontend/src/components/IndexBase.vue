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
  <div class="index-wrapper">
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
      <!-- without paging
      <IndexItem v-for="d in dataFilter"
                 :item="d"
                 :display="display"
      ></IndexItem>
      -->
      <!-- with vue-virtual-scroll:
           https://github.com/Akryum/vue-virtual-scroller/blob/master/packages/vue-virtual-scroller/README.md#recyclescroller
      <RecycleScroller class="scroller"
                      :items="dataFilter"
                      :direction="horizontal"
                      :item-size="`${100/3}px`"
                      key-field="href"
                      v-slot="{ item }"
      ><IndexItem class="the-item"
                  :item="item"
                  :display="display"
      ></IndexItem></RecycleScroller>
      -->

      <!-- as a vue-virtual-scroll-grid
           https://github.com/rocwang/vue-virtual-scroll-grid?tab=readme-ov-file
      -->
      <!--<Grid :length="dataFilter.length"
            :pageSize="20"
            :pageProvider="(pageNumber, pageSize) =>
                dataFilter.slice(pageNumber * pageSize, pageNumber+1 * pageSize)"
      > <template v-slot:default="{ item, style, index }"></template>
      </Grid>
      -->

      <IndexItem v-for="d in pageRenderer(pageNumber, pageSize)"
                 :item="d"
                 :display="display"
      ></IndexItem>

    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, computed } from "vue";

// import Grid from "vue-virtual-scroll-grid";
import $ from "jquery";

import IndexItem from "@components/IndexItem.vue";

/*******************************************************/

const props = defineProps([ "display"      // which component to use for rendering a component: `resource` => `IndexItem.vue`, `concept` => `IndexItem.vue`
                          , "data"         // data to display
                          , "itemsPerRow"  // (optional) number of items to display for each row
                          ])  // the data to display.
const dataFull   = ref([]);  // all items of the index
const dataFilter = ref([]);  // index items filtered in `.index-filter-wrapper`

const pageNumber = ref(0);
const pageSize = 20;

const pageRenderer = (pNumber, pSize) =>
  dataFilter.value.slice(pNumber * pSize, pNumber+1 * pSize);

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

}

/*******************************************************/


onMounted(() => {
  dataFull.value = props.data;
  dataFilter.value = dataFull.value;
})
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
.index-inner-wrapper {
  width: 100%;
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
</style>