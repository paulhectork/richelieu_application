<!-- ErrInternal.vue
     a component that displays an error message when an error occurs
-->

<template>
  <div class="err-internal">
    <h1>Erreur</h1>
    <p>Une erreur interne est survenue</p>
  </div>
</template>


<script setup>

</script>


<style scoped>
.err-internal {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
h1 {
  font-family: var(--cs-font-sans-serif);
}
</style>