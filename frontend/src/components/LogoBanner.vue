<!-- LogoBanner.vue

    a horizontal rectangle containing a banner of all the collaborator
    insitututions and financers' logos
-->

<template>
  <div class="logobanner-outer-wrapper">
    <div class="logobanner-inner-wrapper">
      <div class="logobanner-partners-wrapper logobanner-block">
        <div v-if="headers===true"><h2 class="logobanner-logo-title">
              Partenaires</h2>
        </div>
        <div class="logobanner-partners">
            <div class="logobanner-partners-row1">
            <a class="logobanner-logo-wrapper"
               href="https://www.inha.fr/">
              <span class="img-wrapper">
                <img src="@/assets/icons/logo_partenaire_inha_orig.png"
                     alt="Logo de l'Institut national de l'histoire de l'art">
              </span>
            </a>
            <a class="logobanner-logo-wrapper"
               href="https://www.bnf.fr/">
              <span class="img-wrapper">
                <img src="@/assets/icons/logo_partenaire_bnf_orig.png"
                     alt="Logo de la Bibliothèque nationale de France"
                     class="toobig">
              </span>
            </a>
            <a class="logobanner-logo-wrapper"
               href="https://www.chartes.psl.eu/">
              <span class="img-wrapper">
                <img src="@/assets/icons/logo_partenaire_enc_orig.png"
                     alt="Logo de l'École nationale des chartes">
              </span>
            </a>
            <a class="logobanner-logo-wrapper"
               href="https://www.epfl.ch/">
              <span class="img-wrapper">
                <img src="@/assets/icons/logo_partenaire_epfl_orig.png"
                     alt="Logo de l'École polytechnique fédérale de Lausanne"
                     class="toobig">
              </span>
            </a>
          </div>
          <div class="logobanner-partners-row2">
            <a class="logobanner-logo-wrapper"
               href="https://www.dfk-paris.org/">
              <span class="img-wrapper">
                <img src="@/assets/icons/logo_partenaire_dfk_orig.png"
                     alt="Logo du Centre allemand d'histoire de l'art (Deutsches forum für Kunstgeschichte)"
                >
              </span>
            </a>
            <a class="logobanner-logo-wrapper"
               href="https://www.centrechastel.sorbonne-universite.fr/">
              <span class="img-wrapper">
                <img src="@/assets/icons/logo_partenaire_cac_orig.png"
                     alt="Logo du centre André Chastel">
              </span>
            </a>
            <a class="logobanner-logo-wrapper"
               href="https://www.map.cnrs.fr/">
              <span class="img-wrapper">
                <img src="@/assets/icons/logo_partenaire_map_orig.png"
                     alt="Logo de l'unité de recherche du CNRS Modèles et
                          simulations pour l'architecture et le patrimoine"
                     class="toobig">
              </span>
            </a>
          </div>
        </div>
      </div>

      <div class="logobanner-financers-wrapper logobanner-block">
        <div v-if="headers===true"><h2 class="logobanner-logo-title">
          Avec le soutien de</h2></div>
        <div class="logobanner-financers">
          <a class="logobanner-logo-wrapper"
             href="https://www.banque-france.fr/">
            <span class="img-wrapper">
              <img src="@/assets/icons/logo_partenaire_bdf_orig.png"
                   alt="Logo de la Banque de France">
            </span>
          </a>
          <a class="logobanner-logo-wrapper"
             href="https://www.sciences-patrimoine.org/">
            <span class="img-wrapper">
              <img src="@/assets/icons/logo_partenaire_fsp_orig.png"
                   alt="Logo de la Fondation des Sciences du Patrimoine">
            </span>
          </a>
          <div><!-- empty item for grid positionning --></div>
          <a class="logobanner-logo-wrapper"
             href="https://www.caissedesdepots.fr/">
            <span class="img-wrapper">
              <img src="@/assets/icons/logo_partenaire_cdd_orig.png"
                   alt="Logo de la Caisse des Dépôts">
            </span>
          </a>
        </div>
      </div>
    </div>
  </div>

</template>


<script setup>
const props = defineProps(["headers"]);
const headers = props.headers || false;  // defaults to false
console.log(headers);
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
  grid-template-columns: 70% 30%;
  grid-template-rows: 100%;
  justify-items: center;
  align-items: center;
}
.logobanner-inner-wrapper > div {
  height: 100%;
}
.logobanner-logo-title {
  font-size: 20px;
  margin: 2% 0 0 15px;
  font-variant-caps: small-caps;
 }

/************************************/

.logobanner-partners {
  display: grid;
  grid-template-columns: 100%;
  grid-template-rows: 50% 50%;
  transform: translateY(-10%);
  height: 100%;
}
.logobanner-partners-row1 {
  display: grid;
  grid-template-columns: repeat(4, 25%);
  grid-template-rows: 100%;
  align-items: center;
  justify-items: center;
}
.logobanner-partners-row2 {
  display: grid;
  grid-template-columns: repeat(3, 33%);
  grid-template-rows: 100%;
  align-items: center;
  justify-items: center;
}
/*
.logobanner-partners a {
  height: 100%;
  width: 100%;
}
*/

/************************************/

.logobanner-financers-wrapper {
  border-left: var(--cs-main-border);
}
.logobanner-financers {
  display: grid;
  grid-template-columns: 50% 50%;
  grid-template-rows: 50% 50%;
  height: 100%;
}

/************************************/

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
</style>