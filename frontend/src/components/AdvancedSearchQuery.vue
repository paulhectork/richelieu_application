<!-- an advanced search form on the `iconography` SQL table.

     this creates a JSON object with the query parameters,
     which are passed to the parent. the parent updates the
     URL, fetches the answer and calls another component to
     display the results
-->

<template>
  <Vueform class="advanced-search-form">
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
                   search="true"
                   strict="false"
                   :native="false"
                   :items="themeArray"
      ></SelectElement>
      <SelectElement name="namedEntity"
                     label="Sujet"
                     placeholder="Sélectionner un sujet"
                     search="true"
                     strict="false"
                     :native="false"
                     :items="namedEntityArray"
      ></SelectElement>
      <SelectElement name="institution"
                     label="Institution"
                     placeholder="Sélectionner une institution de conservation"
                     search="true"
                     strict="false"
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
    <GroupElement name="date"
                  label="Date">
      <RadiogroupElement view="tabs"
                         submit="false"
                         default="dateRange"
                         :items="[{ label:'Plage de dates', value:'dateRange' },
                                  { label:'Date exacte', value:'dateExact' },
                                  { label:'Avant', value:'dateBefore' },
                                  { label:'Après', value:'dateAfter'}]"
                         @change="changeDateSearchType"
      ></RadiogroupElement>
      <ObjectElement name="dateRange"
                     class="date-range-form"
                     v-if="dateSearchType === 'dateRange'"
                     :columns="{ container:12, wrapper:6, label:0 }"
      >
        <TextElement name="dateStart"
                     placeholder="1800"
        ></TextElement>
        <TextElement name="dateEnd"
                     placeholder="1900">
        ></TextElement>
      </ObjectElement>
      <TextElement name="dateExact"
                   placeholder="1824 (exact)"
                   v-else-if="dateSearchType === 'dateExact'"
      ></TextElement>
      <TextElement name="dateBefore"
                   placeholder="1824 (avant)"
                   v-else-if="dateSearchType === 'dateBefore'"
      ></TextElement>
      <TextElement name="dateAfter"
                   placeholder="1824 (après)"
                   v-else
      ></TextElement>
    </GroupElement>

  </Vueform>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";

import { clickOrTouchEvent } from "@globals";


/******************************************/

const themeArray       = ref([]);  // string array
const namedEntityArray = ref([]);  // string array
const institutionArray = ref([]);  // string array
const allowedDateRange = ref([]);  // int array: [minDate, maxDate]
const dateSearchType   = ref("dateRange");  // str: the type of date filter to display

/**
 * `o` has a key `entry_name` and
 * other data. return `entry_name` only
 * @param {Object} o: the object to process
 * @returns {string}
 */
function objToName(o) {
  return o.entry_name;
}

function changeDateSearchType (val) {
  dateSearchType.value = val
}

// load the data from the DB
(() => {
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
       .then(r => allowedDateRange.value = r.data )
})()

/******************************************/

</script>


<style scoped>
.advanced-search-form {
  margin: 0 5%;
}
</style>