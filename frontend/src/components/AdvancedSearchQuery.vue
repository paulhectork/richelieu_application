<!-- an advanced search form on the `iconography` SQL table.

     this creates a JSON object with the query parameters,
     which are passed to the parent. the parent updates the
     URL, fetches the answer and calls another component to
     display the results

     structure of each field:
     each field is made of a boolean operator (and,or,not)
     and of the actual input field (FormKitRadioTabs, FormKitRepeatableText...).
     the structure can be manipulated using the <div> containers
     for each part of the field:

     <div class="form-field-outer-wrapper">              <=== the wrapper around the whole field
      <div class="form-field-boolean-op-wrapper"></div>  <=== the wrapper around the FormKitBooleanOp
      <div class="form-field-input-wrapper"></div>       <=== the wrapper around the actual input
     </div>

     see:
     for an in-depth explanation of FormKit:
        https://formkit.com/essentials/architecture
-->

<template>
  <FormKit type="form"
           name="theForm"
           :actions="true"
           id="advanced-search-form"
           submit-label="Lancer la recherche"
           :submit-attrs="{ inputClass  : 'form-submit-input',
                            wrapperClass: 'form-submit-wrapper',
                            outerClass  : 'form-submit-outer' }"
           @submit="onSubmit"
  >

    <!-- reset the form on click -->
    <div class="reset-button-wrapper">
      <FormKit type="button"
               name="resetButton"
               id="reset-button"
               @click="resetForm"
      >Réinitialiser les paramètres</FormKit>
    </div>

    <!-- select inputs -->
    <div v-if="namedEntityArray.length
               && themeArray.length
               && institutionArray.length"
    >
      <div class="form-field-outer-wrapper">
        <FormKit type="fkBooleanOp"
                 id="themeBooleanOp"
                 name="themeBooleanOp"
        ></FormKit>
        <FormKit type="fkSelect"
                 name="theme"
                 label="Thème"
                 help="Sélectionner un thème"
                 placeholder="Sélectionner un thème"
                 :options="themeArray"
        ></FormKit>
      </div>
      <div class="form-field-outer-wrapper">
        <FormKit type="fkBooleanOp"
                 name="namedEntityBooleanOp"
                 id="namedEntityBooleanOp"
        ></FormKit>
        <FormKit type="fkSelect"
                 name="namedEntity"
                 label="Sujet"
                 placeholder="Sélectionner un sujet"
                 help="Sélectionner un sujet"
                 :options="namedEntityArray"
        ></FormKit>
      </div>
      <div class="form-field-outer-wrapper">
        <FormKit type="fkBooleanOp"
                 name="institutionBooleanOp"
                 id="institutionBooleanOp"
        ></FormKit>
        <FormKit type="fkSelect"
                 name="institution"
                 label="Institution"
                 help="Sélectionner une institution"
                 placeholder="Sélectionner une institution"
                 :options="institutionArray"
        ></FormKit>
      </div>
    </div>

    <!-- free text inputs -->

    <div class="form-field-outer-wrapper">
      <FormKit type="fkBooleanOp"
               name="titleBooleanOp"
               id="titleBooleanOp"
      ></FormKit>
      <FormKit type="fkRepeatableText"
               name="title"
               id="title"
               label="Titre"
               labelText="Titre"
               help="Le titre de la ressource iconographique doit contenir les mots entrés ici."
               placeholder="Ex: Le Moniteur de la Mode"
               validation="textArrayValidator"
      ></FormKit>
    </div>
    <div class="form-field-outer-wrapper">
      <FormKit type="fkBooleanOp"
               name="authorBooleanOp"
               id="authorBooleanOp"
      ></FormKit>
      <FormKit type="fkRepeatableText"
               name="author"
               label="Auteur ou autrice"
               placeholder="Ex: Jules David"
               help="Le nom de l'auteur ou de l'autrice doit contenir les mots entrés ici."
               validation="textArrayValidator"
      ></FormKit>
    </div>
    <div class="form-field-outer-wrapper">
      <FormKit type="fkBooleanOp"
               name="publisherBooleanOp"
               id="publisherBooleanOp"
      ></FormKit>
      <FormKit type="fkRepeatableText"
               name="publisher"
               label="Maison d'édition"
               placeholder="Bellizard"
               help="Le nom de l'éditeur ou de la maison d'édition doit contenir les mots entrés ici."
               validation="textArrayValidator"
      ></FormKit>
    </div>

    <!-- date inputs -->
    <div>
      <FormKit type="fkRadioTabs"
               id="date-filter"
               name="dateFilter"
               label="Date"
               help="Choisir le type de filtre pour la date"
               value="dateRange"
               default="dateRange"
               :options="allowedDateSearchTypes"
      ></FormKit>

      <FormKit v-if="dateFilterType==='dateRange'"
               type="group"
               name="date"
               label="Date"
               help="Choisir une tranche de dates au format AAAA-AAAA"
      >
        <div class="date-range">
          <FormKit type="number"
                   name="dateStart"
                   label="Date de début"
                   placeholder="Ex: 1810"
                   :data-allowedDateRange="allowedDateRange"
                   validation="dateRangeValidator"
          ></FormKit>
          <FormKit type="number"
                   name="dateEnd"
                   label="Date de fin"
                   placeholder="Ex: 1891"
                   :data-allowedDateRange="allowedDateRange"
                   validation="dateRangeValidator"
          ></FormKit>
        </div>
      </FormKit>

      <FormKit v-else-if="dateFilterType==='dateExact'"
               type="number"
               name="date"
               label="Date exacte"
               placeholder="Ex: 1891"
               :data-allowedDateRange="allowedDateRange"
               validation="dateValidator"
      ></FormKit>
      <FormKit v-else-if="dateFilterType==='dateBefore'"
               type="number"
               name="date"
               label="Avant"
               placeholder="Ex: 1891"
               :data-allowedDateRange="allowedDateRange"
               validation="dateValidator"
      ></FormKit>
      <FormKit v-else
               type="number"
               name="date"
               label="Après"
               placeholder="Ex: 1810"
               :data-allowedDateRange="allowedDateRange"
               validation="dateValidator"
      ></FormKit>
    </div>

    <!-- the submit button
    <FormKit type="submit"
             id="form-submit"
    >Lancer la recherche</FormKit>
    -->

  </FormKit>
</template>

<script setup>
import { ref, onMounted, computed, watch } from "vue";
import axios from "axios";

import { reset } from "@formkit/core";
import { useFormKitNodeById, FormKitMessages } from '@formkit/vue';
import $ from "jquery";

// import FormKitRadioTabs from "@components/FormKitRadioTabs.vue";
import { clickOrTouchEvent } from "@globals";
import { IconographyQueryParams } from "@modules/iconographyQueryParams";
// import { isEmptyArray, isEmptyScalar, isNumberInRange, isValidNumberRange } from "@utils/functions";

/******************************************/

const props = defineProps(["queryError"]);   // an error occured while fetching data from the backend
const emit = defineEmits(['query-params']);  // to send the query params to the parent

const dateFilterNode   = useFormKitNodeById("date-filter");  // useFormKitNodeById targets a FormKit node by it's HTML id and creates a vue ref.
const themeArray       = ref([]);                            // string array
const namedEntityArray = ref([]);                            // string array
const institutionArray = ref([]);                            // string array
const allowedDateRange = ref([]);                            // int array: [minDate, maxDate]
const dateFilterType   = ref("dateRange");                   // str: the type of date filter to display

// `items` in the html form to set the `allowedDateRanger`
const allowedDateSearchTypes = [ { label:'Plage de dates', value:'dateRange' }
                               , { label:'Date exacte'   , value:'dateExact' }
                               , { label:'Avant'         , value:'dateBefore'}
                               , { label:'Après'         , value:'dateAfter' }]

/******************************************/

/**
 * when clicking on `#reset-button`, reset all values in the form.
 * custom formkit components must be reset manually
 *
 * PROBLEM!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
 * THE RESETTING ISN'T DONE ON CUSTOM FORMKIT INPUTS !!!!!!!!!!!!!!!
 * PROBLEM!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
 *
 */
function resetForm() {
  useFormKitNodeById("advanced-search-form", (formNode) => formNode.reset() );
}

/**
 * transform a string into an object following the
 * structure defined by formjit objects:
 * { "label": <value to display>, "value": <value sent by the form> }
 * https://formkit.com/inputs/select#array-of-objects
 * @param {string} item
 * @returns {Object}
 */
function itemToFormEntry(item) {
  return { "label": item.entry_name, "value": item.entry_name }
}

/**
 * sorter for an array of items created by `itemToFormEntry`
 * see: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/sort
 * @param val1, val2: the two items to sort
 */
function sortByValue(val1, val2) {
  return val1.value.toLowerCase() < val2.value.toLowerCase()
         ? -1
         : val1.value.toLowerCase() > val2.value.toLowerCase()
         ? 1
         : 0;  // val1 === val2
}

/**
 * handle a form submission. basically we clean the input data,
 * make sure that at least 1 field has been filled out, and pass
 * the query data to the parent.
 * the heavy work is handled by `IconographyQueryParams`
 * @param {Object} formData: the form data as a JSON
 * @param {Object} formNode: the FormKit core node
 */
function onSubmit(formData, formNode) {
  // console.log("formData", formData)

  // remove possible errrors that are shown by a previous submission
  formNode.clearErrors();

  const queryParams = new IconographyQueryParams(formData, "form");

  console.log("AdvancedSearchQuery.onSubmit.queryParams.toJson()   :", queryParams.toJson() );
  console.log("AdvancedSearchQuery.onSubmit.queryParams.allEmpty() :", queryParams.allEmpty());

  // if no input data has been added, display an error message
  // else, submit the form.
  if ( queryParams.allEmpty() ) {
    formNode.setErrors(["Au moins un champ doit être rempli pour lancer une recherche."])
    return false;

  } else {
    emit("query-params", queryParams);
    return true;
  }
}

/**
 * if a query on the backend fails, `AdvancedSearchView` passes
 * to this component a `queryError` with value `true`. in this
 * case, display an error message on the form.
 */
watch(props, (newProps, oldProps) => {
  if ( newProps.queryError ) {
    useFormKitNodeById("advanced-search-form", (formNode) =>
      formNode.setErrors(["Le serveur a rencontré une erreur."]) );
  };

})

/******************************************/

onMounted(() => {
  // fetch data
  axios.get(new URL("/i/theme", __API_URL__))
       .then(r => themeArray.value = r.data
                                      .map(itemToFormEntry)
                                      .sort((a,b) => sortByValue(a,b)) );
  axios.get(new URL("/i/named-entity", __API_URL__))
       .then(r => namedEntityArray.value = r.data
                                            .map(itemToFormEntry)
                                            .sort((a,b) => sortByValue(a,b)) )
  axios.get(new URL("/i/institution", __API_URL__))
       .then(r => institutionArray.value = r.data
                                            .map(itemToFormEntry)
                                            .sort((a,b) => sortByValue(a,b)) );
  axios.get(new URL("/i/iconography-overall-date-range", __API_URL__))
       .then(r => {
         allowedDateRange.value = r.data; })
       .catch(e => {
         console.error("AdvancedSearchQuery: axios error on `allowedDateRange`", e);
         allowedDateRange.value = [ 1700,2100 ];
       });

  // else, on `mousedown` on the submit button, it is redimensionned...
  $("#advanced-search-form .form-submit-input").css({width: "100%"});

  // form events
  dateFilterNode.value.on("commit", (e) => { dateFilterType.value = e.payload; });
})
</script>


<style scoped>
#advanced-search-form {
  margin: 0 5%;
}
.form-field-wrapper {
  display: grid;
  grid-template-columns: 15% 85%;
  grid-template-rows: 100%;
}
.date-range {
  display: flex;
  flex-direction: row;
  justify-content: space-around;
  align-items: start;
  width: 100%;
}
.date-range > * {
  width: 100%;
  margin: 0 1vw 1vw 1vw;
}
.formkit-actions {
  margin-top: 2vh;
}
.reset-button-wrapper {
  display: flex;
  flex-direction: column;
  align-items: end;

}
.reset-button-wrapper button {
  background-color: blue;
}
</style>