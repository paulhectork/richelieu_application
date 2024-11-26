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
  <div class="iconography-loader-wrapper"
       v-if="loadState === 'loading'"
  ><UiLoader></UiLoader></div>
  <div class="iconography-outer-wrapper"
       v-else-if="iconography && loadState === 'loaded'">
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
        <dl v-html="structuredCartel"
            class="iconography-cartel"
        ></dl>
      </div>
    </div>

  </div>

  <div class="iconography-error-wrapper"
       v-else
  >
    <ErrNotFound></ErrNotFound>
  </div>
  <DownloadButtonGroup @download="onDownload"/>

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

import DownloadButtonGroup from "@components/DownloadButtonGroup.vue";
import { downloadData } from "@utils/download";
import { iconographyToCsvRecord } from "@utils/toCsvRecord";
import MapIconographyMain from "@components/MapIconographyMain.vue";
import IiifViewer from "@components/IiifViewer.vue";
import UiLoader from "@components/UiLoader.vue";
import ErrNotFound from "@components/ErrNotFound.vue";

import { clickOrTouchEvent } from "@globals";
import { stringifyActorArray
       , stringifyNamedEntityArray
       , stringifyThemeArray
       , stringifyInstitutionArray
       , stringifyGenericArray
       , stringifyDate } from "@utils/stringifiers";

/***************************************************/

const route       = useRoute();
const idUuid      = ref(route.params.idUuid);
const iconography = ref();
const loadState   = ref("loading");  // "loading"/"loaded"/"error"
const viewerType  = ref("osd");  // "osd" for a IIIF viewer, "leaflet" for a leaflet map of the place of this image


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

const structuredCartel = computed(() => {
  const cartel = [],  // Array of [ title, data ]
        icn = iconography.value;

  if ( icn.theme != null && icn.theme.length )
    cartel.push([ icn.theme.length > 1 ? "Thèmes" : "Theme"
                , `<span>${stringifyThemeArray(icn.theme, true)}</span>` ]);
  if ( icn.named_entity != null && icn.named_entity.length )
    cartel.push([ icn.named_entity.length > 1 ? "Entités nommées" : "Entité nommée"
                , `<span>${stringifyNamedEntityArray(icn.named_entity, true)}</span>` ]);
  if ( icn.title != null && icn.title.length > 1 )
    cartel.push([ "Autre(s) titre(s)"
                , `<span>${stringifyGenericArray(icn.title)}</span>` ]);
  if ( icn.author != null && icn.author.length )
    cartel.push([ icn.author.length > 1 ? "Auteurs ou autrices" : "Auteur ou autrice"
                ,  `<span>${stringifyActorArray(icn.author, false)}</span>` ])
  if ( icn.corpus != null )
    cartel.push([ "Corpus", `<span>${icn.corpus}</span>` ]);
  if ( icn.date != null && icn.date.length )
    cartel.push([ "Date", `<span>${stringifyDate(icn.date)}</span>` ]);
  if ( icn.publisher != null && icn.publisher.length )
    cartel.push([ "Édition", `<span>${stringifyActorArray(icn.publisher, false)}</span>` ]);
  if ( icn.technique != null && icn.technique.length )
    cartel.push([ icn.technique.length > 1 ? "Techniques" : "Technique"
                , `<span>${stringifyGenericArray(icn.technique)}</span>` ]);
  if ( icn.institution != null && icn.institution.length )
    cartel.push([ "Institution"
                , `<span>${stringifyInstitutionArray(icn.institution, true)}</span>` ]);
  if ( icn.inventory_number != null )
    cartel.push([ "Numéro d'inventaire", `<span>${icn.inventory_number}</span>` ]);
  if ( icn.source_url || icn.iiif_url ) {
    let urls = "<span class='external-links'>";
    if ( icn.source_url ) {
      urls += `<a href="${icn.source_url}">Lien vers la source</a>`; }
    if ( icn.iiif_url ) {
      urls += `<a href="${icn.iiif_url}">Manifeste IIIF</a>`; }
    urls += "</span>"
    cartel.push([ "Liens externes", urls ]);
  }
  cartel.push([ "Licence", `<span>${icn.licence.entry_name}</span>` ]);

  // represent cartel as an HTML descriptive list
  return cartel.map((titleData) =>
    `<dt>${titleData[0]}</dt><dd>${titleData[1]}</dd>\n`)
    .join("");
})

/***************************************************/

function getIconographyResource() {
  axios
  .get(apiTarget.value)
  .then(r => r.data)
  .then(data => {
    iconography.value = data[0];
    loadState.value = "loaded";
  })
  .catch(e => {
    console.error("IcoonographyMainView.getIconographyResource() : ", e);
    loadState.value = "error";
  })
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

function onDownload(fileType) {
  if (fileType === "json") {
    downloadData(iconography.value, "json", "iconography")
  } else if (fileType === "csv") {
    downloadData([iconographyToCsvRecord(iconography.value)], "csv", "iconography");
  }
}
</script>


<style scoped>
.iconography-loader-wrapper,
.iconography-error-wrapper,
.iconography-outer-wrapper {
  width: 100%;
  height: var(--cs-portrait-main-height);
}
@media ( orientation:landscape ) {
  .iconography-loader-wrapper,
  .iconography-error-wrapper,
  .iconography-outer-wrapper {
    height: var(--cs-landscape-main-height);
  }
}

.iconography-outer-wrapper {
  display: grid;
  grid-template-rows: 1fr 85%;
}
.title-wrapper {
  display: flex;
  flex-direction: column;
  justify-content: center;
}
.viewer-cartel-wrapper {
  display: grid;
  grid-template-columns: 50% 50%;
  border-top: var(--cs-negative-border);
}
@media ( orientation:portrait ) {
  .viewer-cartel-wrapper {
    grid-template-rows: 60vh 2fr;
    grid-template-columns: 100%;
    border-right: var(--cs-negative-border);
    margin: 0 3%;
  }
}

/*************************************/

.title-wrapper > h1 {
  margin: 10px 0;
}

/*************************************/

.viewer-wrapper {
  display: grid;
  grid-template-columns: 100%;
  grid-template-rows: 90% 10%;
  max-height: 100%;
  border-bottom: var(--cs-negative-border);
}
.iiif-wrapper, .leaflet-wrapper {
  height: 100%;
}
.iiif-wrapper :deep(.static-viewer) {
  max-height: 100%;
  max-width: 100%;
}
.viewer-selector {
  display: flex;
  flex-direction: row;
  justify-content: space-around;
  border-top: var(--cs-negative-border);
}
.viewer-selector > button {
  width: 50%;
}

@media ( orientation:portrait ) {
  .viewer-wrapper {
    border-left: var(--cs-negative-border);
  }
}

/*************************************/

.cartel-wrapper {
  border-left: var(--cs-negative-border);
  border-bottom: var(--cs-negative-border);
  height: 100%;
}

dl.iconography-cartel {
  display: grid;
  grid-template-rows: auto;
  grid-template-columns: max(120px, 30%) calc(100% - max(120px, 30%));  /** 30% / 70% with a minimum of 120px for the <dt/> */
  height: 100%;
  margin: 0;
}
.iconography-cartel :deep(dt),
.iconography-cartel :deep(dd) {
  border-bottom: var(--cs-negative-border);
  margin: 0;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  padding: 10px 0 10px 15px;
}
.iconography-cartel :deep(dt:last-of-type),
.iconography-cartel :deep(dd:last-of-type) {
  border-bottom: none;
}

.iconography-cartel :deep(.external-links) {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  text-align: center;
}
.iconography-cartel :deep(.external-links > a) {
  width: 100%;
}
:deep(.external-links > a:last-child) {
  border-left: var(--cs-main-border);
}
.negative-default :deep(.external-links > a:last-child) {
  border-left: var(--cs-negative-border);
}
</style>
