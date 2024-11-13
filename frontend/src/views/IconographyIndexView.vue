<!-- IconographyView.vue
     a view for the iconography index
-->

<template>
  <h1>Iconographie</h1>
  <IndexCount :indexCount="dataFull.length"
              dataType="iconography"
              v-if="isLoaded"
  ></IndexCount>

  <UiLoader v-if="!isLoaded"></UiLoader>
  <div v-else>
    <IndexIconographyFilter :data="dataFull"
                            @iconography-filter="handleIconographyFilter"
    ></IndexIconographyFilter>
    <DownloadButtonGroup v-if="dataToDownload" :data="dataToDownload" filename="iconography"/>
    <IndexBase display="resource"
               :data="dataFilter"
    ></IndexBase>

  </div>

</template>

<script setup>
import { computed, onMounted, ref } from "vue";
import axios from "axios";

import IndexBase from "@components/IndexBase.vue";
import UiLoader from "@components/UiLoader.vue";
import IndexCount from "@components/IndexCount.vue";

import IndexIconographyFilter from "@components/IndexIconographyFilter.vue";

import { indexDataFormatterIconography } from "@utils/indexDataFormatter";
import DownloadButtonGroup from "../components/DownloadButtonGroup.vue";

/******************************************/

const apiTarget = new URL("/i/iconography", __API_URL__);
const dataFull = ref([]);      // the full index, independent of user filters
const dataFilter = ref([]);    // the data to pass to `IndexBase.vue`. this can depend on user-defined filters. an array of { href: <url to redirect to when clicking on an item>, img: <url to the background img to display>, text, <text to display> }
const isLoaded = ref(false);   // switched to true when the data is loaded, will hide the loader and show the index

/**
 * Mapping between resource uuids and their corresponding flattened data
 * to pass to `IndexBase.vue` that will be downloaded using the DownloadButtonGroup.
 *
 * @type {Record<string, unknown>}
 */
const flattenedResources = computed(() =>
  // dataFull.value.map((resource) => {}) creates a dict of `{ id_uuid : data }`
  Object.fromEntries(dataFull.value.map((resource) =>
    [
      resource.id_uuid, {
        title: resource.title.join(', '),
        iiif_url: resource.iiif_url,
        authors: resource.authors.map(author => author.entry_name).join(', '),
        date: resource.date?.join(', ')
      }
    ]
  ))
);

/**
 * @type {Array<unknown>}
 */
const dataToDownload = computed(() => dataFilter.value.map((resource) => flattenedResources.value[resource.idUuid]));

/******************************************/

/**
 * when IndexIconographyFilter returns the filtered array
 * of Iconography objects, update `dataFilter`, which will
 * trigger the updating of `IndexBase`.
 * @param {Array<Object>} iconographyData
 */
function handleIconographyFilter(iconographyData) {
  dataFilter.value = indexDataFormatterIconography(iconographyData);
}

/******************************************/

onMounted(() => {
  axios.get(apiTarget)
  .then((r) => r.data)
  .then(data => { dataFull.value   = data;
                  dataFilter.value = indexDataFormatterIconography(dataFull.value);
                  isLoaded.value   = true;
  })
})
</script>

<style scoped>

</style>
