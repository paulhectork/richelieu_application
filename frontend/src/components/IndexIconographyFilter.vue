<template>

  <div class="filter-outer-wrapper">
    <FormKit type="form"
             name="iconographyIndexFilter"
             id="iconography-index-filter"
             @submit="onSubmit"
    >
      <FormKit type="text"
                id="title-filter"
               name="titleFilter"
               label="Titre"
               placeholder="Filter par titre"
               help="Afficher les œuvres dont le titre contient le(s) mot(s)"
               validation="textValidator"
      ></FormKit>
      <FormKit type="text"
               id="author-filter"
               name="authorFilter"
               label="Auteur ou autrice"
               placeholder="Filtrer par nom d'auteur ou autrice"
               help="Afficher les auteurs dont le nom contient le(s) mot(s)"
               validation="textValidator"
      ></FormKit>
      <FormKit type="fkSlider"
               id="date-filter"
               name="dateFilter"
               label="Date"
               help="Filter par date"
               number="integer"
               :step="1"
               :minVal="minDate"
               :maxVal="maxDate"
      ></FormKit>
      <FormKit type="fkSelect"
               id="order-by"
               name="orderBy"
               label="Réordonner"
               :multiple="false"
               help="Définir un critère pour l'ordre des résultats"
               :options="[ { label: 'Auteur ou autrice (par défaut)', value: 'author' }
                         , { label: 'Titre de l\'œuvre', value: 'title' }
                         , { label: 'Date', value: 'date' } ]"
      ></FormKit>
    </FormKit>
  </div>

</template>


<script setup>
import { onMounted, ref, computed } from "vue";

import _ from "lodash";

/*************************************/

const props = defineProps(["data"]);
const data = ref(props.data || []);

const currentFilter = ref();  // the filter applied by the user, defined in onSubmit

const minDate = computed(() =>
  Math.min(...data.value.filter(i => i.date != null && i.date.length)
                        .map(i => i.date[0])));
const maxDate = computed(() =>
  Math.max(...data.value.filter(i => i.date != null && i.date.length)
                        .map(i => i.date[1])));

/*************************************/

function onSubmit(formData, formNode) {
  let dataFilter = [];  // elements of `data` that fit `formData`

  console.log( currentFilter.value, formData );

  if ( Object.values(formData).every(i => i == undefined || i === "") ) {
    formNode.setErrors("Définir au moins un filtre pour lancer la recherche")
  } else if ( _.isEqual(currentFilter.value, formData) ) {
    formNode.setErrors("Les filtres sont les mêmes qu'avant. Il faut les changer pour relancer une recherche.")
  } else {
    currentFilter.value = formData;
  }

}

/*************************************/

onMounted(() => {
})


</script>


<style scoped>

</style>