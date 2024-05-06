<!-- IconographyView.vue
     a view for the iconography catalogue
-->

<template>
  <h1>Iconographie</h1>
  <div><DataTableComponent :api-target="apiTarget"
                           :process-response="processResponse"
                           :columns-definition="columnsDefinition"
  ></DataTableComponent></div>
</template>

<script setup>
import { stringifyDate, stringifyAuthor } from "@utils/stringifiers";
import { manifestToThumbnail } from "@utils/iiif";
import { fnToIconographyFile } from "@utils/functions";
import DataTableComponent from "@components/DataTableComponent.vue";

const apiTarget = new URL("/i/iconography", __API_URL__);
const columnsDefinition = [ { data: "thumbnail",
                              title: "Image",
                              render: (data, type, row, meta) => {
                                // retrieve the image from a manifest if there is one
                                return data != null
                                // ? `<img src="${manifestToThumbnail(data)}">`
                                ? `<img src="${fnToIconographyFile(data)}"
                                        alt="Image de: ${row.title[0]}">`
                                : "Image manquante"
                              }
                            },
                            { data: "iiif_url",
                              title: "URL IIIF",
                              render: (data, type, row, meta) => {
                                 return data != null && data.match(/^https?/g)
                                ? `<a href="${data}">${data}</a>`
                                : "Lien IIIF manquant"
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
  const cnt = [];
  return JSON.parse(r.request.response)
             .map((e) => { let authors = [];
                           e.authors.map((a) => { authors.push(stringifyAuthor(a)) });
                           e.authors = JSON.stringify(authors);
                           e.date = stringifyDate(e.date);
                           e.thumbnail = e.thumbnail.length ? e.thumbnail[0] : null;
                           return e })
}
</script>

<style>
</style>

