<template>
  <div class="footer-outer-wrapper">
    <footer>
      <div class="footer-inner-wrapper">
        <div class="footer-info-wrapper">
          <button><RouterLink to="/documentation/donnees">
            Données ouvertes</RouterLink></button>
          <button><RouterLink to="/documentation/api">
            API</RouterLink></button>
          <button><RouterLink to="/documentation/mentions">
            Crédits et mentions légales</RouterLink></button>
        </div>
        <div class="footer-logo-wrapper">
          <LogoBanner></LogoBanner>
        </div>
      </div>
    </footer>
  </div>
</template>


<script setup>

import LogoBanner from "@components/LogoBanner.vue";
</script>

<style scoped>
.footer-outer-wrapper {
  height: 100%;
  width: 100%;
}
footer {
  margin-top: 5vh;
}
.footer-inner-wrapper {
  height: 100%;
  width: 100%;
  display: grid;
  grid-template-columns: 100%;
  grid-template-rows: 25% 75%;
  border-top: var(--cs-main-border);
}
.footer-info-wrapper {
  border-bottom: var(--cs-main-border);
  display: flex;
  align-items: center;
  justify-content:center;
}
.footer-info-wrapper > * {
  flex: 1 1 0px;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>