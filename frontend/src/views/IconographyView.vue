<!-- IconographyView.vue
     a view for the iconography index
-->

<template>
  <h1>Index de l'iconographie</h1>
  <Index :display="display"
         :data="dataFilter"
  ></Index>

</template>

<script setup>
import { onMounted, ref } from "vue";
import axios from "axios";

import { indexDataFormatterIconography } from "@utils/indexDataFormatter";
import Index from "@components/Index.vue";
// import DataTableComponent from "@components/DataTableComponent.vue";

const apiTarget = new URL("/i/iconography", __API_URL__);
const dataFull = ref([]);      // the full index, independent of user filters
const dataFilter = ref([]);    // the data to pass to `Index.vue`. this can depend on user-defined filters. an array of { href: <url to redirect to when clicking on an item>, img: <url to the background img to display>, text, <text to display> }
const display = "resource";


onMounted(() => {
  axios.get(apiTarget).then((r) => {
    dataFull.value = JSON.parse(r.request.response);
    dataFilter.value = indexDataFormatterIconography(dataFull.value);
  })
})
</script>

<style scoped>
</style>

<!-- UNUSED / OLD CODE

/**
 * structure a response to fit the model of `DataTables`
 * @ param {Object} r: the response returned by the API
 */
function processResponse(r) {
  return JSON.parse(r.request.response)
             .map((e) => { e.thumbnail = e.thumbnail.length
                                         ? fnToIconographyFile(e.thumbnail[0])
                                         : null;
                           return e })
}

const columnsDefinition = [ { dataFilter: "thumbnail",
                              title: "Image",
                              render: (dataFilter, type, row, meta) => {
                                // retrieve the image from a manifest if there is one
                                return dataFilter != null
                                // ? `<img src="${manifestToThumbnail(dataFilter)}">`
                                ? `<img src="${fnToIconographyFile(dataFilter)}"
                                        alt="Image de: ${row.title[0]}">`
                                : "Image manquante"
                              }
                            },
                            { dataFilter: "iiif_url",
                              title: "URL IIIF",
                              render: (dataFilter, type, row, meta) => {
                                 return dataFilter != null && dataFilter.match(/^https?/g)
                                ? `<a href="${dataFilter}">${dataFilter}</a>`
                                : "Lien IIIF manquant"
                              }
                            },
                            { dataFilter: "authors", title: "Auteur.ice.s" },
                            { dataFilter: "date", title: "Date de création" },
                            { dataFilter: "title", title: "Titre" } ];
-->