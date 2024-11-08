<template>
  <div class="textpage-text-wrapper">
    <h3 id="abdoc-credits">Crédits</h3>
    <dl>
      <dt>Direction scientifique</dt>
      <dd>Charlotte Duvette</dd>
      <dt>Développement et ingénierie de la donnée</dt>
      <dd>Paul Kervegan et Marina Hervieu</dd>
      <dt>Graphisme</dt>
      <dd>Lou Ong et Paul Kervegan</dd>
      <dt>Recherches historiques</dt>
      <dd>Charlotte Duvette, Louise Thiroux, Justine Gain,
        Teoman Akgönül, Esther Da Silva et Louise Baranger</dd>
      <dt>Remerciements</dt>
      <dd>Pour leur aide à l'élaboration, au développement et au suivi du projet,
        l'équipe adresse ses remerciements à&nbsp;:
        <strong>Jean-Christophe Carius</strong> (INHA),
        <strong>Manuel Charpy</strong> (CNRS, InVisu),
        <strong>Éric Mermet</strong> (CNRS, Paris Time Machine),
        <strong>Laurent Costa</strong> (CNRS, Paris Time Machine),
        <strong>Jean-Philippe Moreux</strong> (Bibliothèque nationale de France)
      </dd>
    </dl>
  </div>

  <div class="textpage-text-wrapper">
    <h3 id="abdoc-mentions">Mentions légales</h3>
    <dl>
      <dt>Propriétaire du site</dt>
      <dd>Institut national d'histoire de l'art (INHA),
        2 rue Vivienne, 75002, Paris&nbsp;; tél&nbsp;:
        +33&nbsp;(0)&nbsp;1&nbsp;47&nbsp;03&nbsp;89&nbsp;00
      </dd>
      <dt>Directeur de la publication</dt>
      <dd>Éric de Chassey, directeur général de l'INHA</dd>
      <dt>Équipe éditoriale</dt>
      <dd>
        <ul>
          <li><strong>Charlotte Duvette</strong>,
            chercheuse postdoctorante et responsable scientifique
            du programme <i>Richelieu. Histoire du quartier</i>&nbsp;</li>
          <li><strong>Paul Kervegan</strong>, ingénieur d'études au
            sein du projet <i>Richelieu</i>&nbsp;</li>
          <li><strong>Louise Thiroux</strong>, doctorante et chargée
            d'études documentaires au sein du projet</li>
        </ul>
      </dd>
      <dt>Hébergeur</dt>
      <dd>INHA, 2 rue Vivienne, 75002 Paris&nbsp;; tel&nbsp;:
        +33&nbsp;(0)1&nbsp;47&nbsp;03&nbsp;89&nbsp;00</dd>
      <dt>Conception et réalisation du site</dt>
      <dd>Paul Kervegan et Marina Hervieu
        (<a href="https://www.inha.fr/fr/recherche/le-departement-des-etudes-et-de-la-recherche/service-numerique-de-la-recherche.html">Service
          numérique de la Recherche &mdash; INHA</a>)</dd>
      <dt>Conditions de réutilisation des données du site</dt>
      <dd>
        <p>L'ensemble des contenus et des métadonnées disponibles sur
          le site est placé sous licence
          <a href="https://creativecommons.org/licenses/by/4.0/">Creative
          Commons Attribution 4.0</a>, sauf mention contraire.
        </p>
        <p>Le code source de ce site est diffusé sous licence libre
          <a href="https://www.gnu.org/licenses/gpl-3.0.html">GNU GPL v3.0</a>.</p>
        <p>Voir <RouterLink to="/documentation/donnees">la page dédiée à ce
          sujet</RouterLink> dans la documentation pour plus d'informations.</p>
      </dd>
    </dl>
  </div>

</template>


<script setup>
import { onMounted } from "vue";

/****************************************/

const emit     = defineEmits(["h2"]);
const subtitle = "Crédits et mentions légales";

/****************************************/

onMounted(() => emit("h2", subtitle))
</script>


<style scoped>

</style>
