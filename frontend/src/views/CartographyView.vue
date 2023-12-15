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
                           e.file = e.file.length > 0
                                    ? fnToCartographyFile(e.file[0])
                                    : null;
                           return e; })
}

function columnsFormatter(colClassNames) {
  /**
   * define the `DataTables.columns` array
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
    , { data: "description", title: "Adresse", className: colClassNames }
  ]
}

let n = {
  "uuid": "qr1f3e5601548874b0daa0dfe0308f320d4",
  "description": "Neuve-des-Petits-Champs (rue) ; n°9 ; 2e, 3e arr. (anciens) ; 1er, 2e arr. (actuels)",
  "date": "Date inconnue",
  "location": "",
  "file": "qr198377dc6192a4dfebb3bf0d295d33fcd_epsg3857.png"
}

axios.get(apiTarget, { responseType: "json" })
     .then((r) => console.log( processResponse(r) ));
</script>
