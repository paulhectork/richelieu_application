<template>
  <div class="index-iconography-outer-wrapper">
    <div class="index-iconography-inner-wrapper">
      <IndexIconographyFilter v-if="!hideFilter"
                              :data="dataFull"
                              @iconography-filter="handleIconographyFilter"
      ></IndexIconographyFilter>

      <DownloadButtonGroup v-if="dataToDownload" :data="dataToDownload" filename="iconography"/>

      <IndexBase display="resource"
                 :data="dataFilter"
                 :itemsPerRow="itemsPerRow"
      ></IndexBase>
    </div>
  </div>
</template>


<script setup>
import { computed, onMounted, ref, watch, toRaw } from "vue";
import {mapValues} from "lodash"

import IndexIconographyFilter from "@components/IndexIconographyFilter.vue";
import IndexBase from "@components/IndexBase.vue";
import DownloadButtonGroup from "../components/DownloadButtonGroup.vue";

import { indexDataFormatterIconography } from "@utils/indexDataFormatter";
import { stringifyDate } from "@utils/stringifiers";

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

/**
 * Mapping between resource uuids and their corresponding flattened data
 * that will be downloaded using the DownloadButtonGroup.
 *
 * @type {Record<string, unknown>}
 */
const idToJson = computed(() =>
  Object.fromEntries(dataFull.value.map((resource) =>
    [
      resource.id_uuid, {
        uuid: resource.id_uuid,
        title: resource.title.join(', '),
        iiif_url: resource.iiif_url,
        authors: resource.authors.map(author => ({name: author.entry_name, uuid: author.id_uuid})),
        date: resource.date
      }
    ]
  ))
);

/**
 * Mapping between resource uuids and their corresponding flattened data
 * that will be downloaded using the DownloadButtonGroup.
 *
 * @type {Record<string, unknown>}
 */
const idToCsv = computed(() => 
  Object.fromEntries(dataFull.value.map((resource) => 
    [
    resource.id_uuid, {
        uuid: resource.id_uuid,
        title: resource.title.join('|'),
        iiif_url: resource.iiif_url,
        authors: resource.authors.map(author => author.entry_name).join('|'),
        authors_uuids: resource.authors.map(author => author.id_uuid).join('|'),
        date: stringifyDate(resource.date),
      }]
    )
  )
);


/**
 * @type {Array<unknown>}
 */
const dataToDownload = computed(() => dataFilter.value.length > 0 ? 
  ({
    json: dataFilter.value.map((resource) => idToJson.value[resource.idUuid]),
    csv: dataFilter.value.map((resource) => idToCsv.value[resource.idUuid]),
  }) : null
);

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
