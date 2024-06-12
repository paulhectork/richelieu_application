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
    <GroupElement>
      <TextElement name="title"
                   label="Titre"
                   placeholder="Le Moniteur de la Mode"
                   input-type="text"
      ></TextElement>
      <TextElement name="author"
                   label="Auteur ou autrice"
                   placeholder="Jules David"
      ></TextElement>
      <TextElement name="publisher"
                   label="Édition"
                   placeholder="Bellizard"
      ></TextElement>
    </GroupElement>

    <!-- query structured metadata: themes, named entites -->
    <GroupElement>
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
                  v-if="allowedDateRange.length && dateValidationRule.length"
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
        <TextElement name="dateStart"
                     placeholder="1800"
                     input-type="number"
                     :rules="dateValidationRule"
        ></TextElement>
        <TextElement name="dateEnd"
                     placeholder="1900"
                     input-type="number"
                     :rules="dateValidationRule"
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

const form$              = ref(null);         // VueForm
const themeArray         = ref([]);           // string array
const namedEntityArray   = ref([]);           // string array
const institutionArray   = ref([]);           // string array
const allowedDateRange   = ref([]);           // int array: [minDate, maxDate]
const dateSearchType     = ref("dateRange");  // str: the type of date filter to display
const dateValidationRule = ref([]);           // string array. how dates are validated. defined as a `ref` to wait for `allowedDateRange` to load

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
  /* preprocessing */

  let queryData = form.data;
  let dateFilter = queryData.dateFilter;
  console.log(queryData);

  // queryData.date is either a scalar
  // (if `dateFilter` is one of `dateStart`, `dateEnd`, `dateExact`)
  // or a proxy. convert it to an array of 1 or 2 items to have a plain JSON
  queryData.date = dateFilter === "dateRange"
                   ? [ queryData.date.dateStart, queryData.date.dateEnd ]
                   : [ queryData.date ];  //.filter(x => x != null);

  const isEmptyScalar = sca => sca == null || sca === "" || sca.length === 0;
  const isEmptyArray = arr => arr.length === 0 || !arr.some(x => !isEmptyScalar(x));

  /*****************************************/
  /* extra validation */

  /*************************************************
   * PROBLÈME:
   * LES CHAMPS DE TEXTE VIDE NE SONT PAS RETOURNÉS
   * + LES FONCTIONS GÉNÉRIQUES C'EST COMPLIQUÉ
   * => SIMPLIFIER?
   ************************************************/

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
        dateValidationRule.value = [ "nullable"
                                   , "numeric"
                                   , `between:${allowedDateRange.value[0]},${allowedDateRange.value[1]}` ];
       });
})
</script>


<style scoped>
.advanced-search-form {
  margin: 0 5%;
}
</style>