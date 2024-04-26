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
        <Transition name="sidebar">
          <Sidebar v-if="domStore.mobileSidebarActive || domStore.windowOrientation==='landscape'"/>
        </Transition>
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
               ? 'mobile-sidebar-active' : 'mobile-sidebar-hidden'
  };
  console.log(classes);
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
  grid-template-rows: var(--cs-navbar-height-mobile) calc(100vh - var(--cs-navbar-height-mobile));
  margin: 0;
  padding: 0;
  height: 100vh;
  width: 100vw;
  overflow: hidden;
}
.main-wrapper {
  display: grid;
  grid-template-rows: 100%;
  grid-template-columns: 100vw;
  margin-top: var(--cs-navbar-height-mobile);
}
.main-wrapper.mobile-sidebar-hidden {
  grid-template-columns: 100vw 0vw;
}
.main-wrapper.mobile-sidebar-active {
  grid-template-columns: 100vw 60vh;
}
@media ( orientation: landscape ) {
  .app-wrapper {
    grid-template-rows: var(--cs-navbar-height-desktop) calc(100vh - var(--cs-navbar-height-desktop));
  }
  .main-wrapper {
    grid-template-columns: 75% 25%;
    margin-top: var(--cs-navbar-height-desktop);
  }
  .main-wrapper.mobile-sidebar-hidden {
    grid-template-columns: 75% 25%;
  }
}

/* sidebar slide in/out animation */
/* stable state */
.sidebar-enter-to {
  transform: translateX(0vw);
}
/* transitions states */
.sidebar-enter-active
, .sidebar-leave-active {
  transition: translateX 0s;/*all 0.8s cubic-bezier(1, 0.5, 0.8, 1);*/
}
/* start / end states */
.sidebar-enter-from
, .sidebar-leave-to {
  transform: translateX(-60vw);
}
.portrait .sidebar {
  transform: translateX(-60vw);
}
</style>

