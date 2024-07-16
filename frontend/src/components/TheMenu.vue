<!-- TheMenu.vue
     the menu for the website.
 -->

<template>
  <div class="sidebar fill-parent">

    <ul class="sidebar-menu fill-parent border-bottom">
      <li><RouterLink to="/iconographie"
                      class="menu-text"
      >Iconographie</RouterLink></li>
      <li><RouterLink to="/sujet"
                      class="menu-text"
      >Sujets</RouterLink></li>
      <li><RouterLink to="/theme"
                      class="menu-text"
      >Thèmes</RouterLink></li>
      <li><RouterLink to="/recherche"
                      class="menu-text"
      >Recherche avancée</RouterLink></li>
      <li><RouterLink to="/lieu"
                      class="menu-text"
      >Lieux</RouterLink></li>
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
  position: absolute;
  top: var(--cs-navbar-height-mobile);
  height: calc(100vh - var(--cs-navbar-height-mobile));
  width: 100vw;

  display: grid;
  grid-template-rows: 60% 40%;
  z-index: 10;

  color: var(--cs-main-default);
  background-color: var(--cs-main-default-bg);
  border-left: var(--cs-border);
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
  overflow: hidden;
	display: flex;
	align-items: center;
  justify-content: center;
}
.sidebar-visual > img {
  /*max-width: 100%;*/
  min-width: 120%;
  object-fit: center;
}

@media ( orientation: landscape ) {
  .sidebar {
    height: calc(100vh - var(--cs-navbar-height-desktop));
    top: var(--cs-navbar-height-desktop);
  }
  .sidebar-menu > li > a {
    font-size: var(--cs-fontsize-menu-desktop);
  }
}
</style>
