<template>

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
