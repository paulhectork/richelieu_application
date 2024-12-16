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

    <DownloadButtonGroup @download="onDownload"/>

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
import { computed, onMounted, ref } from "vue";
import axios from "axios";

import $ from "jquery";

import DownloadButtonGroup from "@components/DownloadButtonGroup.vue";
import UiLoader from "@components/UiLoader.vue";
import IndexPlace from "@components/IndexPlace.vue";

import { indexDataFormatterPlace } from "@utils/indexDataFormatter";
import { useListExport } from "@composables/useListExport";
import { downloadData } from "@utils/download";
import { placeToCsvRecord } from "@utils/toCsvRecord";
import "@typedefs";

/**********************************************/

const apiTarget  = new URL("/i/place", __API_URL__);
const dataFull   = ref([]);     /** @type {typedefs.PlaceItemLite[]} the full index, independant of user filters */
const dataFilter = ref([]);     /** @type {typedefs.IndexBaseItem[]} the data to pass to `IndexBase.vue`, can vary based on user filters */
const display    = "resource";  /** @type {String} which display style to use */
const isLoaded   = ref(false);  /** @type {typedefs.AsyncRequestState} hide the loader, show the index when toggled to true */

const selection = computed(() => dataFilter.value.map(({idUuid}) => idUuid));

/**********************************************/

const dataToExport = useListExport(
  dataFull,
  selection,
  {
    toJSON(resource) { return resource },
    toCSV: placeToCsvRecord
  },
)

async function onDownload(fileType) {
  downloadData(dataToExport[fileType].value, fileType, "places")
}

/**********************************************/

onMounted(() => {
  axios.get(apiTarget).then((r) => {
    dataFull.value   = JSON.parse(r.request.response);
    dataFilter.value = indexDataFormatterPlace(dataFull.value);
    isLoaded.value   = true;
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
