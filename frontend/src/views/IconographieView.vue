<template>
    <h1>Iconographie</h1>
    <table id="iconography-catalog"
           class="row-border hover compact"
    ></table>
</template>

<script setup>
import $ from "jquery";
import DataTable from "datatables.net-dt";
import axios from "axios";
import { onMounted } from "vue";
import { stringifyDate, stringifyAuthor } from "@utils/stringifiers";
import { manifestToThumbnail } from "@utils/requests";

const target = new URL("/i/iconography", __API_URL__);
const colNames = [
  "uuid"
  , "url_manifest"
  , "date"
  , "authors"
  , "title"
]
const colClassNames = "dt-body-left dt-head-center";

function processResponse(r) {
  /**
   * structure a response to fit the model of `DataTables`
   * @param {Object} r: the response returned by the API
   */
  r = JSON.parse(r.request.response);
  for ( let i=0; i<r.length; i++ ) {
    let authors = [];
    for ( let j=0; j<r[i].authors.length; j++ ) {
      authors.push(stringifyAuthor( r[i].authors[j] ));
    }
    r[i].authors = JSON.stringify(authors);
    r[i].date = stringifyDate(r[i].date);
  }
  return r
}

onMounted(() => {
  axios.get(target, { responseType: "json" })
       .then((r) => {
          let d = processResponse(r);
          $("#iconography-catalog").DataTable({
            data: d,
            columns: [
              { data: "url_manifest", title: "Image", className: colClassNames,
                render: (data, type, row, meta) => {
                  // there is a manifest
                  if ( data != null ) {
                    let url = manifestToThumbnail(data);
                    return `<img src="${manifestToThumbnail(data)}">`
                  } else {
                    return "Image manquante"
                  }
                  ;
                }
              }
              , { data: "authors", title: "Auteur.ice.s", className: colClassNames }
              , { data: "date", title: "Date de création", className: colClassNames }
              , { data: "title", title: "Titre", className: colClassNames } ]
          })
       })
       // .catch((e) => { console.log(e); console.log("connard"); });
}
)
</script>

<style>
@import "datatables.net-dt/css/jquery.dataTables.min.css";

th {
  font-weight: bolder;
  font-size: 50;
}
td {
  font-weight: lighter !important;
}
</style>

