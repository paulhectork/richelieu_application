<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <div class="navbar-container">
    <nav class="navbar">
      <h1 class="navbar-brand"
          id="app-title"
      >
        <RouterLink to="/">Richelieu. Histoire du quartier</RouterLink>
      </h1>
      <div class="navbar-links">
        <RouterLink to="/iconographie">Iconographie</RouterLink>
        <RouterLink to="/cartographie">Cartographie</RouterLink>
      </div>
    </nav>
  </div>
</template>

<style scoped>
.navbar-container {
  width: 100%;
  height: 100%;
  border-bottom: 1px solid;
  display: flex;
  align-items: center;
  justify-content: center;
}
.navbar {
  width: 95%;
  height: 95%;
  display: grid;
  grid-template-rows: 100%;
  grid-template-columns: 30% 70%;
}
.navbar-links {
  display: flex;
  flex-direction: row;
  align-items: center;
}
.navbar-links > * {
  margin: 0vw 1vw;
}
h1 {
  margin: 0;
  padding: 0;
  font-size: max(3vh, 18px);
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>

