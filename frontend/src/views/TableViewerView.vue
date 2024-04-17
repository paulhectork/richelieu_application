<template>
  <h1>Voir les tables</h1>
  <p>Voir les données pour la table
    <select v-model="selectedTable"
            name="selectTable"
            @change="loadTable(selectedTable)"
    >
      <option value="">Choisir la table</option>
      <option v-for="tn in tableNames"
              :value="tn"
      >{{ tn }}</option>
    </select>
  </p>
  <div><DataTableComponent v-if="selectedTable !== ''"
                           :api-target="apiTableTarget"
                           :process-response="processResponse"
                           :columns-definition="columnsDefinition"
  ></DataTableComponent></div>
</template>


<script setup>
import axios from "axios";
import { onMounted, ref } from "vue";
import DataTableComponent from "@components/DataTableComponent.vue"

// basic variables
const apiTargetListTables = new URL ("/i/list-tables", __API_URL__);
const apiTargetTableViewer = new URL("/i/table-viewer/", __API_URL__);
const columnsDefinition = [];

// reactive variables
const tableNames = ref([]);     // array will be filled in `onMounted()`
const selectedTable = ref("");  // the currently selected table from the `<select>` above
const apiTableTarget = ref(""); // the URL from which to fetch datatable data. defined in `loadTable()`

// functions

/**
 * structure a response to fit the model of `DataTables`
 * @param {Object} r: the response returned by the API
 */
function processResponse(r) {
  return JSON.parse(r.request.response);
}

/**
 * 1. delete the previous dataTable
 * 2. fetch data on the table from the backend
 * 3. create a new datatable to display the results
 *
 * OU ALORS ON REND `columnsDefinition` ET `processResponse`
 * RESPONSIVE ET ON MODIFIE JUSTE LES ATTRIBUTS ENVOYÉS
 * À DATATABLES
 *
 * @param {str} tableName: the name of the table
 */
function loadTable(tableName) {
  apiTableTarget.value = new URL(tableName, apiTargetTableViewer);
}

// hooks

onMounted(() => {
  axios.get(apiTargetListTables)
       .then((r) => {
        tableNames.value = JSON.parse(r.request.response);
      })
})

</script>


<style>

</style>