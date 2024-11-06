<!-- TheFooter.vue
  just a footer.

  the only fancy thing is that `.footer-gradient` is a div
  working as a margin between `main` and the footer, containing
  a gradient. this gradient is:
  - black-to-white on negative themed pages,
  - white-to-black otherwise

  props:
  - gradient (string)
      "main"|"negative", this prop is sent from App.vue to define the
      class of `.footer-gradient`, and thus the type of gradient used;
-->

<template>
  <div class="footer-outer-wrapper">
    <div class="footer-gradient"
         :class="gradientClass"
    ></div>
    <footer>
      <div class="footer-inner-wrapper">
        <div class="footer-info-wrapper">
          <ul class="footer-info list-invisible">
            <li><button><RouterLink to="/documentation/donnees">
              Données ouvertes</RouterLink></button></li>
            <li><button><RouterLink to="/documentation/api">
              API</RouterLink></button></li>
            <li><button><RouterLink to="/documentation/mentions">
              Crédits et mentions légales</RouterLink></button></li>
          </ul>
        </div>
        <div class="footer-logo-wrapper">
          <LogoBanner :headers="true"></LogoBanner>
        </div>
      </div>
    </footer>
  </div>
</template>


<script setup>
import { watch,ref,onMounted } from "vue";

import LogoBanner from "@components/LogoBanner.vue";

/***********************************/

const props = defineProps(["gradient"]);
const gradientClass = ref();

/***********************************/

function setGradientClass(gradient) {
  const allowed = ["main", "negative"];
  if ( !allowed.includes(gradient) ) {
    console.error(`TheFooter.setGradientClass() : 'gradient' must be one of ${allowed}, got ${gradient}`);
  } else {
    gradientClass.value = gradient;
  }
}

/***********************************/

watch(props, (newP, oldP) => {
  setGradientClass(newP.gradient);
})

onMounted(() => {
  setGradientClass(props.gradient);
})


</script>

<style scoped>
.footer-outer-wrapper {
  height: 100%;
  width: 100%;
}
.footer-gradient {
  height: 40vh;
}
.footer-gradient.negative {
  /*background: linear-gradient(black 10%, 80%, white);*/
  background-color: var(--cs-negative-default-bg);
}
.footer-gradient.main {
  /*background: linear-gradient(white 10%, 80%, black);*/
  background-color: var(--cs-main-default-bg);
}
footer {
  height: 100%;
}
@media ( orientation:portrait ) {
  footer {
    margin-bottom: calc(2 * var(--cs-portrait-sidebar-height));
  }
}
.footer-inner-wrapper {
  height: 100%;
  width: 100%;
  display: grid;
  grid-template-columns: 100%;
  grid-template-rows: 30% 70%;
  border-top: var(--cs-main-border);
}

/*******************************/

.footer-info-wrapper {
  border-bottom: var(--cs-main-border);
  display: flex;
  align-items: center;
  justify-content:center;
}
.footer-info {
  display: flex;
  align-items: center;
  justify-content:center;
  height: 100%;
  width: 80%
}
.footer-info > * {
  flex: 1 1 0px;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 70%;
}
.footer-info button {
  width: 100%;
  height: 100%;
  font-size: 100%;
}
.footer-info button > a {
  text-decoration: none;
  color: var(--cs-main-default);
}
.footer-info button:hover > a,
.footer-info button:active > a {
  text-decoration: none;
  color: var(--cs-main-default-secondary);
}
@media ( max-height: 600px ) {
  .footer-info button > a {
    text-wrap: nowrap;  /* avoid the text to overflow outside of the button */
  }
}
/*******************************/
</style>