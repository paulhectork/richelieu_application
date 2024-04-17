<template>
  <div class="datatable-container">

    <table id="datatable-catalog"></table>
    <!--
    <DataTable id="datatable-catalog"
               class="row-border hover compact fill-parent"
               ref="table"
               :options="tableOptions"
               @click="console.log($('table').width())"
    ></DataTable>
    -->
  </div>
</template>

<script setup>
import $ from "jquery";
import { ref, watch, computed } from 'vue';
import axios from "axios";
import { onMounted } from "vue";
import { domStore } from "@stores/dom";
import DataTable from "datatables.net-dt";

// Vue3-DataTables stuff
// import DataTable from 'datatables.net-vue3';
// import DataTablesLib from "datatables.net-dt";
// DataTable.use(DataTablesLib);

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
 * * `apiTarget`        : the URL from which to get the data
 * * `processResponse`  : a function defining how to transform
 *                        the response received  from `apiTarget`
 * * `columnsDefinition`: an array matching the `DataTables.columns`
 *                        object, defining specific processing for
 *                        certain columns. this array can be empty.
 *
 *                        structure example (1 entry per column):
 *                        `[
 *                          { data: <key in the response 1>,
 *                            title: <human readable title 1>,
 *                            render: <custom rendering function> },
 *                          { data: <key in the response>,
 *                            title: <human readable title 2>,
 *                            render: <custom rendering function }
 *                        ]`
 * see:
 * * https://datatables.net/manual/data/
 * * https://datatables.net/reference/option/columns
 * * https://datatables.net/manual/ajax#JSON-data-source
 */
const classNames = "dt-body-left dt-head-center";
const props = defineProps([ "apiTarget"              // {URL}      : the targeted URL in the backend api
                          , "processResponse"        // {function} : function to transform the response JSON to create the `DataTables.data` object
                          , "columnsDefinition"]);   // {function} : function creating the `DataTables.columns`, to format the column objects;

// default datatable options
const tableOptions = {
  // width and height change on window resize
  autoWidth: false,
  autoHeight: false,
  // make the table scrollable
  scrollX: "100%",
  scrollY: "100%",
  paging: false
};

let dt;
const table=ref();
const tableData=ref([[]]);
const tableColumns=ref([[]]);

/**
 * `computed()` allows vue to track to changes with `watch()`
 * in `props` in the same way that `ref()` changes are tracked.
 * see: https://stackoverflow.com/a/70631776/17915803
 */
const localApiTarget = computed(() => props.apiTarget);
const localColumnsDefinition = computed(() => props.columnsDefinition);

/**
 * create the `DataTables.columns` object by extending
 * `props.columnsDefinition` (the columns object defined
 * in the parent) with column definitions for all other
 * columns present in the `props.apiTarget` response
 * but not in `props.columnsDefinition`
 *
 * @param {Array<string>} allColsNames: all column names retrieved from `apiTarget`
 * @param {object}        dataSample  : the first row of data, to sniff for specfic cases
 *                                      on which we'll apply special rendering (URLS, objects)
 */
function createColumns(allColsNames, dataSample) {
  /**
   * fetch a custom column object in `props.columnsDefinition`
   * based on a column name `_colName`
   * @param {string} _colName: a column name
   */
  const getCustomColObj = (_colName) => {
    localColumnsDefinition.value.map((c) => {
      if ( c.data === _colName ) { return c; }
    })
    return false;
  }

  const outCols = [];  // our output: an array of DataTables.column objects
  allColsNames.map((colName) => {
    let colObj = getCustomColObj(colName);

    // if a custom processing is defined in `props.columnsDefinition`,
    // get it and add our extra html class names to it
    if (colObj) {
      colObj.className = classNames;
      outCols.push(colObj);

    // else, define generic processing
    } else {
      // basic definition
      colObj = { data: colName, title: colName, className: classNames };

      // define custom renderers for specific columns
      let renderer = undefined;  // will be defined below
      // URL columns
      if (  typeof(dataSample[colName]) === "string"
         && dataSample[colName].match(/^https?/g) ) {
        renderer = (data,type,row,meta) => {
          return data != null    // `!= null` matches `null` and `undefined`
          ? `<a href="${data}">`
          : data;
        }
      // object columns (array or dict)
      } else if ( typeof(dataSample[colName]) === "object" ) {
        renderer = (data,type,row,meta) => {
          return data != null
          ? JSON.stringify(data, 2)
          : data;
        }
      }

      if ( renderer !== undefined ) { colObj.render = renderer }
      outCols.push(colObj);
    }
  });
  return outCols;
}

/**
 * create a datatable based on the data available at the
 * address `apiTarget`
 * @param {URL} apiTarget: the URL from which to fetch data
 */
function buildDataTable(apiTarget) {
  axios.get(props.apiTarget, { responseType: "json" })
       .then((r) => {
        console.log(1);

        const d = props.processResponse(r);
        const colNames = Object.keys(d[0]);

        console.log(2);

        // delete the datatable if necessary
        if ( $.fn.dataTable.isDataTable($("#datatable-catalog")) ) {
          console.log("is datatable");
          $("#datatable-catalog").DataTable().clear().destroy();
        }
        $("#datatable-catalog").empty();

        console.log(3);

        // create the new table
        $("#datatable-catalog").DataTable({
          data: d,
          columns: createColumns( colNames, d[0] ),
          // width and height change on window resize
          autoWidth: false,
          autoHeight: false,
          // make the table scrollable
          scrollX: "100%",
          scrollY: "100%",
          paging: false
        })
      })

}

// hooks

onMounted(() => {
  /* Vue3 style -- doesn't work: :columns must be set
     by default in the `html:DataTable` but my cols are
     defined asynchronously
  dt = table.value.dt;
  axios.get(props.apiTarget, { responseType: "json" })
       .then((r) => {
         tableData.value = props.processResponse(r);
         const colNames = Object.keys(tableData.value[0]);
         tableColumns.value = createColumns( colNames, tableData.value[0] );
         console.log(tableColumns.value);

         dt.destroy();
         dt.columns(tableColumns);
         dt.rows.add(d);
  })
  */

  /* JQuery style */
  console.log(">>>", props.apiTarget.href);
  buildDataTable(props.apiTarget);

  watch(localApiTarget, (newApiTarget, oldApiTarget) => {
      buildDataTable(newApiTarget);
  })

})
</script>


<style>
@import "datatables.net-dt/css/jquery.dataTables.min.css";
.datatable-container {
  margin: 10px;
  padding: 2px;
  border: var(--cs-border)
}
th {
  font-weight: bolder;
  font-size: 50;
}
td {
  font-weight: lighter !important;
  font-family: sans-serif;
  font-size: 12px;
}
/* not working
tr {
  height: 15px !important;
  overflow: scroll;
}
*/
</style>

