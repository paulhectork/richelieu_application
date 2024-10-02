<!-- App.vue
     this component is the starting point for the app.
     it manages basic app-wide processes.

     2 importants actions happen here:
     - log the window orientation in `domStore` (landscape or portrait)
     - handling the showing/hiding of the menu (see below).

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
    <TheNavbar :menu-active="menuActive"
               @menu-active-update="updateMenuActive"
    ></TheNavbar>

    <!-- content + navbar -->
    <div class="main-wrapper fill-parent">
      <!-- main content: pages -->
      <main>
        <RouterView></RouterView>  <!-- display content that corresponds to a url targeted by `router-link` -->
      </main>
      <!-- sidebar -->
      <TheSidebar></TheSidebar>
    </div>
  </div>

  <!-- full page menu -->
  <TheMenu v-if="menuActive"></TheMenu>
</template>


<script setup>
import { onMounted, onUnmounted, watch, ref } from "vue";
import { RouterView, useRoute, useRouter } from 'vue-router';

import $ from "jquery";

import { domStore } from "@stores/dom.js";
import TheNavbar from '@components/TheNavbar.vue';
import TheMenu from "@components/TheMenu.vue";
import TheSidebar from "@components/TheSidebar.vue";

/**********************************************************/

const route = useRoute();
const menuActive = ref(false);

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

function updateMenuActive(newState) {
  menuActive.value = newState;
}

// doesn't work: the event is fired multiple times and so the menu is
// closed and reopened instantly.
// function closeMenuOnEscape(e) {
//   if ( menuActive.value === true && e.key === "Enter" ) {
//     menuActive.value = !menuActive.value;
//     console.log(e, e.key, menuActive.value);
//   }
// }

/**********************************************************/

// on page change, close the menu + scroll `main` back to top of page
watch(route, (newRoute, oldRoute) => {
  menuActive.value = false;
  $("main").scrollTop(0);
})

onMounted(() => {
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
  height: 100vh;
  width: 100vw;
}
.main-wrapper {
  /* the two lines below are important
     for the behaviour of the page when
     scrolling */
  position: fixed;
  overflow-y: scroll;
  overflow-x: hidden;

  /* on mobile, TheSidebar is on the bottom of the page
     with a height of 15vh; on desktop, it is on the side
     of the page width a width of 10vw.
   */
  display: grid;
  grid-template-columns: 100%;
  grid-template-rows: 85% 15%;

  margin-top: var(--cs-navbar-height);
  height: calc(100vh - var(--cs-navbar-height));
}
main {
  height: 100%;
  width: 100%;
  overflow: scroll;
}

@media ( orientation: landscape ) {
  .main-wrapper {
    grid-template-columns: 90% 10%;
    grid-template-rows: 100%;
  }
}


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

