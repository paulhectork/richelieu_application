<!-- an advanced search form on the `iconography` SQL table.

     this creates a JSON object with the query parameters,
     which are passed to the parent. the parent updates the
     URL, fetches the answer and calls another component to
     display the results

     see:
     https://vueform.com/docs/handling-form-data
-->

<template>
  <Vueform ref="form$"
           class="advanced-search-form"
           :endpoint="onSubmit"
  >
    <!-- full text basic info -->
    <TextElement name="title"
                 label="Titre"
                 placeholder="Le Moniteur de la Mode"
    ></TextElement>
    <TextElement name="author"
                 label="Auteur ou autrice"
                 placeholder="Jules David"
    ></TextElement>
    <TextElement name="publisher"
                 label="Édition"
                 placeholder="Bellizard"
    ></TextElement>

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
                  v-if="allowedDateRange.length">
      <RadiogroupElement view="tabs"
                         :submit="false"
                         default="dateRange"
                         :items="allowedDateFilters"
                         @change="changeDateSearchType"
      ></RadiogroupElement>
      <ObjectElement name="dateRange"
                     class="date-range-form"
                     v-if="dateSearchType === 'dateRange'"
                     :columns="{ container:12, wrapper:6, label:0 }"
      >
        <TextElement name="dateStart"
                     placeholder="1800"
                     input-type="number"
                     :rules="[ 'nullable'
                             , 'numeric'
                             , `between:${allowedDateRange[0]},${allowedDateRange[1]}` ]"
        ></TextElement>
        <TextElement name="dateEnd"
                     placeholder="1900"
                     input-type="number"
                     :rules="[ 'nullable'
                             , 'numeric'
                             , `between:${allowedDateRange[0]},${allowedDateRange[1]}` ]"
        ></TextElement>
      </ObjectElement>
      <TextElement name="dateExact"
                   placeholder="1824 (exact)"
                   input-type="number"
                   :rules="[ 'nullable'
                           , 'numeric'
                           , `between:${allowedDateRange[0]},${allowedDateRange[1]}` ]"
                   v-else-if="dateSearchType === 'dateExact'"
      ></TextElement>
      <TextElement name="dateBefore"
                   placeholder="1824 (avant)"
                   input-type="number"
                   :rules="[ 'nullable'
                           , 'numeric'
                           , `between:${allowedDateRange[0]},${allowedDateRange[1]}` ]"
                   v-else-if="dateSearchType === 'dateBefore'"
      ></TextElement>
      <TextElement name="dateAfter"
                   placeholder="1824 (après)"
                   input-type="number"
                   :rules="[ 'nullable'
                           , 'numeric'
                           , `between:${allowedDateRange[0]},${allowedDateRange[1]}` ]"
                   v-else
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

const form$            = ref(null);         // VueForm
const themeArray       = ref([]);           // string array
const namedEntityArray = ref([]);           // string array
const institutionArray = ref([]);           // string array
const allowedDateRange = ref([]);           // int array: [minDate, maxDate]
const dateSearchType   = ref("dateRange");  // str: the type of date filter to display

// `:items` in the html form to set the `allowedDateRanger`
const allowedDateFilters = [ { label:'Plage de dates', value:'dateRange' }
                           , { label:'Date exacte', value:'dateExact' }
                           , { label:'Avant', value:'dateBefore' }
                           , { label:'Après', value:'dateAfter'}]

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
function onSubmit(formData, form) {
  console.log(formData);
  console.log(form);
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
       .then(r => allowedDateRange.value = r.data );
})
</script>


<style scoped>
.advanced-search-form {
  margin: 0 5%;
}
</style>