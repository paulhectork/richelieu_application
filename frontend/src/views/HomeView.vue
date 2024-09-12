<!-- HomeView.vue
     the homepage of our app.

     the themes and namedEntities received from the backend
     have the following structure:
     both are arrays of:
     ```
     {
        "category_name" : "<category name>",
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
  <div class="home-wrapper">
    <div id="named-entity-wrapper"
         class="home-block home-block-even home-block-row1">
      <h1>Entités nommées</h1>
      <ul class="list-preview list-invisible">
        <li v-for="ne in namedEntitiesFormatted">
          <HomeItemPreview :resource="ne"
          ></HomeItemPreview>
        </li>
      </ul>
    </div>

    <div id="theme-wrapper"
         class="home-block home-block-odd home-block-row1">
      <h1>Thèmes</h1>
      <ul class="list-preview list-invisible">
        <li v-for="te in themesFormatted">
          <HomeItemPreview :resource="te"
          ></HomeItemPreview>
        </li>
      </ul>
    </div>

    <div id="article-wrapper"
         class="home-block home-block-even home-block-row2">
      <h1>Articles</h1>
      <ul class="list-invisible list-preview">
        <li v-for="ar in articlesFormatted">
          <HomeItemPreview :resource="ar"
          ></HomeItemPreview>
        </li>
      </ul>
    </div>

    <div id="map-wrapper"
         class="home-block home-block-odd home-block-row2">
      <div class="map-title-wrapper">
        <h1>Carte</h1>
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

import axios from "axios";
import $ from "jquery";
import _ from "lodash";

import HomeItemPreview from "@components/HomeItemPreview.vue";
import { articles } from "@modules/articleIndexData.js";
import { urlToFrontendNamedEntityCategory
       , urlToFrontendThemeCategory
       , urlToArticleMain } from "@utils/url";


/**************************************************/

// `*Formatted`: arrays restructured to fit the HomeItemPreview data model
const namedEntitiesFormatted = ref([]);
const themesFormatted        = ref([]);
const articlesFormatted      = ref([]);

/**************************************************/

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
  let len = Math.round(categoryName.length * 0.8),               // maximum allowed string size
      rgx = new RegExp(`^.{${len}}.+?((?=\\s*&mdash;)|(?=$))`);  // match until the next &mdash; or end of line
  preview = preview.sort((a,b) => a.length - b.length)           // shorter elements of `preview` first
                   .join(" &mdash; " );                          // transform array into &mdash-separated string
  return preview.match(rgx) !== null ? preview.match(rgx)[0] : preview;
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
                   ? urlToFrontendNamedEntityCategory(el.category_name)
                   : urlToFrontendThemeCategory(el.category_name)
    }
  })

/**
 * format the array of articles `articles` (see @modules/articleIndexData)
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
  console.log("hello !");
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
  grid-template-rows: 50% 50%;
  grid-template-columns: 50% 50%;
  height: 100%;
  width: 100%;
}

/***********************************/

.home-block {
  display: grid;
  grid-template-columns: 100%;
  grid-template-rows: auto 2fr;
  /*border-bottom: var(--cs-border);*/
}
.home-block-even {
  border-right: var(--cs-border);
}

/***********************************/

.home-block-odd > h1 {
  text-align: right;
}
h1 {
  background-color: white;
  width: 100%;
  font-size: 300%;
  font-weight: normal;
}

/************************************/

.map-title-wrapper {
  display: flex;
  flex-direction: column;
  width: 100%;
  align-items: flex-end;
  transform: translateY(25vh);
}
.map-title-wrapper > h1 {
  width: fit-content;
  padding: 10px;
}
.map-outer-wrapper {
  min-height: 100%;
  width: 100%;
}
.map-inner-wrapper {
  display: flex;
  align-items: end;
  justify-content: center;
  min-width: 100%;
  height: 100%;
  overflow: hidden;
}
.map-inner-wrapper > img {
  height: auto;
  object-fit: cover;
  min-width: 100%;
}

/***********************************/

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
</style>