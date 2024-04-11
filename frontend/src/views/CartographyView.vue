<template>
  <h1>Cartographie</h1>
  <div><DataTable :api-target="apiTarget"
                  :process-response="processResponse"
                  :columns-formatter="columnsFormatter"
  ></DataTable></div>
</template>

<script setup>
import axios from "axios";
import DataTable from "@components/DataTable.vue";
import { stringifyDate } from "@utils/stringifiers";
import { fnToCartographyFile } from "@utils/functions";

const apiTarget = new URL("/i/cartography", __API_URL__);

function processResponse(r) {
  /**
   * structure a response to fit the model of `DataTables`
   * @param {Object} r: the response returned by the API
   */
  return JSON.parse(r.request.response)
             .map((e) => { e.date = stringifyDate(e.date);
                           e.file = fnToCartographyFile(e.file[0]);
                           return e; })
}

function columnsFormatter(colClassNames) {
  /**
   * define the `DataTables.columns` array. see
   * `IconographyView` for more information
   */
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
     .then((r) => processResponse(r));
</script>
