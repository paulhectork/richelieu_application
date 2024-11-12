<!-- App.vue
    this component is the starting point for the app.
    it manages basic app-wide processes.

    3 importants actions happen here:
    - log the window orientation in `domStore` (landscape or portrait)
    - handling the showing/hiding of the menu (see below).
    - switching color theme between light/dark, based on the route's path
      (see `toThemeNegative` and `maybeChangeTheme`)

    interaction between App.vue, TheMenu.vue and TheNavbar.vue:
    how is the menu displayed ?
    - hiding/showing the menu is defined in `App.vue` and `TheNavbar.vue`.
    - App.vue contains a `menuActive` ref. if `true`, the menu is shown and
       the burger button in TheNavbar takes the shape of a cross. else,
       the menu is hidden and the burger is in its normal state.
    - App.vue listens to route changes. when the route changes, `menuActive`
       is set to close and TheMenu is hidden.
    - App.vue passes menuActive as a prop to TheNavbar.
    - TheNavbar determines the style of `#burger` (cross or burger) and
       the display of the menu when interacting with `#burger` based
       on menuActive. when `#burger` is clicked, TheNavbar emits an event
       (menu-active-update) to App.vue, and App.vue will switch the flag
       menuActive: if true-> false, if false -> true. this will toggle the
       visibility of the menu.
-->

<template>


  <div class="app-wrapper main-default">
    <!-- navbar -->
    <div class="navbar-outer-wrapper">
      <TheNavbar v-if="route.path !== '/'"
                 :menu-active="menuActive"
                 @menu-active-update="updateMenuActive"
      ></TheNavbar>
    </div>

    <!-- main + sidebar + footer -->
    <div class="content-wrapper fill-parent"
         :style="{ visibility: menuActive ? 'hidden' : 'visible'  }  /** avoid stuff from overlapping with the menu */"
    >
      <!-- main content: pages -->
      <div class="main-footer-wrapper">
        <main :class="themeNegative ? 'negative-default' : 'main-default'">
          <RouterView></RouterView>  <!-- display content that corresponds to a url targeted by `router-link` -->
        </main>
        <!-- footer -->
        <div class="footer-outer-wrapper">
          <TheFooter :gradient="themeNegative ? 'negative' : 'main'"></TheFooter>
        </div>
      </div>

      <!-- sidebar -->
      <div class="sidebar-outer-wrapper">
        <TheSidebar></TheSidebar>
      </div>
    </div>
  </div>

  <!-- full page menu -->
  <TheMenu v-if="menuActive"></TheMenu>
</template>


<script setup>
import { onMounted, onUnmounted, watch, ref } from "vue";
import { RouterView, useRoute } from 'vue-router';

import $ from "jquery";

import TheNavbar from '@components/TheNavbar.vue';
import TheMenu from "@components/TheMenu.vue";
import TheSidebar from "@components/TheSidebar.vue";
import TheFooter from "@components/TheFooter.vue";

import { domStore } from "@stores/dom.js";

/**********************************************************/

const route         = useRoute();
const menuActive    = ref(false);
const themeNegative = ref(false);

// if route.path matches anything in this regex, a negative color theme will be set.
const toThemeNegative = [ /^\/entite-nommee\/qr1/g
                        , /^\/entite-nommee\/[^\/]+\/qr1/g
                        , /^\/theme\/qr1/g
                        , /^\/theme\/[^\/]+\/qr1/g
                        , /^\/iconographie\/qr1/g
                        , /^\/institution\/qr1/g
                        , /^\/lieu\/qr1/g
                        ];

/**********************************************************/

// are we in `landscape` or `portrait` mode?
function calcWindowOrientation() {
  setTimeout(() => {
    const orientation = $(window).width() >= $(window).height()
                        ? "landscape"
                        : "portrait";
    domStore.setWindowOrientation(orientation);
  }, 1000)
}

/**
 * when changing page, close the menu
 */
const updateMenuActive = (newState) =>
  menuActive.value = newState;

/**
 * if `route.path` matches any of the regexes in `toThemeNegative`,
 * set `themeNegative` to `true`, which will change the page's color theme.
 */
const maybeChangeTheme = () =>
  themeNegative.value =
    toThemeNegative.find(rgx => route.path.match(rgx) ) !== undefined;


/**********************************************************/

/**
 * on page change,
 * - close the menu
 * - scroll `main` back to top of page
 * - set a negative theme if necessary
 */
watch(route, (newRoute, oldRoute) => {
  maybeChangeTheme();
  menuActive.value = false;
  $("main").scrollTop(0);
})

onMounted(() => {
  maybeChangeTheme();
  calcWindowOrientation();
  addEventListener("resize", calcWindowOrientation);
  // $(document).on("keyup", closeMenuOnEscape)
})

onUnmounted(() => {
  removeEventListener("resize", calcWindowOrientation);
  // $(document).off("keyUp", closeMenuOnEscape);
})
</script>


<style>
.app-wrapper {
  display: grid;
  grid-template-columns: 100%;
  grid-template-rows: var(--cs-navbar-height)
                      calc(100vh - var(--cs-navbar-height));
  margin: 0;
  padding: 0;
  /*
  height: 100vh;
  width: 100vw;
  overflow-x: hidden;
  overflow-y: auto;
  */
}

/****************************************/

.content-wrapper {
  /* the two lines below are important
     for the behaviour of the page when
     scrolling */
  /* fwig,
    - enabling `position: fixed` with overflow rules
      messes up the `vue-router`'s scrollBehavior()
      (exactly this problem :
      https://medium.com/@andrewmasonmedia/how-to-fix-scroll-to-top-scrollbehaviour-not-working-in-vue-router-b443c0fecf91)
    - diabling `position: fixed` and overflow rules
      fixes `scrollBehavior()` but generates CSS bugs:

      v lazy loading in IndexBase gets broken
      v TheSidebar: scrolling broken
      v the UiLoader on IconographyMain also goes byebye
      v loaders disappear on ArticleMainView's image part
      v ArticleMainView: the stickyness of the image part fails
      x the mobile navbar and sidebar are slightly laggy
      x there's a wee-bit of unintened horizontal scrolling
        in portrait displays.
   */
  /*
  position: fixed;
  overflow-y: scroll;
  overflow-x: hidden;
  margin-top: var(--cs-navbar-height);
  height: calc(100vh - var(--cs-navbar-height));
  max-width: 100vw;
  */

  /*
  on mobile, TheSidebar is on the bottom of the page
  with a height of var(--cs-sidebar-portrait-height).
  on desktop, it is on the side of the page width a
  width of 10%.
  */
  display: grid;
  grid-template-columns: 100%;
  grid-template-rows: calc(100% - var(--cs-sidebar-portrait-height)) var(--cs-sidebar-portrait-height);
}

@media ( orientation: landscape ) {
  .content-wrapper {
    grid-template-columns: calc(100% - var(--cs-sidebar-landscape-width)) var(--cs-sidebar-landscape-width);
    grid-template-rows: 100%;
  }
}
.sidebar-outer-wrapper {
  position: fixed;

  /** setting bottom and not top avoids empty space on top  */
  /*top: calc( 100vh - var(--cs-sidebar-portrait-height) );*/
  bottom: 0;
  left: 0;
  height: var(--cs-sidebar-portrait-height);
  width: 100vw;
  background-color: var(--cs-main-default-bg);
  border-right: var(--cs-main-border);
}

@media ( orientation:landscape ) {
  .sidebar-outer-wrapper {
    top: var(--cs-navbar-height);
    left: calc(100% - var(--cs-sidebar-landscape-width));
    height: calc(100vh - var(--cs-navbar-height));
    width: var(--cs-sidebar-landscape-width);
  }
}

.footer-outer-wrapper {
  height: max(40vh, 150px);  /* min 150px: the logo banner has a min height of 100px */
}
@media ( orientation:portrait ) {
  .footer-outer-wrapper {
    /* to make sure that it's not hidden by the sidebar */
    margin-bottom: var(--cs-sidebar-portrait-height);
  }
}

/** removing the `height: 100%` allows the scrollbar to be on the
    whole page, not just the `main`, but may break
    stuff. be careful ! */
main {
  /* height: 100%; */
  width: 100%;
  min-height: calc(100vh - var(--cs-navbar-height) - var(--cs-sidebar-portrait-height));
}
@media ( orientation:landscape ) {
  main {
    min-height: calc(100vh - var(--cs-navbar-height));
  }
}

/**************************************/


/** UNUSED ???????????????????????????????????? */
/* sidebar slide in/out animation
 * works with `opacity` but not with translateX
 */
/* stable state */
.sidebar-enter-to {
  transform: translateX(-60vw);
  /*opacity: 1;*/
}
/* transitions states */
.sidebar-enter-active
, .sidebar-leave-active {
  transition: transform 1s;/*all 0.8s cubic-bezier(1, 0.5, 0.8, 1);*/
}
/* start/end states */
.sidebar-enter-from
, .sidebar-leave-to {
  transform: translateX(0vw);
}
/* base/constant state */
.portrait .sidebar {
  transform: translateX(-60vw);
}
</style>

