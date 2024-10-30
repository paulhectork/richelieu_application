<!-- main page for a single iconography item.
     this page contains:
     * .viewer-wrapper: a viewer. there are 2 types of viewers and
       we can toggle:
       > IiifViewer: a IIIF viewer for the image
       > .leaflet-<id_uuid>: a leaflet viewer showing the
         places the image is connected to.
     * .cartel-wrapper: a table with all of the metadata
-->

<template>
  <div class="iconography-outer-wrapper"
       v-if="iconography">
       <!--
        v-if="iconographyLoaded.value===true">
       -->

    <div class="title-wrapper">
      <h1>{{ iconography.title ? iconography.title[0] : "" }}</h1>
    </div>

    <div class="viewer-cartel-wrapper">

      <div class="viewer-wrapper">
        <div class="viewer">

          <div v-if="viewerType === 'osd'"
               class="iiif-wrapper"
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
               class="leaflet-wrapper"
          >
            <MapIconographyMain :lflId="`lfl-${idUuid}`"
                                :placeGeoJson="iconography.place"
            ></MapIconographyMain>
          </div>
        </div>

        <div class="viewer-selector">
          <button :class="viewerType === 'osd' ? 'button-activated' : ''"
                  @click="(e) => toggleViewer(e)"
                  @touchend="(e) => toggleViewer(e)"
                  value="osd"
          >Image</button>
          <button :class="viewerType === 'leaflet' ? 'button-activated' : ''"
                  @click="(e) => toggleViewer(e)"
                  @touchend="(e) => toggleViewer(e)"
                  value="leaflet"
          >Carte</button>
        </div>
      </div>

      <div class="cartel-wrapper">
        <table>
          <tr v-if="iconography.theme != null && iconography.theme.length">
            <td>{{ iconography.theme.length > 1 ? "Thèmes" : "Theme" }}</td>
            <td v-html="stringifyThemeArray(iconography.theme, true)"></td>
          </tr>
          <tr v-if="iconography.named_entity != null && iconography.named_entity.length">
            <td>{{ iconography.named_entity.length > 1 ? "Entités nommées" : "Entité nommée" }}</td>
            <td v-html="stringifyNamedEntityArray(iconography.named_entity, true)"></td>
          </tr>

          <tr v-if="iconography.title != null && iconography.title.length > 1">
            <td>Autre(s) titre(s)</td>
            <td>{{ stringifyGenericArray(iconography.title) }}</td>
          </tr>
          <tr v-if="iconography.author != null && iconography.author.length">
            <td>{{ iconography.author.length > 1 ? "Auteurs ou autrices" : "Auteur ou autrice" }}</td>
            <td v-html="stringifyActorArray(iconography.author, false)"></td>
          </tr>
          <tr v-if="iconography.corpus != null">
            <td>Corpus</td>
            <td>{{  iconography.corpus }}</td>
          </tr>
          <tr v-if="iconography.date != null && iconography.date.length">
            <td>Date</td>
            <td>{{ stringifyDate(iconography.date) }}</td>
          </tr>
          <tr v-if="iconography.publisher != null && iconography.publisher.length">
            <td>Édition</td>
            <td v-html="stringifyActorArray(iconography.publisher, false)"></td>
          </tr>
          <tr v-if="iconography.technique != null && iconography.technique.length">
            <td>{{ iconography.technique.length > 1 ? "Techniques" : "Technique" }}</td>
            <td>{{ stringifyGenericArray(iconography.technique) }}</td>
          </tr>
          <tr v-if="iconography.institution != null && iconography.institution.length">
            <td>Institution</td>
            <td v-html="stringifyInstitutionArray(iconography.institution, true)"></td>
          </tr>
          <tr v-if="iconography.inventory_number != null">
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
import { ref, watch, onMounted, onUpdated, computed } from "vue";
import { useRoute } from "vue-router";

import axios from "axios";

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
.iconography-outer-wrapper {
  width: 100%;
  height: var(--cs-portrait-main-height);
  display: grid;
  grid-template-rows: 15% 85%/*1fr 85%*/;
  background-color: pink;
}
@media ( orientation:landscape ) {
  .iconography-outer-wrapper {
    height: var(--cs-landscape-main-height);
  }
}
.title-wrapper {
  display: flex;
  flex-direction: column;
  justify-content: center;
}
.viewer-cartel-wrapper {
  display: grid;
  grid-template-columns: 50% 50%;
  border-top: var(--cs-main-border);
}
.negative-default .viewer-cartel-wrapper {
  border-top: var(--cs-negative-border);
}
@media ( orientation:portrait ) {
  .viewer-cartel-wrapper {
    grid-template-rows: 70vh 2fr;
    grid-template-columns: 100%;
  }
}

/*************************************/

.viewer-wrapper {
  display: grid;
  grid-template-columns: 100%;
  grid-template-rows: 90% 10%;
  max-height: 100%;
}
.iiif-wrapper, .leaflet-wrapper {
  height: 100%;
}
:deep(.static-viewer) {
  flex-grow: 1;
}
.viewer-selector {
  display: flex;
  flex-direction: row;
  justify-content: space-around;
  border-top: var(--cs-main-border);
}
.negative-default .viewer-selector {
  border-top: var(--cs-negative-border);
}
.viewer-selector > button {
  width: 50%;
}

/*************************************/

.cartel-wrapper {
  border-left: var(--cs-main-border);
  height: 100%;
}
.negative-default .cartel-wrapper {
  border-left: var(--cs-negative-border);
}
table {
  display: table;  /* use display:block instead ??? */
  height: 100%;
  overflow: scroll;
}
td {
  padding: 10px;
}
td:first-child {
  font-weight: 700;
  width: 30%;
  min-width: 120px;
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
  border-left: var(--cs-main-border);
}
.negative-default .external-links > a:last-child {
  border-left: var(--cs-negative-border);
}
</style>