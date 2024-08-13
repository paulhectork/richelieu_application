<!-- main page for a single iconography item.
     this page contains:
     * .viewer-container: a viewer. there are 2 types of viewers and
       we can toggle:
       > IiifViewer: a IIIF viewer for the image
       > .leaflet-<id_uuid>: a leaflet viewer showing the
         places the image is connected to.
     * .cartel-container: a table with all of the metadata
-->

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
        <div class="viewer">

          <div v-if="viewerType === 'osd'"
               class="iiif-container"
          >
            <!--
            <IiifViewer v-if="iconography.iiif_url"
                        :osdId="`iiif-${idUuid}`"
                        :iiifUrl="iconography.iiif_url"
                        :backupImgUrl="imageUrl"
            ></IiifViewer>
            <div v-else><p>Pas d'image IIIF à montrer</p></div>
            -->
            <IiifViewer :osdId="`iiif-${idUuid}`"
                        :iiifUrl="iconography.iiif_url"
                        :backupImgUrl="imageUrl"
            ></IiifViewer>
          </div>
          <div v-else
               class="leaflet-container"
          >
            <MapIconographyMain :lflId="`lfl-${idUuid}`"
                                :placeGeoJson="iconography.place"
            ></MapIconographyMain>
          </div>
        </div>

        <div class="viewer-selector">
          <button :class="viewerType === 'osd' ? 'contrast-default' : ''"
                  @click="(e) => toggleViewer(e)"
                  @touchend="(e) => toggleViewer(e)"
                  value="osd"
          >Image</button>
          <button :class="viewerType === 'leaflet' ? 'contrast-default' : ''"
                  @click="(e) => toggleViewer(e)"
                  @touchend="(e) => toggleViewer(e)"
                  value="leaflet"
          >Carte</button>
        </div>
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

import MapIconographyMain from "@components/MapIconographyMain.vue";
import IiifViewer from "@components/IiifViewer.vue";
import { clickOrTouchEvent } from "@globals";
import { stringifyActorArray
       , stringifyNamedEntityArray
       , stringifyThemeArray
       , stringifyInstitutionArray
       , stringifyGenericArray
       , stringifyDate } from "@utils/stringifiers";

/***************************************************/

const route = useRoute();
const idUuid = ref(route.params.idUuid);
const iconography = ref();
const viewerType = ref("osd");  // "osd" for a IIIF viewer, "leaflet" for a leaflet map of the place of this image

const apiTarget = computed(() =>
  new URL(`/i/iconography/${idUuid.value}`, __API_URL__) );
// a backup image url in case the IIIF one doesn't load properly
const imageUrl = computed(() => {
  return iconography.value !== undefined
  ? iconography
    .value
    .filename
    .filter( f => !f.url.match(/compress|thumbnail/) )[0].url
  : "not yet defined" });

/***************************************************/

function getIconographyResource() {
  axios
  .get(apiTarget.value)
  .then((r) => {
    iconography.value = r.data[0] })
}

function toggleViewer(e) {
  viewerType.value = e.target.value;
}

/***************************************************/

watch(() => route.params.idUuid, (newIdUuid, oldIdUuid) => {
  idUuid.value = newIdUuid;
  getIconographyResource();
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
  grid-template-rows: 1fr 85%;
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
.viewer-container {
  display: grid;
  grid-template-columns: 100%;
  grid-template-rows: 90% 10%;
}
.iiif-container, .leaflet-container {
  height: 100%;
}
.viewer-selector {
  display: flex;
  flex-direction: row;
  justify-content: space-around;
  border-top: var(--cs-border);
}
.viewer-selector > button {
  width: 50%;
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