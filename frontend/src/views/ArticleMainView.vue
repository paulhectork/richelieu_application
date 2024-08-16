<!--  ArticleMainView.vue

      a component that displays an in-depth article,
      with extra data fetched from the database.

      this component is composed of 4 components:
      * `Article\d+`: (Article1, Article14...):
          the article itself, loaded dynamically based on the
          `articleName` parameter in the URL. if the article
          looked for is not found, a 404 is displayed instead
      * `IiifViewer`: a IIIF viewer to display important images
          for the article
      * `IndexBase`: an index of relevant, but not directly
          related, iconography entries
      * `ArticleFootnote`: rfootnotes for an article

      how to the components interact?
      * `ArticleMainView` handles the interaction between
          components and ALL generic processes (all things that
          can and will be repeated from one article to another)
      * `Article\d+` contains the DATA specific to an article:
          the article itself, query parameters to build the IndexBase,
          UUIDs for the iconography ressources to display in the
          IIIF viewer, footnotes... all of that is emitted to
          `ArticleMainView`. the data changes from an article to
          another, but the processes are always the same, so they
          are handled by the current component.
      * `IiifViewer`, `IndexBase` and `ArticleFootnote` display data
          fetched from `Article\d+` and passed to them from `ArticleMainView`
-->


<template>

  <div class="article-main-wrapper">

    <div class="article-viewer-wrapper">
      <div class="iiif-wrapper">
        <div v-if="iconographyMainCurrent"
             class="iiif-inner-wrapper">
          <IiifViewer :osdId="iconographyMainCurrent.id_uuid"
                      :iiifUrl="iconographyMainCurrent.iiif_url"
                      @osd-viewer="setCurrentIiifViewer"

          ></IiifViewer>
          <div class="iiif-cartel">
            <p v-html="stringifyIconographyResource(iconographyMainCurrent)"></p>
          </div>
        </div>
      </div>
      <div class="article-wrapper">
        <component :is="articleComponent"
                   @query-params="fetchIndex"
                   @iiif-id-uuid="fetchIiif"
                   @footnotes="setArticleFootnotes"
                   @vue:mounted="registerArticleEvents"
        >
        </component>
      </div>
    </div>

    <div class="article-index-wrapper">
      <h2>Resources liées {{ iconographyIndex.length
                              ? `(${iconographyIndex.length})`
                              : "" }}
      </h2>
      <IndexBase v-if="iconographyIndex.length"
                 :data="iconographyIndex"
                 display="resource"
      ></IndexBase>
      <LoaderComponent v-else></LoaderComponent>
    </div>

  </div>

  <ArticleFootnote v-if="currentFootnoteContent.length"
                   :footnoteContent="currentFootnoteContent"
                   :footnotePosition="currentFootnotePos"
                   :footnoteHtmlId="currentFootnoteHtmlId"
                   @unmount-footnote="unmountFootnote"
  ></ArticleFootnote>

</template>


<script setup>
import { onMounted, onUnmounted, ref, shallowRef, defineAsyncComponent } from 'vue';
import { useRoute, useRouter } from "vue-router";

import axios from "axios";
import _ from "lodash";
import $ from "jquery";

import IndexBase from "@components/IndexBase.vue";
import IiifViewer from "@components/IiifViewer.vue";
import ArticleFootnote from "@components/ArticleFootnote.vue";
import LoaderComponent from "@components/ui/LoaderComponent.vue";
import { stringifyIconographyResource } from "@utils/stringifiers.js";
import { IconographyQueryParams } from "@modules/iconographyQueryParams.js";
import { indexDataFormatterIconography } from "@utils/indexDataFormatter.js";

/************************************************/

const route                  = useRoute();
const articleName            = ref(route.params.articleName);
const articleComponent       = shallowRef();  // the currentcomponent, or NotFound.vue if articleName is not a key of `urlMapper` below. `shallowRef` is used to avoid vue performance warnings

const iconographyIndex       = ref([]);       // array of iconography objects to display in an index
const iconographyMainArray   = ref([]);       // array of a few iconography resources (2-6) from which to display IIIFs
const iconographyMainCurrent = ref();         // the iconography ressource currently viewed in the IIIF viewer. can be modified when clicking on `.button-eye`.
const iiifViewer             = ref();         // openseadragon viewer returned by `IiifViewer.vue`

const articleFootnotes       = ref({})        // the footnotes of the `articleComponent`. structure: { <footnote key>: <footnote content> }
const currentFootnoteContent = ref("")        // when a footnote is clicked, this ref will hold its HTML content
const currentFootnoteHtmlId  = ref("")        // the htmlId of the current footnote, if a footnote is displayed
const currentFootnotePos     = ref([])        // [x:float, y:float]. where to position the

// url to component name mapper
const urlMapper = { "bourse"             : "Article01.vue"
                  , "mode"               : "Article02.vue"
                  , "menu"               : "Article03.vue"
                  , "nature"             : "Article04.vue"
                  , "cafe"               : "Article05.vue"
                  , "chantier"           : "Article06.vue"
                  , "reseau"             : "Article07.vue"
                  , "actualite"          : "Article08.vue"
                  , "habiter"            : "Article09.vue"
                  , "patrimonialisation" : "Article10.vue"
                  , "mobilier"           : "Article11.vue"
                  , "theatre"            : "Article12.vue"
                  , "prostitution"       : "Article13.vue"
                  , "banque"             : "Article14.vue" }

/************************************************/

/**
 * dynamically import the article component based
 * on the name in the route. if no comonent is found,
 * NotFound is imported.
 * using `@` in imports doesn't work in dynamic loading,
 * see: https://stackoverflow.com/a/72977926/17915803
 * @param {string} articleName
 * @returns {ComponentPublicInstance}: the vue component
 */
function loadCurrentArticleComponent(articleName) {
  let componentName = Object.keys(urlMapper).includes(articleName)
                      ? urlMapper[articleName]
                      : "NotFound.vue";
  return defineAsyncComponent(() => import(`../components/${componentName}` /* @vite-ignore */));
}

/**
 * run a backend query to get an index
 * matching the query parameters for an article.
 *
 * warning: quer parameters for an article must match
 * what's expected by IconographyQueryParams.fromRoute
 * (keys and values can be omitted if they contain no data.):
 * @example
 * INPUT:
 * => {
 * =>   "title": [ "le moniteur de la mode" ],
 * =>   "author": [ "atget", "daumier" ],
 * =>   "publisher": [],
 * =>   "theme": [ "actualité", "architecture" ],
 * =>   "namedEntity": [ "Ardit éditeur" ],
 * =>   "institution": [ "Musée Carnavalet" ],
 * =>   "dateBooleanOp": "and",
 * =>   "date.0.filter": "dateRange",
 * =>   "date.0.data.0": "1860",
 * =>   "date.0.data.1": "1900",
 * =>   "date.1.filter": "dateBefore",
 * =>   "date.1.data.0": "1850",
 * =>   "titleBooleanOp": "and",
 * =>   "authorBooleanOp": "and",
 * =>   "publisherBooleanOp": "and",
 * =>   "themeBooleanOp": "and",
 * =>   "namedEntityBooleanOp": "and",
 * =>   "institutionBooleanOp": "and"
 * => }
 * @param {Object} newQueryParams: a object containing
 *    query params, with a structure like the one above.
 * @returns
 */
function fetchIndex(newQueryParams) {
  let queryParams = new IconographyQueryParams(newQueryParams, "route");
  let targetUrl = new URL("/i/iconography/search", __API_URL__);

  axios
  .post( targetUrl.href, queryParams.toJson() )
  .then(r => { iconographyIndex.value = indexDataFormatterIconography(r.data);  })
  .catch(e => { console.error( `ArticleMainIndex.fetchIndex(queryParams): backend error (${e.response?.data})`
                             , "on query:"
                             , queryParams.toJson()
                             , "error dump:"
                             , e);
  })
}

/**
 * from an array of iconography uuids, fetch the iconography
 * resources from the backend in order to build our main
 * IIIF viewer.
 * @param {Array<string>} iconographyIdUuidArray: the array of iconography uuids
 */
 function fetchIiif(iconographyIdUuidArray) {
  let targetUrl = new URL(`/i/iconography-from-uuid`, __API_URL__);

  axios.get( targetUrl.href, { params: { id_uuid: iconographyIdUuidArray },
                               paramsSerializer: { indexes:null } } )
       .then(r => { iconographyMainArray.value = r.data;
                    let firstIdUuid = $($(".button-eye")[0]).attr("data-key");
                    setCurrentIconographyMain(firstIdUuid);
       })
       .catch(e => console.error("ArticleMainView.fetchIiif(): backend error with parameters:"
                                , iconographyIdUuidArray, `error stack:`, e));
  // erreurs axios/cors quand on refresh: ça ne pose pas de prolbème,
  // mais il y a une explication ici si besoin:
  // https://github.com/axios/axios/issues/801
}

/**
 * set the `articleFootnotes` ref from the `footnotes`
 * emitted by the child `Article\d+` component.
 * @param {Object} footnotes: the footnotes
 *   (strucutre: { <footnote key>: <footnote content> })
 */
function setArticleFootnotes(footnotes) {
  articleFootnotes.value = footnotes;
}

/**
 * after a viewer has been created, assign it to the
 * `iiifViewer`. also set the size of the viewer
 * if in portrait mode.
 * @param {Openseadragon.viewer} viewer: the openseadragon viewer emitted by `IiifViewer.vue`.
 */
function setCurrentIiifViewer(viewer) {
  iiifViewer.value = viewer.value;
}

/**
 * build a IIIF viewer for an iconography resource
 * @param {string} iconographyIdUuid
 */
function setCurrentIconographyMain(iconographyIdUuid) {
  iconographyMainCurrent.value =
    iconographyMainArray.value.filter(i => i.id_uuid == iconographyIdUuid)[0];
}

/**
 * when clicking on a `.button-eye` button, change
 * the iiif viewer to display the ressource it points to.
 * the new iconography ressource is identified by its id_uuid,
 * which is stored in the `.button-eye`'s @data-key attribute.
 *
 * this function triggers the entire changing stack:
 * setting the new `iconographyMainCurrent` will change
 * the props sent to `IiifViewer.vue`, which will trigger
 * `IiifViewer.vue` to delete the old viewer and generate
 * a new one.
 */
function switchIconographyMainOnClick(evt) {
  let newIconographyIdUuid = $(evt.currentTarget).attr("data-key");
  if ( newIconographyIdUuid !== iconographyMainCurrent.id_uuid ) {
    setCurrentIconographyMain(newIconographyIdUuid)
  }
}

function unmountFootnote() {
  console.log("hi");
  // 2 méthodes: en cliquant sur le bouton croix ou en cliquant hors de la modale
  currentFootnoteContent.value = "";
  currentFootnoteHtmlId.value  = "";
  currentFootnotePos.value     = [];
}

function mountFootnoteOnClick(evt) {
  let footnoteKey = $(evt.currentTarget).attr("data-key");
  if ( Object.keys(articleFootnotes.value).includes(footnoteKey) ) {
    currentFootnoteContent.value = articleFootnotes.value[footnoteKey];
    currentFootnoteHtmlId.value  = `article-footnote-${footnoteKey}`;
    currentFootnotePos.value     = [];
  } else {
    console.error(`ArticleMainView.mountFootnoteOnClick(): could not resolve footnote for key "${footnoteKey}". expected one of :`,
                  Object.keys(articleFootnotes.value));
  }
}

/**
 * register events on `.article-wrapper`. event registering must
 * be called within a function because this allows us to wait for
 * the Article\d+ component to be mounted with the @vue:mounted hook.
 * see: https://stackoverflow.com/a/72486795/17915803
 */
function registerArticleEvents() {
  $(".button-eye").on("click", switchIconographyMainOnClick);
  $(".button-eye").on("touchend", switchIconographyMainOnClick);
  $(".button-ellipsis").on("click", mountFootnoteOnClick);
  $(".button-ellipsis").on("touchend", mountFootnoteOnClick);
}

/************************************************/

onMounted(() => {
  articleComponent.value = loadCurrentArticleComponent(articleName.value);
})
onUnmounted(() => {
  $(".button-eye").off("click", switchIconographyMainOnClick);
  $(".button-eye").off("touchend", switchIconographyMainOnClick);
  $(".button-ellipsis").off("click", mountFootnoteOnClick);
  $(".button-ellipsis").off("touchend", mountFootnoteOnClick);
})
</script>


<style scoped>
.article-viewer-wrapper {
  display: flex;
  flex-direction: column-reverse;
  border-bottom: var(--cs-border);
}
@media ( orientation: landscape ) {
  .article-viewer-wrapper {
    display: grid;
    grid-template-columns: 40% 60%;
    grid-template-rows: 100%;
  }
}

/***************************************/

.iiif-wrapper {
  height: 100%;
}
.iiif-inner-wrapper {
  height: 100%;
  max-height: calc(100vh - var(--cs-navbar-height));
  position: sticky;
  top: 0;
  display: grid;
  grid-template-rows: 1fr min-content;  /* min content will resize the `.iiif-cartel` to contain the complete cartel, while keeping the `.iiif-viewer` size as big as possible */
}
.article-viewer-wrapper :deep(.iiif-viewer) {
  height: 70vh;
}
@media ( orientation:landscape ) {
  .article-viewer-wrapper :deep(.iiif-viewer) {
    height: auto;
  }
}
.iiif-cartel {
  width: 100%;
  text-align: center;
  border-top: var(--cs-border);
  margin: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

/***************************************/

.article-wrapper {
  padding: 0 1vw;
  border-left: var(--cs-border);
}
.article-index-wrapper {
  min-height: 30vh;
}
</style>