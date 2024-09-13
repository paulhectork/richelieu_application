<!-- TheMenu.vue
     the menu for the website.
 -->

<template>
  <div class="menu-container fill-parent negative-default">

    <ul class="menu fill-parent border-bottom list-invisible">
      <li>
        <div class="menu-category has-subcategories">
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
          </ul>
        </div>
      </li>

    </ul>
    <!--
    <div class="menu-container-visual">
      <img :src="menuCropPath">
    </div>
    -->
  </div>
</template>


<script setup>
import { onMounted, ref } from "vue";
import { RouterLink, RouterView } from "vue-router";
import { domStore } from "@stores/dom";

import $ from "jquery";
import _ from "lodash";
import Color from "color";

/***************************************************/

// store the currently used colors to avoid reusing them more than once on the screen
// useless if we don't use `colorsDark`/`colorsLight` but instead `randomColorLight/Dark`
const currentColors = ref({ light:undefined, dark:undefined });

const colorsDark = [ "#586f53", "#6a536f", "#6f5358", "#476863", "#475d68", "#b82650"
                   , "#c8184a", "#b61c1c", "#8e052c", "#810505", "#730000", "#660000"
                   , "#590000", "#4c0000", "#400000"];
const colorsLight = [ "#ff9393", "#fdbcb4", "#db6446", "#e67b5e", "#ecce69", "#e1c155"
                    , "#ecb06d", "#e1c14b", "#e3b63c", "#e9a232", "#e06d52" ]


/**************************************************/

/**
 *  functions to get a random color from an array of predefined colors
 */
const removeValFromArray = (arr, val) =>
  _.pull(_.clone(arr), val);  // _.clone is to avoid modifying in-place the `arr`
const getRandomColor = (arr, aldreadyUsedColor) =>
    aldreadyUsedColor != null
    ? _.sample( removeValFromArray(arr, aldreadyUsedColor) )
    : _.sample(arr);

/**
 * functions to get random colors.
 * - Math.random() > 0.5 ? ... allows to chose between two different gradiens for variety
 * - toFixed(1) rounds to .1 => we yield a random color from
 *     a discrete scale made of 10 steps (0..0.9).
 */
const randomColorLight = () =>
  Math.random() > 0.5
  ? new Color("#8dc6af").mix(new Color("#67e5cc"), Math.random().toFixed(1))
  : new Color("#67e57e").mix(new Color("#67e57e"), Math.random().toFixed(1));
const randomColorDark = () =>
  Math.random() > 0.5
  ? new Color("#700045").mix(new Color("#510708"), Math.random().toFixed(1))
  : new Color("#510b07").mix(new Color("#030191"), Math.random().toFixed(1));

/**************************************************/

onMounted(() => {
  // on hover, color the different clickable elements

  $(".menu-subcategories > li")
  .on("mouseenter", (e) => {
    // let color = getRandomColor(colorsLight, currentColors.value.light);
    // currentColors.value.light = color;
    let color = randomColorLight();
    $(e.currentTarget).css({ backgroundColor: color });
  })
  .on("mouseleave", (e) =>
    $(e.currentTarget).css({ backgroundColor: "var(--cs-main-default-bg)" }) );

  $(".menu-category:not(.has-subcategories)")
  .on("mouseenter", (e) => {
    // let color = getRandomColor(colorsDark, currentColors.value.dark);
    // currentColors.value.dark = color;
    let color = randomColorDark();
    $(e.currentTarget).css({ backgroundColor: color });
  })
  .on("mouseleave", (e) =>
    $(e.currentTarget).css({ backgroundColor: "var(--cs-negative-default-bg)" }) );
})
</script>


<style scoped>
h1 {
  font-family: var(--cs-font-sans-serif-accentuate);
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

.menu-container {
  position: fixed;
  top: var(--cs-navbar-height);
  height: calc(100vh - var(--cs-navbar-height));
  width: 100vw;

  display: flex;
  align-items: center;
  justify-content: center;

  border-left: var(--cs-border);
}
.menu {
  display: grid;
  grid-template-columns: 100%;
  grid-template-rows: repeat(6, max( 80px, calc(100%/6) ));  /* max/calc allows a min-height of 80px for all li elements */
  overflow: scroll;

  height: 100%;
  margin: 0;
  padding: 3vh 3vw;
}
@media ( orientation:landscape ) {
  .menu {
    grid-template-columns: 50% 50%;
    grid-template-rows: repeat(3, max( 150px, calc(100%/3) ));    /* max/calc allows a min-height of 150px for all li elements */
  }
}

/****************************************/

.menu > li {
  transition: background-color 0s;
  border: var(--cs-border);
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
  padding: 1px;
  display: flex;
  align-items: stretch;
  width: 100%;
}
.menu-subcategories a {
  color: var(--cs-main-default);
  width: 100%;
  height: 100%;
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



/*
li > a.selected {
  color: var(--cs-main-second);
}
*/
/*
.menu-container-visual {
  margin: 0;
  padding: 0;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
}
.menu-container-visual > img {
  min-width: 120%;
  object-fit: center;
}
*/

</style>
