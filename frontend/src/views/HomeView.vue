<template>
  <div class="home-wrapper">
    <div id="named-entity-wrapper"
         class="home-block home-block-even">
      <h1>Entités nommées</h1>

    </div>
    <div id="theme-wrapper"
         class="home-block">
      <h1>Thèmes</h1>

    </div>
    <div id="article-wrapper"
         class="home-block home-block-even">
         <h1>Articles</h1>

    </div>
    <div id="map-wrapper"
         class="home-block">
      <h1>Carte</h1>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";

import axios from "axios";

import HomeThemeOrNamedEntityPreview from "@components/HomeThemeOrNamedEntityPreview.vue";

/**************************************************/

const namedEntities = ref([]);
const themes = ref([]);
const articles = [];

/**************************************************/

function getData() {
  const themeTarget = new URL(`/i/theme`, __API_URL__)
      , namedEntityTarget = new URL(`/i/named-entity`, __API_URL__)
      , params = { params: { preview: true } };
      ;

  axios.get(themeTarget.href, params)
  .then(r => r.data)
  .then(data => { themes.value = data })
  .catch();
  axios.get(namedEntityTarget.href, params)
  .then(r => r.data)
  .then(data => { namedEntities.value = data })
  .catch();
}

/**************************************************/

onMounted(() => {
  getData();

})

</script>

<style scoped>
.home-wrapper {
  display: grid;
  grid-template-rows: 50% 50%;
  grid-template-columns: 50% 50%;
  height: 100%;
  width: 100%;
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
#named-entity-wrapper {
  background-color: palegreen;
}
#theme-wrapper {
  background-color: palevioletred;
}
#article-wrapper {
  background-color: plum;
}
#map-wrapper {
  background-color: pink;
}
</style>