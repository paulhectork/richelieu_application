<!-- AssociationIndexView.vue

     an index combining two filters on the database:
     fromTable and toTable are two tables describing the iconography dataset
     (like places, named entities...). we build an index of
     all Iconography items that are tagged with fromTable.fromIdUuid
     and toTable.toIdUuid.

     currently only implemented for:
     - theme <-> theme
     - theme <-> named entity
     - place <-> place

     this association index is accessed when clicking on
     the "Ressources associées" part

     props:
     - fromTable  (string) : the name of the `from` table
     - fromIdUuid (string) : the `id_uuid` value of the `to` table
     - toTable    (string) : the name of the "to" table
    - toIdUuid    (string) : the `id_uuid` value of the `from` table

     WARNING: TABLE NAMES MUST BE WRITTED IN snake_case, LIKE IN THE DATABASE
-->

<template>
  <!-- display the combined index -->
  <div v-if="loadState === 'loading'">
    <UiLoader></UiLoader>
  </div>
  <div v-else-if="loadState === 'loaded'">
    <h1 v-if="Object.keys(from).length && Object.keys(to).length">
      {{ capitalizeFirstChar(from.entryName) }} <!--({{ from.table }})-->
      &amp;
      {{ capitalizeFirstChar(to.entryName) }} <!--({{ to.table }})-->
    </h1>

    <div class="index-wrapper">

      <p v-if="dataFull.length === 1">
        {{ dataFull.length }} ressource est associée à cette combinaison.</p>
      <p v-else-if="dataFull.length > 1">
        {{ dataFull.length }} ressources sont associées à cette combinaison.
      </p>
      <p v-else>Aucun résultat ne correspond à cette combinaison.</p>

      <p>Voir tous les résultats pour
        <RouterLink :to="toFrontendSlug(from)"
                    v-html="from.entryName"
        ></RouterLink>
        et
        <RouterLink :to="toFrontendSlug(to)"
                    v-html="to.entryName"
        ></RouterLink>.
      </p>

      <IndexBase :data="dataFilter"
                 display="resource"
      ></IndexBase>

    </div>
  </div>

  <!-- display an error message -->
  <div v-if="loadState === 'error'">
    <ErrNotFound></ErrNotFound>
  </div>

</template>


<script setup>
import { onMounted, ref } from "vue";

import axios from "axios";

import IndexBase from "@components/IndexBase.vue";
import ErrNotFound from "@components/ErrNotFound.vue";
import UiLoader from "@components/UiLoader.vue";

import { capitalizeFirstChar  } from "@utils/strings";
import { indexDataFormatterIconography } from "@utils/indexDataFormatter.js";

/***************************************/

const props = defineProps([ "toIdUuid", "fromIdUuid", "fromTable", "toTable" ]);

const from       = ref({});     // { entryName: "...", idUuid: "qr1...", table: "table name" }
const to         = ref({});     // { entryName: "...", idUuid: "qr1...", table: "table name" }
const dataFull   = ref([]);     // array of iconography objects (without filtering). populated in `getData`
const dataFilter = ref([]);     // array of iconography objects (with optional filtering)
const loadState  = ref("loading");  // "loading"/"loaded"/"error"

/***************************************/

/**
 * get an object with the structure of `from` or `to` and build a
 * slug to redirect to that resource's main page.
 */
const toFrontendSlug = (resource) => {
  let slug = "/";
  const implementedTables = [ "theme", "named_entity", "place" ];
  if ( implementedTables.includes(resource.table) ) {
    slug += resource.table === "named_entity"
            ? "entite-nommee"
            : resource.table === "place"
            ? "lieu"
            : "theme"
    slug += `/${resource.idUuid}`
    return slug
  } else {
    console.error(`AssociationIndexView.toFrontendSlug(): tableName must be one of ${implementedTables}, got ${tableName}.`)
    return
  }
}

/**
 * retrieve human redeable names for the ressources `toIdUuid` and `fromIdUuid`.
 * from those names and the props, build the `from` and `to` refs.
 */
async function getNames() {
  // select the proper backend route based on `fromTable` and `toTable`
  let fromRoute, toRoute;
  switch ( props.fromTable ) {
    case "place":
      fromRoute = new URL(`/i/place-address/${props.fromIdUuid}`, __API_URL__);
      break;
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
    case "place":
      toRoute = new URL(`/i/place-address/${props.toIdUuid}`, __API_URL__);
      break;
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
         .then(([fromName, toName]) => {
            // while `named-entity-name` and `theme-name` return an <Array<String>>,
            // `place-address` returns an <Array<Object>> and so we need to extract
            // the address string from that object.
            if (props.fromTable === "place" && props.toTable === "place") {
              return [fromName?.data[0].address, toName?.data[0].address]
            } else {
              return [fromName?.data[0], toName?.data[0]]
            }
         })
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
  // build params. we expect that `props.fromTable`
  // and `props.toTable` are valid table names.
  const params = { from_table  : props.fromTable,
                   to_table    : props.toTable,
                   from_id_uuid: props.fromIdUuid,
                   to_id_uuid  : props.toIdUuid };
  const tgt = new URL("/i/association/index", __API_URL__);

  // run the query and populate the `dataFull` and `dataFilter` refs
  return axios
         .get(tgt.href, { params:params })
         .then(r => r.data)
         .then(data => { dataFull.value   = data;
                         dataFilter.value = indexDataFormatterIconography(dataFull.value);
                         loadState.value  = "loaded"; })
         .catch(e => { loadState.value = "error"; console.error(e); });
         // TODO ERROR HANDLING?????
}

/***************************************/

onMounted(() => {
  getNames().catch((e) => { loadState.value = "error"; console.error(e) });
  getData().catch((e) => { loadState.value = "error"; console.error(e) });
})
</script>


<style scoped>
.index-wrapper {
  min-height: 100%;
}
</style>