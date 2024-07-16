<!-- TheVisualBar.vue

     a decorative bar that is on the side of the website
-->

<template>
  <div class="visual-bar-container">
    <img :src="menuCropPath">
  </div>
</template>


<script setup>
import $ from "jquery";

const menuCropPath = "../src/assets/media/menu_crop.jpg";

</script>


<style scoped>
.visual-bar-container {
  background-color: red;
  width: 100%;
  height: 100%;
  overflow: hidden;
}
img {
  object-fit: center;
  min-height: 100%;
  min-width: 100%;

}
</style>