<!-- IconographyView.vue
     a view for the iconography catalogue
-->

<template>
  <h1>Iconographie</h1>
    <!-- <DataTableComponent :api-target="apiTarget"
                           :process-response="processResponse"
                           :columns-definition="columnsDefinition"
    ></DataTableComponent> -->

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
// import DataTableComponent from "@components/DataTableComponent.vue";

const apiTarget = new URL("/i/iconography", __API_URL__);
const dataFull = ref([]);      // the full catalog, independent of user filters
const dataFilter = ref([]);    // the data to pass to `Catalog.vue`. this can depend on user-defined filters. an array of { href: <url to redirect to when clicking on an item>, img: <url to the background img to display>, text, <text to display> }
const display = "resource";   // use `CatalogItem`


onMounted(() => {
  axios.get(apiTarget).then((r) => {

    dataFull.value = JSON.parse(r.request.response);
    dataFilter.value = dataFull.value.map((c) => {
      return { href : new URL(`/i/iconography/${c.id_uuid}`, __API_URL__).href,
               img  : c.thumbnail.length ? fnToIconographyFile(c.thumbnail[0]).href : null,
               text : stringifyIconographyResource(c) };
    })

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