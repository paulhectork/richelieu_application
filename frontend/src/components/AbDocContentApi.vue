<template>
  <div class="textpage-text-wrapper">
    <iframe title="API documentation and playground":src="swagger_url" class="swagger"/>
  </div>
</template>


<script setup>
import { onMounted } from "vue";

/****************************************/
const swagger_url = __SWAGGER_URL__;
const emit = defineEmits(["h2"]);
const subtitle = "";

/****************************************/

onMounted(() => emit("h2", subtitle))
</script>


<style scoped>
.swagger {
  width: 100%;
  height: 2000px;
}
</style>
