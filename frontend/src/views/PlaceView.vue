<!-- PlaceView.vue
     a view for the place index
-->

<template>

  <h1>Index des lieux</h1>
  <p>
    L'idée, c'est qu'on aura un viewer en deux parties.
    À gauche, une liste de lieux, situés par leurs noms.
    À droite, une carte leaflet. À gauche, il y aura un
    boutton "Voir sur la carte". onClick, le vecteur et
    le raster s'afficheront sur la carte et on zoomera
    dessus. En cliquant sur un "Voir sur la carte" d'un
    autre lieu, on supprimera les anciens rasters et
    vecteurs et on affichera les nouveaux. En cliquant
    sur le nom du lieu, on sera réorienté.e.s sur la page
    principale de celui-ci.
  </p>
  <p>Pour le moment c'est un dossier en cours.</p>
  <p>:)</p>
  <IndexPlace :display="display"
              :data="dataFilter"
  ></IndexPlace>

</template>

<script setup>
import { onMounted, ref } from "vue";
import axios from "axios";

import { stringifyAddressResource } from "@utils/stringifiers";
import { fnToCartographyFile } from "@utils/functions";
import IndexPlace from "@components/IndexPlace.vue";

const apiTarget  = new URL("/i/place", __API_URL__);
const dataFull   = ref([]);     // the full index, independant of user filters
const dataFilter = ref([]);     // the data to pass to `Index.vue`, can vary based on user filters
const display    = "resource";  // which display style to use

onMounted(() => {
  axios.get(apiTarget).then((r) => {

    dataFull.value   = JSON.parse(r.request.response);

    dataFilter.value = dataFull.value.map((c) => {
      return { href : new URL(`/lieu/${c.id_uuid}`, window.location.href).href,
               img  : c.filename.length ? fnToCartographyFile(c.filename[0].url).href : null,
               text : c.address.length ? stringifyAddressResource(c.address[0]) : "Addresse inconnue" };
    })


  })
})

</script>


<style scoped>

</style>
