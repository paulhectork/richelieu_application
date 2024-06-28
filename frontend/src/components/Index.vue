<template>
  <div class="index-container animate__animated animate__slideInLeft">
    <IndexItem v-for="d in data"
               :item="d"
               :display="display"
    ></IndexItem>
  </div>
</template>

<script setup>
import { onMounted } from "vue";

import IndexItem from "@components/IndexItem.vue";

const props = defineProps([ "display"  // which component to use for rendering a component: `resource` => `IndexItem.vue`, `concept` => `IndexItem.vue`
                          , "data" ])  // the data to display. [{ "href": <url to redirect to on click>, "img": <url to the background image>, "text": <text to display in the `IndexItem`> }]
</script>

<style>
.index-container {
  width: 100%;
  display: grid;
  grid-auto-rows: 40vh;
  grid-template-columns: repeat(3, 33%);
}
</style>