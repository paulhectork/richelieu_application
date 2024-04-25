<!-- Navbar.vue
     a navbar that is always displayed on top
     of the viewport.

    a burger menu is displayed to show/hide
    the navbar when :
    `@media ( min-width: 900px ) and ( orientation: landscape )`
-->

<template>
  <nav class="navbar border-bottom fill-parent">
    <h1 class="navbar-brand"
        id="app-title"
    >
      <RouterLink to="/">Richelieu. Histoire du quartier</RouterLink>
    </h1>

    <div id="burger"
    >
      <span></span>
      <span></span>
      <span></span>
    </div>
  </nav>
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router';
import { computed } from "vue";
import $ from "jquery";

//const displayBurger = computed(() => {
//  window.matchMedia( "@media ( min-width: 900px ) and ( orientation: landscape )")
//});
</script>

<style scoped>
.navbar {
  top: 0;
  z-index: 2;
  position: fixed;
  height: var(--cs-navbar-height-mobile);
  background-color: white;

  display: grid;
  flex-direction: row;
  grid-template-columns: 1fr auto;
  grid-template-rows: 100%;
  justify-items: start;
  align-items: center;
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
  color: var(--cs-link-default);
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

#burger {
  width: 10vw;
  height: 4.5vh;
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
  min-width: 4.5vw;
  width: 100%;
  background-color: var(--cs-main-default);
  transition: transform 1s, opacity 1.1s, background-color 0.5s;
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

