<template>
  <div class="home-wrapper">
    <div id="named-entity-wrapper"
         class="home-block home-block-even home-block-row1">
      <h1>Entités nommées</h1>
      <ul class="list-preview list-invisible">
        <li v-for="ne in namedEntities">
          <HomeThemeOrNamedEntityPreview :resource="ne"
                                         tableName="named_entity"
          ></HomeThemeOrNamedEntityPreview>
        </li>
      </ul>

    </div>
    <div id="theme-wrapper"
         class="home-block home-block-odd home-block-row1">
      <h1>Thèmes</h1>
      <ul class="list-preview list-invisible">
        <li v-for="te in themes">
          <HomeThemeOrNamedEntityPreview :resource="te"
                                         tableName="theme"
          ></HomeThemeOrNamedEntityPreview>
        </li>
      </ul>
    </div>
    <div id="article-wrapper"
         class="home-block home-block-even home-block-row2">
        <h1>Articles</h1>
        <ul class="list-invisible list-preview">
          <li v-for="a in articles"><RouterLink :to="`/article/${a.urlSlug}`"
                                                v-html="a.title"
          ></RouterLink></li>
        </ul>
    </div>
    <div id="map-wrapper"
         class="home-block home-block-odd home-block-row2">
      <h1>Carte</h1>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from "vue";

import axios from "axios";
import $ from "jquery";
import _ from "lodash";

import HomeThemeOrNamedEntityPreview from "@components/HomeThemeOrNamedEntityPreview.vue";
import { articles } from "@modules/articleIndexData.js";

/**************************************************/

const namedEntities = ref([]);
const themes = ref([]);

/**************************************************/


async function getData() {
  const themeTarget = new URL(`/i/theme`, __API_URL__)
      , namedEntityTarget = new URL(`/i/named-entity`, __API_URL__)
      , params = { params: { preview: true } };
      ;

  return Promise.all([
    axios.get(themeTarget.href, params)
    .then(r => r.data)
    .then(data => { themes.value = data.slice(0,6); })
    .catch()
    ,
    axios.get(namedEntityTarget.href, params)
    .then(r => r.data)
    .then(data => { namedEntities.value = data.slice(0,6) })
    .catch()
  ]);
}

/**
 * hide the overfloweing `.home-block-row1 .list-preview > li` elements
 */
function hideOverflow() {
  console.log("hello !");
  document.querySelectorAll(".home-block-row1 .list-preview").forEach(parent => {
    let cuttingFloor = parent.offsetTop + parent.offsetHeight;  // children lower than that will be hidden

    $(parent).children().each(function () {  // don't use arrow functions to be able to use `this`
      $(this)[0].offsetTop + $(this)[0].offsetHeight > cuttingFloor
      ? $(this).css({ visibility: "hidden" })
      : $(this).css({ visibility: "visible" });
    })
  });
}

/**************************************************/

onMounted(() => {
  getData().then(hideOverflow);
  $(window).on("resize", () => _.debounce(hideOverflow, 250)());  // _.debounce returns a function, so we need to run it.
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
.home-block-row1 {
  display: grid;
  grid-template-columns: 100%;
  grid-template-rows: auto 2fr;
  border-bottom: var(--cs-border);

}
.home-block-even {
  border-right: var(--cs-border);
}
h1 {
  background-color: white;
  width: 100%;
  font-weight: normal;
}
.home-block:not(.home-block-even) > h1 {
  text-align: right;
}
.list-preview {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  align-items: flex-start;
  overflow: hidden;
  background-color: lightslategray;
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