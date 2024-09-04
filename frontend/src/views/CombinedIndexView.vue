<!-- CombinedIndexView.vue
     an index combining two filters on the database:
     themeA + themeB, namedEntityA + namedEntityB...

     this combined index is accessed when clicking on
     the "Ressources associées" part
-->

<template>

</template>


<script setup>

const props = defineProps([ "toIdUuid", "fromIdUuid", "fromTable", "toTable" ]);

console.log(props.toIdUuid)
</script>


<style scoped>

</style>