<template>
  <div class="textpage-text-wrapper">
    <h3 id="abdoc-data-pres">En bref</h3>
    <p>Le project <i>Richelieu</i> donne accès aux données de la recherche
      produites et réutilisées, ainsi qu'au code et aux outils numériques
      produits, sous des licences libres. L'ensemble des données du projet
      sont disponibles sous licence <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode.fr">
        Creative Commons CC BY-BC-SA 4.0</a>.
    </p>
  </div>
  <div class="textpage-text-wrapper">
    <h3 id="abdoc-data-cite-data">Citer les données</h3>
    <p>Pour accéder aux données brutes, une
      <RouterLink to="/documentation/api">API</RouterLink>
      est disponible et permet une réutilisation facile. Un <i>datapaper</i>
      est en cours de constitution pour faciliter la réutilisation des données
      du projet.</p>
    <p>Les données sont diffusées sous licence
      <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode.fr">
        Creative Commons CC BY-BC-SA 4.0</a>,
      qui permet le partage, la réutilisation et la modification des données,
      aux conditions suivantes&nbsp;:
    </p>
    <ul>
      <li>Attribution des données au projet <i>Richelieu</i>, et indication
        des modifications apportées</li>
      <li>La réutilisation doit être limitée à des usages non-commerciaux</li>
      <li>Les réutilisations et modifactions des données présentées dans
        ce site doivent également être partagées sous licence CC BY-BC-SA 4.0.
      </li>
      <li>Il n'est pas possible d'ajouter des restrictions additionnelles
        en réutilisant des données de ce projet.</li>
    </ul>
    <p>Pour citer les données du projet&nbsp;:</p>
    <div class="multi-line-quote-wrapper">
      <q><div class="csl-bib-body">
        <div data-csl-entry-id="duvette_richelieu_2024" class="csl-entry">
          Duvette, C., Thiroux, L., Gain, J., Kervegan, P., Akgönül, T.,
          Dasilva, E., &#38; Baranger, L. (2024).
          <i>Richelieu. Histoire du quartier (données de recherche)</i> (1.0).
          <a href="https://quartier-richelieu.inha.fr">https://quartier-richelieu.inha.fr</a></div>
        </div></q>
    </div>
    <div class="multi-line-quote-wrapper">
      <code><pre>
 <!---->@misc{duvette_richelieu_2024,
 <!---->      title = {Richelieu. Histoire du quartier (données de recherche)},
 <!---->      rights = {Licence {CC} {BY}-{NC}-{SA} 4.0},
 <!---->      url = {https://quartier-richelieu.inha.fr},
 <!---->      version = {1.0},
 <!---->      author = {Duvette, Charlotte and Thiroux, Louise and Gain, Justine and Kervegan, Paul and Akgönül, Teoman and Dasilva, Esther and Baranger, Louise},
 <!---->      urldate = {2023-11-10},
 <!---->      date = {2024},
 <!---->      langid = {french},
 <!---->}
      </pre></code>
    </div>
  </div>
  <div class="textpage-text-wrapper">
    <h3 id="abdoc-data-cite-data">Citer le site et le code</h3>
    <p>L'intégralité des outils produits par le projet <i>Richelieu</i> sont
      accessibles sur le dépôt <a href="https://gitlab.inha.fr/snr/rich.data/">
        GitLab de l'INHA</a>. Plus spécifiquement, le code du site est disponible
      à <a href="https://gitlab.inha.fr/snr/rich.data/application">cette addresse</a>.
    </p>
    <p>Le code produit par le projet <i>Richelieu</i> est rendu disponible sous la
      licence libre <a href="https://www.gnu.org/licenses/gpl-3.0.html">GNU GPL v. 3.0</a>.
    </p>
    <p>Pour citer le site&nbsp;:</p>
    <div class="multi-line-quote-wrapper">
      <q><div class="csl-bib-body">
        <div data-csl-entry-id="kervegan_richelieu_2024" class="csl-entry">
          Kervegan, P., Hervieu, M., Duvette, C., Thiroux, L., Gain, J., Akgönül, T.,
          Dasilva, E., &#38; Baranger, L. (2024). <i>Richelieu. Histoire du quartier
          (site)</i> (1.0). 2024-11.
          <a href="https://gitlab.inha.fr/snr/rich.data/application">https://gitlab.inha.fr/snr/rich.data/application</a></div>
      </div></q>
    </div>
    <div class="multi-line-quote-wrapper">
      <code><pre>
<!---->@software{kervegan_richelieu_2024,
<!---->          title = {Richelieu. Histoire du quartier (site)},
<!---->          rights = {Licence {GNU} {GPL} v3.0},
<!---->          url = {https://gitlab.inha.fr/snr/rich.data/application},
<!---->          version = {1.0},
<!---->          publisher = {2024-11},
<!---->          author = {Kervegan, Paul and Hervieu, Marina and Duvette, Charlotte and Thiroux, Louise and Gain, Justine and Akgönül, Teoman and Dasilva, Esther and Baranger, Louise},
<!---->          editoratype = {collaborator},
<!---->          urldate = {2024-11-12},
<!---->          date = {2024-11},
<!---->}
      </pre></code>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from "vue";

/****************************************/

const emit = defineEmits(["h2"]);
const subtitle = "Ouverture et réutilisation des données";

/****************************************/

onMounted(() => emit("h2", subtitle))

</script>

<style scoped>
.multi-line-quote-wrapper {
  font-style: normal;
  border: var(--cs-main-border);
  margin: 5%;
  padding: 2% 5%;
}
code {
  font-size: 80%;
}
pre {
  overflow: scroll;
  max-width: 100%;
  margin: 0;
}
</style>