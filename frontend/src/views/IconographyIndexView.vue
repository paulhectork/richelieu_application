<!-- IconographyIndexView.vue
     a view for the iconography index
-->

<template>
  <h1>Iconographie</h1>
  <H2IndexCount :indexCount="dataFull.length"
              dataType="iconography"
              v-if="isLoaded"
  ></H2IndexCount>

  <UiLoader v-if="!isLoaded"></UiLoader>
  <div v-else>
    <IndexIconography :data="dataFull"></IndexIconography>

  </div>

</template>

<script setup>
import { onMounted, ref } from "vue";
import axios from "axios";

import UiLoader from "@components/UiLoader.vue";
import H2IndexCount from "@components/H2IndexCount.vue";
import IndexIconography from "@components/IndexIconography.vue";

/******************************************/

const apiTarget = new URL("/i/iconography", __API_URL__);
const dataFull = ref([]);      // the full index, independent of user filters
const isLoaded = ref(false);   // switched to true when the data is loaded, will hide the loader and show the index


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
