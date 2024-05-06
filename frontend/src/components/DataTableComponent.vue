<!-- DataTableComponent.vue
     a generic component to display a datatable
     based on component received from the parent
-->

<template>
  <div class="datatable-container"
       @scroll="useDisplayButton">
    <table id="datatable-catalog" class="row-border order-column"></table>
  </div>

  <UpDownScroller></UpDownScroller>
</template>


<script setup>
import { onMounted } from "vue";
import { ref, watch, computed } from 'vue';

import $ from "jquery";
import axios from "axios";
import DataTable from "datatables.net-dt";

import { domStore } from "@stores/dom";
import { isKindaEmpty } from "@utils/functions";
import UpDownScroller from "@components/ui/UpDownScroller.vue";

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
const tableData = ref();                             // {Object}   : the data in the column. array of dicts, with 1 dict per row `[ {<header>: <value>} ]`


/********************************************
 * DATATABLES STUFF
 ********************************************/

/**
 * create the `DataTables.columns` object by extending
 * `props.columnsDefinition` (the columns object defined
 * in the parent) with column definitions for all other
 * columns present in the `props.apiTarget` response
 * but not in `props.columnsDefinition`
 */
function createColumns() {
  const allColsNames = Object.keys(tableData.value[0])
  const dataSample = tableData.value[0]

  /*************
   * functions
   */

  /**
   * fetch a custom column object in `props.columnsDefinition`
   * based on a column name `_colName`
   * @param {string} _colName: a column name
   */
  const getCustomColObj = (_colName) => {
    let matchedColObj = undefined;
    props.columnsDefinition.forEach((c) => {
      if ( c.data === _colName ) { matchedColObj = c; };
    })
    return matchedColObj;
  }

  /**
   * DataTable.column renderers for specific columns:
   * Object (JSON, array) and URLs
   * https://datatables.net/reference/option/columns.render
   * @param {*} data: the column values
   */
  const rendererObject = (data,type,row,meta) => {
    return data != null ? JSON.stringify(data, 2) : data;
  }
  const rendererUrl = (data,type,row,meta) => {
    return data != null ? `<a href="${data}">${data}</a>` : data;
  }

  const emptyCounter = (colName) => {
    let i=0;
    tableData.value.map((tableRow) => {
      i += isKindaEmpty(tableRow[colName]) ? 1 : 0
    })
    return `<p>${i} entrées vides sur ${tableData.value.length}</p>`
  }

  /***********
   * process
   */
  const outCols = [];  // our output: an array of DataTables.column objects
  allColsNames.map((colName) => {
    let colObj = getCustomColObj(colName);

    // if a custom processing is defined in `props.columnsDefinition`
    // for the column `colObj`, get it and add our extra html class names to it
    if ( colObj !== undefined ) {
      colObj.className = classNames;
      colObj.footer = emptyCounter(colName);
      outCols.push(colObj);

    // else, define generic processing
    } else {
      // basic definition
      colObj = { data: colName,
                 title: colName,
                 className: classNames,
                 footer: emptyCounter(colName) };

      // define custom renderers for specific columns
      let renderer = undefined;  // will be defined below
      // URL columns
      if ( typeof(dataSample[colName]) === "string"
         && dataSample[colName].replace('/(^"|"$)/g', "").match(/^https?/g) ) {
        renderer = rendererUrl;
      // object columns (array or dict)
      } else if ( typeof(dataSample[colName]) === "object" ) {
        renderer = rendererObject;
      }
      if ( renderer !== undefined ) { colObj.render = renderer }

      outCols.push(colObj);
    }
  });
  return outCols;
}


/**
 * create a datatable based on the data available
 * at the address `props.apiTarget`
 */
function buildDataTable() {
  axios.get(props.apiTarget, { responseType: "json" })
       .then((r) => {

        tableData.value = props.processResponse(r);

        // delete the datatable if necessary
        if ( $.fn.dataTable.isDataTable($("#datatable-catalog")) ) {
          console.log("is datatable");
          $("#datatable-catalog").DataTable().clear().destroy();
        }
        $("#datatable-catalog").empty();

        // create the new table
        $("#datatable-catalog").DataTable({
          data: tableData.value,
          columns: createColumns(),
          // width and height change on window resize
          autoWidth: false,
          autoHeight: false,
          // make the table scrollable
          scrollX: "100%",
          scrollY: "100%",

          paging: false
        });

        // displayButtonDown.value = useDisplayButtonDown();
        // displayButtonUp.value = useDisplayButtonUp();
      })
}


/********************************************
 * HOOKS
 ********************************************/
onMounted(() => {
  buildDataTable()

  watch(props, (newProps, oldProps) => {
    newProps.apiTarget.value === oldProps.apiTarget.value
    ? buildDataTable()
    : false;
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
#datatable-catalog th {
  font-weight: bolder;
  font-size: 50;
}
#datatable-catalog td {
  font-weight: lighter !important;
  font-family: sans-serif;
  font-size: 12px;

  /* avoid having the td masking the header */
  position: relative;
  z-index: -1;
}
#datatable-catalog.row-border td {
  border-top: none;
  border-bottom: var(--cs-border);
}
#datatable-catalog td:has(img) {
  display: table-cell;
  align-items: center;
  justify-content: center;
}
#datatable-catalog img {
  border: var(--cs-border);
}

.dataTables_filter {
  margin: 1vh 1vw;
}
.dataTables_scrollHead {
  position: sticky !important;
  top: 0;/*var(--cs-navbar-height-mobile);*/
  background-color: var(--cs-main-second-bg);
}
.dataTables_scrollHead * {
  background-color: var(--cs-main-second-bg);
}
@media ( orientation:landscape ) {
  .dataTables_scrollHead {
    /*top: var(--cs-navbar-height-desktop);*/
  }
}
</style>

