<template>
  <div class="index-iconography-outer-wrapper">
    <div class="index-iconography-inner-wrapper">
      <IndexIconographyFilter v-if="!hideFilter"
                              :data="dataFull"
                              @iconography-filter="handleIconographyFilter"
      ></IndexIconographyFilter>

      <DownloadButtonGroup @download="onDownload"/>

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

import IndexIconographyFilter from "@components/IndexIconographyFilter.vue";
import IndexBase from "@components/IndexBase.vue";
import DownloadButtonGroup from "@components/DownloadButtonGroup.vue";

import { indexDataFormatterIconography } from "@utils/indexDataFormatter";
import { iconographyToCsvRecord } from "@utils/toCsvRecord"
import { downloadData } from "@utils/download"

/*************************************************/

const props       = defineProps([ "data", "oneItemRow", "hideFilter" ]);
const hideFilter  = ref(false);
const itemsPerRow = ref();
const dataFull    = ref([]);  // array of iconography objects sent from the parent. this one is never modified.
const dataFilter  = ref([]);  // data, possibly modified by `IndexIconographyFilter`, and reshaped with indexDataFormatterIconography

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

const selection = computed(() => dataFilter.value.map(({idUuid}) => idUuid));

async function onDownload(fileType) {
  const apiTarget = new URL("/i/iconography/from-uuid/full", __API_URL__);
  const {data: jsonData} = await axios.post(apiTarget, selection.value);
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
.index-iconography-inner-wrapper {

}
</style>
