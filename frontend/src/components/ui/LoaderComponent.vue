<!-- LoaderComponent.vue

    a very simple CSS loader. its height can be set on the parent. -->

<template>
  <div class="loader-wrapper">
    <span class="loader"></span>
  </div>
</template>

<script setup>
</script>

<style scoped>
.loader-wrapper {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}
.loader {
  width: 48px;
  height: 48px;
  border: var(--cs-border);
  border-radius: 50%;
  display: inline-block;
  position: relative;
  box-sizing: border-box;
  animation: rotation 1s linear infinite;
}
.loader::after {
  content: '';
  box-sizing: border-box;
  position: absolute;
  left: 0;
  top: 0;
  background: var(--cs-main-default);
  width: 10px;
  height: 10px;
  transform: translate(-50%, 150%);
  border-radius: 50%;
}

@keyframes rotation {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>