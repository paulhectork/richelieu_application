<!-- PlaceView.vue
     a view for the place index.
     this component gets the data, most of the
     actual work takes place in `@components/IndexPlace.vue`
-->

<template>

  <div class="index-place-container">

    <div class="top-container">
      <h1>Index des lieux</h1>
    </div>

    <div class="bottom-container">
      <UiLoader v-if="!isLoaded"></UiLoader>
      <IndexPlace v-else
                  :display="display"
                  :data="dataFilter"
      ></IndexPlace>
    </div>

  </div>

</template>

<script setup>
import { onMounted, ref } from "vue";
import axios from "axios";

import $ from "jquery";

import { indexDataFormatterPlace } from "@utils/indexDataFormatter";
import UiLoader from "@components/UiLoader.vue";
import IndexPlace from "@components/IndexPlace.vue";

const apiTarget  = new URL("/i/place", __API_URL__);
const dataFull   = ref([]);     // the full index, independant of user filters
const dataFilter = ref([]);     // the data to pass to `IndexBase.vue`, can vary based on user filters
const display    = "resource";  // which display style to use
const isLoaded   = ref(false);  // hide the loader, show the index when toggled to true

onMounted(() => {
  axios.get(apiTarget).then((r) => {
    dataFull.value   = JSON.parse(r.request.response);
    dataFilter.value = indexDataFormatterPlace(dataFull.value);
    isLoaded.value = true;
  })

  // quick fix for the height/scrolling of `.bottom-container`
  $(".bottom-container").css({ maxHeight: $(window).height() - $(".bottom-container")[0].getBoundingClientRect().top })
})

</script>


<style scoped>
.index-place-container {
  display: grid;
  grid-template-rows: auto 2fr;
  height: 100%;
}
</style>
