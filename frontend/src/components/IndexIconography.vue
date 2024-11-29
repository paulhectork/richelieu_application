<!-- IndexIconography.vue
  a component that centralizes all indexes/catalogs of Iconography objects.

  this view is to be used every time we need to display an array
  of `Iconography.serialize_lite()`. what is does is wrap IndexBase
  with a few extra functionnalities:
    - FilterIndexIconographyIndex allows to filter the disiplayed data
    - DownloadButtonGroup allows to download the filtered data in CSV or JSON
    - IndexBase handles the UI display of the iconography index)

  props:
    - data (Array<Object>)
          an array of Iconography.serialize_lite objects
    - oneItemRow (bool)
        a flag indicating that the IndexBase build will display only 1 item per row
        (useful for small viewports: `CartographyPlaceInfo`)
    - hideFilter (bool)
        a flag to hide the FilterIndexIconography block

  as with all collections with filters, we use 2 refs:
    - dataFull (Array<Object>)
          stores the data sent from the backend and isn't modified.
    - dataFilter (Array<Object>)
          stores data corresponding to user-defined filters and
          reformatted to fit the data structure expected by IndexBase.
-->

<template>
  <div class="index-iconography-outer-wrapper">
    <div class="index-iconography-inner-wrapper">
      <FilterIndexIconography v-if="!hideFilter"
                              :data="dataFull"
                              @iconography-filter="handleIconographyFilter"
      ></FilterIndexIconography>

      <div class="download-button-wrapper"
           :class="{ 'download-loading': downloadLoading }"
      >
        <UiLoader v-if="downloadLoading"></UiLoader>
        <DownloadButtonGroup @download="onDownload"
                             :disableButtons="downloadLoading"
        />
      </div>

      <IndexBase display="resource"
                 :data="dataFilter"
                 :itemsPerRow="itemsPerRow"
      ></IndexBase>
    </div>
  </div>
</template>


<script setup>
import { computed, onMounted, ref, watch } from "vue";
import axios from "axios";

import DownloadButtonGroup from "@components/DownloadButtonGroup.vue";
import FilterIndexIconography from "@components/FilterIndexIconography.vue";
import IndexBase from "@components/IndexBase.vue";
import UiLoader from "@components/UiLoader.vue";

import { indexDataFormatterIconography } from "@utils/indexDataFormatter";
import { iconographyToCsvRecord } from "@utils/toCsvRecord"
import { downloadData } from "@utils/download"

/*************************************************/

const props           = defineProps([ "data", "oneItemRow", "hideFilter" ]);
const hideFilter      = ref(false);
const itemsPerRow     = ref();
const dataFull        = ref([]);  // array of iconography objects sent from the parent. this one is never modified.
const dataFilter      = ref([]);  // data, possibly modified by `IndexIconographyFilter`, and reshaped with indexDataFormatterIconography
const downloadLoading = ref(false);  // true when an async request is happening in onDownload. will display an `UiLoader`

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

/**
 * @type {Array<String>} : an array of Iconography.id_uuid that fit the current dataFilter
 */
const selection = computed(() => dataFilter.value.map(({idUuid}) => idUuid));

/**
 * when DownloadButtonGroup emits @download, fetch
 * `Iconography.serialize_main` jsons for all items in `selection`.
 * the ref `downloadLoading` displays a loader.
 * @param {String} fileType : csv|json
 */
async function onDownload(fileType) {
  downloadLoading.value = true;
  const apiTarget = new URL("/i/iconography/from-uuid/full", __API_URL__);
  const {data: jsonData} = await axios.post(apiTarget, selection.value);
  downloadLoading.value = false;
  if (fileType === "json") {
    downloadData(jsonData, "json", "iconography");
  } else {
    const csvData = jsonData.map(iconographyToCsvRecord)
    downloadData(csvData, "csv", "iconography");
  }
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
.download-button-wrapper {
  display: grid;
  grid-template-columns: 100%;
  grid-template-rows: 100%;
  transition: background-color 1s;
  min-height: 50px;
}
.download-button-wrapper > * {
  grid-row: 1;
  grid-column: 1;
}
.download-button-group {
  transition: opacity .3s;
}
/*
.download-loading {
  background: linear-gradient( to bottom
                             , white 10%
                             , rgba(1,1,1,.3) 40%
                             , rgba(1,1,1,.3) 40%
                             , white 100%
                             );
}
*/
.download-loading > .download-button-group {
  opacity: 0.2;
}
</style>
