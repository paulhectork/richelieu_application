<!-- IndexCount.vue
   a pretty simple h2 title for index pages stating
   how many resources are being displayed

   props:
    - indexCount (Number) : the number of resources displayed
    - dataType   (String) : the type of resource displayed by the index
-->

<template>
  <h2 v-if="indexCount <= 0">
    Aucune {{ dataTypeAsString }}
    associée
  </h2>
  <h2 v-else-if="indexCount === 1">
    Une {{ dataTypeAsString }}
    associée
  </h2>
  <h2 v-else>
    {{ indexCount }} {{ dataTypeAsString }}
    associées
  </h2>
</template>

<script setup>
import { onMounted, watch, computed, ref } from "vue";

/***************************************/

const props = defineProps(["indexCount", "dataType"]);
const indexCount = ref();
const dataType = ref();

/**
 * computed user-exposed datatype based on the actual
 * kind of data and number of items in the related index
 */
 const dataTypeAsString = computed(() =>
  dataType.value === "iconography" && indexCount.value > 1
  ? "ressources iconographiques"
  : dataType.value === "iconography" && indexCount.value <= 1
  ? "ressource iconographique"
  : dataType.value === "theme" && indexCount.value > 1
  ? "thèmes"
  : dataType.value === "theme" && indexCount.value <= 1
  ? "thème"
  : dataType.value === "namedEntity" && indexCount.value > 1
  ? "entités nommées"
  : dataType.value === "namedEntity" && indexCount.value <= 1
  ? "entité nommée"
  : dataType.value === "place" && indexCount.value > 1
  ? "lieux"
  : dataType.value === "place" && indexCount.value <= 1
  ? "lieu"
  : "ressource(s)"
)

/***************************************/

/**
 * validate and set the global refs
 */
function setData() {
  let allowedTypes = [ "iconography", "theme", "place", "namedEntity" ];
  if ( !allowedTypes.includes(props.dataType) ) {
    console.error(`IndexCount.onMounted : invalid value for 'props.dataType'. expected one of '${allowedTypes}', got '${props.dataType}'`);
    dataType.value = undefined;
  } else {
    dataType.value = props.dataType;
  }
  indexCount.value = props.indexCount;
}

/***************************************/

watch(props, (newP, oldP) => {
  setData();
})

onMounted(() => {
  setData();
})
</script>