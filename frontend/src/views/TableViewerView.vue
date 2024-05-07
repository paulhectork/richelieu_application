<template>
  <h1>Voir les tables</h1>

  <p>Voir les données pour la table
    <select v-model="selectedTable"
            name="selectTable"
            @change="loadTable(selectedTable)"
    >
      <option value="" selected disabled>Choisir la table</option>
      <option v-for="tn in tableNames"
              :value="tn"
      >{{ tn }}</option>
    </select>
  </p>

  <p v-if="selectedTable != null && resultsCount > 0"
  >La table <code>{{ selectedTable }}</code>
  contient <b>{{ resultsCount }}</b> entrées.</p>

  <div><DataTableComponent v-if="selectedTable != null"
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
const selectedTable = ref();  // the currently selected table from the `<select>` above
const apiTableTarget = ref(""); // the URL from which to fetch datatable data. defined in `loadTable()`
const resultsCount = ref(0);    // number of results returned by `apiTableTarget`

// functions

/**
 * structure a response to fit the model of `DataTables`
 * @param {Object} r: the response returned by the API
 */
function processResponse(r) {
  const d = JSON.parse(r.request.response);
  resultsCount.value = d.length;
  return d;
}

/**
 * update the URL `apiTableTarget`. the rest of the processing
 * (querying data, updating the table...) is done in the child
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
        tableNames.value = JSON.parse(r.request.response).sort();
      }).catch((err) => { 
      	console.log(err); 
      })
})

</script>


<style>

</style>
