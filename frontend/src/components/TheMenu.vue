<!-- TheMenu.vue
     the menu for the website.
 -->

<template>
  <div class="menu-container fill-parent">

    <ul class="menu fill-parent border-bottom">
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

    <div class="menu-container-visual">
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
.menu-container {
  position: absolute;
  top: var(--cs-navbar-height);
  height: calc(100vh - var(--cs-navbar-height));
  width: 100vw;

  display: grid;
  grid-template-rows: 60% 40%;
  z-index: 10;

  color: var(--cs-main-default);
  background-color: var(--cs-main-default-bg);
  border-left: var(--cs-border);
}
.menu {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: center;
  padding: 0 2vw;
}
.menu > li {
  margin: 2.6vh 0;
  list-style: none;
  transition: background-color 0s;
}
.menu > li > a {
  color: var(--cs-main-second-bg);
  text-decoration: none;
  font-variant: small-caps;
  font-size: var(--cs-fontsize-menu-mobile);
}
li > a.selected {
  background-color: var(--cs-main-second-bg);
  color: var(--cs-main-second);
}
.menu-container-visual {
	margin: 0;
	padding: 0;
  overflow: hidden;
	display: flex;
	align-items: center;
  justify-content: center;
}
.menu-container-visual > img {
  /*max-width: 100%;*/
  min-width: 120%;
  object-fit: center;
}

@media ( orientation: landscape ) {
  .menu > li > a {
    font-size: var(--cs-fontsize-menu-desktop);
  }
}
</style>
