<!-- InstitutionIndexView.vue
     an index page of all institutions
-->

<template>
  <div v-if="loadState==='error'">
    <ErrNotFound></ErrNotFound>
  </div>
  <div v-else>
    <h1>Institutions</h1>

    <UiLoaderComponent v-if="loadState==='loading'"></UiLoaderComponent>
    <IndexBase v-else
               display="concept"
               :data="dataFilter"
    ></IndexBase>
  </div>

</template>


<script setup>
import { onMounted, ref, computed, watch } from "vue";
import { useRoute } from "vue-router";
import axios from "axios";

import { indexDataFormatterInstitution } from "@utils/indexDataFormatter";
import {capitalizeString} from "@utils/stringifiers";

import UiLoaderComponent from "@components/UiLoaderComponent.vue";
import ErrNotFound from "@components/ErrNotFound.vue";
import IndexBase from "@components/IndexBase.vue";

/*******************************************************************/

const apiTarget  = new URL ("/i/institution", __API_URL__);
const dataFull   = ref([]);
const dataFilter = ref([]);
const loadState  = ref("loading");  // loading/loaded/error

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

/*******************************************************************/

onMounted(() => {
  getData()
});
</script>


<style scoped>

</style>