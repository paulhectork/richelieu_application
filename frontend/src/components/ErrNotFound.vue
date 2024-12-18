<template>

  <!-- ErrNotFound.vue
  
       component for when an element is not found.
       is called by @views/ErrNotFoundView.vue for unregistered routes,
       and used as a standalone component when the route exists,
       but route parameters are invalid (i.e., the UUID of an
       iconography entry does not exist. in that case, the URL
       is valid, but no data can be fetched the UUID, and so we
       display the ErrNotFound.vue component inside IconographyMainView.vue.)
  -->


  <div class="not-found">
    <h1>[404]</h1>
    <p>Cette page n'a pas été trouvée ou n'existe pas!</p>
  </div>
</template>


<script setup>

</script>


<style scoped>
.not-found {
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
