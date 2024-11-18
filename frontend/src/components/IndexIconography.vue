<!-- IndexIconography.vue
  a component that centralizes all indexes/catalogs of Iconography objects.

  so basically, it handles communication between:
  - the parent component (which sends an array of Iconography objects)
  - child `IndexBase` (which handles the UI display of the iconography index)
  - child `FilterIndexIconography` (which filters the data sent from the parent).

  props:
    - data (Array<Object>)
        the array of iconography objects sent from the parent.
        their structure is defined in the backend: Iconography.serialize_lite()
    - oneItemRow (bool)
        a flag indicating that the IndexBase build will display only 1 item per row
        (useful for small viewports: `CartographyPlaceInfo`)
    - hideFilter (bool)
        a flag to hide to remove the FilterIndexIconography block
-->

<template>
  <div class="index-iconography-outer-wrapper">
    <div class="index-iconography-inner-wrapper">
      <FilterIndexIconography v-if="!hideFilter"
                              :data="dataFull"
                              @iconography-filter="handleIconographyFilter"
      ></FilterIndexIconography>

      <IndexBase display="resource"
                 :data="dataFilter"
                 :itemsPerRow="itemsPerRow"
      ></IndexBase>
    </div>
  </div>
</template>


<script setup>
import { onMounted, ref, watch } from "vue";

import FilterIndexIconography from "@components/FilterIndexIconography.vue";
import IndexBase from "@components/IndexBase.vue";

import { indexDataFormatterIconography } from "@utils/indexDataFormatter";

/*************************************************/

const props       = defineProps([ "data", "oneItemRow", "hideFilter" ]);
const hideFilter  = ref(false);
const itemsPerRow = ref();
const dataFull    = ref([]);  // array of iconography objects sent from the parent. this one is never modified.
const dataFilter  = ref([]);  // data, possibly modified by `FilterIndexIconography`, and reshaped with indexDataFormatterIconography

/*************************************************/

function setRefs(theProps) {
  dataFull.value    = theProps.data;
  hideFilter.value  = theProps.hideFilter || false;
  itemsPerRow.value = theProps.oneItemRow === true ? 1 : undefined;
  dataFilter.value  = indexDataFormatterIconography(theProps.data);

  console.log("****", hideFilter.value, itemsPerRow.value);
}

function handleIconographyFilter(iconographyData) {
  dataFilter.value = indexDataFormatterIconography(iconographyData);
}

/*************************************************/

watch(props, (newP, oldP) => {
  console.log("IndexIconography.watch : new props !", newP)
  setRefs(newP);
})

onMounted(() => {
  setRefs(props);
})

</script>


<style scoped>
.index-iconography-outer-wrapper {
  height: 100%;
  width: 100%;
}
.index-iconography-inner-wrapper {

}
</style>