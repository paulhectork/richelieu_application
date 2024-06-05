<!-- ThemeView.vue
     an index page for all of our themes -->

<template>
  <h1>Index des sujets</h1>
  <p>Les sujets sont des points d'intérêt découverts dans chacune des images.</p>
  <Index :display="display"
         :data="dataFilter"
  ></Index>
</template>

<script setup>
import { onMounted, ref } from "vue";
import axios from "axios";

import { stringifyThemeOrNamedEntityResource } from "@utils/stringifiers";
import { fnToIconographyFile } from "@utils/functions";
import Index from "@components/Index.vue";

const apiTarget = new URL("/i/named-entity", __API_URL__);
const dataFull = ref([]);   // the full index, independent of user filters
const dataFilter = ref([]); // the data to pass to `Index.vue`. this can depend on user-defined filters. an array of { href: <url to redirect to when clicking on an item>, img: <url to the background img to display>, text, <text to display> }
const display = "concept";  // define the view to use in `IndexItem`


onMounted(() => {
  axios.get(apiTarget).then((r) => {

    dataFull.value   = JSON.parse(r.request.response);

    dataFilter.value = dataFull.value.map((c) => {
      return { idUuid : c.id_uuid,
               href   : new URL(`/sujet/${c.id_uuid}`, window.location.href).href,
               iiif   : c.iiif_url != null ? new URL(c.iiif_url) : c.iiif_url,
               img    : c.thumbnail.length ? fnToIconographyFile(c.thumbnail[0]).href : null,
               text   : stringifyThemeOrNamedEntityResource(c)
      }
    })

  })
})


</script>

<style scoped>

</style>