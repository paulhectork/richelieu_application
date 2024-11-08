<!-- LogoBanner.vue

    a horizontal rectangle containing a banner of all the collaborator
    insitututions and financeurs' logos
-->

<template>
  <div class="logobanner-outer-wrapper">
    <div class="logobanner-inner-wrapper">
      <div class="logobanner-porteurs-wrapper logobanner-block">
        <div v-if="headers===true"
             class="logobanner-title-wrapper"
        ><h2>Un projet porté par</h2></div>
        <div class="logobanner-porteurs img-wrapper">
          <img src="@/assets/icons/logo_institutions_thinborders.png"
               alt="Logos des institutions porteuses du projet">
        </div>
      </div>

      <div class="logobanner-partenaires-wrapper logobanner-block">
        <div v-if="headers===true"
             class="logobanner-title-wrapper"
        ><h2>Avec l'aide de</h2></div>
        <div class="logobanner-partenaires img-wrapper">
          <img src="@/assets/icons/logo_help_layout.png">
        </div>
      </div>

      <div class="logobanner-financeurs-wrapper logobanner-block">
        <div v-if="headers===true"
             class="logobanner-title-wrapper"
        ><h2>Avec le soutien de</h2></div>
        <div class="logobanner-financeurs img-wrapper">
          <img src="@/assets/icons/logo_financers_thinborders.png"
               alt="Logos des financeurs du projet">
        </div>
      </div>
    </div>
  </div>

</template>


<script setup>
const props = defineProps(["headers"]);
const headers = props.headers || false;  // defaults to false
</script>


<style scoped>
.logobanner-outer-wrapper {
  height: 100%;
  width: 100%;
  min-height: 100px;
}
.logobanner-inner-wrapper {
  height: 100%;
  width: 100%;
  display: grid;
  grid-template-columns: 50% 15% 1fr;
  grid-template-rows: 100%;
  justify-items: center;
  align-items: center;
}
.logobanner-block {
  height: 100%;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-between;
  /*
  display: grid;
  grid-template-rows: max(10%, 25px) 2fr;
  grid-template-columns: 100%;
  */
}
.logobanner-block:not(:first-child) {
  border-left: var(--cs-main-border);
}
.logobanner-title-wrapper {
  width: 100%;
}
.logobanner-title-wrapper > h2 {
  font-size: 20px;
  margin: 2% 0 0 15px;
  font-variant-caps: small-caps;
  width: 100%;
  margin: 5px;
 }
.img-wrapper {
  height: 100%;
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
}
img {
  height: 100%;
  width:  100%;
  object-fit: contain;
  position: absolute;
  padding: 5px;
}

/*
a {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}
a > .img-wrapper{
  height: 100%;
  width: 100%;
  max-width: 200px;
  max-height: 160px;
}
img {
  height: 100%;
  width: 100%;
  object-fit: contain;
}
.toobig {
  height: 80%;
  width: 80%;
}
*/

</style>