<template>
  <table id="datatable-catalog"
         class="row-border hover compact fill-parent"
         @click="console.log($('table').width())"
  ></table>
</template>

<script setup>
import $ from "jquery";
import { ref, watch } from 'vue';
import DataTable from "datatables.net-dt";
import axios from "axios";
import { onMounted } from "vue";
import { domStore } from "@stores/dom";

const colClassNames = "dt-body-left dt-head-center"; // essayer de le décaler dans `DataTable.vue`
const props = defineProps([ "apiTarget"           // {URL}      : the targeted URL in the backend api
                          , "processResponse"     // {function} : function to transform the response JSON to create the `DataTables.data` object
                          , "columnsFormatter"]); // {function} : function creating the `DataTables.columns`, to format the column objects;

onMounted(() => {
  axios.get(props.apiTarget, { responseType: "json" })
       .then((r) => {
         const d = props.processResponse(r);
         $("#datatable-catalog").DataTable({
           data: d,
           columns: props.columnsFormatter(colClassNames),
           autoWidth: false,  // allows width resize
           autoHeight: false  // allows height resize
         })
       })
})
</script>


<style>
@import "datatables.net-dt/css/jquery.dataTables.min.css";
th {
  font-weight: bolder;
  font-size: 50;
}
td {
  font-weight: lighter !important;
  font-family: sans-serif;
  font-size: 12px;
}
</style>

