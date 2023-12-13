<template>
  <div class="sidebar fill-parent sticky-top">
    <ul class="sidebar-menu fill-parent">
      <li><RouterLink to="/iconographie"
                      class="menu-text"
      >Iconographie</RouterLink></li>
      <li><RouterLink to="/cartographie"
                      class="menu-text"
      >Cartographie</RouterLink></li>
    </ul>
    <div class="sidebar-visual">
      <img :src="menuCropPath">
    </div>
  </div>
</template>

<script setup>
import $ from "jquery";
import { onMounted } from 'vue';
import { RouterLink, RouterView } from 'vue-router'

const menuCropPath = "../src/assets/media/menu_crop.jpg"

onMounted(() => {});
</script>

<style scoped>
.sidebar {
  max-height: 100vh;
  display: grid;
  grid-template-rows: 60% 40%;
  border-left: var(--cs-border);
  top: var(--cs-navbar-height-mobile);
}
@media ( orientation: landscape ) {
  .sidebar {
    top: var(--cs-navbar-height-desktop);
  }
}
.sidebar-menu {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: center;
  border-bottom: var(--cs-border);
  padding: 0 2vw;
}
.sidebar-menu > li {
  margin: 2.6vh 0;
  list-style: none;
  transition: background-color 0s;
}
.sidebar-menu > li > a {
  color: var(--cs-bg-focus);
  text-decoration: none;
  font-variant: small-caps;
  font-size: var(--cs-fontsize-menu-mobile);
}
li > a.selected {
  background-color: var(--cs-bg-focus);
  color: var(--cs-focus);
}
.sidebar-menu
.sidebar-visual {
	margin: 0;
	padding: 0;
	overflow: hidden;
	display: flex;
	flex-direction: center;
	align-items: center;
}
.sidebar-visual img {
  width: 120%;
}

</style>
