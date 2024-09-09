<template>
  <div class="cartography-wrapper">
    <div id="map-main"></div>
  </div>
  <div class="warn-wrapper">
    <div class="warn">
      <p>Cette page est encore en développement</p>
    </div>
  </div>


</template>


<script setup>
import { onMounted, ref } from "vue";

import L from "leaflet";

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
.warn-wrapper {
  position: absolute;
  transform: translateY(-100%);
  height: 100%;
  width: 100%;
  z-index: 999;
  display: grid;
  align-items: center;
  justify-content: center;
}
.warn {
  opacity: 1;
  background-color: white;
  border: var(--cs-border);
}
.warn > p {
  margin: 30px;
}
</style>