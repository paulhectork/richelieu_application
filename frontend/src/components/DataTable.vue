<template>
  <table id="datatable-catalog"
         class="row-border hover compact"
  ></table>
</template>

<script setup>
import $ from "jquery";
import { computed } from "vue";
import DataTable from "datatables.net-dt";
import axios from "axios";
import { onMounted } from "vue";
import { stringifyDate, stringifyAuthor } from "@utils/stringifiers";
import { manifestToThumbnail } from "@utils/requests";

const colClassNames = "dt-body-left dt-head-center"; // essayer de le décaler dans `DataTable.vue`
const props = defineProps(["apiTarget"             // {URL}      : the targeted URL in the backend api
                           , "processResponse"     // {function} : function to transform the response JSON to create the `DataTables.data` object
                           , "columnsFormatter"]); // {function} : function creating the `DataTables.columns`, to format the column objects;

onMounted(() => {
  axios.get(props.apiTarget, { responseType: "json" })
       .then((r) => {
         const d = props.processResponse(r);
         $("#datatable-catalog").DataTable({
           data: d,
           columns: props.columnsFormatter(colClassNames)
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
}
</style>

