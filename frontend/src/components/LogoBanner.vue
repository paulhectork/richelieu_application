<!-- LogoBanner.vue

    a horizontal rectangle containing a banner of all the collaborator
    insitututions and financers' logos
-->

<template>
  <div class="logobanner-outer-wrapper">
    <div class="logobanner-inner-wrapper">
      <div class="logobanner-partners">

        <div class="logobanner-partners-row1">
          <a class="logobanner-logo-wrapper"
             href="https://www.inha.fr/">
            <img src="@/assets/icons/logo_partenaire_inha_orig.png"
                 alt="Logo de l'Institut national de l'histoire de l'art">
          </a>
          <a class="logobanner-logo-wrapper"
             href="https://www.bnf.fr/">
            <img src="@/assets/icons/logo_partenaire_bnf_orig.png"
                 alt="Logo de la Bibliothèque nationale de France"
                 class="toobig">
          </a>
          <a class="logobanner-logo-wrapper"
             href="https://www.chartes.psl.eu/">
            <img src="@/assets/icons/logo_partenaire_enc_orig.png"
                 alt="Logo de l'École nationale des chartes">
          </a>
          <a class="logobanner-logo-wrapper"
             href="https://www.epfl.ch/">
            <img src="@/assets/icons/logo_partenaire_epfl_orig.png"
                 alt="Logo de l'École polytechnique fédérale de Lausanne"
                 class="toobig">
          </a>
        </div>
        <div class="logobanner-partners-row2">
          <a class="logobanner-logo-wrapper"
             href="https://www.dfk-paris.org/">
            <img src="@/assets/icons/logo_partenaire_dfk_orig.png"
                 alt="Logo du Centre allemand d'histoire de l'art (Deutsches forum für Kunstgeschichte)"
            >
          </a>
          <a class="logobanner-logo-wrapper"
             href="https://www.centrechastel.sorbonne-universite.fr/">
            <img src="@/assets/icons/logo_partenaire_cac_orig.png"
                 alt="Logo du centre André Chastel">
          </a>
          <a class="logobanner-logo-wrapper"
             href="https://www.map.cnrs.fr/">
            <img src="@/assets/icons/logo_partenaire_map_orig.png"
                 alt="Logo de l'unité de recherche du CNRS Modèles et
                      simulations pour l'architecture et le patrimoine"
                 class="toobig">
          </a>
        </div>
      </div>
      <div class="logobanner-financers">
        <a class="logobanner-logo-wrapper"
           href="https://www.banque-france.fr/">
          <img src="@/assets/icons/logo_partenaire_bdf_orig.png"
               alt="Logo de la Banque de France">
        </a>
        <a class="logobanner-logo-wrapper"
           href="https://www.sciences-patrimoine.org/">
          <img src="@/assets/icons/logo_partenaire_fsp_orig.png"
               alt="Logo de la Fondation des Sciences du Patrimoine">
        </a>
        <div><!-- empty item for grid positionning --></div>
        <a class="logobanner-logo-wrapper"
           href="https://www.caissedesdepots.fr/">
          <img src="@/assets/icons/logo_partenaire_cdd_orig.png"
               alt="Logo de la Caisse des Dépôts">
        </a>
      </div>
    </div>
  </div>

</template>


<script setup>

</script>


<style scoped>
.logobanner-outer-wrapper {
  height: 100%;
  width: 100%;
  min-height: 100px;
}
.logobanner-inner-wrapper {
  height: 100%;
  display: grid;
  grid-template-columns: 70% 30%;
  grid-template-rows: 100%;
  justify-items: center;
  align-items: center;
}
.logobanner-inner-wrapper > div {
  height: 100%;
}
.logobanner-partners {
  display: grid;
  grid-template-columns: 100%;
  grid-template-rows: 60% 40%;
  transform: translateY(-10%);
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
.logobanner-partners a {
  height: 100%;
  width: 100%;
}
.logobanner-financers {
  display: grid;
  grid-template-columns: 50% 50%;
  grid-template-rows: 50% 50%;
  border-left: var(--cs-main-border);
}
a {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
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