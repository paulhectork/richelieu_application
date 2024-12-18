<template>

  <!-- FormDate.vue
  
       a component with a repeatable date search field.
       this component can encapsulate several date fields
       of different types: dateExact, dateBefore, dateAfter,
       dateRange. it is a distinct component for clarity.
  
       this component contains an <ul>, where each <li>
       is a complete date field. this date field contains:
       - a date filter, which helps us to use the kind of date search
         (dateStart, dateBefore, dateAfter, dateExact)
       - a date input, with either one or two number fields.
  
       output structure:
       *****************
       the form returns a dict where each date search (each <li> in the HTML)
       is identified by an UUID which serves as the root for the different
       keys of the dict: <uuid>-date-filter targets the date filter,
       <uuid>-date-dateStart the first date of a range.
       if we're filtering by a date range the structure is:
        {
          <uuid>-date-filter: "dateRange",
          <uuid>-date: {
            <uuid>-date-dateStart: <1st date of the range>,
            <uuid>-date-dateEnd: <2nd date of the range>
          }
        }
       else:
        { <uuid>-date-filter: "dateExact"|"dateBefore"|"dateAfter",
          <uuid>-date: <the date> }
  
      output example:
      ***************
      {
        // input 1
        "form-repeatable-date-11de98a2-9cce-4d3b-909a-ec683af1bf87-date-filter": "dateRange",
        "form-repeatable-date-11de98a2-9cce-4d3b-909a-ec683af1bf87-date": {
          "form-repeatable-date-11de98a2-9cce-4d3b-909a-ec683af1bf87-dateStart": "1920",
          "form-repeatable-date-11de98a2-9cce-4d3b-909a-ec683af1bf87-dateEnd": "1930"
        },
        // input 2
        "form-repeatable-date-0a1b675a-7bf2-42d4-b565-9f4d0fc7b4af-date-filter": "dateBefore",
        "form-repeatable-date-0a1b675a-7bf2-42d4-b565-9f4d0fc7b4af-date": "1801",
        // input 3
        "form-repeatable-date-b9c62d68-631f-4d17-9c3e-bbda7e8c5caa-date-filter": "dateAfter",
        "form-repeatable-date-b9c62d68-631f-4d17-9c3e-bbda7e8c5caa-date": "1872"
      }
   -->



  <div class="form-field-input-wrapper">
    <FormKit type="group"
             name="date"
             id="form-repeatable-date"
    >

      <ul class="list-invisible">
        <li v-for="[htmlId, dateField] in Object.entries(inputFields)"
            :id="htmlId"
        >
          <!-- <p>{{ htmlId.slice(-5) }}</p> -->

          <!-- the actual date input -->
          <div class="input-wrapper">
            <!-- select the date filter type -->
            <FormKit type="fkRadioTabs"
                     :id="`${htmlId}-date-filter`"
                     :name="`${htmlId}-date-filter`"
                     label="Date"
                     help="Choisir le type de filtre pour la date"
                     value="dateRange"
                     default="dateRange"
                     :options="allowedDateSearchTypes"
                     @input="newInput => updateDateFilter(newInput, htmlId)"
            ></FormKit>

            <!-- date range -->
            <FormKit v-if="inputFields[htmlId].filter==='dateRange'"
                     type="group"
                     :name="`${htmlId}-date`"
                     label="Date"
                     help="Choisir une tranche de dates au format AAAA-AAAA"
            >
              <div class="date-range">
                <FormKit type="number"
                         :name="`${htmlId}-dateStart`"
                         label="Date de début"
                         placeholder="Ex: 1810"
                         :data-allowedDateRange="allowedDateRange"
                         validation="dateRangeValidator"
                         @input="newInput => updateDateData(newInput, htmlId, 0)"
                ></FormKit>
                <FormKit type="number"
                         :name="`${htmlId}-dateEnd`"
                         label="Date de fin"
                         placeholder="Ex: 1891"
                         :data-allowedDateRange="allowedDateRange"
                         validation="dateRangeValidator"
                         @input="newInput => updateDateData(newInput, htmlId, 1)"
                ></FormKit>
              </div>
            </FormKit>

            <!-- exact date -->
            <FormKit v-else-if="inputFields[htmlId].filter==='dateExact'"
                     type="number"
                     :name="`${htmlId}-date`"
                     label="Date exacte"
                     placeholder="Ex: 1891"
                     :data-allowedDateRange="allowedDateRange"
                     validation="dateValidator"
                     @input="newInput => updateDateData(newInput, htmlId, 0)"
            ></FormKit>

            <!-- before -->
            <FormKit v-else-if="inputFields[htmlId].filter==='dateBefore'"
                     type="number"
                     :name="`${htmlId}-date`"
                     label="Avant"
                     placeholder="Ex: 1891"
                     :data-allowedDateRange="allowedDateRange"
                     validation="dateValidator"
                     @input="newInput => updateDateData(newInput, htmlId, 0)"
            ></FormKit>

            <!-- after -->
            <FormKit v-else
                     type="number"
                     :name="`${htmlId}-date`"
                     label="Après"
                     placeholder="Ex: 1810"
                     :data-allowedDateRange="allowedDateRange"
                     validation="dateValidator"
                     @input="newInput => updateDateData(newInput, htmlId, 0)"
            ></FormKit>
          </div>

          <!-- add/delete buttons -->
          <div class="button-container">
            <UiButtonCross v-if="displayUiButtonCross(htmlId)"
                        type="button"
                        @click="popField(htmlId)"
                        @touchEnd="popField(htmlId)"
            ></UiButtonCross>
            <UiButtonPlus v-if="displayUiButtonPlus(htmlId)"
                        type="button"
                        @click="addField"
                        @touchEnd="addField"
            ></UiButtonPlus>
          </div>

        </li>
      </ul>

    </FormKit>

  </div>

</template>


<script setup>
import { onMounted, ref } from "vue"
import axios from "axios";

import $ from "jquery";
import { useFormKitNodeById } from "@formkit/vue";

import UiButtonCross from "@components/UiButtonCross.vue";
import UiButtonPlus from "@components/UiButtonPlus.vue";

/****************************************/

const allowedDateRange = ref([]);                               // int array: [minDate, maxDate]
const inputFields      = ref({});                               // { <html id>: { filter: <type of date filter>, data: [<array of dates>] } }. this stores our data, while defining our html
const repeatableDateNode = useFormKitNodeById("form-repeatable-date");

// `items` in the html form to set the `allowedDateRanger`
const allowedDateSearchTypes = [ { label:'Plage de dates', value:'dateRange' }
                               , { label:'Date exacte'   , value:'dateExact' }
                               , { label:'Avant'         , value:'dateBefore'}
                               , { label:'Après'         , value:'dateAfter' }];

/****************************************/

/**
 * generate a unique name, html id...
 */
const makeId = () => `form-repeatable-date-${window.crypto.randomUUID()}`;

/**
 * add a field to the repeatable date field.
 * we add `[undefined, undefined]` to `data` since the
 */
const addField = () => {
  inputFields.value[makeId()] = { filter:"dateRange", data:[undefined, undefined] };
}

/**
 * delete a field based on its html id
 */
const popField = (htmlId) => {
  if ( Object.keys(inputFields.value).includes(htmlId) ) {
    delete inputFields.value[htmlId]
  }
}

/**
 * display or hide the buttons in `.button-container`
 */
const displayUiButtonPlus = (htmlId) =>
  Object.keys(inputFields.value).indexOf(htmlId)
  === Object.keys(inputFields.value).length - 1;

const displayUiButtonCross = () =>
  Object.keys(inputFields.value).length > 1;


/**
 * update the date `filter` key of an input field.
 * this also includes updating the `data` with default values.
 * @param {string} input: the new date filter
 * @param {string} htmlId: the id of the FormKitRadioTabs element,
 *  to be able to add the values to the proper entry of `inputFields`
 */
function updateDateFilter(input, htmlId) {
  // $("li").css({ backgroundColor: "var(--cs-main-default-bg)" });
  // $(`#${htmlId}`).css({ backgroundColor: "var(--cs-plum)" });
  inputFields.value[htmlId].filter = input;
  inputFields.value[htmlId].data = input==="dateRange"
                                   ? [undefined,undefined]
                                   : [undefined];
}

/**
 * update the `data` key of an input field, based on
 * this input field's HTML ID.
 * @param {string} input: the new date data
 * @param {string} htmlId: the html ID of the new input
 * @param {Number} position: the position at which to insert `input`.
 *  useful when, for an input `filter==='dateRange'`: `data` is an
 *  array, the start date is at position 0, the end date at position 1.
 */
function updateDateData(input, htmlId, inputPosition=0) {
  if ( ![0,1].includes(inputPosition) ) {
    console.error(`FormRepeatableDate.updateDateData(): inputPosition
                   must be 0 or 1, got", ${inputPosition}`)
  }
  inputFields.value[htmlId].data[inputPosition] = input;
}

/****************************************/

onMounted(() => {
  // fetch necessary data
  axios.get(new URL("/i/iconography/date-range", __API_URL__))
       .then(r => {
         allowedDateRange.value = r.data; })
       .catch(e => {
         console.error("AdvancedSearchQuery: axios error on `allowedDateRange`", e);
         allowedDateRange.value = [ 1700,2100 ];  });

  addField();
})

</script>


<style scoped>
li {
  display: grid;
  grid-template-columns: 2fr auto;
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
</style>
