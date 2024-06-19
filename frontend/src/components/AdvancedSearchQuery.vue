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
  >
    <!-- free text inputs -->
    <FormKit type="text"
             name="title"
             label="Titre"
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
               name="namedEntity"
               label="Sujet"
               placeholder="Sélectionner un sujet"
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
      <!--
      <FormKit type="radio"
               name="dateFilter"
               id="date-filter"
               outer-class="radio-tabs"
               label="Date"
               help="Choisir un comment filtrer les dates"
               input-class="to-hide"
               :options="allowedDateSearchTypes"
               :sections-schema="{ //input  : { $el: 'span' }      // hide the display of the radio button
                                 }"
      ></FormKit>
      -->

      <!--    :type="dateFilterType==='dateRange' ? 'group' : 'hidden'" -->
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
        ></FormKit>
        <FormKit type="number"
                 name="dateEnd"
                 label="Date de fin"
                 placeholder="Ex: 1891"
        ></FormKit>
      </FormKit>
      <FormKit v-else-if="dateFilterType==='dateExact'"
               type="number"
               name="date"
               label="Date exacte"
               placeholder="Ex: 1891"
      ></FormKit>
      <FormKit v-else-if="dateFilterType==='dateBefore'"
               type="number"
               name="date"
               label="Avant"
               placeholder="Ex: 1891"
      ></FormKit>
      <FormKit v-else
               type="number"
               name="date"
               label="Après"
               placeholder="Ex: 1810"
      ></FormKit>
    </div>


  </FormKit>
</template>

<script setup>
import { ref, onMounted, watch } from "vue";
import axios from "axios";

import { useFormKitNodeById, createInput } from '@formkit/vue';
import $ from "jquery";

// import FormRadioTabs from "@components/FormRadioTabs.vue";
import { clickOrTouchEvent } from "@globals";
import { isEmptyArray, isEmptyScalar } from "@utils/functions";


/******************************************/

const dateFilterNode   = useFormKitNodeById("date-filter");  // useFormKitNodeById targets a FormKit node by it's HTML id and creates a vue ref.
const themeArray       = ref([]);                            // string array
const namedEntityArray = ref([]);                            // string array
const institutionArray = ref([]);                            // string array
const allowedDateRange = ref([]);                            // int array: [minDate, maxDate]
const dateFilterType   = ref("dateRange");                   // str: the type of date filter to display

const theDateSearchType = ref();

/*************************************************
 * ON EN EST OÙÙÙÙÙÙÙÙÙÙÙÙÙÙÙÙÙÙÙÙÙÙÙÙÙÙÙÙÙÙÙÙÙÙÙÙ
 * * j'ai créé FormRadioTabs, qui marche (enfin, je
 *   crois)
 * * j'essaye de récupérer la valeur dans le parent,
 *   pour faire 2 choses: modifier le filtre `date`
 *   en fonction de `dateFilterType`, et récupérer
 *   le type de filtre dans le parent.
 *   il faudrait savoir si la valeur changée dans
 *   `FormRadioTabs` est reçue ou non par notre
 *   formulaire FormKit. c'est un problème différent
 *   de savoir si les données sont reçues par le formulaire
 *   et pourquoi est-ce que le filtre `date` n'est
 *   pas misa à jour: la maj de celui-ci dépend de
 *   du ref `dateFilterType`.
 *
 * il faut ptet utiliser des watchers avec des `v-model`.
 * Dans mes tests, `watch` fonctionne sur des `v-model`
 * par défaut (type texte) de FormKit, mais j'ai pas
 * réussi à les faire marcher avec mes inputs customs.
 */
watch(theDateSearchType, (newType, oldType) => {
  console.log(newType, oldType);
})

/******************************************/

// `items` in the html form to set the `allowedDateRanger`
const allowedDateSearchTypes = [ { label:'Plage de dates', value:'dateRange' }
                               , { label:'Date exacte'   , value:'dateExact' }
                               , { label:'Avant'         , value:'dateBefore' }
                               , { label:'Après'         , value:'dateAfter'}]

// validation rules
const textValidationRule = ref(['min:3']);
/**
 * `dateValidationRule` and `dateRangeValidationRule` are
 * defined as functions, to allow to tweak the rules for each field
 * we should use `nullable` and `numeric`, but
 * if `nullable`, then `numeric` isn't applied and vice-versa....
 * (passed through the template to make shure that `allowedDateRange`
 * is loaded)
 * @param {Array<Number>} dateRange: the maximum/minimum dates allowed.
 * same as `allowedDateRange`, but passing it as an argument allows us
 * to make sure it's loaded
 */
const dateValidationRule = dateRange =>
  [ "nullable"
  , "numeric"
  , `between:${dateRange[0]},${dateRange[1]}` ];
const dateRangeValidationRule = (dateRange, fieldName) => {
  // basic date validation. see below for a
  // long version which doesn't work
  return [ "nullable"
         , "numeric"
         , `between:${dateRange[0]},${dateRange[1]}` ];

  /**
   * set dynamically the `required` and `nullable` fields.
   * on my end, it works (`isRequired` and `isNullable` return
   * the proper values), but:
   * 1) in some cases, it doesn't work, so post-submit verifications
   *    are still needed
   * 2) more importantly, using `nullable` is disables the effect
   *    of the `numeric` rule, which allows the user to submit a
   *    form with invalid data.
   *
   * TLDR: it is too much work for it to work and we still need to
   * do background validation. so we switch back to a simple validation.
   *
   * the idea is that:
   * for date ranges, we have two fields, `dateStart` and `dateEnd`.
   * either both must be filled, or none must be filled. this function
   * checks wether the two fields contain data, and sets the `required`
   * and `nullable` fields based on that.
   * it works for most cases, but not all (don't know why), so some
   * extra validation will be necessary in `onSubmit`
   */
  // const isRequired = () => {
  //   // yes the values must be targeted within
  //   // the functions, else they aren't updated
  //   // when the validation is triggered.
  //   let dateStartValue = $(`#dateStart`).val();
  //   let dateEndValue = $(`#dateEnd`).val();
  //   /*
  //   console.log("required",
  //               dateEndValue, dateStartValue,
  //               !isEmptyScalar(dateStartValue) || !isEmptyScalar(dateEndValue));
  //   */
  //   return !isEmptyScalar(dateStartValue) || !isEmptyScalar(dateEndValue);
  // }
  // const isNullable = () => {
  //   let dateStartValue = $(`#dateStart`).val();
  //   let dateEndValue = $(`#dateEnd`).val();
  //   /*
  //   console.log("nullable",
  //               dateEndValue, dateStartValue,
  //               isEmptyScalar(dateStartValue) && isEmptyScalar(dateEndValue));
  //   */
  //   return isEmptyScalar(dateStartValue) && isEmptyScalar(dateEndValue);
  // }
  // /***************************************************************************
  //  ***************************************************************************
  //  * `NUMERIC` IS NOT APPLIED WHEN
  //  * `nullable` IS SET => THIS FUNCTION
  //  * UNAPPLIES `numeric` !!!!!!!!!!!!!!
  //  ***************************************************************************
  //  ***************************************************************************/
  // return [ "numeric"
  //        , `between:${dateRange[0]},${dateRange[1]}`
  //        , { nullable: isNullable }
  //        , { required: isRequired }
  //        ]
}

/******************************************/

/**
 * change the `dateFilterType` value to
 * change the date filter to display in the form
 * @param {string} val: the new value
 */
function changeDateSearchType (val) {
  dateFilterType.value = val
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
 *
 * @param {*} e
 */
function onSubmit(form, formData) {
  console.log("submitted !")

  /* basic definitions */

  let data = form.data;
  // replace scalar `s` by `null` if the scalar `s` contains no data.
  const scalar2null = s => isEmptyScalar(s) ? null : s;
  // simplify a string
  const simplifyString = s => s.toLowerCase().trim().replaceAll(/\s+/g, " ");

  /* extra validation */

  // our form as JSON (pretty much the same structure
  // as `form.data`, but we make its structure explicit here).
  // we set `null` as default value when no data is provided
  // for a field
  const queryData = { title: scalar2null(data.title),
                      author: scalar2null(data.author),
                      publisher: scalar2null(data.publisher),
                      theme: scalar2null(data.theme),
                      namedEntity: scalar2null(data.namedEntity),
                      institution: scalar2null(data.institution),
                      dateFilter: data.dateFilter,
                      date: (data.dateFilter === "dateRange"
                            ? [ data.date.dateStart, data.date.dateEnd ]
                            : [ data.date ]).map(scalar2null)  // replace `undefined` and <empty string> by `null`
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

  // make sure we have valid dates
  // (a date is a 4-digit number,
  // a date range is 2 4-digit numbers, start of the range <= end of the range)
  if ( ! queryData.date.every(x => x==null) ) {
    // it's a valid date, but not a date range
    let hasValidDate = queryData.dateFilter !== "dateRange"     // not a date range
                       && queryData.date.every(x => !isNaN(x)); // the date is a valid number
    // it's a date range, with 2 numbers
    let hasDateRange = queryData.dateFilter==="dateRange"
                       && queryData.date.length === 2           // has 2 items
                       && queryData.date.every(x => !isNaN(x)); // all values are numbers
    // it's a valid date range (start date is lower than end date)
    let hasValidDateRange = queryData.dateFilter==="dateRange"
                           && Number(queryData.date[0]) <= Number(queryData.date[1]);

    /**
     * LE PROBLÈME: AVEC NUMERIC, SI IL Y A DES CARACTÈRES NON-NUMÉRIQUES,
     * ALORS ILS NE SONT PAS RENVOYÉS ICI ET ON A UNDEFINED. DONC ON NE PEUT
     * PAS AFFICHER QUE LA DATE EST INVALIDE, MAIS EN TOUT CAS LES DONNÉES
     * NE SONT PAS RÉCUPÉRÉES
     */
    if ( !hasValidDate || !hasDateRange || !hasValidDateRange ) {
      // display error message
      console.log("noooo");
      //console.log(
        form$.value.el$("date").messageBag
                                          .prepends
                                          .errors
                                          .push("hello")
       // )  //.apppend('Prepended error', "message")
    }
  }

  // console.log("pre", queryData, queryData.author, queryData.date);

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
        allowedDateRange.value = r.data;
       });


  // form events
  dateFilterNode.value.on("commit", (e) => { dateFilterType.value = e.payload; });
})
</script>


<style scoped>
#advanced-search-form {
  margin: 0 5%;
}
</style>