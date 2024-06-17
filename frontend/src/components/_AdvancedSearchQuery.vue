<!-- an advanced search form on the `iconography` SQL table.

     this creates a JSON object with the query parameters,
     which are passed to the parent. the parent updates the
     URL, fetches the answer and calls another component to
     display the results

     see:
     https://vueform.com/docs/handling-form-data
-->

<template>
  <!-- :endpoint+@submit allows to disable
       endpoint fetching in favour of our
       own onSubmit function -->
  <Vueform ref="form$"
           class="advanced-search-form"
           validate-on=""
           :endpoint=false
           @submit="async (form$, FormData) => onSubmit(form$, FormData)"
  >
    <!-- full text basic info -->
    <GroupElement name="text-search">
      <TextElement name="title"
                   label="Titre"
                   placeholder="Le Moniteur de la Mode"
                   input-type="text"
                   :rules="textValidationRule"
      ></TextElement>
      <TextElement name="author"
                   label="Auteur ou autrice"
                   placeholder="Jules David"
                   :rules="textValidationRule"
      ></TextElement>
      <TextElement name="publisher"
                   label="Édition"
                   placeholder="Bellizard"
                   :rules="textValidationRule"
      ></TextElement>
    </GroupElement>

    <!-- query structured metadata: themes, named entites -->
    <GroupElement name="structured-search">
      <SelectElement name="theme"
                     label="Thème"
                     placeholder="Sélectionner un thème"
                     :search="true"
                     :strict="false"
                     :native="false"
                     :items="themeArray"
      ></SelectElement>
      <SelectElement name="namedEntity"
                     label="Sujet"
                     placeholder="Sélectionner un sujet"
                     :search="true"
                     :strict="false"
                     :native="false"
                     :items="namedEntityArray"
      ></SelectElement>
      <SelectElement name="institution"
                     label="Institution"
                     placeholder="Sélectionner une institution de conservation"
                     :search="true"
                     :strict="false"
                     :native="false"
                     :items="institutionArray"
      ></SelectElement>
    </GroupElement>

    <!-- query dates -->
    <!--
    <SliderElement name="date"
                   label="Date de création"
                   merge="100"
                   :min="allowedDateRange[0]"
                   :max="allowedDateRange[1]"
                   :default="[ 1800, 1900 ]"
    ></SliderElement>
    -->
    <!-- query dates
         the `v-if` allows to wait for `allowedDateRange`
         to be loaded before initializing the `rules` attributes.
         this mimics an anync loading of the rules -->
    <GroupElement name="date"
                  label="Date"
                  v-if="allowedDateRange.length
                        && dateValidationRule.length
                        && dateRangeValidationRule"
    >
      <RadiogroupElement view="tabs"
                         name="dateFilter"
                         default="dateRange"
                         :items="allowedDateSearchTypes"
                         @change="changeDateSearchType"
      ></RadiogroupElement>
      <ObjectElement v-if="dateSearchType === 'dateRange'"
                     name="date"
                     class="date-range-form"
                     :columns="{ container:12, wrapper:6, label:0 }"
      >
        <!-- if one of the 2 dates is given, the other is mandatory -->
        <TextElement name="dateStart"
                     id="dateStart"
                     placeholder="1800"
                     input-type="number"
                     :rules="dateRangeValidationRule(allowedDateRange)"
        ></TextElement>
        <TextElement name="dateEnd"
                     id="dateEnd"
                     placeholder="1900"
                     input-type="number"
                     :rules="dateRangeValidationRule(allowedDateRange)"
        ></TextElement>
      </ObjectElement>
      <TextElement v-else-if="dateSearchType === 'dateExact'"
                   name="date"
                   placeholder="1824 (exact)"
                   input-type="number"
                   :rules="dateValidationRule(allowedDateRange)"
      ></TextElement>
      <TextElement v-else-if="dateSearchType === 'dateBefore'"
                   name="date"
                   placeholder="1824 (avant)"
                   input-type="number"
                   :rules="dateValidationRule(allowedDateRange)"
      ></TextElement>
      <TextElement v-else
                   name="date"
                   placeholder="1824 (après)"
                   input-type="number"
                   :rules="dateValidationRule(allowedDateRange)"
      ></TextElement>
    </GroupElement>

    <!-- submit -->
    <ButtonElement name="register"
                   button-label="Lancer la recherche"
                   :submits="true"
                   :full="true"
                   size="lg"
    ></ButtonElement>

  </Vueform>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import axios from "axios";

import $ from "jquery";

import { clickOrTouchEvent } from "@globals";
import { isEmptyArray, isEmptyScalar } from "@utils/functions";


/******************************************/

const form$            = ref(null);         // VueForm
const themeArray       = ref([]);           // string array
const namedEntityArray = ref([]);           // string array
const institutionArray = ref([]);           // string array
const allowedDateRange = ref([]);           // int array: [minDate, maxDate]
const dateSearchType   = ref("dateRange");  // str: the type of date filter to display

/******************************************/

// `items` in the html form to set the `allowedDateRanger`
const allowedDateSearchTypes = [ { label:'Plage de dates', value:'dateRange' }
                               , { label:'Date exacte', value:'dateExact' }
                               , { label:'Avant', value:'dateBefore' }
                               , { label:'Après', value:'dateAfter'}]

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
 * change the `dateSearchType` value to
 * change the date filter to display in the form
 * @param {string} val: the new value
 */
function changeDateSearchType (val) {
  dateSearchType.value = val
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
  /*
  let validDateRange = queryData.dateFilter === "dateRange"
                       ? queryData.date.length === 2                                     // contains 2 items
                         && ( queryData.date.filter(x => !isNaN(x)).length === 0  // that are numbers
                            || queryData.date.every(x => x==null) )                      // or none of the 2 values are numbers
                         && queryData.dateFilter[0] <= queryData.dateFilter[1]           // dateStart < dateEnd
                       : true;

  console.log("validDateRange", validDateRange)
  */


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



  /*
  // queryData.date is either a scalar
  // (if `dateFilter` is one of `dateStart`, `dateEnd`, `dateExact`)
  // or a proxy. convert it to an array of 1 or 2 items to have a plain JSON
  queryData.date = dateFilter === "dateRange"
                   ? [ queryData.date.dateStart, queryData.date.dateEnd ]
                   : [ queryData.date ];  //.filter(x => x != null);

  const isEmptyScalar = sca => sca == null || sca === "" || sca.length === 0;
  const isEmptyArray = arr => arr.length === 0 || !arr.some(x => !isEmptyScalar(x));

  /***************************************** /
  /* extra validation * /


  // have we set at least one filter?
  let allEmptyFilters = (
    Object
    .keys(queryData)
    .filter(k => k !== "dateFilter" )  // `dateFilter` gets a default value which can't help us to make a query on its own => don't take it into account
    .map((k) => Array.isArray(queryData[k])
                ? isEmptyArray(queryData[k])  // either array doesn't have a length or it contains only null or undefined elts
                : isEmptyScalar(queryData[k]) )
  )
  console.log(allEmptyFilters);
  */


  /* send the JSON to parent */
}

// load the data from the DB

/******************************************/

onMounted(() => {
  axios.get(new URL("/i/theme", __API_URL__))
       .then(r => themeArray.value = r.data
                                      .map(x => x.entry_name)
                                      .sort() );
  axios.get(new URL("/i/named-entity", __API_URL__))
       .then(r => namedEntityArray.value = r.data
                                            .map(x => x.entry_name)
                                            .sort() )
  axios.get(new URL("/i/institution", __API_URL__))
       .then(r => institutionArray.value = r.data
                                            .map(x => x.entry_name)
                                            .sort() );
  axios.get(new URL("/i/iconography-overall-date-range", __API_URL__))
       .then(r => {
        allowedDateRange.value = r.data;
       });
})
</script>


<style scoped>
.advanced-search-form {
  margin: 0 5%;
}
</style>