<!-- an advanced search form on the `iconography` SQL table.

     this creates a JSON object with the query parameters,
     which are passed to the parent. the parent updates the
     URL, fetches the answer and calls another component to
     display the results

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
    <!-- free text inputs -->
    <FormKit type="text"
             name="title"
             label="Titre"
             :validation="textValidationRule"
             help="Le titre de la ressource iconographique doit contenir les mots entrés ici."
             placeholder="Ex: Le Moniteur de la Mode"
    ></FormKit>
    <FormKit type="text"
             name="author"
             label="Auteur ou autrice"
             placeholder="Ex: Jules David"
             :validation="textValidationRule"
             help="Le nom de l'auteur ou de l'autrice doit contenir les mots entrés ici."
    ></FormKit>
    <FormKit type="text"
             name="publisher"
             label="Édition"
             placeholder="Bellizard"
             :validation="textValidationRule"
             help="Le nom de l'éditeur ou de la maison d'édition doit contenir les mots entrés ici."
    ></FormKit>

    <!-- select inputs -->
    <div v-if="namedEntityArray.length
               && themeArray.length
               && institutionArray.length"
    >
      <FormKit type="formSelect"
               name="namedEntity"
               label="Sujet"
               placeholder="Sélectionner un sujet"
               help="Sélectionner un sujet"
               :options="namedEntityArray"
      ></FormKit>
      <FormKit type="formSelect"
               name="theme"
               label="Thème"
               help="Sélectionner un thème"
               placeholder="Sélectionner un thème"
               :options="themeArray"
      ></FormKit>
      <FormKit type="formSelect"
               name="institution"
               label="Institution"
               help="Sélectionner une institution"
               placeholder="Sélectionner une institution"
               :options="institutionArray"
      ></FormKit>
    </div>

    <!-- date inputs -->
    <div>
      <FormKit type="formRadioTabs"
               id="date-filter"
               name="dateFilter"
               label="Date"
               help="Choisir le type de filtre pour la date"
               value="dateRange"
               :options="allowedDateSearchTypes"
      ></FormKit>

      <FormKit v-if="dateFilterType==='dateRange'"
               type="group"
               name="date"
               label="Date"
               help="Choisir une tranche de dates au format AAAA-AAAA"
      >
        <div class="date-range"
        >
          <FormKit type="number"
                   name="dateStart"
                   label="Date de début"
                   placeholder="Ex: 1810"
                   validation="dateRangeValidator"
                   :validation-rules="dateValidationRule"
                   :validation-messages="{ dateRangeValidator: dateRangeValidationMessage }"
                   validation-visibility="submit"
          ></FormKit>
          <FormKit type="number"
                   name="dateEnd"
                   label="Date de fin"
                   placeholder="Ex: 1891"
                   validation="dateRangeValidator"
                   :validation-rules="dateValidationRule"
                   :validation-messages="{ dateRangeValidator: dateRangeValidationMessage }"
                   validation-visibility="submit"
          ></FormKit>
        </div>
      </FormKit>

      <FormKit v-else-if="dateFilterType==='dateExact'"
               type="number"
               name="date"
               label="Date exacte"
               placeholder="Ex: 1891"
               validation="dateValidator"
               :validation-rules="dateValidationRule"
               :validation-messages="{ dateValidator: dateValidationMessage }"
      ></FormKit>
      <FormKit v-else-if="dateFilterType==='dateBefore'"
               type="number"
               name="date"
               label="Avant"
               placeholder="Ex: 1891"
               validation="dateValidator"
               :validation-rules="dateValidationRule"
               :validation-messages="{ dateValidator: dateValidationMessage }"
      ></FormKit>
      <FormKit v-else
               type="number"
               name="date"
               label="Après"
               placeholder="Ex: 1810"
               validation="dateValidator"
               :validation-rules="dateValidationRule"
               :validation-messages="{ dateValidator: dateValidationMessage }"
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
import { ref, onMounted, computed } from "vue";
import axios from "axios";

import { useFormKitNodeById, FormKitMessages } from '@formkit/vue';
import $ from "jquery";

// import FormRadioTabs from "@components/FormRadioTabs.vue";
import { clickOrTouchEvent } from "@globals";
import { isEmptyArray, isEmptyScalar, isNumberInRange, isValidNumberRange } from "@utils/functions";


/******************************************/

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

// validation rules
// see: https://formkit.com/essentials/validation#custom-rules
// and: https://stackoverflow.com/a/76391706/17915803

/** shorthand to access the array `allowedDateRange` */
const allowedDateRangeCurrent = () =>
  allowedDateRange.value.length
  ? [ allowedDateRange.value[0], allowedDateRange.value[1] ]
  : [];

const dateValidationRule = {
  dateValidator: (node) =>
    isNumberInRange(node.value, allowedDateRangeCurrent()),

  // need to find a way to run `isValidNumberRange`
  // only on submit? or at least, to rerun it on submit
  dateRangeValidator: (node) => {
    let parent = node.at("$parent");
    if ( parent.value ) {
      let dateRange = [ parent.value.dateStart, parent.value.dateEnd ];

      // if at least one field is filled, we check that our range is valid
      // else, both our fields are empty, so it's valid
      return dateRange.some(x => x!=null)
             ? dateRange.every(x => isNumberInRange(x, allowedDateRangeCurrent()) )  // every number is in the allowed range
               && isValidNumberRange(dateRange)                                      // dateStart < dateEnd
             : true;
    }
    return true;
  }
};

const textValidationRule = [ ["length", 3] ];  // more than 3 chars

const dateValidationMessage = computed(() =>
  `La date doit être au format 'AAAA' et comprise entre
  ${allowedDateRangeCurrent()[0]} et ${allowedDateRangeCurrent()[1]}`);

const dateRangeValidationMessage = computed(() =>
  `La tranche de dates doit composée de deux dates au format 'AAAA',
   comprises entre ${allowedDateRangeCurrent()[0]} et ${allowedDateRangeCurrent()[1]}`);

/******************************************/

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
 * handle a form submission. there are 3 steps:
 * - restructure slightly formData and replace all empty-ish values by undefined
 * - assert that at least 1 field has been filled (so that we can run a query)
 * - if `formData` isn't empty, update `queryParams` so that the parent
 *   can run the query. else, update the form to display an error message
 * @param {Object} formData: the form data as a JSON
 * @param {Object} formNode: the FormKit core node
 */
function onSubmit(formData, formNode) {

  // remove possible errrors that are shown by a previous submission
  formNode.clearErrors();

  // replace scalar `s` by `undefined` if the scalar `s` contains no data.
  const scalar2undefined = s => isEmptyScalar(s) ? undefined : s;
  // simplify a string
  const simplifyString = s => s.toLowerCase().trim().replaceAll(/\s+/g, " ");

  /* extra validation */

  // simplify the form. we replace all undefined-ish scalars
  // by `undefined` to simplify further processing. the only
  // item that's really changed is `date`, which is transformed
  // into an array of strings (2 if `dateFilter==='dateRange'`, 1 otherwise)
  formData = { title: scalar2undefined(formData.title),
               author: scalar2undefined(formData.author),
               publisher: scalar2undefined(formData.publisher),
               theme: scalar2undefined(formData.theme),
               namedEntity: scalar2undefined(formData.namedEntity),
               institution: scalar2undefined(formData.institution),
               dateFilter: formData.dateFilter,
               date: (formData.dateFilter === "dateRange"
                     ? [ formData.date.dateStart, formData.date.dateEnd ]
                     : [ formData.date ]).map(scalar2undefined)  // replace `undefined` and <empty string> by `null`
  };

  // check that at least 1 of the fields has
  // been filled to be able to run the SQL query
  let allEmpty = (Object.keys(formData)
                        .filter(k =>  k !== "dateFilter")  // dateFilter has a default value but is useless if a date isn't submitted => remove it
                        .map(k => formData[k] instanceof Array
                                  ? isEmptyArray(formData[k])
                                  : formData[k] === undefined )
                 ).every(x => x===true)

  // display an error message if no input data has been added
  if ( allEmpty ) {
    // submitErrors.value.push("Au moins un champ doit être rempli pour lancer une recherche.")
    formNode.setErrors(["Au moins un champ doit être rempli pour lancer une recherche."])
    return false;

  } else {
    // simplify the user-inputted strings:
    // simplify the strings, convert the dates to number
    Object.keys(formData)
          // don't modify these fields: they contain normalized data
          .filter(k => !["theme", "institution", "namedEntity", "dateFilter"].includes(k))
          // simplify all other fields
          .forEach(k =>
            formData[k] = typeof formData[k] === "string"
                          ? simplifyString(formData[k])
                          : Array.isArray(formData[k])
                          ? formData[k].map(x =>
                              typeof x === "string" && !isNaN(x)
                              ? Number(x)              // if it's not NaN, convert it to number
                              : typeof x === "string"
                              ? simplifyString(x)      // if it's another kind of string, simplify it
                              : x)                     // if it's another type (shouldn't happen), simply return it
                          : formData[k] );
    emit("query-params", formData);
  }
}

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
         console.log("AdvancedSearchQuery: axios error on `allowedDateRange`", e);
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
</style>