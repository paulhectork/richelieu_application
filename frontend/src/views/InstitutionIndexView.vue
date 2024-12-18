<template>

  <!-- InstitutionIndexView.vue
       an index page of all institutions
  -->


  <div v-if="loadState==='error'">
    <ErrNotFound></ErrNotFound>
  </div>
  <div v-else>
    <h1>Institutions</h1>

    <DownloadButtonGroup @download="onDownload"/>
    <UiLoader v-if="loadState==='loading'"></UiLoader>
    <IndexBase v-else
               display="concept"
               :data="dataFilter"
    ></IndexBase>
  </div>

</template>


<script setup>
import { computed, onMounted, ref } from "vue";

import axios from "axios";

import DownloadButtonGroup from "@components/DownloadButtonGroup.vue";
import UiLoader from "@components/UiLoader.vue";
import ErrNotFound from "@components/ErrNotFound.vue";
import IndexBase from "@components/IndexBase.vue";

import { institutionToCsvRecord } from "@utils/toCsvRecord";
import { downloadData } from "@modules/download";
import { useListExport } from "@composables/useListExport";
import { indexDataFormatterInstitution } from "@utils/indexDataFormatter";

import "@typedefs";

/*******************************************************************/

const apiTarget  = new URL ("/i/institution", __API_URL__);
const dataFull   = ref([]);         /** @type {typedefs.InstitutionItemLite[]} */
const dataFilter = ref([]);         /** @type {typedefs.IndexBaseItem[]} */
const loadState  = ref("loading");  /** @type {typedefs.AsyncRequestState} loading/loaded/error */

/*******************************************************************/

/**
 * get institution data from the backend
 */
function getData() {
  axios.get(apiTarget.href)
  .then(r => r.data)
  .then(data => { dataFull.value = data;
                  dataFilter.value = indexDataFormatterInstitution(data);
                  loadState.value = "loaded" })
  .catch(e => { console.error(e);
                loadState.value = "error" });
}

const selection = computed(() => dataFilter.value.map(({idUuid}) => idUuid));

const dataToExport = useListExport(
  dataFull,
  selection,
  {
    toJSON(resource) {
      return resource;
    },
    toCSV: institutionToCsvRecord,
  },
)

function onDownload(fileType) {
  downloadData(dataToExport[fileType].value, fileType, "institution")
}

/*******************************************************************/

onMounted(() => {
  getData()
});
</script>


<style scoped>

</style>
