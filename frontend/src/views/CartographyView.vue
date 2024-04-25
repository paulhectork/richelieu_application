<!-- CartographyView.vue
     a view for the cartography catalogue
-->

<template>
  <h1>Cartographie</h1>
  <div><DataTableComponent :api-target="apiTarget"
                           :process-response="processResponse"
                           :columns-definition="columnsDefinition"
  ></DataTableComponent></div>
</template>

<script setup>
import axios from "axios";
import DataTableComponent from "@components/DataTableComponent.vue";
import { stringifyDate } from "@utils/stringifiers";
import { fnToCartographyFile } from "@utils/functions";

const apiTarget = new URL("/i/cartography", __API_URL__);
const columnsDefinition = [ { data: "file",
                              title: "Image",
                              render: (data,type,row,meta) => {
                                return data != null
                                ? `<img style="max-width: 100px" src="${data}">`
                                : "Image manquante";
                                }
                            },
                            { data: "date", title: "Date" },
                            { data: "title", title: "Titre" } ];

/**
 * structure a response to fi t the model of `DataTables.data`
 * @param {Object} r: the res ponse returned by the API
 */
function processResponse(r) {
  return JSON.parse(r.request.response)
             .map((e) => { e.date = stringifyDate(e.date);
                           e.file = fnToCartographyFile(e.file[0]);
                           return e; })
}
</script>
