<template>
  <div class="textpage-text-wrapper">
    <h3 id="abdoc-data-pres">Page en cours de création</h3>
  </div>
</template>


<script setup>
import { onMounted } from "vue";

/****************************************/

const emit = defineEmits(["h2"]);
const subtitle = "";

/****************************************/

onMounted(() => emit("h2", subtitle))
</script>


<style scoped>

</style>
