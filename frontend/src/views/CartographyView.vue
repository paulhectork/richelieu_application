<template>
  <WaitingToComeToLife></WaitingToComeToLife>
  <div class="cartography-wrapper">
    <div id="map-main"></div>
  </div>
</template>


<script setup>
import { onMounted, ref } from "vue";

import L from "leaflet";

import WaitingToComeToLife from "@components/WaitingToComeToLife.vue";
import { globalDefineMap } from "@utils/leafletUtils";

/************************************************************/

const map = ref();  // defined in onMounted

/************************************************************/

onMounted(() => {
  map.value = globalDefineMap("map-main");
  console.log(map.value);
})
</script>


<style scoped>
.cartography-viewer {
  height: calc(100vh - var(--cs-navbar-height));
  width: 100%;
}
#map-main {
  height: calc(100vh - var(--cs-navbar-height));
  width: 100%;
}
</style>