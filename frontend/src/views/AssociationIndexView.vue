<!-- AssociationIndexView.vue

     an index combining two filters on the database:
     themeA + themeB, namedEntityA + namedEntityB...

     this association index is accessed when clicking on
     the "Ressources associées" part


     WARNING: TABLE NAMES MUST BE WRITTED IN snake_case, LIKE IN THE DATABASE
-->

<template>
  <!-- display the combined index -->
  <div v-if="error !== true">
    <h1 v-if="Object.keys(from).length && Object.keys(to).length">
      {{ capitalizeString(from.entryName) }} <!--({{ from.table }})-->
      &amp;
      {{ capitalizeString(to.entryName) }} <!--({{ to.table }})-->
    </h1>

    <div class="index-wrapper">
      <div v-if="loaded"
           class="index-wrapper">
        <p v-if="dataFull.length === 1">
        {{ dataFull.length }} ressource est associée à cette combinaison.</p>
        <p v-else-if="dataFull.length > 1">
          {{ dataFull.length }} ressources sont associées à cette combinaison.
        </p>
        <p v-else>Aucun résultat ne correspond à cette combinaison.</p>

        <IndexBase :data="dataFilter"
                   display="resource"
        ></IndexBase>
      </div>

      <div v-else>
        <UiLoaderComponent></UiLoaderComponent>
      </div>
    </div>
  </div>

  <!-- display an error message -->
  <div v-if="error === true">
    <ErrNotFound></ErrNotFound>
  </div>

</template>


<script setup>
import { onMounted, ref } from "vue";

import axios from "axios";

import IndexBase from "@components/IndexBase.vue";
import ErrNotFound from "@components/ErrNotFound.vue";
import UiLoaderComponent from "@components/UiLoaderComponent.vue";

import { capitalizeString } from "@utils/stringifiers";
import { indexDataFormatterIconography } from "@utils/indexDataFormatter.js";

/***************************************/

const props = defineProps([ "toIdUuid", "fromIdUuid", "fromTable", "toTable" ]);

const from       = ref({});     // { <entryName>: "...", <idUuid>: "qr1...", <table>: "table name" }
const to         = ref({});     // { <entryName>: "...", <idUuid>: "qr1...", <table>: "table name" }
const dataFull   = ref([]);     // array of iconography objects (without filtering). populated in `getData`
const dataFilter = ref([]);     // array of iconography objects (with optional filtering)
const loaded     = ref(false);  // switched to true once the backend has returned results, with no error.
const error      = ref(false);  // switched to true if an error occurs

/***************************************/

/**
 * retrieve human redeable names for the ressources `toIdUuid` and `fromIdUuid`.
 * from those names and the props, build the `from` and `to` refs.
 */
async function getNames() {
  // select the proper backend route based on `fromTable` and `toTable`
  let fromRoute, toRoute;
  switch ( props.fromTable ) {
    case "theme":
      fromRoute = new URL(`/i/theme-name/${props.fromIdUuid}`, __API_URL__);
      break;
    case "named_entity":
      fromRoute = new URL(`/i/named-entity-name/${props.fromIdUuid}`, __API_URL__);
      break;
    default:
      throw new Error(`AssociationIndexView.getNames(): could not build URL for "fromTable": "${props.fromTable}"`);
  }
  switch ( props.toTable ) {
    case "theme":
      toRoute = new URL(`/i/theme-name/${props.toIdUuid}`, __API_URL__);
      break;
    case "named_entity":
      toRoute = new URL(`/i/named-entity-name/${props.toIdUuid}`, __API_URL__);
      break;
    default:
      throw new Error(`AssociationIndexView.getNames(): could not build URL for "toTable": "${props.toTable}"`)
  }

  // console.log("fromRoute", fromRoute)
  // console.log("toRoute", toRoute);
  return Promise
         .all([ axios.get(fromRoute), axios.get(toRoute) ])
         .then(([fromName, toName]) => [fromName?.data[0], toName?.data[0]])
         .then(([fromName, toName]) => {
           // validate and assign names to our `refs`
           if ( fromName === undefined ) {
             throw new Error(`AssociationIndexView.getNames(): could not find name in table "${props.fromTable}" for "${props.fromIdUuid}"`);
           }
           if ( toName === undefined ) {
             throw new Error(`AssociationIndexView.getNames(): could not find name in table "${props.toTable}" for "${props.toIdUuid}"`);
           }
           from.value = { entryName: fromName
                        , idUuid: props.fromIdUuid
                        , table: props.fromTable };
           to.value   = { entryName: toName
                        , idUuid: props.toIdUuid
                        , table: props.toTable };
         })
}

/**
 * fetch the iconography ressources for this combined index.
 *
 * we're not running this query using i/search/iconography
 * (the advanced search module), although it could **almost**
 * work: in multi-valued fields, advanced search uses an `or`
 * for the different values: themeA OR themeB.
 * we, on the other hand, want themeA AND themeB.
 * it's quicker to create a nex function rather than to adapt
 * the search module.
 */
async function getData() {
  // build query params (if we don't trust `props.(from|to)Table`
  // and want to map the props tables to tablenames ourselves)
  // let fromKey, toKey;
  // switch ( props.fromTable ) {
  //   case "named_entity":
  //     fromKey = "named_entity";
  //     break;
  //   case "theme":
  //     fromKey = "theme";
  //     break;
  //   default:
  //     throw new Error(`AssociationIndexView.getData(): invalid table name in "props.fromTable": "${from.value.table}"`)
  // }
  // switch ( to.toTable ) {
  //   case "named_entity":
  //     toKey = "namedEntity";
  //     break;
  //   case "theme":
  //     toKey = "theme";
  //     break;
  //   default:
  //     throw new Error(`AssociationIndexView.getData(): invalid table name in "props.toTable": "${from.value.table}"`)
  // }

  // build params. we expect that `props.fromTable`
  // and `props.toTable` are valid table names.
  const params = { from_table  : props.fromTable,
                   to_table    : props.toTable,
                   from_id_uuid: props.fromIdUuid,
                   to_id_uuid  : props.toIdUuid };
  const tgt = new URL("/i/association/index", __API_URL__);

  // run the query and populate the `dataFull` and `dataFilter` refs
  return axios.get(tgt.href, { params:params })
         .then(r => r.data)
         .then(data => { dataFull.value   = data;
                         dataFilter.value = indexDataFormatterIconography(dataFull.value);
                         loaded.value     = true; });
         // TODO ERROR HANDLING?????
}

onMounted(() => {
  getNames().catch((e) => { error.value = true; console.error(e) });
  getData().catch((e) => { error.value = true; console.error(e) });
})
</script>


<style scoped>
.index-wrapper {
  min-height: 100%;
}
</style>