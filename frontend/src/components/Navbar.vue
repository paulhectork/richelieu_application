<template>
  <nav class="navbar border-bottom fill-parent sticky-top">
    <h1 class="navbar-brand"
        id="app-title"
    >
      <RouterLink to="/">Richelieu. Histoire du quartier</RouterLink>
    </h1>
  </nav>
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<style scoped>
.navbar {
  z-index: 2;
  background-color: white;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: left;
}
h1 {
  margin: 0;
  padding: 0;
  font-size: max(3vh, 18px);
  display: flex;
  align-items: center;
  justify-content: center;
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

