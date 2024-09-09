<!-- PlaceMainView.vue

     the main view for a single place, to see it on a map
     and view all of its related iconography
-->

<template>
  <div class="warn-wrapper">
    <div class="warn">
      <p>Cette page est en cours de développement.</p>
    </div>
  </div>
</template>


<script setup>

</script>


<style scoped>
.warn-wrapper {
  position: absolute;
  height: 100%;
  width: 100%;
  z-index: 999;
  display: grid;
  align-items: center;
  justify-content: center;
}
.warn {
  opacity: 1;
  background-color: white;
  border: var(--cs-border);
}
.warn > p {
  margin: 30px;
}

</style>