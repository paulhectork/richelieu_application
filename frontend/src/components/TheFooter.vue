<template>
  <footer>
    <div class="footer-inner-wrapper">
      <div class="footer-info-wrapper">
        <RouterLink to="/documentation/donnees">
          <button>Données ouvertes</button>
        </RouterLink>
        <RouterLink to="/documentation/api">
          <button>API</button>
        </RouterLink>
        <RouterLink to="/documentation/mentions">
          <button>Crédits et mentions légales</button>
        </RouterLink>
      </div>
      <div class="footer-logo-wrapper">
        <LogoBanner></LogoBanner>
      </div>
    </div>
  </footer>
</template>


<script setup>

import LogoBanner from "@components/LogoBanner.vue";
</script>

<style scoped>
footer {
  margin-top: 5vh;
  border-top: var(--cs-main-border);
  height: 100%;
  width: 100%;
}
.footer-inner-wrapper {
  height: 100%;
  width: 100%;
  display: grid;
  grid-template-columns: 100%;
  grid-template-rows: 25% 75%;
}
</style>