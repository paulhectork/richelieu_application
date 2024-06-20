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
           id="advanced-search-form"
           submit-label="Lancer la recherche"
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
             help="Le nom de l'auteur ou de l'autrice doit contenir les mots entrés ici."
    ></FormKit>
    <FormKit type="text"
             name="publisher"
             label="Édition"
             placeholder="Bellizard"
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
               :options="themeArray"
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
        <FormKit type="number"
                 name="dateStart"
                 label="Date de début"
                 placeholder="Ex: 1810"

                 validation="dateRangeValidator"
                 :validation-rules="dateValidationRule"
        ></FormKit>
        <FormKit type="number"
                 name="dateEnd"
                 label="Date de fin"
                 placeholder="Ex: 1891"

                 validation="dateRangeValidator"
                 :validation-rules="dateValidationRule"
        ></FormKit>
      </FormKit>

      <FormKit v-else-if="dateFilterType==='dateExact'"
               type="number"
               name="date"
               label="Date exacte"
               placeholder="Ex: 1891"

               validation="dateValidator"
               :validation-rules="dateValidationRule"
      ></FormKit>
      <FormKit v-else-if="dateFilterType==='dateBefore'"
               type="number"
               name="date"
               label="Avant"
               placeholder="Ex: 1891"

               validation="dateValidator"
               :validation-rules="dateValidationRule"
      ></FormKit>
      <FormKit v-else
               type="number"
               name="date"
               label="Après"
               placeholder="Ex: 1810"

               validation="dateValidator"
               :validation-rules="dateValidationRule"
      ></FormKit>
    </div>


  </FormKit>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import axios from "axios";

import { useFormKitNodeById, createInput } from '@formkit/vue';
import $ from "jquery";

// import FormRadioTabs from "@components/FormRadioTabs.vue";
import { clickOrTouchEvent } from "@globals";
import { isEmptyArray, isEmptyScalar, isNumberInRange, isValidNumberRange } from "@utils/functions";


/******************************************/

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

  // need to find a way to run `isValidNumberRange` only on submit?
  // or at least, to rerun it on submit
  dateRangeValidator: (node) => {
    let parent = node.at("$parent");
    if ( parent.value ) {
      let dateRange = [ parent.value.dateStart, parent.value.dateEnd ];

      // if the 2 fields are filled, we check that our range is valid
      if ( dateRange.every(x => x!=null) ) {
        return dateRange.every(x => isNumberInRange(x, allowedDateRangeCurrent()) )  // every number is in the allowed range
               && isValidNumberRange(dateRange)                                            // dateStart < dateEnd

      // if only `node` is filled, we check that
      // this node is in the allowed range
      } else {
        return isNumberInRange(node.value, allowedDateRangeCurrent())
      }

    }
    // only validate the number if `node.value` isn't undefined
    return node.value != null
           ? isNumberInRange(node.value, allowedDateRangeCurrent())
           : true;

  }
};
const textValidationRule = [ ["length", 3] ];  // more than 3 chars

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
 * handle a form submission
 * @param {*} e
 */
function onSubmit(formData) {
  console.log("submitted !")
  console.log(formData);
  return


  /* basic definitions */

  // replace scalar `s` by `null` if the scalar `s` contains no formData.
  const scalar2null = s => isEmptyScalar(s) ? null : s;
  // simplify a string
  const simplifyString = s => s.toLowerCase().trim().replaceAll(/\s+/g, " ");

  /* extra validation */

  // USELESS??????????????????????????????????????????
  // MAKES THINGS EXPLICIT BUT THAT'S PRETTY MUCH IT
  // our form as JSON (pretty much the same structure
  // as `form.formData`, but we make its structure explicit here).
  // we set `null` as default value when no formData is provided
  // for a field
  const queryData = { title: scalar2null(formData.title),
                      author: scalar2null(formData.author),
                      publisher: scalar2null(formData.publisher),
                      theme: scalar2null(formData.theme),
                      namedEntity: scalar2null(formData.namedEntity),
                      institution: scalar2null(formData.institution),
                      dateFilter: formData.dateFilter,
                      date: (formData.dateFilter === "dateRange"
                            ? [ formData.date.dateStart, formData.date.dateEnd ]
                            : [ formData.date ]).map(scalar2null)  // replace `undefined` and <empty string> by `null`
  };

  // check that at least 1 of the fields has
  // been filled to be able to run the SQL query
  let allEmpty = (Object.keys(queryData)
                        .filter(k =>  k !== "dateFilter")  // dateFilter has a default value but is useless if a date isn't submitted => remove it
                        .map(k => queryData[k] instanceof Array
                                  ? isEmptyArray(queryData[k])
                                  : queryData[k] === null )
                 ).every(x => x===true)
  console.log("allEmpty", allEmpty)

  // simplify the user-inputted strings
  Object.keys(queryData)
        .filter(k => k !== "dateFilter")  // don't modify these fields
        .forEach(k => queryData[k] = typeof queryData[k] === "string"
                                     ? simplifyString(queryData[k])
                                     : Array.isArray(queryData[k])
                                     ? queryData[k].map(x => typeof x === "string"
                                                             ? simplifyString(x)
                                                             : x)
                                     : queryData[k] );

  // console.log("post", queryData, queryData.author, queryData.date);
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
        allowedDateRange.value = r.data; });

  // form events
  dateFilterNode.value.on("commit", (e) => { dateFilterType.value = e.payload; });
})
</script>


<style scoped>
#advanced-search-form {
  margin: 0 5%;
}
</style>