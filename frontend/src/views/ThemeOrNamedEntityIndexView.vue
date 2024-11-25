<!--  ThemeViewOrNamedEntityIndexView.vue
    an index page for all themes or named entities in a category

    lifecycle:
    - the parent `ThemeOrNamedEntityCategoryIndexView`,, redirects
        to this component to display an index of all themes / named entities.
        the URL defines 1 argument/path (compulsory) and 1 parameter (optional):
        - path: <categorySlug>: only themes/named entities from this category will
            be displayed.
        - viewType: a parameter that allows to switch between collection and tree view.
    - on page load or when route parameter changes without a full-page reload
        (for example, clicking on a button in the menu), `initViewHook()` is called.
        it resets all refds to their start state and fetches data based on URL data
    - 2 controllers allow to switch the values of `categorySlug` and `viewType` by
        triggering 2 functions:
         - `changeCategory()` will switch from one category to another
         - `changeViewType()` will switch from "collection"|"tree" view and back.
         - both functions update the route's URL, the refs and fetch backend data

    props :
    - tableName (String)
        "theme"|"named_entity"

    url path and parameter:
    - categorySlug (path, parameter, String)
        a value of theme.category_slug, or named_entity.category_slug or "all".
        used to target a themes/named entities from a specific category. if "all",
        then all values are fetched from the backend
    - viewType (parameter, optional, String)
        "collection"||"tree", defaults to "collection"
        this parameter decides if we'll display a collection of items with images,
        or a tree of category/category-items  with just the name of the item.
-->

<template>
  <div v-if="loadState === 'error'">
    <ErrNotFound></ErrNotFound>
  </div>
  <div v-else>

    <div class="title-controller-wrapper">
      <div class="title-wrapper">
        <h1>Index des
          {{ tableName === "theme" ? "thèmes" : "entités nommées" }}&nbsp;:
          {{ capitalizeFirstChar(categoryName) }}</h1>
        <IndexCount v-if="loadState === 'loaded'"
                    :indexCount="viewType === 'collection'
                                ? dataCollectionFull.length
                                : dataTree.reduce((count, currentCategory) =>
                                   count + currentCategory.entries.length, 0)"
                    :dataType="tableName"></IndexCount>
      </div>

      <div class="view-controller-wrapper">
        <FormKit v-if="categories.length"
                 type="fkSelect"
                 name="categoryControl"
                 id="category-control"
                 label="Changer de catégorie"
                 :multiple="false"
                 :value="categorySlug"
                 :placeholder="categoryName"
                 :options="categories.map(c => {
                    return { value: c.category_slug, label: c.category_name } })"
                 @input="changeCategory"
        ></FormKit>
        <FormKit v-if="viewType"
                 type="fkRadioTabs"
                 name="viewTypeSetter"
                 id="view-type-control"
                 label="Changer le type de vue"
                 :help="`Définir la vue des ${tableName === 'theme' ? 'thèmes' : 'entités nommées'}`"
                 :value="viewType"
                 :options="[ { value: 'collection', label: 'collection' }
                           , { value: 'tree', label: 'arborescence' }]"
                 @input="changeViewType"
        ></FormKit>
      </div>
    </div>


    <!-- presentation text for each category -->
    <div v-if="tableName === 'theme'"
         class="index-headtext-wrapper">
      <p v-if="categorySlug === 's-habiller'">
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
      <p v-if="categorySlug === 'se-divertir'">
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
      <p v-if="categorySlug === 'representer'">
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
      <p v-if="categorySlug === 's-informer'">
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
      <p v-if="categorySlug === 'consommer'">La notion de consommation fait
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
      <p v-if="categorySlug === 'habiter'">Habiter est envisagé au sens
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
    <div v-else class="index-headtext-wrapper">
      <!--
      <p v-if="categorySlug === 'acteurs-et-actrices'"></p>
      <p v-if="categorySlug === 'banques'"></p>
      <p v-if="categorySlug === 'cafes-et-restaurants'"></p>
      <p v-if="categorySlug === 'commerces'"></p>
      <p v-if="categorySlug === 'epiceries-et-alimentation'"></p>
      <p v-if="categorySlug === 'evenements'"></p>
      <p v-if="categorySlug === 'institutions-et-organisations'"></p>
      <p v-if="categorySlug === 'mode-et-objets'"></p>
      <p v-if="categorySlug === 'personnalites-et-fiction'"></p>
      <p v-if="categorySlug === 'publications-et-photographies'"></p>
      <p v-if="categorySlug === 'sante'"></p>
      <p v-if="categorySlug === 'theatres-et-spectacles'"></p>
      <p v-if="categorySlug === 'ville-et-architecture'"></p>
      -->
    </div>

    <UiLoader v-if="loadState === 'loading'"></UiLoader>
    <div v-else-if="loadState === 'loaded'">
      <div v-if="viewType === 'collection'">
        <FilterIndexThemeOrNamedEntity v-if="dataCollectionFull.length"
                                      :data="dataCollectionFull"
                                      @theme-or-named-entity-filter="handleFilter"
        ></FilterIndexThemeOrNamedEntity>

        <IndexBase v-if="viewType === 'collection'"
                  :display="display"
                  :data="dataCollectionFilter"
        ></IndexBase>
      </div>

      <div v-else-if="viewType === 'tree'" class="tree-wrapper">
        <ul class="tree-category list-invisible">
          <li v-for="category in dataTree.sort((a, b) =>
                      a.category.localeCompare(b.category))"
              class="category-wrapper">
            <span class="category-title">
              Catégorie&nbsp;:
              <RouterLink :to="tableName === 'theme'
                               ? urlToFrontendThemeCategory(category.category_slug).pathname
                               : urlToFrontendNamedEntityCategory(category.category_slug).pathname"
                           v-html="category.category"
                           class="tree-category-name"
              ></RouterLink>
              ({{ category.entries.length }}
              {{ category.entries.length != 1 ? "entrées" : "entrée" }})
            </span>
            <ul class="category-entries">
              <li v-for="item in category.entries.sort((a, b) =>
                          a.entry_name.localeCompare(b.entry_name))"
                  class="category-entry">
                <RouterLink :to="tableName === 'theme'
                                 ? urlToFrontendTheme(category.category_slug, item.id_uuid).pathname
                                 : urlToFrontendNamedEntity(category.category_slug, item.id_uuid).pathname"
                            v-html="item.entry_name"
                ></RouterLink>
              </li>
            </ul>
          </li>
        </ul>
      </div>
    </div>

  </div>

</template>

<script setup>
import { onMounted, ref, computed, watch } from "vue";
import { useRoute, useRouter } from "vue-router";

import axios from "axios";

import UiLoader from "@components/UiLoader.vue";
import IndexBase from "@components/IndexBase.vue";
import IndexCount from "@components/IndexCount.vue";
import ErrNotFound from "@components/ErrNotFound.vue";
import FilterIndexThemeOrNamedEntity from "@components/FilterIndexThemeOrNamedEntity.vue";

import { urlToFrontendTheme
       , urlToFrontendNamedEntity
       , urlToFrontendThemeCategory
       , urlToFrontendNamedEntityCategory } from "@utils/url.js";
import { indexDataFormatterTheme
       , indexDataFormatterNamedEntity } from "@utils/indexDataFormatter";
import { capitalizeFirstChar } from "@utils/strings";

/*************************************************************/

const route   = useRoute();
const router  = useRouter();
const props   = defineProps(["tableName"]);
const display = "concept";       // define the view to use in `IndexItem`

const tableName            = ref();    // (string) "theme"|"namedEntity"
const viewType             = ref();    // (string) "collection"|"tree". the kind of display to use. defaults to "collection"
const categorySlug         = ref();    // (string) theme.category_slug or named_entity.category_slug of "all" if we want to retrieve all themes/named entities
const categoryName         = ref()     // (string) theme.category or named_entity.category or "tout" if categorySlug === 'all'
const categories           = ref([]);  // (Array<Object>) : all allowed categories. an array of { category_name: String, category_slug: String }
const dataCollectionFull   = ref([]);  // (Array<Object>) the full index when viewType==='collection', independent of user filters
const dataCollectionFilter = ref([]);  // (Array<Object>) the data to pass to `IndexBase.vue` when viewType==='collection'. this can depend on user-defined filters. an array of { href: <url to redirect to when clicking on an item>, img: <url to the background img to display>, text, <text to display> }
const dataTree             = ref([]);  // (Array<Object>) the data when viewType==='tree'

const loadState = ref("loading");  // toggled to true when data has loaded, hides the loader


/*************************************************************/
/** DATA FETCHING */

/**
 * get the category name for the current category,
 * based on the value of `categorySlug`.
 * 2 fallbacks:
 *  - if `categorySlug==='all'`, then use a default category name
 *  - if `apiTarget` returns an empty string, then categorySlug is
 *    not found on the database. then, `categoryName` falls back
 *    to the value of `categorySlug`
 */
function getCurrentCategoryName() {
  if (categorySlug.value === "all") {
    categoryName.value = "toutes catégories confondues"
  } else {
    const apiTarget = tableName.value === "theme"
      ? new URL(`/i/theme/category/name/${categorySlug.value}`, __API_URL__)
      : new URL(`/i/named-entity/category/name/${categorySlug.value}`, __API_URL__);
    axios.get(apiTarget)
      .then(r => r.data)
      .then(data => categoryName.value = data.length
                    ? data
                    : categorySlug.value)
      .catch(e => {
        console.error(e);
        categoryName.value = categorySlug.value
      });
  }
}

/**
 * get all allowed categories for the Theme|NamedEntity table.
 * structure: <Array<{ category_name: String, category_slug: String }>>
 */
function getCategories() {
  const apiTarget = tableName.value === "theme"
                  ? new URL(`/i/theme/category/name/all`, __API_URL__)
                  : new URL(`/i/named-entity/category/name/all`, __API_URL__);
  axios.get(apiTarget)
  .then(r => r.data)
  .then(data => {
    categories.value = [ { category_name: "tout voir", category_slug: "all" }, ...data ];
  })
  .catch(e => {
    console.error(e);
    categories.value = []
  });
}

/**
 * get backend data when `viewType === 'tree'`: fetch a tree of
 * data for a category or for all categories.
 */
function getDataTree() {
  const apiTarget = tableName.value === "theme"
                  ? new URL(`/i/theme/tree/${categorySlug.value}`, __API_URL__)
                  : new URL(`/i/named-entity/tree/${categorySlug.value}`, __API_URL__);
  axios.get(apiTarget)
  .then(r => r.data)
  .then(data => {
    dataTree.value = data;
    loadState.value = "loaded"
  })
  .catch(e => {
    console.error(e);
    loadState.value = "error"
  });

}

/**
 * get backend data when `viewType === 'collection'`:
 * fetch all theme or iconography resources for a single category
 * (or for all categories, if `categorySlug === "all"`).
 */
function getDataCollection() {
  const apiTarget = tableName.value === "theme"
    ? new URL("/i/theme", __API_URL__)
    : new URL("/i/named-entity", __API_URL__);
  axios.get(apiTarget.href, { params: { category_slug: categorySlug.value } })
    .then(r => r.data)
    .then(data => {
      dataCollectionFull.value = data;
      dataCollectionFilter.value = tableName.value === "theme"
                                 ? indexDataFormatterTheme(data)
                                 : indexDataFormatterNamedEntity(data);
      loadState.value = "loaded";
    })
    .catch(e => {
      console.error(e);
      loadState.value = "error"
    });
}

/*************************************************************/
/** FRONTEND FILTERING */

/**
 * when `FilterIndexThemeOrNamedEntity` emits a new array of
 * filtered Theme or NamedEntity objects, update `dataCollectionFilter`.
 *
 * @param {Array<Object>} filteredData: the new filtered array of
 *    Iconography or NamedEntity objects
 */
function handleFilter(filteredData) {
  dataCollectionFilter.value = tableName.value === "theme"
                             ? indexDataFormatterTheme(filteredData)
                             : indexDataFormatterNamedEntity(filteredData);
}


/*************************************************************/
/** HOOKS: CHANGE STATE (VIEWTYPE OR CATEGORY) */

/**
 * hook to handle a change of `cateogry`.
 * when the user inputs new data on `#category-control`,
 * change the category: update the router, reset the refs and fetch backend data.
 * @param {String} newCategorySlug: the new `(theme|named_entity).category_slug`
 */
function changeCategory(newCategorySlug) {
  if ( newCategorySlug && newCategorySlug.length && newCategorySlug !== categorySlug ) {
    let newPath = route.path.replace(/[^\/]+$/g, newCategorySlug);  // nice A Scanner Darkly reference :)
    router.replace({ path: newPath, query: { viewType: viewType.value } });
    categorySlug.value         = newCategorySlug
    dataCollectionFull.value   = [];
    dataCollectionFilter.value = [];
    dataTree.value             = [];
    loadState.value            = "loading";
    // fetch the new data
    getCurrentCategoryName();
    if (viewType.value === "collection") getDataCollection();
    else getDataTree();
  }
}

/**
 * hook to handle a change of `viewType`.
 * when the user inputs new data on `#view-type-control`,
 * change the view type (`collection` or `tree`):
 * update the router, reset the necessary refs and fetch backend data.
 * @param {String} newViewType: "collection" || "tree"
 */
function changeViewType(newViewType) {
  if ( newViewType && newViewType.length && newViewType !== viewType.value ) {
    // update the refs and the URL to fit the new state
    router.replace({ query: { viewType: newViewType } });
    viewType.value             = newViewType;
    dataCollectionFull.value   = [];
    dataCollectionFilter.value = [];
    dataTree.value             = [];
    loadState.value            = "loading";
    // fetch the new data
    if (newViewType === "collection") getDataCollection();
    else getDataTree();
  }
}

/**
 * set all global variables to their start state.
 */
 function resetRefs() {
  // check that viewType is valid.
  let newViewType = route.query.viewType || "collection";
  if (!["tree", "collection"].includes(newViewType)) {
    if (__MODE__ === "DEV") console.error(`ThemeOrNamedEntityIndexView.resetRefs() : expected one of ['collection', 'tree'] for 'route.query.viewType', got '${newViewType}'. defaulting to 'collection'`);
    newViewType = "collection";
  }
  tableName.value            = props.tableName;
  viewType.value             = newViewType;
  categorySlug.value         = decodeURIComponent(route.params.categorySlug);
  categoryName.value         = "";
  categories.value           = [];
  dataCollectionFull.value   = [];
  dataCollectionFilter.value = [];
  dataTree.value             = [];
  loadState.value            = "loading";
}

/**
 * hook to reset all refs and fetch back all data (basically
 * a combination of `changeViewType` and `changeCategory`)
 */
function initViewHook() {
  resetRefs();
  getCategories();
  getCurrentCategoryName();
  if (viewType.value === "collection") getDataCollection();
  else getDataTree();
}

/*************************************************************/

watch(props, (oldProps, newProps) => {
  initViewHook()
})

onMounted(() => {
  initViewHook();
})
</script>

<style scoped>
h1 {
  margin-bottom: 5px;
}

.title-controller-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-between;
}
.view-controller-wrapper {
  width: 90%;
  height: 100%;
}

@media (min-width: 800px) {
  .title-controller-wrapper {
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
  }
  .view-controller-wrapper {
    width: auto;
  }
}

/************************************/

.view-controller-wrapper {
  margin: 10px;
}
.view-controller-wrapper :deep(.formkit-wrapper) {
  min-width: 300px;
}
.view-controller-wrapper :deep(.formkit-help) {
  visibility: hidden;
  height: 0;
}

/************************************/

.tree-wrapper {
  /** PROBLEM: NOT WIDE ENOUGH  */
  width: auto;
  margin: 0 5%;
  border: var(--cs-main-border);
  background-color: lavender;
}

.tree-wrapper li {
  width: 100%;
}

.category-title {
  position: relative;
  display: inline-block;
  width: 100%;
  border-top: var(--cs-main-border);
  border-bottom: var(--cs-main-border);
  padding: 10px;
  margin: 10px 0;
}

.category-wrapper:first-child>.category-title {
  border-top: none;
  margin-top: 0;
}
</style>