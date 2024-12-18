<template>
  <!-- FilterIndexThemeOrNamedEntity.vue

    like `@components/FilterIndexIconography`, this component is
    completely standalone: it handles:
    - form html structure
    - retrieving form data
    - data manipulation : getting data from parent, filtering
      and emitting filtered data back to the parent.
    - it does so without any ajax requests.

    the structure of a single Theme or NamedEntity object is:
    @typedefs.ThemeOrNamedEntityItemLite :
      {
      "category_name": "consommer",
      "category_slug": "consommer",
      "entry_name": "alimentation",
      "iconography_count": 364,
      "id_uuid": "qr17eaf451869db4d64b5d9942651d7ed5b",
      "thumbnail": [
        "qr1b6cc58cb98f14868ad4f0d9120cfbb9b_thumbnail.jpg"
      ]
    }
  -->

  <div class="filter-outer-wrapper">
    <h3>Filter les données
      <span v-if="currentCount > 1"
            v-html="`(${currentCount} résultats)`"></span>
      <span v-else-if="currentCount === 1"
            v-html="`(${currentCount} résultat)`"></span>
      <span v-else
            v-html="`(Aucun résultat)`"></span>
    </h3>

    <div class="filter-loader-wrapper">
      <div class="loader-wrapper"
           v-if="isLoading===true"
      >
        <UiLoader style="height: 100%"
        ></UiLoader>
      </div>

      <div class="form-outer-wrapper"
           :class="{ 'is-loading': isLoading }"
      >
        <div class="form-wrapper">
          <!-- `tne` = Theme or Named Entity  -->
          <FormKit type="form"
                   name="tneFilter"
                   id="tne-filter"
                   ref="theForm"
                   @submit="onSubmit"
          >
            <div class="form-row1-wrapper">
              <FormKit type="text"
                       id="entry-name-filter"
                       outer-class="entry-name-outer"
                       name="entryNameFilter"
                       label="Nom"
                       placeholder="Filtrer par nom"
                       help="Afficher les entrées contenant le(s) mot(s)"
                       validation="textValidator"
              ></FormKit>
              <FormKit v-if="sliderMin && sliderMax"
                       type="fkSlider"
                       id="count-slider"
                       name="countSlider"
                       label="Nombre de ressources liées"
                       help="Filter par nombre de ressources iconographiques"
                       number="integer"
                       :step="1"
                       :minVal="sliderMin"
                       :maxVal="sliderMax"
              ></FormKit>
            </div>
            <div class="form-row2-wrapper">
              <FormKit type="fkSelect"
                       id="order-by"
                       name="orderBy"
                       label="Réordonner"
                       @input="onOrderByInput"
                       :multiple="false"
                       help="Réorganniser l'ordre d'affichage des résultats"
                       :options="[ { label: 'Nombre de ressources liées', value:'count'}
                                 , { label: 'Ordre alphabétique', value:'entry_name' } ]"
              ></FormKit>
              <FormKit type="fkSelect"
                       id="order-direction"
                       name="orderDirection"
                       label="Ordre"
                       :multiple="false"
                       help="Réorganniser l'ordre d'affichage des résultats"
                       :options="[ { label: 'Ascendant (par défaut)', value:'asc'}
                                 , { label: 'Descendant', value:'desc' } ]"
                       :disabled="disableOrderDirection"
              ></FormKit>
            </div>

          </FormKit>
        </div>

        <div class="form-messages-wrapper">
          <!-- error messages will be displayed here. see:
               https://formkit.com/essentials/validation#moving-validation-messages
          -->
          <FormKitMessages :node="theForm?.node"/>
        </div>

      </div>
    </div>
  </div>
</template>


<script setup>
import { onMounted, ref, watch } from "vue";

import { FormKitMessages } from "@formkit/vue";
import _ from "lodash";

import UiLoader from "@components/UiLoader.vue";

import { simplifyHtml } from "@utils/strings";
import "@typedefs";

/**************************************/

/**
 * @typedef FilterParameters
 *    theme or named entity filter parameters structure
 * @type {object}
 * @property {String?} entryNameFilter: themes or named enitity names must contain this string
 * @property {number[]?} countSlider: filter only items within a range of [min, max]
 * @property {String?} orderBy: sorting key
 * @property {("asc"|"desc")} orderDirection: sorting direction

 */

const props = defineProps(["data"]);
const emit  = defineEmits(["themeOrNamedEntityFilter"]);

const data          = ref();  /** @type {typedefs.ThemeOrNamedEntityItemLite[]} */
const theForm       = ref();  /** @type {FormKitNode} */
const currentFilter = ref();  /** @type {FilterParameters?} */
const currentCount  = ref();  /** @type {Number?} */
const sliderMin     = ref();  /** @type {Number?} */
const sliderMax     = ref();  /** @type {Number?} */

const isLoading     = ref(false);
const disableOrderDirection = ref(true);  // `orderDirection` is disabled unless `orderBy` is not undefined.

/**************************************/

/**
 * reset the refs
 * @param {typedefs.ThemeOrNamedEntityItemLite[]} theData : new array of themes or named entites
 */
function setRefs(theData) {
  data.value = theData;
  currentCount.value = theData.length;
  sliderMin.value = Math.min(...theData.map(x => x.iconography_count));
  sliderMax.value = Math.max(...theData.map(x => x.iconography_count));
}

/**
 * when the input `orderBy` changes, set `disableOrderDirection`,
 * which will enable/disable the `orderDirection` input.
 */
function onOrderByInput(theInput) {
  disableOrderDirection.value = theInput == null || !theInput.length;
}

/**
 * do the actual filtering
 *
 * @param {FilterParameters} filterParams: user-defined filters
 * @param {typedefs.ThemeOrNamedEntityItemLite[]} dataObj: array of Theme or NamedEntity objects.
 */
function filterThemeOrNamedEntity(filterParams, dataObj) {

  let entryNameFilter = filterParams.entryNameFilter,
      countSlider     = filterParams.countSlider,
      orderBy         = filterParams.orderBy,
      orderDirection  = filterParams.orderDirection || "asc";

  if ( entryNameFilter && entryNameFilter.length ) {
    entryNameFilter = simplifyHtml(entryNameFilter);
    dataObj = dataObj.filter(x =>
      simplifyHtml(x.entry_name).includes(entryNameFilter) );
  }
  if ( countSlider && countSlider.length ) {
    dataObj = dataObj.filter(x => x.iconography_count >= countSlider[0]
                               && x.iconography_count <= countSlider[1]);
  }
  if ( orderBy && orderBy.length ) {
    // data is first sorted in ascending order. then, if necessary,
    // order is reversed using `Array.reverse()`
    dataObj = orderBy === "count"
              ? dataObj.sort((a,b) => a.iconography_count - b.iconography_count)
              : orderBy === "entry_name"
              ? dataObj.sort((a,b) => a.entry_name.localeCompare(b.entry_name) )
              : console.error(`FilterIndexThemeOrNamedEntity.filterThemeOrNamedEntity() : expected one of ['count', 'entry_name'], got ${orderBy}`);
    if ( orderDirection === "desc" ) {
      dataObj = dataObj.reverse();
    }
  }
  return dataObj;
}

/**
 * this function is exactly the same as `@components/FilterIndexIconography.vue`.
 *
 * @param {FilterParameters} formData : the filter
​ * @param {FormKitNode} formNode : formKit formNode. https://formkit.com/api-reference/formkit-core#formkitnode
 */
function onSubmit(formData, formNode) {
  let dataFilter = [];  // elements of `data` that fit `formData`

  formNode.clearErrors();  // remove previous error messages

  if ( Object.values(formData).every(i => i == undefined || i === "") ) {
    formNode.setErrors("Définir au moins un filtre pour lancer la recherche")
  } else if ( _.isEqual(currentFilter.value, formData) ) {
    formNode.setErrors("Les filtres sont les mêmes qu'avant. Il faut les changer pour relancer une recherche.")
  } else {
    isLoading.value = true;
    currentFilter.value = formData;
    dataFilter = data.value;
    dataFilter = filterThemeOrNamedEntity(formData, dataFilter);
    // adding fake latency ensures that UiLoader is seen by the user,
    // and that the user will see that the data displayed has changed.
    setTimeout(() => {
      emit("themeOrNamedEntityFilter", dataFilter);
      currentCount.value = dataFilter.length;
      isLoading.value = false;
    }, 750);
  }
}

/**************************************/

watch(props, (newP, oldP) => {
  setRefs(newP.data);
})

onMounted(() => {
  setRefs(props.data);
})
</script>


<style scoped>
/**
 * for once, the media query is based on window width and not window orientation:
 * if width <= 750px, we'll have 4 rows / 1 column;
 * else, we'll have 2 rows / 2 columns.
 */
#tne-filter {
  display: flex;
  flex-direction: column;
}
.form-row1-wrapper, .form-row2-wrapper {
  display: grid;
  grid-template-rows: 50% 50%;
  grid-template-columns: 100%;
}
.form-row1-wrapper > div, .form-row2-wrapper > div {
    margin: 10px;
  }
#tne-filter :deep(.formkit-outer[data-type=submit]) {
  margin-top: 2%;
  display: flex;
  align-items: center;
  justify-content: center;
}
#tne-filter :deep(.formkit-outer[data-type=submit] > .formkit-wrapper) {
  width: 70%;
}
#tne-filter :deep(.formkit-outer[data-type=submit] button) {
  min-height: 40px;
}

@media ( min-width: 750px ) {
  #tne-filter {
    display: grid;
    grid-template-columns: 100%;
    grid-template-rows: repeat(3, calc(100%/3));
  }
  .form-row1-wrapper, .form-row2-wrapper {
    grid-template-columns: 50% 50%;
    grid-template-rows: 100%;
  }
  .form-row1-wrapper > div, .form-row2-wrapper > div {
    margin: 0 10px 0 10px;
  }
}
</style>