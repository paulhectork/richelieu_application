<!-- IndexIconographyFilter.vue

  a block that performs filtering of an array of iconography objects.
  this component is completely standalone:
  - it receives the `data` array containing all of our iconography entries,
  - contains the HTML form to do the filtering
  - receives the user inputted data from the form
  - performs the filtering
  - emits the filtered `data` to the parent.
  all filtering is done on the frontend, there's no communication
  with the backend. this may be less performant than custom backend
  queries, but makes it way easier to implement `IndexIconographyFilter`
  in different parts of the app.

  during filtering, a loader is displayed on top of the filter.
  this is to make sure that the user sees that something is happening
  and understand that the data displayed in the index is updated.

  css-wise, it supports `main-default` and `negative-default` themes.

  props:
    - data (Array<Object>):
        an array of Iconography objects.

  emits:
    - iconographyFilter (Array<Object>):
        the `data`, updated to fit the user-defined filters, is sent back to the parent.
-->

<template>

  <div class="filter-outer-wrapper">
    <h3>Filtrer les données
      <span v-if="currentIconographyCount > 1"
            v-html="`(${currentIconographyCount} résultats)`"></span>
      <span v-else-if="currentIconographyCount === 1"
            v-html="`(${currentIconographyCount} résultat)`"></span>
      <span v-else
            v-html="`(Aucun résultat)`"></span>
    </h3>

    <div class="filter-loader-wrapper">
      <div class="loader-wrapper"
           v-if="isLoading === true"
      >
        <UiLoader style="height: 100%"
        ></UiLoader>
      </div>

      <div class="form-outer-wrapper"
           :class="{ 'is-loading': isLoading }"
      >
        <div class="form-wrapper">
          <FormKit type="form"
                   name="iconographyIndexFilter"
                   id="iconography-index-filter"
                   ref="theForm"
                   @submit="onSubmit"
          >
            <FormKit type="text"
                     id="title-filter"
                     name="titleFilter"
                     label="Titre"
                     placeholder="Filter par titre"
                     help="Afficher les œuvres dont le titre contient le(s) mot(s)"
                     validation="textValidator"
            ></FormKit>
            <FormKit type="text"
                     id="author-filter"
                     name="authorFilter"
                     label="Auteur ou autrice"
                     placeholder="Filtrer par nom d'auteur ou autrice"
                     help="Afficher les auteurs dont le nom contient le(s) mot(s)"
                     validation="textValidator"
            ></FormKit>
            <FormKit type="fkSelect"
                     id="order-by"
                     name="orderBy"
                     label="Réordonner (ordre ascendant)"
                     :multiple="false"
                     help="Définir un critère pour l'ordre des résultats"
                     :options="[ { label: 'Auteur ou autrice', value: 'author' }
                               , { label: 'Titre de l\'œuvre', value: 'title' }
                               , { label: 'Date', value: 'date' } ]"
            ></FormKit>
            <FormKit v-if="minDate && maxDate"
                     type="fkSlider"
                     id="date-filter"
                     outer-class="date-filter-wrapper"
                     name="dateFilter"
                     label="Date"
                     help="Filter par date"
                     number="integer"
                     :step="1"
                     :minVal="minDate"
                     :maxVal="maxDate"
            ></FormKit>
            <!-- TODO ORDER ASCENDANT / DESCENDANT -->
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

import { stripHtml, simplifyAndUnaccentString } from "@utils/strings";

/*************************************/

const props                   = defineProps(["data"]);
const emit                    = defineEmits(["iconographyFilter"]);  // after filtering, send filtered data back to the parent

const data                    = ref();  // the data sent from the parent. this is never modified (so why is it in a ref ???)
const theForm                 = ref();  // the FormKitNode form.
const currentFilter           = ref();  // the filter applied by the user, defined in onSubmit. this ref allows to compare a new filter with the previous filter, to avoid running the same filter twice.
const currentIconographyCount = ref();  // number of iconography items currently displayed
const minDate                 = ref();  // min/max allowed dates for the slider `#date-slider`.
const maxDate                 = ref();  // min/max allowed dates for the slider `#date-slider`.
const isLoading               = ref(false);  // when true, a loader will be displayed on top of the form.

/*************************************/

/**
 * a combination of 2 string simplifiers.
 * @param {String} s
 */
const localStringSimplify = s =>
  s != null && typeof s === "string"
  ? simplifyAndUnaccentString(stripHtml( s ))
  : console.error(`IndexIconographyFilter.localStringSimplify: 's' must be string, got '${s}' instead`);


/**
 * function performing the filtering heavywork.
 * using the params `filterParams`, it applies successive
 * filters to `filterObj`, before returning `filterObj`.
 *
 * TODO: optimize this function ?
 *
 * @param {Object} filterParams: the user-defined filter.structure:
 *  { titleFilter  : String|undefined,
 *    authorFilter : String|undefined,
 *    dateFilter   : undefined|Array<Number>,   // [YYYY,YYYY]
 *    orderBy      : "author"|"date"|"title"
 *  }
 * @param {Array<Object>} dataObj: an array of Iconography objects
 */
function filterIconography(filterParams, dataObj) {
  let start, end;
  start = performance.now();

  ////////////////////////////////
  // 1) FILTERING dataObj
  if ( filterParams.titleFilter && filterParams.titleFilter.length ) {
    let theTitleFilter = localStringSimplify( filterParams.titleFilter );
    dataObj = dataObj.filter((d) => {
      // d.title is an array => stringify it.
      let title = localStringSimplify( d.title.join(" ") );
      return title.includes(theTitleFilter)
    })
  }

  if ( filterParams.authorFilter && filterParams.authorFilter.length ) {
    let theAuthorFilter = localStringSimplify( filterParams.authorFilter );
    dataObj = dataObj.filter((d) => {
      // d.authors is an array of objects => extract the author name, stringify the array and simplify it
      let author = localStringSimplify(d.authors.map(d => d.entry_name).join(" "));
      return author.includes(theAuthorFilter);
    });
  }

  if ( filterParams.dateFilter && filterParams.dateFilter.length ) {
    let theDateFilter = filterParams.dateFilter;
    dataObj = dataObj.filter((d) =>
      // filter: d.date is defined + d.date is in the range of `theDateFilter`
      d.date
      && d.date[0] >= theDateFilter[0]
      && d.date[1] <= theDateFilter[1])
  }

  ////////////////////////////////
  // 2) REORDERING dataObj

  // how does title sorting work ? for each object in `dataObj`, `title`
  // is an array of strings. what we do is:
  // - 1) create 2 arrays: `dataObjWithTitle`, containing
  //    items of `dataObj` that have a title and can be filtered,
  //    `dataObjWithoutTitle`, containing all of the items without
  //    title (can't be filtered).
  // - 2) sort `dataObjWithTitle` by title, using `localeCompare` (https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/localeCompare)
  //    before sorting the full `dataObjWithTitle`, we sort, for
  //    each item in `dataObj`, its `title` array alphabetically.
  // - 3) concatenate `dataObjWithTitle` and `dataobjWithoutTitle`:
  //    items without a title will be at the end of the reordered `dataObj` array.
  if ( filterParams.orderBy && filterParams.orderBy === "title" ) {
    let dataObjWithTitle = dataObj.filter((d) =>
      d.title && d.title.length);
    let dataObjWithoutTitle = dataObj.filter(d =>
      !d.title || !d.title.length);
    dataObjWithTitle = dataObjWithTitle.sort((a,b) => {
      // transform `a` and `b`, arrays of authors objects into simplified strings
      // the inner `.sort((x,y) => x.localeCompare(y))` allows to sort
      // the `a.title` and `b.title` arrays before comparing them together
      a = localStringSimplify( a.title.sort((x,y) => x.localeCompare(y)).join(" ") );
      b = localStringSimplify( b.title.sort((x,y) => x.localeCompare(y)).join(" ") );
      return a.localeCompare(b);
    })
    dataObj = [ ...dataObjWithTitle, ...dataObjWithoutTitle ];
  }

  // works pretty much the same as ordering by title, except that
  // each `dataObj` item contains an array of authors object
  // with the structure { entry_name: <author name(string)>, id_uuid: <author id uuid (string)> }
  else if ( filterParams.orderBy && filterParams.orderBy === "author" ) {
    let dataObjWithAuthor = dataObj.filter(d =>
      d.authors && d.authors.length);
    let dataObjWithoutAuthor = dataObj.filter(d =>
      !d.authors || d.authors.length < 1);

  dataObjWithAuthor = dataObjWithAuthor.sort((a,b) => {
      // transform `a` and `b`, arrays of authors objects into simplified strings
      // the inner `.sort((x,y) => x.localeCompare(y))` allows to sort
      // the `a.author` and `b.author` arrays before comparing `a` and `b`.
      a = localStringSimplify( a.authors.map(x => x.entry_name).sort((x,y) => x.localeCompare(y)).join(" ") );
      b = localStringSimplify( b.authors.map(x => x.entry_name).sort((x,y) => x.localeCompare(y)).join(" ") );
      return a.localeCompare(b);
    })
    dataObj = [ ...dataObjWithAuthor, ...dataObjWithoutAuthor ];
  }
  else if ( filterParams.orderBy && filterParams.orderBy === "date" ) {
    let dataObjWithDate = dataObj.filter(d =>
      d.date && d.date.length);
    let dataObjWithoutDate = dataObj.filter(d =>
      !d.date || d.date.length < 1 );
    dataObjWithDate =
      dataObjWithDate.sort((a,b) => a.date[0] - b.date[0]);
    dataObj = [ ...dataObjWithDate, ...dataObjWithoutDate ];  // 1st, put the elements with a date, then the elements without a date.
  }

  end = performance.now();
  console.log(`IndexIconographyFilter.filterIconography() : ${end-start}ms. to complete.`)
  return dataObj;
}

/**
 * filter the `data` object based on the filters defined
 * by the user, received in `formData`. this function handles
 * the global process, while `filterIconography()` handles the
 * internal filtering.
 *
 * the process:
 * - receive form data
 * - ensure that it's valid (not empty or not the same as the
 *   previously defined filter)
 * - do the filtering
 * - emit the filtered data back to the parent
 *
 * @param {Object} formData :
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
    dataFilter = filterIconography(formData, dataFilter);
    // adding fake latency ensures that UiLoader is seen by the user,
    // and that the user will see that the data displayed has changed.
    setTimeout(() => {
      emit("iconographyFilter", dataFilter);
      currentIconographyCount.value = dataFilter.length;
      isLoading.value = false;
    }, 750);
  }
}

/**
 * define all the refs from `props.data`. used in `onMounted` and `watch(props)`
 * @param {Array<Object>} theData: array of Iconography objects to filter
 */
function setRefs(theData) {
  data.value = theData;
  minDate.value = Math.min(...theData.filter(i => i.date != null && i.date.length)
                                        .map(i => i.date[0]));
  maxDate.value = Math.max(...theData.filter(i => i.date != null && i.date.length)
                                        .map(i => i.date[1]));
  currentIconographyCount.value = theData.length;

}

/*************************************/

watch(props, (newP, oldP) => {
  setRefs(newP.data);
})

onMounted(() => {
  setRefs(props.data);
})


</script>


<style scoped>
.filter-outer-wrapper {
  margin: 3%;
  border: var(--cs-main-border);
}
.negative-default .filter-outer-wrapper {
  border: var(--cs-negative-border);
}
.filter-loader-wrapper {
  display: grid;
  padding: 2%;
  border-top: var(--cs-main-border);
}
.negative-default .filter-loader-wrapper {
  border-top: var(--cs-negative-border);
}

.filter-loader-wrapper > :deep(*) {
  grid-column-start: 1;
  grid-row-start: 1;
}
.loader-wrapper {
  z-index: 2;
}
.form-outer-wrapper {
  transition: opacity .3s ease-out;
}
.form-outer-wrapper.is-loading {
  opacity: 0.2;
  transition: opacity .3s ease-in;
}

/***********************/

/** general styling of the form, for mobile and desktop */
form#iconography-index-filter {
  display: grid;
  height: max-content;
}
@media ( orientation:landscape ) {
  form#iconography-index-filter {
    grid-template-columns: repeat(3, 33.33%);
    grid-template-rows: 50% 50%;
  }
  #iconography-index-filter .date-filter-wrapper {
    grid-column: 1 / 3;
  }
}
#iconography-index-filter .formkit-outer {
  position: relative;
  margin: 3px;
}
@media ( orientation:portrait ) {
  #iconography-index-filter {
    grid-template-columns: 50% 50%;
    grid-template-rows: repeat(3, 33.33%);
  }
  #iconography-index-filter > * {
    min-height: 60px;
  }
  #iconography-index-filter :deep(.formkit-actions) {
    grid-column: 1 / 3;
  }
}

/** input-level styling: hide the help, transform the messages to popups */
#iconography-index-filter :deep(.formkit-help) {
  visibility: hidden !important;
  height: 0;
}
#iconography-index-filter :deep(.formkit-wrapper) {
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  align-items: start;
}
#iconography-index-filter :deep(.formkit-inner) {
  width: 100%;
}
/** error messages are displayed as popups: the `.formkit-outer`
    has a position:relative, which allows .formkit-messages to
    be positionned with a position:absolute relative to `.formkit-outer`.
    then, we just position .formkit-messages above the `.formkit-outer`
    and add a pure CSS arrow tooltip (see rule below).
    otherwise the messages get hidden by other inputs with display:grid.
 */
#iconography-index-filter :deep(.formkit-outer .formkit-messages) {
  background-color: var(--cs-main-default-bg);
  transform: translateY(-110%);
  position: absolute;
  top: 0;
  left: 0;
  padding: 5px;
  border: var(--cs-main-border);
}
.negative-default #iconography-index-filter :deep(.formkit-outer .formkit-messages) {
  background-color: var(--cs-negative-default-bg);
  border: var(--cs-negative-border);
}
#iconography-index-filter :deep(.formkit-outer .formkit-messages:after) {
  /** css tooltip. see: https://css-tricks.com/snippets/css/css-triangle/ */
  content: '';
  position: absolute;
  top: 100%;
  left: 50%;
  height: 0px;
  width: 0px;
  transform: translateX(-15px);
  border: solid transparent 15px;
  border-top-color: var(--cs-main-default);
  background: transparent;
}
.negative-default #iconography-index-filter :deep(.formkit-outer .formkit-messages:after) {
  border-top-color: var(--cs-negative-default);
}

/** submit button styling  */
#iconography-index-filter :deep(.formkit-actions) {
  display: flex;
  align-items: center;
  justify-content: center;
}
#iconography-index-filter :deep(.formkit-actions .formkit-outer[data-type=submit]) {
  width: 70%;
  height: 40%;

}
#iconography-index-filter :deep(.formkit-actions button[type=submit]) {
  width: 100%;
  height: 100%;
  box-shadow: 3px 3px var(--cs-main-second-bg);
}

/***********************/

.form-messages-wrapper {
}
</style>