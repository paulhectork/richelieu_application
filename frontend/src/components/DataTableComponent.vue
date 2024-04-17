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
    props.columnsDefinition.map((c) => {
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
          ? JSON.stringify(data)
          : data;
        }
      }

      if ( renderer !== undefined ) { colObj.render = renderer }
      outCols.push(colObj);
    }
  });
  return outCols;
}

// hooks

onMounted(() => {
  console.log(">>>", props.apiTarget);
  axios.get(props.apiTarget, { responseType: "json" })
       .then((r) => {
         const d = props.processResponse(r);
         const colNames = Object.keys(d[0]);
         $("#datatable-catalog").DataTable({
           data: d,
           columns: createColumns( colNames, d[0] ),
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

