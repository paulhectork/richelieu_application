<!-- IconographyIndexView.vue
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
    <IndexIconography :data="dataFull"></IndexIconography>

  </div>

</template>

<script setup>
import { computed, onMounted, ref } from "vue";
import axios from "axios";

import UiLoader from "@components/UiLoader.vue";
import IndexCount from "@components/IndexCount.vue";
import IndexIconography from "@components/IndexIconography.vue";

/******************************************/

const apiTarget = new URL("/i/iconography", __API_URL__);
const dataFull = ref([]);      // the full index, independent of user filters
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

/******************************************/

onMounted(() => {
  axios.get(apiTarget)
  .then((r) => r.data)
  .then(data => { dataFull.value   = data;
                  isLoaded.value   = true;
  })
})
</script>

<style scoped>

</style>
