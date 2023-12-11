<script setup>
import { RouterView } from 'vue-router'
import Navbar from './components/Navbar.vue'
import Sidebar from "./components/Sidebar.vue"
</script>

<template>
  <div class="app-container">
    <!-- navbar -->
    <Navbar/>

    <!-- main content: pages + sidebar -->
    <main>
      <Sidebar/>
      <RouterView/>  <!-- display content that corresponds to a url targeted by `router-link` -->
    </main>
  </div>
</template>

<style>
.app-container {
  display: grid;
  grid-template-columns: 100%;
  grid-template-rows: 8vh 92vh;
  margin: 0;
  padding: 0;
}
</style>

