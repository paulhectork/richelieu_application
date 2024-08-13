<!-- NotFoundView.vue

     a view displayed when a route is not registered / a page
     does not exist. also implemented as a non-view component
     to use when a route exists, but is parameters are invalid
     (for example, in @views/IconographyMainView, when an UUID
     is invalid/points to nothing in the database).
-->

<template>
  <NotFound></NotFound>
</template>

<script setup>
import NotFound from "@components/NotFound.vue";
</script>

<style scoped>
</style>