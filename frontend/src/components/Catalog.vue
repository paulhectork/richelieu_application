<template>
  <div class="catalog-container">
    <CatalogItem v-for="d in data"
                 :item="d"
                 :display="display"
    ></CatalogItem>
  </div>
</template>

<script setup>
import { onMounted, watch } from "vue";

import CatalogItem from "@components/CatalogItem.vue";

const props = defineProps([ "display"  // which component to use for rendering a component: `resource` => `CatalogItem.vue`, `concept` => `CatalogItem.vue`
                          , "data" ])  // the data to display. [{ "href": <url to redirect to on click>, "img": <url to the background image>, "text": <text to display in the `CatalogItem`> }]

onMounted(() => {
  watch(props, (_old, _new) => {
    console.log(_old, _new.data[0].href);
  })

})
</script>

<style>
.catalog-container {
  width: 100%;
  display: grid;
  grid-auto-rows: 40vh;
  grid-template-columns: repeat(3, 33%);
  grid-gap: 5px;
}
</style>