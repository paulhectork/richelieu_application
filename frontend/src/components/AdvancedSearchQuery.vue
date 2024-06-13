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
                     id="dateStart"
                     placeholder="1800"
                     input-type="number"
                     :rules="dateRangeValidationRule(allowedDateRange, 'dateEnd')"
        ></TextElement>
        <TextElement name="dateEnd"
                     id="dateEnd"
                     placeholder="1900"
                     input-type="number"
                     :rules="dateRangeValidationRule(allowedDateRange, 'dateStart')"
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
 * @param {string} otherFieldName: if `dateSearchType === 'dateRange'`,
 * we have two fields, `dateStart` and `dateEnd`. we need to make sure
 * thanks to that, we can require `dateStart` and `dateEnd` to be filled
 * if the other one contains data.
 */
const dateValidationRule = dateRange =>
  [ "nullable"
  , "numeric"
  , `between:${dateRange[0]},${dateRange[1]}` ];

const dateRangeValidationRule = (dateRange, otherFieldName) => {
  // `true` if one of the two fields contain data, false otherwise
  /*
  let containsData =
    $("#dateStart, #dateEnd").length
    ? [ $("#dateStart, #dateEnd")[0].value, $("#dateStart, #dateEnd")[1].value ]  // array of inputed values for both fields
      .some(x => x != "")
    : false;

  // containsData works but the below doesn't
  ///////////////////////////////////////////

  // let requiredOrNullable = containsData ? "required" : "nullable";
  // console.log(">", containsData, requiredOrNullable);

  // a new upper / lowerbound defined by the input in `otherFieldName`
  let addRule;
  if ( containsData ) {
    addRule = { required: () => true }
  } else {
    addRule = { nullable: () => true }
  } return [ "numeric"
           , `between:${dateRange[0]},${dateRange[1]}`
           , addRule
           ]
  */
  return [ "numeric"
         , `between:${dateRange[0]},${dateRange[1]}`
         , { required: (form$, Validator) => {
              Validator.watch(["dateStart", "dateEnd"]);
              let otherFieldValue = form$.el$(otherFieldName)?.value;
              console.log(otherFieldValue,
                          otherFieldValue !== undefined);
              return otherFieldValue !== undefined //|| otherFieldValue !== ""
           }
         }
         ]
  /*
  return [ "numeric"
         , `between:${allowedDateRange.value[0]},${allowedDateRange.value[1]}`
         , { required: [otherFieldName, true] }
         , { nullable: [otherFieldName, false] } ]
  */

}
/*
const dateRangeValidationRule = (dateRange, otherFieldName) => {
  let out = [ "numeric"
    , `between:${dateRange[0]},${dateRange[1]}`
    , { required: (form$, Validator) => {
        Validator.watch([ "dateStart", "dateEnd" ]);
        console.log( "required:"
                   , otherFieldName
                   , form$.el$(otherFieldName)?.value
                   , form$.el$(otherFieldName)?.value != null );
        return form$.el$(otherFieldName)?.value != null
      }
    }, { nullable: (form$, Validator) => {
        Validator.watch([ "dateStart", "dateEnd" ]);
        console.log( "nullable:"
                   , otherFieldName
                   , form$.el$(otherFieldName)?.value
                   , form$.el$(otherFieldName)?.value == null );
        return form$.el$(otherFieldName)?.value == null
      }
    }//[otherFieldName, true] }
  ]//, { nullable: [otherFieldName, false] } ];
  // console.log(out);
  console.log("******************");
  return out;
}
*/


const textValidationRule = ref(['min:3']);

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

  // make sure we have a valid date range (start of the range < end of the range)
  let validDateRange = queryData.dateFilter === "dateRange"
                       ? queryData.dateFilter[0] <= queryData.dateFilter[1]
                       : true;

  console.log(validDateRange)


  // check that at least 1 of the fields has
  // been filled to be able to run the SQL query
  let allEmpty = (Object.keys(queryData)
                        .filter(k =>  k !== "dateFilter")  // dateFilter has a default value but is useless if a date isn't submitted => remove it
                        .map(k => queryData[k] instanceof Array
                                  ? isEmptyArray(queryData[k])
                                  : queryData[k] === null )
                 ).every(x => x===true)
  // console.log(allEmpty)

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
       });
})
</script>


<style scoped>
.advanced-search-form {
  margin: 0 5%;
}
</style>