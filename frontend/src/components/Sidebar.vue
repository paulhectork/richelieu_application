<!-- Sidebar.vue
     the sidebar displayed on the website.
     hidden by default on mobile versions,
     when:

    `@media ( min-width: 900px ) and ( orientation: landscape )`
 -->

<template>
  <div class="sidebar fill-parent">

    <!-- button to hide the sidebar
    <div class="fill-parent border-bottom sidebar-masquer">
      <button @click="domStore.toggleSidebar"
      >Masquer</button>
    </div>
    -->

    <ul class="sidebar-menu fill-parent border-bottom">
      <li><RouterLink to="/iconographie"
                      class="menu-text"
      >Iconographie</RouterLink></li>
      <li><RouterLink to="/cartographie"
                      class="menu-text"
      >Cartographie</RouterLink></li>
      <li><RouterLink to="/table-viewer"
                      class="menu-text"
      >Voir les tables</RouterLink></li>
    </ul>

    <div class="sidebar-visual">
      <img :src="menuCropPath">
    </div>

  </div>
</template>


<script setup>
import { RouterLink, RouterView } from "vue-router";
import { domStore } from "@stores/dom";

const menuCropPath = "../src/assets/media/menu_crop.jpg";
</script>


<style scoped>
.sidebar {
  position: fixed;
  height: calc(100vh - var(--cs-navbar-height-mobile));
  display: grid;
  /* with a button to hide sidebar
  grid-template-rows: 5% 55% 40%;
  */
  grid-template-rows: 60% 40%;
  border-left: var(--cs-border);
}
.sidebar-masquer {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: start;
}
.sidebar-masquer > button {
  margin: 0;
  height: 100%;
  border: unset;
  border-right: var(--cs-border);
}
.sidebar-menu {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: center;
  padding: 0 2vw;
}
.sidebar-menu > li {
  margin: 2.6vh 0;
  list-style: none;
  transition: background-color 0s;
}
.sidebar-menu > li > a {
  color: var(--cs-main-second-bg);
  text-decoration: none;
  font-variant: small-caps;
  font-size: var(--cs-fontsize-menu-mobile);
}
li > a.selected {
  background-color: var(--cs-main-second-bg);
  color: var(--cs-main-second);
}
.sidebar-visual {
	margin: 0;
	padding: 0;
  width: 25%;
	overflow: hidden;
	display: flex;
	align-items: center;
  justify-content: center;
}
.sidebar-visual > img {
  width: 120%;
}

@media ( orientation: landscape ) {
  .sidebar {
    height: calc(100vh - var(--cs-navbar-height-desktop));
  }
}
</style>
