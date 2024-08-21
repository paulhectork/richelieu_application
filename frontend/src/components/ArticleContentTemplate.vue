<!-- ArticleComponentTemplate.vue:

     a basic template for all the ArticleContent...
     components. actually unused in the app.
-->

<template>
  <!--
    images and footnotes:
    <ButtonEllipsis data-key="..."></ButtonEllipsis>
    <ButtonEye data-key="an UUID of iiifIdUuid"></ButtonEye>
   -->

  <!-- title and subtitle -->
  <div class="article-header">
    <h1></h1>
    <h2></h2>
  </div>

  <!-- the article itself -->
  <div class="article-body">

  </div>

  <!-- author name -->
  <div class="article-footer">
    <p></p>
  </div>

</template>


<script setup>
import { onMounted, ref } from "vue";


import ButtonEye from "@components/ui/ButtonEye.vue";
import ButtonArrow from "@components/ui/ButtonArrow.vue";
import ButtonEllipsis from "@components/ui/ButtonEllipsis.vue";
import { urlToFrontendTheme, urlToFrontendNamedEntity } from "@utils/url.js";

/**********************************************/

const emit    = defineEmits(["queryParams", "iiifIdUuidArray", "footnotes"]);  // what to emit to `ArticleMainView.vue`

const iiifIdUuidArray = [];  // the UUIDs of iconography ressources from which to display a IIIF image
const queryParams     = {};  // the parameters to run a backend advanced search query
const footnotes       = {};  // { <footnote key>: <footnote html content> }: the footnotes for the current article

/**********************************************/

// when the component is mounted, send data to parent
onMounted(() => {
  emit("iiifIdUuidArray", iiifIdUuidArray);
  emit("queryParams", queryParams);
  emit("footnotes", footnotes);
})

</script>


<style scoped>

</style>