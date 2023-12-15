<template>
  <h1>Iconographie</h1>
  <!-- SYNTAX FOR PROPS:
    `<Child :props-name="data or javascript variable"/>`
    or `<Child props-name="data or javascript variable"/>`
    `:` indicates that we are dealing with js data instead of just strings
    (arrays, objects, ints...)
    `props-name` should be written in `kebab-case` in the parent template's
    HTML and will be converted into `camelCase` in the child's js
  -->
  <div><DataTable :api-target="apiTarget"
                  :process-response="processResponse"
                  :columns-formatter="columnsFormatter"
  ></DataTable></div>
</template>

<script setup>
import { stringifyDate, stringifyAuthor } from "@utils/stringifiers";
import { manifestToThumbnail } from "@utils/requests";
import DataTable from "@components/DataTable.vue";

const apiTarget = new URL("/i/iconography", __API_URL__);

function processResponse(r) {
  /**
   * structure a response to fit the model of `DataTables`
   * @param {Object} r: the response returned by the API
   */
  return JSON.parse(r.request.response)
             .map((e) => { let authors = [];
                           e.authors.map((a) => { authors.push(stringifyAuthor(a)) });
                           e.authors = JSON.stringify(authors);
                           e.date = stringifyDate(e.date);
                           return e; })
}

function columnsFormatter(colClassNames) {
  /**
   * define the `DataTables.column` array. we define this as a function
   * to be able to add the key-value pair `className: htmlClassNames` to
   * each item in the `columns`, since it is complicated to mutate a prop
   * and `colClassNames` are defined in `DataTable.vue`
   * @param {str} colClassNames : space-separated classes to add to each column
   * @returns {Array}           : the DataTable.columns object
   */
  return [
    { data: "url_manifest", title: "Image", className: colClassNames,
      render: (data, type, row, meta) => {
        // there is a manifest
        if ( data != null ) {
          let url = manifestToThumbnail(data);
          return `<img src="${manifestToThumbnail(data)}">`
        } else {
          return "Image manquante"
        }
      }
    }
    , { data: "authors", title: "Auteur.ice.s", className: colClassNames }
    , { data: "date", title: "Date de création", className: colClassNames }
    , { data: "title", title: "Titre", className: colClassNames }
  ]
}
</script>

<style>
</style>

