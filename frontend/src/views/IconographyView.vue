<template>
  <h1>Iconographie</h1>
  <div><DataTableComponent :api-target="apiTarget"
                           :process-response="processResponse"
                           :columns-formatter="columnsFormatter"
  ></DataTableComponent></div>
</template>

<script setup>
import { stringifyDate, stringifyAuthor } from "@utils/stringifiers";
import { manifestToThumbnail } from "@utils/requests";
import DataTableComponent from "@components/DataTableComponent.vue";

const apiTarget = new URL("/i/iconography", __API_URL__);

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

/**
 * define the `DataTables.column` array. we define this as a function
 * to be able to add the key-value pair `className: htmlClassNames` to
 * each item in the `columns`, since it is complicated to mutate a prop
 * and `colClassNames` are defined in `DataTableComponent.vue`
 *
 * @param {array} responseColumnNames: the column names in the
 * response object
 * @param {str} addClassNames: additional html classes to add
 *                             to the column names (space separated)
 */
function columnsFormatter(responseColumnNames, addClassNames) {
  // if a column name is in `Object.keys(customProcessing)`,
  // the matching value will be used in the returned `columns`
  // object. else, there will be a default process
  const customProcessing = {
    "iiif_url": { data: "iiif_url",
                  title: "Image",
                  className: addClassNames,
                  render: (data, type, row, meta) => {
                    // there is a manifest
                    if ( data != null ) {
                      return `<img src="${manifestToThumbnail(data)}">`
                    } else {
                      return "Image manquante"
                    }
                  }
    },
    "authors": { data: "authors", title: "Auteur.ice.s", className: addClassNames },
    "date": { data: "date", title: "Date de création", className: addClassNames },
    "title": { data: "title", title: "Titre", className: addClassNames }
  }
  let out = responseColumnNames.map((colName) => {
    console.log(colName);
    return Object.keys(customProcessing).includes(colName)
    ? customProcessing[colName]
    : { data: colName, title: colName, className: addClassNames }
  })
  return out;
}
</script>

<style>
</style>

