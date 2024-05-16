<template>
  <div class="index-container">
    <IndexItem v-for="d in data"
               :item="d"
               :display="display"
    ></IndexItem>
  </div>
</template>

<script setup>
import { onMounted, watch } from "vue";

import IndexItem from "@components/IndexItem.vue";

const props = defineProps([ "display"  // which component to use for rendering a component: `resource` => `IndexItem.vue`, `concept` => `IndexItem.vue`
                          , "data" ])  // the data to display. [{ "href": <url to redirect to on click>, "img": <url to the background image>, "text": <text to display in the `IndexItem`> }]

onMounted(() => {
  watch(props, (_old, _new) => {
    console.log(_old, _new.data[0].href);
  })

})
</script>

<style>
.index-container {
  width: 100%;
  display: grid;
  grid-auto-rows: 40vh;
  grid-template-columns: repeat(3, 33%);
  /*grid-gap: 10px;*/
}
</style>