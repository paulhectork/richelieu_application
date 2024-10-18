<!-- IndexAssociationRedirects.vue
     an html:p redirecting to other related ressources

     used in main pages that display an index of iconography resources
     (like ThemeMainVew, NamedEntityMainView...) to point to an array of
     related ressources (themes or named entites that are often tagged together
     with the current named entity, for example).

     this component is generic: in theory, it could describe relationships
     between any tableA and tableB. clicking on any item in `props.to` will
     redirect to a association index, displaying iconography resources tagged
     with both `props.from` and the current item in `props.to`, for example:
      * an index for iconography ressources tagged with
        theme:fiction + theme:édition, or theme).
      * an index for iconography ressources tagged with
        theme:fiction + named_entity:Robert Macaire

     props
     *****
     fromTable : the name of the table whose main page we're on: theme, for ex.

     toTable   : the name of the table we're building relationships to.
                 items displayed in IndexAssociationRedirects belong to `toTable`.

     from      : describes the ressource whose main page we're on
                 (ThemeMainView, NamedEntityMainView...). structure:

                 >>> { entry_name: <entry name of the ressource:string>,
                 ...   id_uuid   : <id uuid:string>
                 ... }

     to        : array of resources linked to `from` in another
                (or the same) database table. structure: an array of
                 items with pretty much the same structure as `from`:

                 >>> [ { entry_name: <entry name of the ressource:string>,
                 ...     id_uuid   : <id uuid:string>,
                 ...     count     : <number of relations between `from` and the current item in `to`>
                 ...   },
                 ...   ...
                 ... ]

     WARNING: TABLE NAMES MUST BE WRITTED IN snake_case, LIKE IN THE DATABASE
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
      ({{ t.count }} occurrence{{ t.count > 1 ? "s" : ""}})<span
        v-if="idx === props.to.length-2"> et </span>        <!-- `t` is the last el in `to` -->
      <span v-else-if="idx <= props.to.length-2">, </span>  <!-- `t` is any other element in `to` -->
      <span v-else>.</span>                                 <!-- end with `.` -->
    </span>
  </p>
</template>


<script setup>
import { onMounted, ref, computed } from "vue";

import { capitalizeFirstChar  } from "@utils/strings.js";

/*****************************************/

const props = defineProps([ "from", "to", "fromTable", "toTable" ]);

/*****************************************/

/**
 * return a string like:
 * "Thème associé", "Thèmes associés", "Entité nommée associée", "Entités nommées associées"
 * based on if a name is masc or fem and on of `to` is an array of 1 or more items.
 */
const introString = computed(() => {
  // { <tablename>: [ <human readable singular>, <human readable plural>, <"m"|"f": gender of the word> ] }
  const tableToNameMapper =
    { "theme"        : [ "thème", "thèmes", "m" ],
      "named_entity" : [ "entité nommée", "entités nommées", "f" ],
      "place"        : [ "lieu", "lieux", "m" ] };

  // exit if props.toTable doesn't allow us to build a string
  if ( !Object.keys(tableToNameMapper).includes(props.toTable) ) {
    console.error(`IndexAssociatedRessources.nameFromTable(): could not set gender or name for "props.toTable": "${props.toTable}"`);
    return "Ressource(s) associée(s)&nbsp;: ";
  }
  // else, build the intro string
  let s = props.to.length === 1
          ? capitalizeFirstChar( tableToNameMapper[props.toTable][0] )  // singular
          : capitalizeFirstChar( tableToNameMapper[props.toTable][1] ); // plural
  s += " ";
  s += props.to.length === 1 && tableToNameMapper[props.toTable][2] === "m"    // masc singular
       ? "associé"
       : props.to.length > 1 && tableToNameMapper[props.toTable][2] === "m"    // masc plural
       ? "associés"
       : props.to.length === 1 && tableToNameMapper[props.toTable][2] === "f"  // fem singular
       ? "associée"
       : "associées";                                                          // fem plural
  s += "&nbsp;: "
  return s
})

</script>


<style scoped>

</style>