<template>
  <div class="app-wrapper main-default">
    <!-- navbar -->
    <Navbar/>
    <div class="main-wrapper fill-parent"
         :class="setMainWrapperClasses()">
      <!-- main content: pages -->
      <main>
        <RouterView/>  <!-- display content that corresponds to a url targeted by `router-link` -->
      </main>
      <!-- sidebar -->
      <div>
        <!--<Transition name="sidebar">-->
          <Sidebar v-if="domStore.mobileSidebarActive || domStore.windowOrientation==='landscape'"/>
        <!--</Transition>-->
      </div>
    </div>
  </div>
</template>


<script setup>
import { onMounted, onUnmounted } from "vue";
import { RouterView } from 'vue-router';
import $ from "jquery";

import { domStore } from "@stores/dom.js";
import Navbar from '@components/Navbar.vue';
import Sidebar from "@components/Sidebar.vue";

function setMainWrapperClasses() {
  let classes = `${domStore.windowOrientation} `;
  if ( domStore.windowOrientation!== 'landscape' ) {
    classes += domStore.mobileSidebarActive
               ? 'portrait-sidebar-active' : 'portrait-sidebar-hidden'
  };
  // console.log("App.setMainWrapperClasses() : end -", classes);
  return classes;
}

function calcWindowOrientation() {
  setTimeout(() => {
    const orientation = $(window).width() >= $(window).height()
                        ? "landscape"
                        : "portrait";
    domStore.setWindowOrientation(orientation);
  }, 1000)
}


onMounted(() => {
  calcWindowOrientation();
  addEventListener("resize", calcWindowOrientation);
})

onUnmounted(() => {
  removeEventListener("resize", calcWindowOrientation);
})
</script>


<style>
.app-wrapper {
  display: grid;
  grid-template-columns: 100%;
  grid-template-rows: var(--cs-navbar-height-mobile)
                      calc(100vh - var(--cs-navbar-height-mobile));
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

  display: grid;
  grid-template-rows: 100%;
  margin-top: var(--cs-navbar-height-mobile);
  height: calc(100vh - var(--cs-navbar-height-mobile));
}

.main-wrapper.portrait-sidebar-hidden {
  grid-template-columns: 100vw 0vw;
}
.main-wrapper.portrait-sidebar-active {
  grid-template-columns: 100vw var(--cs-sidebar-width-mobile);
  width: 100vw;

}

@media ( orientation: landscape ) {
  .app-wrapper {
    grid-template-rows: var(--cs-navbar-height-desktop)
                        calc(100vh - var(--cs-navbar-height-desktop));
  }
  .main-wrapper {
    margin-top: var(--cs-navbar-height-desktop);
    height: calc(100vh - var(--cs-navbar-height-desktop));
    grid-template-columns: calc(100vw - var(--cs-sidebar-width-desktop))
                           var(--cs-sidebar-width-desktop);
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

