<template>
  <table id="datatable-catalog"
         class="row-border hover compact fill-parent"
         @click="console.log($('table').width())"
  ></table>
</template>

<script setup>
import $ from "jquery";
import { ref, watch } from 'vue';
import axios from "axios";
import { onMounted } from "vue";
import { domStore } from "@stores/dom";
import DataTable from "datatables.net-dt";

/**
 * how does this component work?
 *
 * brief: this component creates a datatable based
 * on information and functions defined in the parent.
 *
 * long: this component only  generates the datatable
 * and provides generic processes for the datatable
 * (generic = works for all data sources). all specific
 * processes (= the processes that depend from a specific
 * data source and can't be generalized to all datatables)
 * are defined in the parent.
 *
 * the parent defines 3 props:
 * * `apiTarget`       : the URL from which to get the data
 * * `processResponse` : a function defining how to transform
 *                       the response received  from `apiTarget`
 * * `columnsFormatter`: a function returning a `DataTables.columns`
 *                       object, defining specific processing for
 *                       each column (see doc below)
 * see:
 * * https://datatables.net/manual/data/
 * * https://datatables.net/reference/option/columns
 * * https://datatables.net/manual/ajax#JSON-data-source
 */

const classNames = "dt-body-left dt-head-center";
const props = defineProps([ "apiTarget"              // {URL}      : the targeted URL in the backend api
                          , "processResponse"        // {function} : function to transform the response JSON to create the `DataTables.data` object
                          , "columnsFormatter"]);    // {function} : function creating the `DataTables.columns`, to format the column objects;

onMounted(() => {
  axios.get(props.apiTarget, { responseType: "json" })
       .then((r) => {
         const d = props.processResponse(r);
         $("#datatable-catalog").DataTable({
           data: d,
           columns: props.columnsFormatter(Object.keys(d[0]), classNames),
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

