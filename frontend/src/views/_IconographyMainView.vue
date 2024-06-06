<template>
  <div class="global-container"
       v-if="iconography">
       <!--
        v-if="iconographyLoaded.value===true">
       -->

    <div class="title-container">
      <h1>{{ iconography.title ? iconography.title[0] : "" }}</h1>
    </div>

    <div class="viewer-cartel-container">

      <div class="viewer-container">
        <div v-if="view === 'image'">
          <IiifViewer v-if="iconography.iiif_url"
                      :osdId="iconography.id_uuid"
                      :iiifUrl="iconography.iiif_url"
          ></IiifViewer>
          <div v-else><p>Pas d'image IIIF à montrer</p></div>
        </div>
        <div v-else><p>Leaflet</p></div>
      </div>

      <div class="cartel-container">
        <table>
          <tr>
            <td>{{ iconography.theme.length > 1 ? "Thèmes" : "Theme" }}</td>
            <td v-html="stringifyThemeArray(iconography.theme, true)"></td>
          </tr>
          <tr>
            <td>{{ iconography.named_entity.length > 1 ? "Sujets" : "Sujet" }}</td>
            <td v-html="stringifyNamedEntityArray(iconography.named_entity, true)"></td>
          </tr>

          <tr v-if="iconography.title.length > 1">
            <td>Autre(s) titre(s)</td>
            <td>{{ stringifyGenericArray(iconography.title) }}</td>
          </tr>
          <tr>
            <td>{{ iconography.author.length > 1 ? "Auteurs ou autrices" : "Auteur ou autrice" }}</td>
            <td v-html="stringifyActorArray(iconography.author, true)"></td>
          </tr>
          <tr v-if="iconography.corpus != null">
            <td>Corpus</td>
            <td>{{  iconography.corpus }}</td>
          </tr>
          <tr>
            <td>Date</td>
            <td>{{ stringifyDate(iconography.date) }}</td>
          </tr>
          <tr>
            <td>Édition</td>
            <td v-html="stringifyActorArray(iconography.publisher, true)"></td>
          </tr>
          <tr>
            <td>{{ iconography.technique.length > 1 ? "Techniques" : "Technique" }}</td>
            <td>{{ stringifyGenericArray(iconography.technique) }}</td>
          </tr>
          <tr>
            <td>Institution</td>
            <td v-html="stringifyInstitutionArray(iconography.institution, true)"></td>
          </tr>
          <tr v-if="iconography.inventory_number">
            <td>Numéro d'inventaire</td>
            <td>{{ iconography.inventory_number }}</td>
          </tr>
          <tr v-if="iconography.source_url || iconography.iiif_url">
            <td>Liens externes</td>
            <td>
              <span class="external-links">
                <a v-if="iconography.source_url"
                   :href="iconography.source_url">Lien vers la source</a>
                <a v-if="iconography.iiif_url"
                   :href="iconography.iiif_url">Manifeste IIIF</a>
              </span>
            </td>
          </tr>
          <tr>
            <td>Licence</td>
            <td>{{ iconography.licence.entry_name }}</td>
          </tr>
        </table>
      </div>
    </div>

  </div>

  <!----
  <div v-else>
    <p>Chargement en cours</p>
  </div>
  -->

</template>


<script setup>
import axios from "axios";
import { ref, watch, onMounted, onUpdated, computed } from "vue";
import { useRoute } from "vue-router";

import IiifViewer from "@components/IiifViewer.vue";
import { stringifyActorArray
       , stringifyNamedEntityArray
       , stringifyThemeArray
       , stringifyInstitutionArray
       , stringifyGenericArray
       , stringifyDate } from "@utils/stringifiers";


const route = useRoute();
const idUuid = ref(route.params.idUuid);
const iconography = ref();
const apiTarget = computed(() =>
  new URL(`/i/iconography/${idUuid.value}`, __API_URL__) );
const view = ref("image");  // "image" for a IIIF viewer, "map" for a leaflet map of the place of this image

function getIconographyResource() {
  axios
  .get(apiTarget.value)
  .then((r) => {
    iconography.value = r.data[0]

  })
}

watch(() => route.params.id_uuid, (newIdUuid, oldIdUuid) => {
  idUuid.value = newIdUuid;
})

onMounted(() => {
  getIconographyResource();
})

onUpdated(() => {

})
</script>


<style scoped>
.global-container {
  display: grid;
  grid-template-rows: 15% 85%;
  width: 100%;
  height: 100%;
}
.title-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
}
.viewer-cartel-container {
  display: grid;
  grid-template-columns: 50% 50%;
  border-top: var(--cs-border);
}

/*************************************/
.viewer-container > div {
  height: 100%;
}

/*************************************/

.cartel-container {
  border-left: var(--cs-border);
}

table {
  height: 100%;
}
td:first-child {
  font-weight: 700;
}
.external-links {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  text-align: center;
}
.external-links > a {
  width: 100%;
}
.external-links > a:last-child {
  border-left: var(--cs-border);
}
</style>