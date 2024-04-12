<template>
  <h1>Voir les tables</h1>
  <p>Voir les données pour la table
    <select name="selectTable">
      <option value="">Choisir la table</option>
      <option v-for="tn in tableNames"
              :value="tn"
              @click="loadTable(tn)"
      >{{ tn }}</option>
    </select>
  </p>
  <!--
  <div><DataTable :api-target="apiTarget"
                  :process-response="processResponse"
                  :columns-formatter="columnsFormatter"
  ></DataTable></div>-
  -->
</template>


<script setup>
import axios from "axios";
import { onMounted, ref } from "vue";
import DataTable from "@components/DataTable.vue"

const tableNames = ref([]);  // will be filled later

const apiTargetListTables = new URL ("/i/list-tables", __API_URL__);
const apiTargetTableViewer = new URL("/i/table-viewer/", __API_URL__);

/**
 * structure a response to fit the model of `DataTables`
 * @param {Object} r: the response returned by the API
 */
function processResponse(r) {
  return JSON.parse(r.request.response);
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

/**
 * 1. delete the previous dataTable
 * 2. fetch data on the table from the backend
 * 3. create a new datatable to display the results
 *
 * OU ALORS ON REND `columnsFormatter` ET `processResponse`
 * RESPONSIVE ET ON MODIFIE JUSTE LES ATTRIBUTS ENVOYÉS
 * À DATATABLES
 *
 * @param {str} tableName: the name of the table
 */
function loadTable(tableName) {
  axios.get(new URL(tableName, apiTargetTableViewer))
       .then((r) => { processResponse(r) });
}

onMounted(() => {
  axios.get(apiTargetListTables)
       .then((r) => {
        tableNames.value = JSON.parse(r.request.response);
      })
})

</script>


<style>

</style>