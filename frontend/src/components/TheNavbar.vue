<template>
  <!-- TheNavbar.vue
      a navbar that is always displayed on top
      of the viewport.

      a burger menu is displayed to show/hide menu.
      how does it work ????? basically,
      - the parent App.vue defines a `menuActive`
        ref with a boolean value:
        - if `true`, the menu must be visible and the burger must
            take the shape of a cross
        - if `false`, the menu must be hidden and the burger in its
            original state (3 horizontal lines).
      - TheNavbar.vue is passed the prop `menuActive` from `App.vue`.
          when clicking on `#burger`, TheNavbar will emit to `App.vue`
          a signal (`menuActiveUpdate`): true if `menuActive===true`,
          false otherwise.
      - when `App.vue` receives `menuActiveUpdate`, it flips the value
          of `menuActive`, thus hiding the menu.
  -->

  <nav class="navbar border-bottom fill-parent">
    <h1 id="app-title"
    >
      <RouterLink to="/accueil"
                  @click="emit('menuActiveUpdate', false) /* close menu on click (if it's open) */"
      >
        <!-- the @ allows the logo to show in production build:
          https://stackoverflow.com/a/70813323/17915803 -->
        <img src="@/assets/icons/logo-text.svg"
             id="logo-richelieu"
             alt="logo du projet Richelieu"
        >
        <span style="visibility: hidden">Quartier Richelieu</span>
      </RouterLink>
    </h1>

    <div class="navbar-right-wrapper">
      <div class="nav-qsb-wrapper">
        <TheQuickSearchBar></TheQuickSearchBar>
      </div>
      <div class="burger-wrapper">
        <div id="burger"
             :class="props.menuActive ? 'burger-cross' : ''"
             @click="emit('menuActiveUpdate', !props.menuActive)"
             @touchend="emit('menuActiveUpdate', !props.menuActive)"
        >
          <span></span>
          <span></span>
          <span></span>
        </div>
      </div>
    </div>
  </nav>
</template>


<script setup>
import { RouterLink, RouterView } from 'vue-router';
import { onMounted, onUnmounted, computed, ref } from "vue";

import $ from "jquery";

import TheQuickSearchBar from "@components/TheQuickSearchBar.vue";

import { domStore } from "@stores/dom";
import { clickOrTouchEvent } from "@globals";
import { cleanClickOrTouchend } from "@utils/functions.js";

/**************************************************************/

const props = defineProps(["menuActive"]);
const emit = defineEmits(["menuActiveUpdate"])

/**************************************************************/

onMounted(() => {
  $("#burger").on(clickOrTouchEvent, (e) => {
    e = cleanClickOrTouchend(e);
  });
})
</script>


<style scoped>
.navbar {
  top: 0;
  left: 0;
  position: fixed;
  z-index: 2;
  height: var(--cs-navbar-height);
  width: 100vw;
  background-color: white;

  display: grid;
    grid-template-columns: 50% 50%;
  grid-template-rows: 100%;
  justify-items: start;
  align-items: center;

}
@media (orientation:landscape) {
  .navbar {
    display: grid;
    grid-template-columns: 1fr auto;
    grid-template-rows: 100%;
    justify-items: start;
    align-items: center;
  }
}

/*****************************/

h1 {
  margin: 0;
  padding: 0;
}
h1 > a {
  display: flex;
  align-items: center;
  justify-content: center;
}
#logo-richelieu {
  height: calc(var(--cs-navbar-height) - 10px);
  object-fit: contain;
  margin-left: 10px;
}

/*****************************/

.navbar-right-wrapper {
  height: 100%;
  height: calc(var(--cs-navbar-height) - 10px);
  width: 100%;
  display: flex;
  flex-direction: row;
  justify-content: flex-end;
}

.nav-qsb-wrapper {
  flex-grow: 2;
}
/*****************************/


.burger-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
}
#burger {
  width: calc(var(--cs-navbar-height) - 20px);
  height: calc(var(--cs-navbar-height) - 20px);
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
  width: 100%;
  background-color: var(--cs-duck);

  transition: max-width .5s
            , transform .5s
            , opacity .25s
            , background-color 0.5s;
}
#burger > span:nth-child(1) {
  transform-origin: top left;
}
#burger > span:nth-child(3) {
  transform-origin: bottom left;
}
#burger:hover > span {
  background-color: var(--cs-main-link-default);
}
.burger-cross > span {
  background-color: var(--cs-main-link-default) !important;
  max-width: 7.5vh;
}
.burger-cross > span:nth-child(2) {
  opacity: 0;
}
.burger-cross > span:nth-child(1) {
  transform: rotate(45deg);
  /*transform: translateY(500%) rotate(45deg);*/
}
.burger-cross > span:nth-child(3) {
  transform: rotate(-45deg);
  /*transform: translateY(-500%) rotate(-45deg);*/
}


/* styling of the title before using a logo
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
  font-size: min(50px, 2.5vh);  /* portrait size * /
  font-weight: 500;
}
#app-title:hover {
  color: var(--cs-main-link-default);
}

@media ( orientation: landscape ) {
	#app-title a {
	  font-size: 4vh;
	}
}
*/


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

