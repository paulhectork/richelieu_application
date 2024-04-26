<!-- Navbar.vue
     a navbar that is always displayed on top
     of the viewport.

    a burger menu is displayed to show/hide
    the navbar when :
    `@media ( min-width: 900px ) and ( orientation: landscape )`
-->

<template>
  <nav class="navbar border-bottom fill-parent">
    <h1 class="navbar-brand"
        id="app-title"
    >
      <RouterLink to="/">Richelieu. Histoire du quartier</RouterLink>
    </h1>

    <div id="burger"
         v-if="domStore.windowOrientation!=='landscape'"
         @click="toggleSidebar"
    >
      <span></span>
      <span></span>
      <span></span>
    </div>
  </nav>
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router';
import { onMounted, onUnmounted, computed, ref } from "vue";
import $ from "jquery";

import { domStore } from "@stores/dom";


function toggleSidebar(e) {
  const $tgt = $(e.target);
  console.log("Navbar.toggleSidebar() : start -",
              domStore.mobileSidebarActive)
  // toggle HTML class
  domStore.mobileSidebarActive
  ? $tgt.removeClass("burger-cross")
  : $tgt.addClass("burger-cross");https://stackoverflow.com/questions/38644337/css-transition-not-working-with-transform-translate
  // toggle the sidebarActive state
  domStore.toggleMobileSidebar();
  console.log("Navbar.toggleSidebar() : end   -",
              domStore.mobileSidebarActive)

}


/**
 * set the visibility of the `#burger`.
const windowOrientation = ref("portrait");  // `portrait` or `landscape`
 */

/*
function setWindowOrientation() {
  windowOrientation.value = $(window).width() > $(window).height()
                            ? "landscape"
                            : "portrait";
}
function onResize() {
  setTimeout(setWindowOrientation, 500); /* triggered after .5s for performance * /
}
*/

/*
onMounted(() => {
  setWindowOrientation();
  addEventListener("resize", onResize);
});

onUnmounted(() => {
  removeEventListener("resize", onResize);
})
*/

//const displayBurger = computed(() => {
//  window.matchMedia( "@media ( min-width: 900px ) and ( orientation: landscape )")
//});
</script>

<style scoped>
.navbar {
  top: 0;
  z-index: 2;
  position: fixed;
  height: var(--cs-navbar-height-mobile);
  background-color: white;

  display: grid;
  flex-direction: row;
  grid-template-columns: 1fr auto;
  grid-template-rows: 100%;
  justify-items: start;
  align-items: center;
}
@media ( orientation: landscape ) {
  .navbar {
    height: var(--cs-navbar-height-desktop);
  }
}
#app-title a {
  margin: 0;
  padding: 0;
  font-size: max(3vh, 18px);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--cs-txt);
  text-decoration: none;
  text-transform: uppercase;
  font-size: min(50px, 2.5vh);  /* portrait size */
  font-weight: 500;
}
#app-title:hover {
  color: var(--cs-link-default);
}

@media ( orientation: landscape ) {
	#app-title a {
	  font-size: 4vh;
	}
}

#burger {
  width: max(5vw, 40px);
  height: 4vh;
  display: flex;
  margin-left: 3vw;
  flex-direction: column;
  justify-content: space-around;
  align-items: flex-end;
  margin-right: 1vw;
  cursor: pointer;
}
#burger > span {
  height: 0.3vh;
  min-height: 2px;
  min-width: 4.5vw;
  width: 100%;
  background-color: var(--cs-duck);
  transition: max-width .5s
            , transform .5s
            , opacity .25s
            , background-color 0.5s;
}
#burger:hover > span {
  background-color: var(--cs-link-default);
}
.burger-cross > span {
  background-color: var(--cs-link-default) !important;
  max-width: 7.5vh;
}
.burger-cross > span:nth-child(2) {
  opacity: 0;
}
.burger-cross > span:nth-child(1) {
  transform: translateY(450%) rotate(45deg);
}
.burger-cross > span:nth-child(3) {
  transform: translateY(-1.3vh) rotate(-45deg);
  transform: translateY(-450%) rotate(-45deg);
}




/*
.navbar {
  width: 95%;
  height: 95%;
  display: grid;
  grid-template-rows: 100%;
  grid-template-columns: 30% 70%;

}
*/
/*
.navbar-links {
  display: flex;
  flex-direction: row;
  align-items: center;
}
.navbar-links > * {
  margin: 0vw 1vw;
}
*/
</style>

