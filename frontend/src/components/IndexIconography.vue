<template>
  <div class="index-iconography-outer-wrapper">
    <div class="index-iconography-inner-wrapper">
      <IndexIconographyFilter v-if="!hideFilter"
                              :data="dataFull"
                              @iconography-filter="handleIconographyFilter"
      ></IndexIconographyFilter>

      <DownloadButtonGroup :data="dataToExport" filename="iconography"/>

      <IndexBase display="resource"
                 :data="dataFilter"
                 :itemsPerRow="itemsPerRow"
      ></IndexBase>
    </div>
  </div>
</template>


<script setup>
import { computed, onMounted, ref, watch } from "vue";

import IndexIconographyFilter from "@components/IndexIconographyFilter.vue";
import IndexBase from "@components/IndexBase.vue";
import DownloadButtonGroup from "../components/DownloadButtonGroup.vue";

import { indexDataFormatterIconography } from "@utils/indexDataFormatter";
import { useListExport } from "@composables/useListExport";
import { stringifyDate } from "@utils/stringifiers";

/*************************************************/

const props       = defineProps([ "data", "oneItemRow", "hideFilter" ]);
const hideFilter  = ref(false);
const itemsPerRow = ref();
const dataFull    = ref([]);  // array of iconography objects sent from the parent. this one is never modified.
const dataFilter  = ref([]);  // data, possibly modified by `IndexIconographyFilter`, and reshaped with indexDataFormatterIconography

/*************************************************/

function setRefs(theProps) {
  dataFull.value    = theProps.data;
  hideFilter.value  = theProps.hideFilter || false;
  itemsPerRow.value = theProps.oneItemRow === true ? 1 : undefined;
  dataFilter.value  = indexDataFormatterIconography(theProps.data);

  console.log("****", hideFilter.value, itemsPerRow.value);
}

function handleIconographyFilter(iconographyData) {
  dataFilter.value = indexDataFormatterIconography(iconographyData);
}

const selection = computed(() => dataFilter.value.map(({idUuid}) => idUuid));

const dataToExport = useListExport(
  dataFull,
  selection,
  {
    toJSON(resource) {
      return {
          uuid: resource.id_uuid,
          title: resource.title.join(', '),
          iiif_url: resource.iiif_url,
          authors: resource.authors.map(
            author => ({name: author.entry_name, uuid: author.id_uuid})
          ),
          date: resource.date
        }
      },
    toCSV(resource) {
      return {
        uuid: resource.id_uuid,
        title: resource.title.join('|'),
        iiif_url: resource.iiif_url,
        authors: resource.authors.map(author => author.entry_name).join('|'),
        authors_uuids: resource.authors.map(author => author.id_uuid).join('|'),
        date: stringifyDate(resource.date),
      }
    }
  },
)

/*************************************************/

watch(props, (newP, oldP) => {
  console.log("IndexIconography.watch : new props !", newP)
  setRefs(newP);
})

onMounted(() => {
  setRefs(props);
})

</script>


<style scoped>
.index-iconography-outer-wrapper {
  height: 100%;
  width: 100%;
}
.index-iconography-inner-wrapper {

}
</style>
