<!-- TheMenu.vue
     the menu for the website.
 -->

<template>
  <div class="menu-wrapper fill-parent negative-default">

    <ul class="menu fill-parent border-bottom list-invisible"
    >
      <li>
        <div class="menu-category has-subcategories"
             id="menu-block-parcourir"
        >
          <h1>Parcourir</h1>
          <ul class="menu-subcategories list-invisible">
            <li class="main-default">
              <RouterLink to="/iconographie"
                          class="menu-text"
              >Iconographie</RouterLink></li>
            <li class="main-default">
              <RouterLink to="/entite-nommee"
                          class="menu-text"
              >Entités nommées</RouterLink>
            </li>
            <li class="main-default">
              <RouterLink to="/theme"
                          class="menu-text"
              >Thèmes</RouterLink>
            </li>
            <li class="main-default">
              <RouterLink to="/lieu"
                          class="menu-text"
              >Lieux</RouterLink>
            </li>
            <li class="main-default">
              <RouterLink to="/institution"
                          class="menu-text"
              >Institutions</RouterLink>
            </li>
          </ul>
        </div>
      </li>

      <li>
        <div class="menu-category">
          <RouterLink to="/cartographie"
                          class="menu-text"
          ><h1>Cartographie</h1></RouterLink>
        </div>
      </li>

      <li>
        <div class="menu-category">
          <RouterLink to="/recherche"
                          class="menu-text"
          ><h1>Recherche avancée</h1></RouterLink>
        </div>
      </li>

      <li>
        <div class="menu-category">
          <RouterLink to="/article"
                          class="menu-text"
          ><h1>Articles</h1></RouterLink>
        </div>
      </li>

      <li>
        <div class="menu-category has-subcategories">
          <h1>Documentation technique</h1>
          <ul class="menu-subcategories list-invisible">
            <li class="main-default">
              <RouterLink to="/documentation/methodologie"
                          class="menu-text"
              >Méthodologie du projet</RouterLink>
            </li>
            <li class="main-default">
              <RouterLink to="/documentation/api"
                          class="menu-text"
              >API</RouterLink>
            </li>
          </ul>
        </div>
      </li>

      <li>
        <div class="menu-category has-subcategories">
          <h1>À propos</h1>
          <ul class="menu-subcategories list-invisible">
            <li class="main-default">
              <RouterLink to="/a-propos/projet"
                          class="menu-text"
              >Le projet</RouterLink>
            </li>
            <li class="main-default">
              <RouterLink to="/a-propos/equipe"
                          class="menu-text"
              >L'équipe</RouterLink>
            </li>
            <li class="main-default">
              <RouterLink to="/a-propos/mentions"
                          class="menu-text"
              >Crédits et mentions légales</RouterLink>
            </li>
          </ul>
        </div>
      </li>

    </ul>
  </div>
</template>


<script setup>
import { onMounted, ref } from "vue";
import { RouterLink, RouterView } from "vue-router";
import { domStore } from "@stores/dom";

import $ from "jquery";
import _ from "lodash";

import { randomColorDark, randomColorLight } from "@utils/colors";

/**************************************************/

onMounted(() => {
  // on hover, color the different clickable elements

  $(".menu-subcategories > li")
  .on("mouseenter", (e) =>
    $(e.currentTarget).css({ backgroundColor: randomColorLight() })
  )
  .on("mouseleave", (e) =>
    $(e.currentTarget).css({ backgroundColor: "var(--cs-main-default-bg)" }) );

  $(".menu-category:not(.has-subcategories)")
  .on("mouseenter", (e) =>
    $(e.currentTarget).css({ backgroundColor: randomColorDark() })
  )
  .on("mouseleave", (e) =>
    $(e.currentTarget).css({ backgroundColor: "var(--cs-negative-default-bg)" }) );
})
</script>


<style scoped>
h1 {
  font-family: var(--cs-font-sans-serif-accentuate);
  color: var(--cs-negative-default);
  margin: 0;
  font-size: 20px;
}
@media ( orientation: landscape ) {
  h1 {
    font-size: 30px;
  }
}
a {
  background-color: transparent;
  text-decoration: none;
  color: var(--cs-negative-default);
}

/**************************************/

/**
 * how is the menu styled ?
 * basically, the menu is a grid of 2col x 3rows
 * on landscapes and 1col x 6rows on portraits.
 *
 * the menu is meant to be fully visible on all viewports,
 * but if we're on a weird viewport (ex: small or
 * landscape-oriented mobile phone), we'll set a minumum
 * block height for all menu items and make the menu scrollable
 * (else, we'd have to set up tons of weird and unmaintainable
 * @media rules).
 *
 * for each list item (`.menu > li`), we set, using
 * `grid-template-rows`, a minimum height is set using `max`.
 *
 * on `.menu-category:not(.has-subcategories)` blocks, the whole
 * block can be clicked to redirect to another page.
 * on `.menu-category.has-subcategories`, only the elements in
 * `.menu-subcategories` can be clicked to redirect.
 */

.menu-wrapper {
  position: fixed;
  top: var(--cs-navbar-height);
  height: calc(100vh - var(--cs-navbar-height));
  width: 100vw;

  display: flex;
  align-items: center;
  justify-content: center;

  border-left: var(--cs-main-border);
  z-index: 2;
}
.menu {
  display: grid;
  grid-template-columns: 100%;
  grid-template-rows: repeat(6, max( 140px, calc(100%/6) ));  /* max/calc allows a min-height of N px for all li elements */
  overflow: scroll;

  height: 100%;
  margin: 0;
  padding: 3vh 3vw;
  max-width: none;
}
@media ( orientation:landscape ) {
  .menu {
    grid-template-columns: 50% 50%;
    grid-template-rows: repeat(3, max( 200px, calc(100%/3) ));    /* max/calc allows a min-height of 150px for all li elements */
  }
}

/****************************************/

.menu > li {
  transition: background-color 0s;
  border: var(--cs-main-border);
  border-color: var(--cs-negative-default);
}
.menu-category {
  width: 100%;
  height: 100%;
}
.menu-category.has-subcategories {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}
.menu-category:not(.has-subcategories) > a > h1 {
  width: 100%;
  height: 100%;
}
.menu-category h1, .menu-category ul {
  padding: 1% 2%;
}
.menu-category:not(.has-subcategories)
, .menu-subcategories > li {
  transition: background-color var(--cs-color-transition);
}

/****************************************/

.menu-subcategories {
  width: 100%;
  display: flex;
  flex-direction: row;
  justify-content: space-around;
  margin-bottom: 3px;
}
.menu-subcategories > li {
  margin: 5px 3px;
  display: flex;
  align-items: stretch;
  width: 100%;
}
.menu-subcategories a {
  color: var(--cs-main-default);
  width: 100%;
  height: 100%;
  min-height: 30px;
  padding: 3px 0;
  text-align: center;
  display: flex;
  align-items: center;
  justify-content: center;
}
@media (orientation:landscape) {
  .menu-subcategories {
    display: block;  /* remove display flex */
  }
  .menu-subcategories > li {
    margin: 5px 0;
  }
  .menu-subcategories a {
    text-align: justify;
    display: block;
  }
}
/** portrait is a pain to style, especially the first block */
@media ( orientation:portrait ) {
  .menu-subcategories > li {
    font-size: 80%;
  }
  #menu-block-parcourir > .menu-subcategories {
    display: grid;
    grid-template-columns: repeat(3,33.33%);
    grid-template-rows: 50% 50%;
    grid-gap: 5px;
  }
  #menu-block-parcourir > .menu-subcategories > li {
    transform: translateY(-20%);
    height: 100%;
    width: 97%;
  }
}


</style>
