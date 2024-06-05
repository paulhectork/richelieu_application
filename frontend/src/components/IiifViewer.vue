<template>
  <div :id="osdId"></div>
</template>

<script setup>
import "openseadragon";

import { manifestToThumbnail } from "@utils/iiif";


props = defineProps(["osdId", "iiifUrl"]);

console.log(">>>", props.iiifUrl.value);

</script>

<style scoped>

</style>