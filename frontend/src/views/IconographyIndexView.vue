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
    ></IndexIconographyFilter>
    <IndexBase display="resource"
               :data="dataFilter"
    ></IndexBase>

  </div>

</template>

<script setup>
import { onMounted, ref } from "vue";
import axios from "axios";

import IndexBase from "@components/IndexBase.vue";
import UiLoader from "@components/UiLoader.vue";
import IndexCount from "@components/IndexCount.vue";

import IndexIconographyFilter from "@components/IndexIconographyFilter.vue";

import { indexDataFormatterIconography } from "@utils/indexDataFormatter";

/******************************************/

const apiTarget = new URL("/i/iconography", __API_URL__);
const dataFull = ref([]);      // the full index, independent of user filters
const dataFilter = ref([]);    // the data to pass to `IndexBase.vue`. this can depend on user-defined filters. an array of { href: <url to redirect to when clicking on an item>, img: <url to the background img to display>, text, <text to display> }
const isLoaded = ref(false);   // switched to true when the data is loaded, will hide the loader and show the index

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

<!-- UNUSED / OLD CODE

/**
 * structure a response to fit the model of `DataTables`
 * @ param {Object} r: the response returned by the API
 */
function processResponse(r) {
  return JSON.parse(r.request.response)
             .map((e) => { e.thumbnail = e.thumbnail.length
                                         ? urlToIconographyFile(e.thumbnail[0])
                                         : null;
                           return e })
}

const columnsDefinition = [ { dataFilter: "thumbnail",
                              title: "Image",
                              render: (dataFilter, type, row, meta) => {
                                // retrieve the image from a manifest if there is one
                                return dataFilter != null
                                // ? `<img src="${manifestToThumbnail(dataFilter)}">`
                                ? `<img src="${urlToIconographyFile(dataFilter)}"
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