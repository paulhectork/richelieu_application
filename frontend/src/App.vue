<template>
  <div class="app-wrapper">
    <!-- navbar -->
    <Navbar/>
    <div class="main-wrapper fill-parent"
         :class="domStore.sidebarHidden ? 'sidebar-hidden' : 'sidebar-visible'">
      <!-- main content: pages -->
      <main>
        <RouterView/>  <!-- display content that corresponds to a url targeted by `router-link` -->
      </main>
      <!-- sidebar -->
      <div>
        <Sidebar />
      </div>
    </div>
  </div>
</template>


<script setup>
import { RouterView } from 'vue-router';
import { domStore } from "@stores/dom.js";
import Navbar from '@components/Navbar.vue';
import Sidebar from "@components/Sidebar.vue";
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
}
.main-wrapper {
  display: grid;
  grid-template-rows: 100%;
  grid-template-columns: 100%;
  top: var(--cs-navbar-height-mobile);
}
.main-wrapper.sidebar-hidden {
  grid-template-columns: 100% 0%;
}
@media ( orientation: landscape ) {
  .app-wrapper {
    grid-template-rows: var(--cs-navbar-height-desktop) calc(100vh - var(--cs-navbar-height-desktop));
  }
  .main-wrapper {
    display: grid;
    grid-template-rows: 100%;
    grid-template-columns: 75% 25%;
    margin-top: var(--cs-navbar-height-desktop);
  }
  .main-wrapper.sidebar-hidden {
    grid-template-columns: 100% 0%;
  }
}
</style>

