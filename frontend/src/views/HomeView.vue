<!-- HomeView.vue
     the homepage of our app.

    this component displays theses, named entites,
    redirections to a map and a modal presenting the project.

    the themes and namedEntities received from the backend
    have the following structure:
    both are arrays of:
    ```
    {
       "category_name" : "<category name, to display on the page>",
       "category_slug" : "<category slug, to build urls>",
       "count"         : <number of associated themes or named entities>,
       "preview"       : [ <Array<string> of a few themes or named entities of that resource> ],
       "thumbnail"     : [ <filename> ]
    }
    ```
    themes, named entities and articles are reformatted to be
    passed to `HomeItemPreview.vue`, with the following structure
    (see HomeItemPreview for more info):
    ```
    {
       title_main   : <string>,
       title_second : <string>,
       title_sub    : <str>,
       href         : <str>,
       thumbnail    : <str>
    }
    ```
-->

<template>

  <!-- without `v-if` on `Transition`, TheHomeModal would slide-out on each page,
     since it would be removed. -->
  <Transition name="slideInOut">
    <TheHomeModal @close-home-modal="onCloseHomeModal"
                  v-if="domStore.homeModalVisible"
    ></TheHomeModal>
  </Transition>

  <div class="home-wrapper">
    <div id="theme-wrapper"
         class="home-block home-block-even home-block-row1">
      <div class="home-block-title-wrapper">
        <h1>Thèmes</h1>
        <div class="home-block-plus-wrapper">
          <span>Voir tous les thèmes</span>
          <RouterLink to="/theme">
            <UiButtonLink></UiButtonLink>
          </RouterLink>
        </div>
      </div>
      <ul class="list-preview list-invisible">
        <li v-for="te in themesFormatted">
          <HomeItemPreview :resource="te"
                           display="category"
          ></HomeItemPreview>
        </li>
      </ul>
    </div>

    <div id="named-entity-wrapper"
         class="home-block home-block-odd home-block-row1">
      <div class="home-block-title-wrapper">
        <div class="home-block-plus-wrapper">
          <span>Voir toutes les entités nommées</span>
          <RouterLink to="/entite-nommee">
            <UiButtonLink></UiButtonLink>
          </RouterLink>
        </div>
        <h1>Noms</h1>
      </div>
      <ul class="list-preview list-invisible">
        <li v-for="ne in namedEntitiesFormatted">
          <HomeItemPreview :resource="ne"
                           display="category"
          ></HomeItemPreview>
        </li>
      </ul>
    </div>

    <div id="article-wrapper"
         class="home-block home-block-even home-block-row2">
      <div class="home-block-title-wrapper">
        <h1>Articles</h1>
        <div class="home-block-plus-wrapper">
          <span>Voir la table des matières</span>
          <RouterLink to="/article">
            <UiButtonLink></UiButtonLink>
          </RouterLink>
        </div>
      </div>
      <ul class="list-invisible list-preview">
        <li v-for="ar in articlesFormatted">
          <HomeItemPreview :resource="ar"
                           display="article"
          ></HomeItemPreview>
        </li>
      </ul>
    </div>

    <div id="map-wrapper"
         class="home-block home-block-odd home-block-row2"
         @mouseover="onMapMouseOver"
         @mouseout="onMapMouseOut"
    >
      <div class="home-block-title-wrapper map-title-wrapper">
        <h1><RouterLink to="/cartographie"
            >Carte</RouterLink></h1>
      </div>
      <RouterLink to="/cartographie"
                  class="map-outer-wrapper"
      >
        <div class="map-inner-wrapper">
          <img src="@/assets/media/home_view_map.png"
             alt="Visuel de carte"
          >
        </div>
      </RouterLink>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from "vue";
import { useRoute } from "vue-router";

import axios from "axios";
import $ from "jquery";
import _ from "lodash";

import UiButtonLink from "@components/UiButtonLink.vue";
import HomeItemPreview from "@components/HomeItemPreview.vue";
import TheHomeModal from "@components/TheHomeModal.vue";

import { domStore } from "@stores/dom.js";
import { articles } from "@globals";
import { urlToFrontendNamedEntityCategory
       , urlToFrontendThemeCategory
       , urlToArticleMain } from "@utils/url";
import { randomColorLight } from "@utils/colors";


/**************************************************/

const route = useRoute();

// `*Formatted`: arrays restructured to fit the HomeItemPreview data model
const namedEntitiesFormatted = ref([]);
const themesFormatted        = ref([]);
const articlesFormatted      = ref([]);

/**************************************************/

/**
 * chnge the background color of the title of the map block when
 *  hovering in/out of the entire map block.
 */
const onMapMouseOver = () =>
  $(".map-title-wrapper > h1").css({ backgroundColor: randomColorLight() });
const onMapMouseOut = () =>
  $(".map-title-wrapper > h1").css({ backgroundColor: "var(--cs-main-default-bg)" });

/**
 * switching domStore.homeModalVisible will close `TheHomeModal` for the entire
 * session: the modal will only be shown again after exiting the site or after
 * a full-page reload (ex: cliking on an internal link made with `<a>`).
 */
 function onCloseHomeModal(e) {
  domStore.homeModalVisible = false;
}

/**
 * for themes and named entities, stringify the `preview` array:
 * for each theme or named entity, get the categoryName's length
 * and create a string representation of the preview that is
 * visually the same length as the categoryName.
 * the regex allows to split `preview` at the end of an item,
 * instead of in the middle
 * @param {Array<String>} preview: the array of theme or category names
 * @param {string} categoryName: the name of the category
 *   the preview items are related to.
 */
function stringifyThemeOrNamedEntityPreview(preview, categoryName) {
  let len = Math.round(categoryName.length * 1.5),               // maximum allowed string size
      rgx = new RegExp(`^.{${len}}.+?((?=\\s*&mdash;)|(?=$))`);  // match until the next &mdash; or end of line
  preview = preview.sort((a,b) => a.length - b.length)           // shorter elements of `preview` first
                   .join(" &mdash; " );                          // transform array into &mdash-separated string
  return preview.match(rgx) !== null
         ? preview.match(rgx)[0]
         : preview;
}

/**
 * format a Theme or NamedEntity array returned by the backend (see `getData()`)
 * into an array that fits the HomeItemPreview data model.
 * @param {Array<Object>} arr: the array to format
 * @param {string} tableName: theme or namedEntity
 */
const formatCategoryArray = (arr, tableName) =>
  arr.map(el => {
    return { title_main: el.category_name,
             title_second: el.count,
             title_sub: stringifyThemeOrNamedEntityPreview(el.preview, el.category_name),
             href: tableName === "namedEntity"
                   ? urlToFrontendNamedEntityCategory(el.category_slug)
                   : urlToFrontendThemeCategory(el.category_slug)
    }
  })

/**
 * format the array of articles `articles` (see @globals)
 * into an array that fits the HomeItemPreview data model.
 */
const formatArticleArray = (arr) =>
  arr.map(el => {
    return { title_main: el.title,
             title_second: undefined,
             title_sub: undefined,//el.subtitle,
             href: urlToArticleMain(el.urlSlug),
             thumbnail: el.image }
  })

/**
 * hide the overfloweing `.home-block-row1 .list-preview > li` elements
 */
function hideOverflow() {
  document.querySelectorAll(".list-preview").forEach(parent => {
    let cuttingFloor = parent.offsetTop + parent.offsetHeight;  // children lower than that will be hidden

    $(parent).children().each(function () {  // don't use arrow functions to be able to use `this`
      $(this)[0].offsetTop + $(this)[0].offsetHeight > cuttingFloor
      ? $(this).css({ visibility: "hidden" })
      : $(this).css({ visibility: "visible" });
    })
  });
}

/**
 * asynchronously fetch data from the backend on Themes and Named Entities
 */
async function getData() {
  const themeTarget = new URL(`/i/theme`, __API_URL__)
      , namedEntityTarget = new URL(`/i/named-entity`, __API_URL__)
      , params = { params: { preview: true } };
      ;

  // Promise.all() allows for an async return, necessary to use hideOverflow() safely
  return Promise.all([
    axios.get(themeTarget.href, params)
    .then(r => r.data)
    .then(data => {
      themesFormatted.value = formatCategoryArray(data, "theme"); })
    ,
    axios.get(namedEntityTarget.href, params)
    .then(r => r.data)
    .then(data => {
      namedEntitiesFormatted.value = formatCategoryArray(data, "namedEntity") })
  ]);
}

/**************************************************/

onMounted(() => {
  articlesFormatted.value = formatArticleArray( articles );
  getData().then( hideOverflow );
  $( window ).on( "resize", _.debounce(hideOverflow, 300) );

})
onUnmounted(() =>
  $(window).off("resize")
)

</script>

<style scoped>
.home-wrapper {
  display: grid;
  grid-template-rows: 70% 70% 70% 40%;
  grid-template-columns: 100%;
  height: calc(100vh - var(--cs-navbar-height) - var(--cs-sidebar-portrait-height));
  width: 100vw;
  overflow-x: hidden;
  padding: 1% 3% 0 3%;
}
.home-block {
  display: grid;
  grid-template-columns: 100%;
  grid-template-rows: max(25%,50px) 75%;  /* 50px: fallback on small viewports */
  border-right: none;
  border-bottom: var(--cs-main-border);
}
.home-block:not(:first-child) {
  margin-top: 3vh;
  margin-bottom: 5vh;
}

@media ( orientation: landscape ) {
  .home-wrapper {
    width: 100%;
    overflow-x: initial;
    height: calc(100vh - var(--cs-navbar-height));
    grid-template-rows: 50% 50%;
    grid-template-columns: 50% 50%;
  }
  .home-block {
    height: 100%;
    border: none;
  }
  .home-block:not(:first-child) {
    margin-top: 0;
    margin-bottom: 0;
  }
  .home-block-even {
    border-right: var(--cs-main-border);
  }
}


/***********************************/
/* title block styling */

.home-block-title-wrapper {
  display: grid;
  grid-template-columns: 2fr auto;
  grid-template-rows: 100%;
  align-items: center;
}
h1 {
  background-color: white;
  width: min-content;
  font-size: 300%;
  font-weight: normal;
  text-wrap: nowrap;
  margin:0% 0;
}
.home-block-odd > .home-block-title-wrapper {
  flex-direction: row-reverse;
}
.home-block-plus-wrapper {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  background-color: white;
  border: var(--cs-main-border);
  padding: 3px;
  margin: 0 1vw;
}
.home-block-plus-wrapper > * {
  text-wrap: nowrap;
}
.home-block-plus-wrapper .button-link {
  height: 5vh;
  width: 5vh;
  min-height: 30px;
  min-width: 30px;
}

/* hide "en savoir plus" on small viewports */
.home-block-plus-wrapper > span {
  visibility: hidden;
  width: 0;
}
@media ( min-width: 1200px ) {
  .home-block-plus-wrapper > span {
    visibility: visible;
    width: auto;
  }
}

/***********************************/
/* .list-preview styling */

.list-preview {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  align-items: flex-start;
  overflow: hidden;
  /*background-color: lightslategray;*/
}
.list-preview > li {
  margin: 5px;
  height: fit-content;
  width: fit-content;
}
.home-block-even .list-preview {
  justify-content: start;
}
.home-block-odd .list-preview {
  justify-content: end;
}

/************************************/
/* map block styling */

#map-wrapper {
  min-width: 100%;
  height: 100%;

  display: grid;
  grid-template-rows: 0% 100%;
  grid-template-columns: 100%;
}
#map-wrapper h1 > a {
  color: var(--cs-main-default);
  text-decoration: none;
}
.map-title-wrapper {
  display: flex;
  flex-direction: column;
  width: 100%;
  align-items: flex-end;
  transform: translateY(25vh);
  flex-grow: 1;
}
.map-title-wrapper > h1 {
  width: fit-content;
  padding: 10px;
  border: var(--cs-main-border);
  margin-right: 5vw;
  transition: background-color .5s;
  cursor: grab;
}
.map-outer-wrapper {
  overflow: hidden;
}
.map-inner-wrapper {
  display: flex;
  align-items: end;
  justify-content: center;
  min-height:100%;
  min-width:100%;
  overflow: hidden;
}
.map-inner-wrapper > img {
  object-fit: contain;
  overflow: hidden;
}

/* this fancy selector targets `h1` when .map-outer-wrapper is hovered/clicked on */
/* done in jQuery instead */
/*
.map-title-wrapper:has(+ .map-outer-wrapper:hover) > h1 {
  background-color: var(--cs-main-second-bg);
  color: var(--cs-main-second);
}
*/
.map-title-wrapper:has(+ .map-outer-wrapper:active) > h1 {
  background-color: var(--cs-main-active-bg) !important;
}

/*****************************************/
/*`#named-entity-wrapper h1` is a bitch to style,
  so we set a different style for when the screen is too
  narrow, on the whole #named-entity-wrapper and on
  its `.home-block-title-wrapper` */
#named-entity-wrapper {
  grid-template-rows: 1fr auto;
}
#named-entity-wrapper > .home-block-title-wrapper {
  grid-template-columns: auto 2fr;
  justify-items: right;
}
#named-entity-wrapper h1 {
  text-wrap: wrap;
  text-align: right;
}
@media ( min-width: 1200px ) {
  #named-entity-wrapper {
    /* on wide viewports, the grid is the same for
      #named-entity-wrapper as it is for other blocks */
    grid-template-rows: max(25%,50px) 75%;
  }
  #named-entity-wrapper h1 {
    text-wrap: nowrap;
  }
}

</style>