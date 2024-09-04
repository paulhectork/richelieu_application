<!--
     used at the top of an index, to display the themes/named entites/etc
     which are the most often associated to a certain theme/named entity/etc.
-->


<template>
  <p>
    <span v-html=introString></span>
    <span v-for="(t, idx) in props.to">
      <RouterLink :to="{ path:'/index-combine'
                       , query:{ toIdUuid: t.id_uuid,
                                 fromIdUuid: props.from.id_uuid,
                                 from: props.fromTable,
                                 to: props.toTable } }">
        {{ t.entry_name }}
      </RouterLink>
      <span v-if="idx === props.to.length-2"> et </span>    <!-- `t` is the last el in `to` -->
      <span v-else-if="idx <= props.to.length-2">, </span>  <!-- `t` is any other element in `to` -->
      <span v-else>.</span>                                 <!-- end with `.` -->
    </span>
  </p>
</template>


<script setup>
import { onMounted, ref, computed } from "vue";

import { capitalizeString } from "@utils/stringifiers";

/*****************************************/

const props = defineProps([ "from", "to", "fromTable", "toTable" ]);

/*****************************************/

/**
 * return a string like:
 * "Thème associé", "Thèmes associés", "Entité nommée associée", "Entités nommées associées"
 * based on if a name is masc or fem and on of `to` is an array of 1 or more items.
 */
const introString = computed(() => {
  // { <tablename>: [ <human readable singular>, <human readable plural> ] }
  const tableToNameMapper = { "theme"       : [ "thème", "thèmes" ],
                              "namedEntity" : [ "entité nommée", "entités nommées" ] };
  const masc = ["theme"];        // table names which are associated to a masculine word
  const fem  = ["named_entity"];  // those associated to a feminine word

  // exit if props.toTable doesn't allow us to build a string
  if ( !Object.keys(tableToNameMapper).includes(props.toTable)
     || (!masc.includes(props.toTable) && !fem.includes(props.toTable))
  ) {
    console.error(`IndexAssociatedRessources.nameFromTable(): could not set gender or name for "props.toTable": "${props.toTable}"`);
    return "Ressource(s) associée(s)";
  }
  // else, build the intro string
  let s = props.to.length === 1
          ? capitalizeString( tableToNameMapper[props.toTable][0] )  // singular
          : capitalizeString( tableToNameMapper[props.toTable][1] ); // plural
  s += " ";
  s += props.to.length === 1 && masc.includes(props.toTable)         // masc singular
       ? "associé"
       : props.to.length > 1 && masc.includes(props.toTable)         // masc plural
       ? "associés"
       : props.to.length === 1 && fem.includes(props.toTable)        // fem singular
       ? "associée"
       : "associées";                                                // fem plural
  s += "&nbsp;: "
  return s
})

</script>


<style scoped>

</style>