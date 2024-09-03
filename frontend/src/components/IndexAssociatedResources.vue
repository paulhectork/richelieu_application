<!--
     used at the top of an index, to display the themes/named entites/etc
     which are the most often associated to a certain theme/named entity/etc.
-->


<template>
  <p><span v-html=introString></span></p>

</template>


<script setup>
import { onMounted, ref, computed } from "vue";

import { capitalizeString } from "@utils/stringifiers";

/*****************************************/

// from      : { <id_uuid>: <human-readable-value> }
// to        : [ { <id_uuid>: <human-readable-value> } ]  (array with the same structure as `from`)
// fromTable : table name of the "from" resource
// toTable   : table name of the "to" resources
const props = defineProps([ "from", "to", "fromTable", "toTable" ])

// { <tablename>: [ <human readable singular>, <human readable plural> ] }
const tableToNameMapper = { "theme"       : [ "thème", "thèmes" ]
                          , "namedEntity" : [ "entité nommée", "entités nommées" ]
                          }

console.log(props.toTable, props.to);

/*****************************************/

/**
 * return a string like:
 * "Thème associé", "Thèmes associés", "Entité nommée associée", "Entités nommées associées"
 * based on if a name is singular or plural, masc or fem.
 */
const introString = computed(() => {
  const masc = ["theme"]        // table names which are associated to a masculine word
  const fem  = ["named_entity"]  // those associated to a feminine word

  // exit if props.toTable doesn't allow us to build a string
  if ( !Object.keys(tableToNameMapper).includes(props.toTable)
     || (!masc.includes(props.toTable) && !fem.includes(props.toTable)) ) {
    console.error(`IndexAssociatedRessources.nameFromTable(): could not set gender or name for "props.toTable": "${props.toTable}"`)
    return "Ressource(s) associée(s)"
  }
  // else, build the intro string
  let s = props.to.length === 1
          ? capitalizeString( tableToNameMapper[props.toTable][0] )  // singular
          : capitalizeString( tableToNameMapper[props.toTable][1] )  // plural
  s += " "
  s += props.to.length === 1 && masc.includes(props.toTable)         // masc singular
       ? "associé"
       : props.to.length > 1 && masc.includes(props.toTable)         // masc plural
       ? "associés"
       : props.to.length === 1 && fem.includes(props.toTable)        // fem singular
       ? "associée"
       : "associées"                                                 // fem plural

  s += "&nbsp;:"
  return s
})

</script>


<style scoped>

</style>