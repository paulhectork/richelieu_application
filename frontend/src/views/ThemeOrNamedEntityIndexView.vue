<!--  ThemeViewOrNamedEntityIndexView.vue
      an index page for all themes or named entities in a category

      see the documentation of ThemeOrNamedEntityCategoryIndexView.vue
      for a more global outlook on the logic.

      props and refs:
        tableName (prop):
        categoryName (props):
        apiTarget (computed property):
-->

<template>
  <div v-if="loadState === 'error'">
    <ErrNotFound></ErrNotFound>
  </div>
  <div v-else>

    <h1>Index des
      {{ tableName === "theme" ? "thèmes" : "entités nommées" }}&nbsp;:
      {{ capitalizeFirstChar(categoryName) }}</h1>

    <!-- presentation text for each category -->
    <div v-if="tableName === 'theme'">
      <p v-if="categoryName==='s\'habiller'">
        La question de l'habillement revêt des significations
        plurielles dans le quartier Richelieu. Elle peut d'abord
        être comprise comme un acte de confection pour autrui,
        en écho avec la forte concentration de tailleurs, de
        marchandes de mode et de nouveautés dans le quartier,
        acteurs majeurs du développement économique de la ville.
        En parallèle, ce savoir-faire, ancré dans ce territoire
        depuis le XVIII<sup>e</sup> siècle, se redouble d'un véritable
        faire-savoir auquel les éditeurs et libraires locaux
        participent en publiant et vendant bon nombre de gravures
        de mode. Haut lieu de la promenade urbaine, mais aussi
        de l'activité salariale, ce cas d'étude permet de retracer
        l'essor et les mutations socio-économiques et matérielles
        de la culture des apparences en milieu urbain. Enfin,
        cette activité, loin de se cantonner aux corps, contribue
        aussi à draper la ville d'un épais et éclectique manteau
        de boutiques, contribuant alors à lier cette notion
        à sa spatialité, son architecture et sa propension
        à faire espace public.</p>
     <p v-if="categoryName==='se divertir'">
        La densité et la variété des activités de divertissement
        qui ont eu lieu dans le quartier Richelieu se perçoivent
        à travers l'abondante production graphique qu'elles
        ont suscité. Les grands et petits spectacles joués
        dans l'espace public ou derrière les portes de la dizaine
        de salles concentrées à l'échelle de quelques rues,
        sont révélés à l'analyse des affiches promotionnelles,
        des vues et des photographies liées aux représentations.
        Plusieurs gravures et dessins rappellent également
        l'importance de ces lieux en matière de sociabilités
        et plus précisément de mondanités. L'iconographie autour
        du théâtre renforce cette image d'une institution dont
        le rapport au loisir était loin d'être cantonné à la
        seule performance artistique de la scène. La musique,
        notamment sous la forme de partitions publiées chez
        les éditeurs spécialisés installés rue Vivienne, fait
        aussi écho aux salles de concert et aux soirées musicales.
        Enfin, l'activité des théâtres, à travers les tickets
        d'entrée et la production de décors ou de costumes,
        éclaire le parcours de certains acteurs et actrices.</p>
      <p v-if="categoryName==='représenter'">
        Ce thème est articulé autour des différents supports
        rendant présent à la vue, mais aussi à l'esprit le
        quartier Richelieu dans toute sa volubilité et sa volatilité.
        Bien avant d'être le réceptacle de l'Agence France-Presse,
        anciennement Havas, les alentours de la place de la
        Bourse et du Palais-Royal sont des espaces où le papier
        règne en maître, rendant ainsi nécessaire d'intégrer
        les éditeurs, imprimeurs et titres de presse à notre
        champ d'étude afin de restituer les réseaux du papier
        dans leur temporalité et leur spatialité. Représenter,
        c'est aussi donner à voir sous la forme d'un substitut,
        leitmotiv des nombreux photographes qui vendent et
        produisent des images du quartier et de ses activités,
        esquissant ainsi des clés de lecture quant à la dimension
        sociale, matérielle et symbolique de ce territoire.
        Représenter est également un moyen d'attirer l'attention
        sur une réalité, parfois peu glorieuse, prérequis des
        caricatures qui, par un humour au vitriol, permettent
        d'infléchir le regard sur les mœurs urbaines. Enfin,
        représenter revient à exprimer matériellement une réalité
        abstraite, voire fantasmée, grand œuvre des cartes
        postales dont les angles de vue orientent les perceptions
        du quartier, contribuant à le figer dans son image
        d'Épinal.</p>
      <p v-if="categoryName==='s\'informer'">
        L'information est, dans ce cadre thématique, intimement
        liée à la dimension politique et historique des différents
        évènements survenus dans le quartier Richelieu. Si
        l'iconographie constitue une fenêtre presque anecdotique
        et ponctuelle sur certains faits qui se sont déroulés
        dans le quartier, à l'instar de bals ou de rencontres
        sportives, elle contribue aussi à donner une forme,
        une structure signifiante à des moments marquants de
        l'Histoire nationale. Parmi ces épisodes cruciaux,
        on dénombre la Révolution française, la révolution
        de juillet 1830, la révolution de 1848 et enfin, la
        Commune de Paris. Le fait d'informer peut être compris
        comme une transmission ou une communication de renseignements
        dans le cas de la Révolution française, dont nous pouvons
        restituer par l'image une chronologie fine. Mais il
        n'en va pas de même pour d'autres révolutions. Le cas
        de la Commune est emblématique de la façon dont l'iconographie
        se plaît à nourrir la désinformation par l'exagération,
        notamment au sujet de l'incendie du Palais-Royal en
        mai 1871. Ce thème accompagne alors les relectures
        historiographiques du récit national par l'entremise
        d'une approche située de la ville.</p>
      <p v-if="categoryName==='consommer'">La notion de consommation fait
        écho à la forte densité des activités économiques recensées dans
        les rues du quartier au XIX<sup>e</sup> siècle. La bourse installée au palais
        Brongniart est l'emblème du dynamisme commercial qui s'empare des
        rues adjacentes où se déroulent diverses transactions&nbsp;:
        banques, alimentation, vente d'objets, ou hygiène et soins du corps.
        Les secteurs sont variés et aisément identifiables à la lecture des
        enseignes, devantures de boutiques, et affiches promotionnelles qui
        abondent dans le corpus iconographique. Si les noms des commerces
        et les marchandises proposées sont parfois au premier plan des
        documents, une analyse plus approfondie des alignements de boutiques
        placés en toile de fond de certaines estampes et photographies
        améliore notre compréhension de la ville commerçante. Les gammes de
        prix et les prestations mises en avant par les commerçants
        fournissent des informations supplémentaires sur les mentalités
        de la réclame publicitaire et sur l'évolution du niveau de vie.
        Les brevets d'invention quant à eux soulignent les innovations à
        l'œuvre et la dimension créatrice du développement économique.</p>
      <p v-if="categoryName==='habiter'">Habiter est envisagé au sens
        large, englobant à la fois les espaces privés et publics qui
        composent le cadre de la vie quotidienne des citadins et des
        citadines qui habitent ou fréquentent le quartier. Le dialogue
        entre l'espace public, la nature, et l'évolution des formes
        architecturales, qu'elles soient existantes ou projetés, se révèle
        à travers divers médiums, des estampes aux photographies.
        L'architecture domestique, tout comme celle des monuments, est
        explorée à travers des documents graphiques produits par des
        architectes et des entrepreneurs identifiés et met en lumière
        aussi bien les grands édifices institutionnels que les habitations
        plus modestes. Le laboratoire de l'urbain s'enrichit par une
        attention portée à l'équipement de la ville, à travers la
        modernisation du mobilier urbain, l'amélioration des réseaux et
        moyens de transports, et la représentation de chantiers&nbsp;: un
        dynamisme qui capte l'attention des observateurs. C'est un aperçu
        de la fabrique de la ville, telle qu'elle a été conçue et vécue
        par ses contemporains.</p>
    </div>
    <div v-else>
      <!--
      <p v-if="categoryName === 'acteurs et actrices'"></p>
      <p v-if="categoryName === 'banques'"></p>
      <p v-if="categoryName === 'cafés et restaurants'"></p>
      <p v-if="categoryName === 'commerces'"></p>
      <p v-if="categoryName === 'épiceries et alimentation'"></p>
      <p v-if="categoryName === 'évènements'"></p>
      <p v-if="categoryName === 'institutions et organisations'"></p>
      <p v-if="categoryName === 'mode et objets'"></p>
      <p v-if="categoryName === 'personnalités et fiction'"></p>
      <p v-if="categoryName === 'publications et photographies'"></p>
      <p v-if="categoryName === 'santé'"></p>
      <p v-if="categoryName === 'théâtres et spectacles'"></p>
      <p v-if="categoryName === 'ville et architecture'"></p>
      -->
    </div>

    <UiLoader v-if="loadState === 'loading'"></UiLoader>
    <IndexBase v-else
           :display="display"
           :data="dataFilter"
    ></IndexBase>

  </div>

</template>

<script setup>
import { onMounted, ref, computed, watch } from "vue";
import { useRoute } from "vue-router";
import axios from "axios";

import { indexDataFormatterTheme
       , indexDataFormatterNamedEntity } from "@utils/indexDataFormatter";
import { capitalizeFirstChar } from "@utils/strings";

import UiLoader from "@components/UiLoader.vue";
import ErrNotFound from "@components/ErrNotFound.vue";
import IndexBase from "@components/IndexBase.vue";

/*************************************************************/

const route        = useRoute();
const props        = defineProps(["tableName"]);

const tableName    = ref(props.tableName);
const categoryName = ref(decodeURIComponent(route.params.categoryName));
const dataFull     = ref([]);         // the full index, independent of user filters
const dataFilter   = ref([]);         // the data to pass to `IndexBase.vue`. this can depend on user-defined filters. an array of { href: <url to redirect to when clicking on an item>, img: <url to the background img to display>, text, <text to display> }
const loadState    = ref("loading");  // toggled to true when data has loaded, hides the loader
const display      = "concept";       // define the view to use in `IndexItem`

const apiTarget = computed(() =>  // defined as a computed property to avoid manually updating the url on tableName.value's change.
  tableName.value === "theme"
  ? new URL("/i/theme", __API_URL__)
  : new URL("/i/named-entity", __API_URL__));

/*************************************************************/

/**
 * reset all global variables when changing page without reloading
 */
function resetView() {
  tableName          = props.tableName;
  dataFull.value     = [];
  dataFilter.value   = [];
  categoryName.value = route.params.categoryName;
}

/**
 * get backend data: fetch all theme or iconography
 * resources for a single category
 */
function getData() {
  axios.get(apiTarget.getter().href, { params: {category:categoryName.value} })
  .then(r => r.data)
  .then(data => { dataFull.value = data;
                  dataFilter.value = tableName.value === "theme"
                                     ? indexDataFormatterTheme(data)
                                     : indexDataFormatterNamedEntity(data);
                  loadState.value = "loaded";
                })
  .catch(e => { console.error(e);
                loadState.value = "error"
              });
}

/*************************************************************/

watch(props, (oldProps, newProps) => {
  resetView();
  getData();
})

onMounted(() => {
  getData();
})
</script>

<style scoped>

</style>