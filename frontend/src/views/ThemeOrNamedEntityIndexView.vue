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
      {{ capitalizeString(categoryName) }}</h1>

    <!-- presentation text for each category -->
    <div v-if="tableName === 'theme'">
      <p v-if="categoryName==='consommer'">La notion de consommation fait
        écho à la forte densité des activités économiques recensées dans
        les rues du quartier au XIXe siècle. La bourse installée au palais
        Brongniart est l'emblème du dynamisme commercial qui s'empare des x
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
        moyens de transports, et la représentation de chantiers : un
        dynamisme qui capte l'attention des observateurs. C'est un aperçu
        de la fabrique de la ville, telle qu'elle a été conçue et vécue
        par ses contemporains.</p>
      <p v-if="categoryName==='représenter'"></p>
      <p v-if="categoryName==='se divertir'"></p>
      <p v-if="categoryName==='s\'habiller'"></p>
      <p v-if="categoryName==='s\'informer'"></p>
    </div>
    <div v-else>
      <p v-if="categoryName === 'acteurs et actrices'">1</p>
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
    </div>

    <UiLoaderComponent v-if="loadState === 'loading'"></UiLoaderComponent>
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
import {capitalizeString} from "@utils/stringifiers";

import UiLoaderComponent from "@components/UiLoaderComponent.vue";
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