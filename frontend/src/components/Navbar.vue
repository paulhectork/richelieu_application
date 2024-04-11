<template>
  <nav class="navbar border-bottom fill-parent">
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
  top: 0;
  z-index: 2;
  position: fixed;
  height: var(--cs-navbar-height-mobile);
  background-color: white;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: left;
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
  color: var(--cs-link);
}

@media ( orientation: landscape ) and ( max-width: 900px ) {
	#app-title a {
	  font-size: 4.5vh;
	}
}

@media ( orientation: landscape ) and ( min-width: 900px ) {
  #app-title a {
    font-size: 4vh;
  }
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

