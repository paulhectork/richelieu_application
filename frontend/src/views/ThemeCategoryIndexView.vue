<template>
  <div v-if="loadState !== 'error'">

    <h1>Index des thèmes</h1>

    <UiLoaderComponent v-if="loadState === 'loading'"></UiLoaderComponent>
    <IndexBase v-else
           :display="display"
           :data="dataFilter"
    ></IndexBase>

  </div>

  <ErrNotFound v-else></ErrNotFound>

</template>


<script setup>
import { onMounted, ref } from "vue";
import axios from "axios";

import { indexDataFormatterThemeCategory } from "@utils/indexDataFormatter";
import UiLoaderComponent from "@components/UiLoaderComponent.vue";
import ErrNotFound from "@components/ErrNotFound.vue";
import IndexBase from "@components/IndexBase.vue";

/*************************************************************/

const apiTarget  = new URL("/i/theme", __API_URL__)
const dataFull   = ref([]);
const dataFilter = ref([]);
const display    = "concept";
const loadState  = ref("loading");  // "loading"/"loaded"/"error"

/*************************************************************/

onMounted(() => {
  axios.get(apiTarget)
  .then(r => r.data)
  .then(data => { dataFull.value = data;
                  dataFilter.value = indexDataFormatterThemeCategory(data);
                  console.log(dataFilter.value);
                  loadState.value = "loaded";
                })
  .catch(e => { console.error(e);
                loadState.value = "error"
              })
  ;
})


</script>


<style scoped>

</style>
