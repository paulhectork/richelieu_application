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
        it resets all refs to their start state and fetches data based on URL data
    - 2 controllers allow to switch the values of `categorySlug` and `viewType` by
        triggering 2 functions:
         - `changeCategory()` will switch from one category to another
         - `changeViewType()` will switch from "collection"|"tree" view and back.
         - both functions update the route's URL, which will trigger watchers to
           update the necessary refs and fetch backend data

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

    <div class="title-controller-wrapper"
        :style="{ 'align-items': loadState === 'loading' ? 'start' : 'center' }"
    >
      <div class="title-wrapper">
        <h1>Index des
          {{ tableName === "theme" ? "thèmes" : "entités nommées" }}&nbsp;:
          {{ capitalizeFirstChar(categoryName) }}</h1>
        <H2IndexCount v-if="loadState === 'loaded'"
                      :indexCount=" viewType === 'collection'
                                  ? dataCollectionFull.length
                                  : dataTree.reduce((count, currentCategory) =>
                                     count + currentCategory.entries.length, 0)"
                      :dataType="tableName"
        ></H2IndexCount>
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
      <div>
        <p v-html="themeCategoryPresentation[categorySlug]"></p>
      </div>
    </div>
    <div v-else class="index-headtext-wrapper">
      <!-- not yet implemented: named entity category presentations don't exist -->
    </div>

    <UiLoader v-if="loadState === 'loading'"></UiLoader>
    <div v-else-if="loadState === 'loaded'"
         class="animate__animated animate__slideInLeft"
    >
      <div v-if="viewType === 'collection'">
        <div class="fitler-outer-wrapper">
          <FilterIndexThemeOrNamedEntity v-if="dataCollectionFull.length"
                                        :data="dataCollectionFull"
                                        @theme-or-named-entity-filter="handleFilter"
          ></FilterIndexThemeOrNamedEntity>
        </div>

        <IndexBase v-if="viewType === 'collection'"
                  :display="display"
                  :data="dataCollectionFilter"
        ></IndexBase>
      </div>

      <div v-else-if="viewType === 'tree'" class="tree-outer-wrapper">
        <TreeComponent :data="dataTreeRestructured"
                       v-if="dataTreeRestructured.length"
        ></TreeComponent>
      </div>
    </div>

  </div>

</template>

<script setup>
import { onMounted, ref, watch, computed } from "vue";
import { useRoute, useRouter } from "vue-router";

import axios from "axios";
import _ from "lodash";

import UiLoader from "@components/UiLoader.vue";
import IndexBase from "@components/IndexBase.vue";
import H2IndexCount from "@components/H2IndexCount.vue";
import ErrNotFound from "@components/ErrNotFound.vue";
import FilterIndexThemeOrNamedEntity from "@components/FilterIndexThemeOrNamedEntity.vue";
import TreeComponent from "@components/TreeComponent.vue";

import { themeCategoryPresentation } from "@globals";
import { urlToFrontendTheme
       , urlToFrontendNamedEntity
       , urlToFrontendThemeCategory
       , urlToFrontendNamedEntityCategory } from "@utils/url.js";
import { indexDataFormatterTheme
       , indexDataFormatterNamedEntity } from "@utils/indexDataFormatter";
import { capitalizeFirstChar } from "@utils/strings";
import "@typedefs";

/*************************************************************/

const route   = useRoute();
const router  = useRouter();
const props   = defineProps(["tableName"]);
const display = "concept";       // define the view to use in `IndexItem`

const tableName            = ref();    /** @type {String} "theme"|"namedEntity" */
const viewType             = ref();    /** @type {String} "collection"|"tree". the kind of display to use. defaults to "collection" */
const categorySlug         = ref();    /** @type {String} theme.category_slug or named_entity.category_slug of "all" if we want to retrieve all themes/named entities */
const categoryName         = ref()     /** @type {String} theme.category_name or named_entity.category_name or "tout" if categorySlug === 'all' */
const categories           = ref([]);  /** @type {typedefs.ThemeOrNamedEntityCategoryItem[]} : all allowed categories */
const dataCollectionFull   = ref([]);  /** @type {typedefs.ThemeOrNamedEntityItemLite[]} the full index when viewType==='collection', independent of user filters */
const dataCollectionFilter = ref([]);  /** @type {typedefs.IndexBaseItem[]} the data to pass to `IndexBase.vue` when viewType==='collection'. this can depend on user-defined filters. an array of { href: <url to redirect to when clicking on an item>, img: <url to the background img to display>, text, <text to display> } */
const dataTree             = ref([]);  /** @type {typedefs.ThemeOrNamedEntityTree} the data when viewType==='tree' */

const loadState = ref("loading");  /** @type {typedefs.AsyncRequestState} */

const dataTreeRestructured = computed(() => restructureToTree(dataTree.value))

/*************************************************************/
/** DATA FETCHING */

/**
 * restructure `data` to fit the data model expected by `TreeComponent`.
 * @param {typedefs.ThemeOrNamedEntityTree} data
 * @returns {typedefs.treeData}
 */
function restructureToTree(data) {
  // url building functions
  const urlToEntry = tableName.value === "theme"
    ? urlToFrontendTheme
    : urlToFrontendNamedEntity;
  const urlToCategory = tableName.value === "theme"
    ? urlToFrontendThemeCategory
    : urlToFrontendNamedEntityCategory;

  // helper functions
  /**
   * @param {ThemeOrNamedEntityTreeItem} x
   * @returns {treeNode}
   */
  const restructureCategoryName = (x) =>
    `<a href="${urlToCategory(x.category_slug)}">${x.category_name}</a>
    (${x.entries.length} ${x.entries.length > 1 ? "entrées" : "entrée"})`;
  /**
   * @param { {entry_name: String, id_uuid: String} } x
   * @returns {treeNode}
   */
   const restructureEntry = (x, categorySlug) => {
    return { nodeLabel: x.entry_name,
             nodeUrl: urlToEntry(categorySlug, x.id_uuid) } }

  // process
  return data.map(category => {
    return { nodeLabel: restructureCategoryName(category),
             nodeUrl: undefined,
             nodeChildren: category.entries.map(entry =>
              restructureEntry(entry, category.category_slug)) }
  })
}


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
    const apiTarget =
      tableName.value === "theme"
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
 * @type { typedefs.ThemeOrNamedEntityCategoryItem }: the structure of `categories`
 */
function getCategories() {
  const apiTarget =
    tableName.value === "theme"
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
    dataTree.value = data;  /** @type { typedefs.ThemeOrNamedEntityTree } */
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
    ? new URL(`/i/theme/category/${categorySlug.value}`, __API_URL__)
    : new URL(`/i/named-entity/category/${categorySlug.value}`, __API_URL__);
  axios.get(apiTarget.href)
    .then(r => r.data)
    .then(data => {
      dataCollectionFull.value = data;  /** @type { typedefs.ThemeOrNamedEntityItemLite[] } */
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
 * @param {typedefs.ThemeOrNamedEntityItemLite[]} filteredData:
 *    the new filtered array of Iconography or NamedEntity objects
 */
function handleFilter(filteredData) {
  dataCollectionFilter.value = tableName.value === "theme"
                             ? indexDataFormatterTheme(filteredData)
                             : indexDataFormatterNamedEntity(filteredData);
}


/*************************************************************/
/** STATE MANAGERS AND HANDLERS */

/**
 * when the user inputs new data on `#category-control`, update the route path.
 * this will trigger the `watch(route.path)`.
 * @param {String} newCategorySlug: the new `(theme|named_entity).category_slug`
 */
function changeCategory(newCategorySlug) {
  if ( newCategorySlug && newCategorySlug.length && newCategorySlug !== categorySlug ) {
    let newPath = route.path.replace(/[^\/]+$/g, newCategorySlug);  // nice A Scanner Darkly reference :)
    router.replace({ path: newPath, query: { viewType: viewType.value } });
  }
}

/**
 * when the user inputs new data on `#view-type-control`,
 * update the router `viewType` param.
 * @param {String} newViewType: "collection" || "tree"
 */
function changeViewType(newViewType) {
  if ( newViewType && newViewType.length && newViewType !== viewType.value ) {
    // update the refs and the URL to fit the new state
    router.replace({ query: { viewType: newViewType } });
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
  tableName.value              = props.tableName;
  viewType.value               = newViewType;
  categorySlug.value           = decodeURIComponent(route.params.categorySlug);
  categoryName.value           = "";
  categories.value             = [];
  dataCollectionFull.value     = [];
  dataCollectionFilter.value   = [];
  dataTree.value               = [];
  loadState.value              = "loading";
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

/**
 * hook to handle a change of `category_slug` in the route path:
 * reset the refs, fetch backend data for the new category.
 */
watch(() => route.path, (newPath, oldPath) => {
  categorySlug.value           = newPath.match(/[^\/]+$/g)[0];
  dataCollectionFull.value     = [];
  dataCollectionFilter.value   = [];
  dataTree.value               = [];
  loadState.value              = "loading";
  // fetch the new data
  getCurrentCategoryName();
  if (viewType.value === "collection") getDataCollection();
  else getDataTree();
})

/**
 * hook to handle a change of `viewType` in the route.
 * reset the necessary refs and fetch backend data.
 */
watch(() => route.query.viewType, (newViewType, oldViewType) => {
  viewType.value               = newViewType;
  dataCollectionFull.value     = [];
  dataCollectionFilter.value   = [];
  dataTree.value               = [];
  loadState.value              = "loading";
  // fetch the new data
  if (newViewType === "collection") getDataCollection();
  else getDataTree();
})

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
@media ( min-width:800px ) {
  .title-controller-wrapper {
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
  }
  .view-controller-wrapper {
    width: auto;
  }
}
.title-wrapper {
  display: flex;
  flex-direction: column;
  justify-content: end;
  align-items: flex-start;
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

</style>