<template>
  <h1>Cartographie</h1>
  <div><DataTableComponent :api-target="apiTarget"
                           :process-response="processResponse"
                           :columns-formatter="columnsFormatter"
  ></DataTableComponent></div>
</template>

<script setup>
import axios from "axios";
import DataTableComponent from "@components/DataTableComponent.vue";
import { stringifyDate } from "@utils/stringifiers";
import { fnToCartographyFile } from "@utils/functions";

const apiTarget = new URL("/i/cartography", __API_URL__);

/**
 * structure a response to fit the model of `DataTables`
 * @param {Object} r: the response returned by the API
 */
function processResponse(r) {
  return JSON.parse(r.request.response)
             .map((e) => { e.date = stringifyDate(e.date);
                           e.file = fnToCartographyFile(e.file[0]);
                           return e; })
}

/**
 * define the `DataTables.columns` array. see
 * `IconographyView` for more information
 */
function columnsFormatter(colClassNames) {
  return [
    { data: "file", title: "Image", className: colClassNames,
      render: (data,type,row,meta) => {
        if ( data != null ) {
          return `<img style="max-width: 100px"
                       src="${data}">`;
        } else {
          return "Image manquante";
        }
      }
    }
    , { data: "date", title: "Date", className: colClassNames }
    , { data: "title", title: "Titre", className: colClassNames }
  ]
}

axios.get(apiTarget, { responseType: "json" })
     //.then((r) => processResponse(r));
</script>
