<!-- ThemeView.vue
     a catalog page for all of our themes -->

<template>
  <h1>Sujets</h1>
    <Catalog :display="display"
             :data="dataFilter"
    ></Catalog>
</template>

<script setup>
import { onMounted, ref } from "vue";
import axios from "axios";

import { stringifyIconographyResource } from "@utils/stringifiers";
import { manifestToThumbnail } from "@utils/iiif";
import { fnToIconographyFile } from "@utils/functions";
import Catalog from "@components/Catalog.vue";

const apiTarget = new URL("/i/named-entity", __API_URL__);
const dataFull = ref([]);   // the full catalog, independent of user filters
const dataFilter = ref([]); // the data to pass to `Catalog.vue`. this can depend on user-defined filters. an array of { href: <url to redirect to when clicking on an item>, img: <url to the background img to display>, text, <text to display> }
const display = "concept";  // define the view to use in `CatalogItem`


onMounted(() => {
  axios.get(apiTarget).then((r) => {
    dataFull.value   = JSON.parse(r.request.response);
    dataFilter.value = dataFull.value.map((c) => {
      return { href : new URL(`/i/named-entity/${c.id_uuid}`, __API_URL__).href,
               img  : c.thumbnail.length ? fnToIconographyFile(c.thumbnail[0]).href : null,
               text : c.entry_name.toUpperCase()
      }
    })
  })
})


</script>

<style scoped>

</style>