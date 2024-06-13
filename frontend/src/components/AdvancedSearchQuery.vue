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
                     placeholder="1800"
                     input-type="number"
                     :rules="dateRangeValidationRule('dateEnd')"
        ></TextElement>
        <TextElement name="dateEnd"
                     placeholder="1900"
                     input-type="number"
                     :rules="dateRangeValidationRule('dateStart')"
        ></TextElement>
      </ObjectElement>
      <TextElement v-else-if="dateSearchType === 'dateExact'"
                   name="date"
                   placeholder="1824 (exact)"
                   input-type="number"
                   :rules="dateValidationRule"
      ></TextElement>
      <TextElement v-else-if="dateSearchType === 'dateBefore'"
                   name="date"
                   placeholder="1824 (avant)"
                   input-type="number"
                   :rules="dateValidationRule"
      ></TextElement>
      <TextElement v-else
                   name="date"
                   placeholder="1824 (après)"
                   input-type="number"
                   :rules="dateValidationRule"
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

import { clickOrTouchEvent } from "@globals";


/******************************************/

const form$                   = ref(null);         // VueForm
const themeArray              = ref([]);           // string array
const namedEntityArray        = ref([]);           // string array
const institutionArray        = ref([]);           // string array
const allowedDateRange        = ref([]);           // int array: [minDate, maxDate]
const dateSearchType          = ref("dateRange");  // str: the type of date filter to display
const dateValidationRule      = ref([]);           // string array. how dates are validated. defined as a `ref` to wait for `allowedDateRange` to load
const dateRangeValidationRule = ref(false);           // array of string|object. how a date range is validated. defined in `onMounted` (for the same reasons as above) as a function that takes into account a `TextElement` @name and defines which fields are required

// `items` in the html form to set the `allowedDateRanger`
const allowedDateSearchTypes = [ { label:'Plage de dates', value:'dateRange' }
                               , { label:'Date exacte', value:'dateExact' }
                               , { label:'Avant', value:'dateBefore' }
                               , { label:'Après', value:'dateAfter'}]
const textValidationRule = ref(['min:3']);  // minimum of 3 chars

/******************************************/

/**
 * `o` has a key `entry_name` and
 * other data. return `entry_name` only
 * @param {Object} o: the object to process
 * @returns {string}
 */
function objToName(o) {
  return o.entry_name;
}

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
  /*****************************************/
  /* basic definitions */

  let data = form.data;

  // a scalar (undefined, null, string or number) contains no data
  const isEmptyScalar = s => s === undefined || s === null || s === "" || s.length === 0;
  // an array is empty, or it contains only elements with no data
  const isEmptyArray = arr => arr.length === 0 || arr.every(x => isEmptyScalar(x));
  // replace scalar `s` by `null` if the scalar `s` contains no data.
  const scalar2null = s => isEmptyScalar(s) ? null : s;
  // simplify a string
  const simplifyString = s => s.toLowerCase().trim().replaceAll(/\s+/g, " ");

  /***************************************** /
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
                            : [ data.date ]).map(x => scalar2null(x))  // replace `undefined` and <empty string> by `null`
  };

  console.log("pre", queryData, queryData.author, queryData.date);

  // simplify the user-inputted strings
  Object.keys(queryData)
        .filter(k => k !== "dateFilter")  // fields to preserve
        .forEach(k => queryData[k] = typeof queryData[k] === "string"
                                     ? simplifyString(queryData[k])
                                     : Array.isArray(queryData[k])
                                     ? queryData[k].map(x => typeof x === "string"
                                                             ? simplifyString(x)
                                                             : x)
                                     : queryData[k] );

  console.log("post", queryData, queryData.author, queryData.date);

  // check that at least 1 of the fields has
  // been filled to be able to run the SQL query
  let allEmpty = (Object.keys(queryData)
                        .filter(k =>  k !== "dateFilter")  // dateFilter has a default value but is useless if a date isn't submitted => remove it
                        .map(k => queryData[k] instanceof Array
                                  ? isEmptyArray(queryData[k])
                                  : queryData[k] === null )
                 ).every(x => x===true)
  // console.log(allEmpty)

  /* in theory handled by a VueForm validator:
   * date must contain an array of 1 or 2 valid numbers.
  let validDateType;
  try {
    queryData.date = queryData.date.map(x => Number(x));
    validDateType = true;
  } catch {
    validDateType = false;
  }*/
  // process `queryData.date`:
  // if querying for a date range (dateFilter === 'dateRange'),
  // `dateStart < dateEnd`
  let validDateRange = queryData.dateFilter === "dateRange"
                       ? queryData.dateFilter[0] <= queryData.dateFilter[1]
                       : true;

  console.log(validDateType, validDateRange)

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
                                      .map(objToName)
                                      .sort() );
  axios.get(new URL("/i/named-entity", __API_URL__))
       .then(r => namedEntityArray.value = r.data
                                            .map(objToName)
                                            .sort() )
  axios.get(new URL("/i/institution", __API_URL__))
       .then(r => institutionArray.value = r.data
                                            .map(objToName)
                                            .sort() );
  axios.get(new URL("/i/iconography-overall-date-range", __API_URL__))
       .then(r => {
        allowedDateRange.value = r.data;
        // we should use `nullable` and `numeric`, but
        // if `nullable`, then `numeric` isn't applied and vice-versa....
        dateValidationRule.value = [ //"required"
                                    "numeric"
                                   , `between:${allowedDateRange.value[0]},${allowedDateRange.value[1]}` ];
        dateRangeValidationRule.value = otherFieldName =>
          // defines wether or not one field is required based on the value of the other field
          [ "numeric"
          , `between:${allowedDateRange.value[0]},${allowedDateRange.value[1]}`
          , { required: [otherFieldName, true] }
          , { nullable: [otherFieldName, false] } ]
       });
})
</script>


<style scoped>
.advanced-search-form {
  margin: 0 5%;
}
</style>