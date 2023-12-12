<template>
    <h1>Iconographie</h1>
    <table id="iconography-catalog"></table>
</template>

<script setup>
import $ from "jquery";
import DataTable from "datatables.net-dt";
import axios from "axios";
import { onMounted } from "vue";
import { backendUrl } from "../utils/constants";

const target = new URL("/i/iconography", backendUrl);
const colNames = [
  "uuid"
  , "url_manifest"
  , "date"
  , "authors"
  , "title"
]

function processResponse(r) {
  /**
   * structure a response to fit the model of `DataTables`
   * ÇA ÇA MARCHE, LE PROBLÈME EST DANS DATATABLE
   * @param {Object} r: the response returned by the API
   */
  r = JSON.parse(r.request.response);
  console.log(r);
  let toStringify = [ "date", "authors", "title" ];
  for ( let i=0; i<toStringify.length; i++) {
    for ( let j=0; j<r.length; j++ ) {
      r[j][toStringify[i]] = JSON.stringify(r[j][toStringify[i]]);
    }
  }
  return r
}


onMounted(() => {
  axios.get(target, { responseType: "json" })
       .then((r) => {
          let data = processResponse(r);
       });
  /*
  $("#iconography-catalog").DataTable({
    ajax: { url: target,
            contentType: "application/json",
            mimeType: "application/json",
            dataType: "json",
            dataSrc: (r) => { processResponse(r) }
    },
    columns: colNames
  })
  */
}
)
</script>
