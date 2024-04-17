<template>
  <h1>Iconographie</h1>
  <div><DataTableComponent :api-target="apiTarget"
                           :process-response="processResponse"
                           :columns-definition="columnsDefinition"
  ></DataTableComponent></div>
</template>

<script setup>
import { stringifyDate, stringifyAuthor } from "@utils/stringifiers";
import { manifestToThumbnail } from "@utils/requests";
import DataTableComponent from "@components/DataTableComponent.vue";

const apiTarget = new URL("/i/iconography", __API_URL__);
const columnsDefinition = [ { data: "iiif_url",
                              title: "Image",
                              render: (data, type, row, meta) => {
                                // retrieve the image from a manifest if there is one
                                return data !== null
                                ? `<img src="${manifestToThumbnail(data)}">`
                                : "Image manquante"
                              }
                            },
                            { data: "authors", title: "Auteur.ice.s" },
                            { data: "date", title: "Date de création" },
                            { data: "title", title: "Titre" } ];

/**
 * structure a response to fit the model of `DataTables`
 * @param {Object} r: the response returned by the API
 */
function processResponse(r) {
  return JSON.parse(r.request.response)
             .map((e) => { let authors = [];
                           e.authors.map((a) => { authors.push(stringifyAuthor(a)) });
                           e.authors = JSON.stringify(authors);
                           e.date = stringifyDate(e.date);
                           return e })
}
</script>

<style>
</style>

