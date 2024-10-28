<!--  ArticleMainView.vue

      a component that displays an in-depth article,
      with extra data fetched from the database.

      this component is composed of 4 components:
      * `ArticleContent...`: (ArticleComponentBourse...):
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
      * `ArticleContent...` contains the DATA specific to an article:
          the article itself, query parameters to build the IndexBase,
          UUIDs for the iconography ressources to display in the
          IIIF viewer, footnotes... all of that is emitted to
          `ArticleMainView`. the data changes from an article to
          another, but the processes are always the same, so they
          are handled by the current component.
      * `IiifViewer`, `IndexBase` and `ArticleFootnote` display data
          fetched from `ArticleContent...` and passed to them
          from `ArticleMainView`

      view @components/ArticleContentTemplate.vue for more info on
      the structure of all the components.
-->


<template>

  <div class="fill-parent"
       v-if="notFoundFlag===true">
    <component :is="articleComponent"
    ></component>
  </div>

  <div v-else
       class="article-main-wrapper">

    <div class="article-viewer-wrapper">
      <div class="iiif-wrapper">
        <div v-if="iconographyMainCurrent"
             class="iiif-inner-wrapper">
          <IiifViewer :osdId="iconographyMainCurrent.id_uuid"
                      :iiifUrl="iconographyMainCurrent.iiif_url"
                      :backupImgUrl="/* first non compress/thumbnail image in the `filename` array */
                                     iconographyMainCurrent
                                     .filename
                                     .filter(x => x.url.match(/^qr1[a-z0-9]+\.[a-z]+$/))
                                     [0]
                                     .url"
                      :folio="iconographyMainCurrent.folio"
                      backupImgDisplay="contain"
                      @osd-viewer="setCurrentIiifViewer"

          ></IiifViewer>
          <div class="iiif-cartel">
            <p v-html="stringifyIconographyResource(iconographyMainCurrent, truncate=false)"></p>
          </div>
        </div>
      </div>
      <div class="article-wrapper">
        <component :is="articleComponent"
                   @query-params="fetchIndex"
                   @iiif-id-uuid-array="fetchIiif"
                   @footnotes="setArticleFootnotes"
                   @vue:mounted="registerArticleEvents"
        >
        </component>
      </div>
    </div>

    <div class="article-index-wrapper">
      <h2>Ressources liées {{ iconographyIndex.length
                              ? `(${iconographyIndex.length})`
                              : "" }}
      </h2>
      <IndexBase v-if="iconographyIndex.length"
                 :data="iconographyIndex"
                 display="resource"
      ></IndexBase>
      <UiLoader v-else></UiLoader>
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
import { onMounted
       , onUnmounted
       , ref
       , shallowRef
       , defineAsyncComponent
       , watch } from 'vue';
import { useRoute } from "vue-router";

import axios from "axios";
import _ from "lodash";
import $ from "jquery";

import IndexBase from "@components/IndexBase.vue";
import IiifViewer from "@components/IiifViewer.vue";
import ArticleFootnote from "@components/ArticleFootnote.vue";
import UiLoader from "@components/UiLoader.vue";

import { stringifyIconographyResource } from "@utils/stringifiers.js";
import { IconographyQueryParams } from "@modules/iconographyQueryParams.js";
import { indexDataFormatterIconography } from "@utils/indexDataFormatter.js";

/************************************************/

const route                  = useRoute();
const articleName            = ref();         // the name of the article, defined in `setArticleName`, allows us to load the relevant `ArticleContent...`.
const articleComponent       = shallowRef();  // the currentcomponent, or ErrNotFound.vue if articleName is not a key of `urlMapper` below. `shallowRef` is used to avoid vue performance warnings
const notFoundFlag           = ref(false);    // true if the component `articleComponent` is `ErrNotFound.vue`

const iconographyIndex       = ref([]);       // array of iconography objects to display in an index
const iconographyMainArray   = ref([]);       // array of a few iconography resources (2-6) from which to display IIIFs
const iconographyMainCurrent = ref();         // the iconography ressource currently viewed in the IIIF viewer. can be modified when clicking on `.button-eye`.
const iiifViewer             = ref();         // openseadragon viewer returned by `IiifViewer.vue`

const articleFootnotes       = ref({})        // the footnotes of the `articleComponent`. structure: { <footnote key>: <footnote content> }
const currentFootnoteContent = ref("")        // when a footnote is clicked, this ref will hold its HTML content
const currentFootnoteHtmlId  = ref("")        // the htmlId of the current footnote, if a footnote is displayed
const currentFootnotePos     = ref([])        // [x:float, y:float]. where to position the

// url to component name mapper
const urlMapper = { "bourse"             : "ArticleContentBourse"
                  , "vivienne"           : "ArticleContentVivienne"
                  , "mode"               : "ArticleContentMode"
                  , "menu"               : "ArticleContentMenu"
                  , "nature"             : "ArticleContentNature"
                  , "cafe"               : "ArticleContentCafe"
                  , "habiter"            : "ArticleContentHabiter"
                  , "patrimonialisation" : "ArticleContentPatrimonialisation"
                  , "mobilier"           : "ArticleContentMobilier"
                  , "theatre"            : "ArticleContentTheatre"
                  , "prostitution"       : "ArticleContentProstitution"
                  , "banque"             : "ArticleContentBanque"
                  , "marginaux"          : "ArticleContentMarginaux"
                  , "revolutions"        : "ArticleContentRevolutions"
}

/************************************************/

/**
 * dynamically import the article component based
 * on the name in the route. if no comonent is found,
 * ErrNotFound is imported.
 * using `@` in imports doesn't work in dynamic loading,
 * see: https://stackoverflow.com/a/72977926/17915803
 * @param {string} articleName
 * @returns {Array<ComponentPublicInstance, bool>}:
 *   an array of 2 elements:
 *   - the vue component
 *   - a boolean that is True if `ErrNotFound` is returned.
 */
function loadCurrentArticleComponent(articleName) {
  let componentName = Object.keys(urlMapper).includes(articleName)
                      ? urlMapper[articleName]
                      : "ErrNotFound";
  return [ defineAsyncComponent(() => import(`../components/${componentName}.vue`))
         , componentName === "ErrNotFound"
         ];
}

/**
 * from the `articleName` param in a vue-router route,
 * trigger the complete article change hook:
 *
 * - define `articleName` ref (the name of the current
 *    article, given in `route.params.articleName`)
 * - define the `articleComponent` ref, which will trigger
 *    the loading of the new article
 * - empty `iconographyIndex`:`
 *    iconographyIndex` is fetched  asynchronously from
 *    fetchIndex()`. if we don't do this, when switching
 *    from componentA to componentB, until the `fetchIndex()`
 *    returns results relevant to `componentB, the index of
 *    `componentA` will be displayed `
 *
 * this function is called on `onMounted`
 * and on route change using `watch(route)`.
 *
 * @param {vue-router.RouteLocationNormalizedLoaded} _route:
 *   the vue-router route.
 */
function articleMounter(_route) {
  iconographyIndex.value = [];  // empty the previous index
  // load the new ArticleContent...
  articleName.value = _route.params.articleName;
  [ articleComponent.value, notFoundFlag.value ] = loadCurrentArticleComponent(articleName.value);
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
  if ( ! Object.keys(newQueryParams).length ) {
    console.error(`ArticleMainView.fetchIndex(): no query parameters on "${articleName.value}"`)
  }

  let queryParams = new IconographyQueryParams(newQueryParams, "route");
  let targetUrl = new URL("/i/search/iconography", __API_URL__);

  axios
  .post( targetUrl.href, queryParams.toJson() )
  .then(r => { iconographyIndex.value = indexDataFormatterIconography(r.data);  })
  .catch(e => { console.error( `ArticleMainIndex.fetchIndex(): backend error (${e.response?.data})`
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
  // basic error checking : do some UiButtonEye@data-key
  // items point to invalid data in `iconographyIdUuidArray` ?
  if ( __MODE__ == "DEV" ) {
    let iiifPointers = [];
    $(".button-eye").each((i, obj) =>
      iiifPointers.push( $(obj).attr("data-key") ));
    let emptyPointers =
          iiifPointers.filter(k => k==null),                              // empty @data-key in UiButtonEllipsis
        missingFromPointers =
          iiifPointers.filter(k => !iconographyIdUuidArray.includes(k)),  // what's in iconographyIdUuidArray but not iiifPointers
        missingFromIdUuidArray =
          iconographyIdUuidArray.filter(k => !iiifPointers.includes(k));  // what's in iiifPointers but not iconographyIdUuidArray
    if ( emptyPointers.length ) {
      console.error(`ArticleMainView.fetchIiif(): '${emptyPointers.length}' UiButtonEye@data-key are empty`); }
    if ( missingFromIdUuidArray.length ) {
      console.error("ArticleMainView.fetchIiif(): the following keys in 'iconographyIdUuidArray' are missing from 'iiifPointers':", missingFromIdUuidArray); }
    if ( missingFromPointers.length ) {
      console.error("ArticleMainView.fetchIiif(): the following items in 'iconographyIdUuidArrayKeys' are missing from 'iconographyIdUuidArray':", missingFromPointers); }

  }
  // fetch data
  let targetUrl = new URL(`/i/iconography-from-uuid`, __API_URL__);
  axios.get( targetUrl.href, { params: { id_uuid: iconographyIdUuidArray },
                               paramsSerializer: { indexes:null } } )
       .then(r => {
          // save the resources to be displayed in a iiif viewer
          iconographyMainArray.value = r.data;
          // set the style
          $(".button-eye").removeClass("button-activated")
          $($(".button-eye")[0]).addClass("button-activated");
          // create the 1st viewer
          let firstIdUuid = $($(".button-eye")[0]).attr("data-key");
          setCurrentIconographyMain(firstIdUuid);
       })
       .catch(e => console.error("ArticleMainView.fetchIiif(): backend error with parameters:"
                                , iconographyIdUuidArray, `error stack:`, e));
  // erreurs axios/cors quand on refresh: ça ne pose pas de problème,
  // mais il y a une explication ici si besoin:
  // https://github.com/axios/axios/issues/801
}

/**
 * set the `articleFootnotes` ref from the `footnotes`
 * emitted by the child `ArticleContent...` component.
 * @param {Object} footnotes: the footnotes
 *   (strucutre: { <footnote key>: <footnote content> })
 */
function setArticleFootnotes(footnotes) {
  // basic error checking : do some UiButtonEllipsis@data-key
  // items point to invalid data in `footnotes` ?
  if ( __MODE__ == "DEV" ) {
    const footnotePointers = [];
    $(".button-ellipsis").each((i, obj) =>
      footnotePointers.push( $(obj).attr("data-key") ));
    let emptyPointers =
          footnotePointers.filter(k => k==null),                              // empty @data-key in UiButtonEllipsis
        missingFromPointers =
          footnotePointers.filter(k => !Object.keys(footnotes).includes(k)),  // what's in footnotes but not footnotePointers
        missingFromFootnotes =
          Object.keys(footnotes).filter(k => !footnotePointers.includes(k));  // what's in footnotePointers but not footnotes
    if ( emptyPointers.length ) {
      console.error(`ArticleMainView.setArticleFootnotes(): '${emptyPointers.length}' UiButtonEllipsis@data-key are empty`); }
    if ( missingFromFootnotes.length ) {
      console.error("ArticleMainView.setArticleFootnotes(): the following keys in 'footnotes' are missing from 'footnotePointers':", missingFromFootnotes); }
    if ( missingFromPointers.length ) {
      console.error("ArticleMainView.setArticleFootnotes(): the following items in 'footnotesKeys' are missing from 'footnotes':", missingFromPointers); }
  }
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
  // set the style as activated
  $(".button-eye").removeClass("button-activated");
  $(evt.currentTarget).addClass("button-activated");

  let newIconographyIdUuid = $(evt.currentTarget).attr("data-key");
  if ( newIconographyIdUuid !== iconographyMainCurrent.id_uuid ) {
    setCurrentIconographyMain(newIconographyIdUuid)
  }
}

/**
 * remove the currently displayed footnote, by clicking
 * `.button-cross` or by clicking outside of the modal
 */
function unmountFootnote() {
  $(".button-ellipsis").removeClass("button-activated");  // unset the style
  currentFootnoteContent.value = "";
  currentFootnoteHtmlId.value  = "";
  currentFootnotePos.value     = [];
}

/**
 * mount a footnote when clicking on a `.button-ellipsis`
 * @param {jQuery.event} evt: the click event
 */
function mountFootnoteOnClick(evt) {
  // set the style
  $(".button-ellipsis").removeClass("button-activated");
  $(evt.currentTarget).addClass("button-activated");
  // display the footnote
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
 * register events on child `ArticleContent...`.
 * event registering must be called within a function
 * because this allows us to wait for the ArticleContent...
 * component to be mounted with the @vue:mounted hook.
 * see: https://stackoverflow.com/a/72486795/17915803
 */
function registerArticleEvents() {
  $(".button-eye").on("click", switchIconographyMainOnClick);
  $(".button-eye").on("touchend", switchIconographyMainOnClick);
  $(".button-ellipsis").on("click", mountFootnoteOnClick);
  $(".button-ellipsis").on("touchend", mountFootnoteOnClick);
}

/**
 * make sure that the important data is filled out
 */
function missingArticleData() {
  if ( !$(".article-header > h1").text().length
    || !$(".article-header > h2").text().length
  ) console.error(`ArticleMainView.missingArticleData(): missing TITLE on article '${route.params.articleName.toUpperCase()}'`)
  if ( !$(".article-footer > p").text().length ) {
    console.error(`ArticleMainView.missingArticleData(): missing AUTHOR NAME on article '${route.params.articleName.toUpperCase()}'`)
  }
}

/************************************************/

watch(route, (newRoute, oldRoute) => {
  articleMounter(newRoute);
})

onMounted(() => {
  articleMounter(route);
  setTimeout(missingArticleData, 1000)
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
  border-bottom: var(--cs-main-border);
}
@media ( orientation: landscape ) {
  .article-viewer-wrapper {
    display: grid;
    grid-template-columns: 45% 55%;
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
  border-top: var(--cs-main-border);
  margin: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}
.iiif-cartel > p {
  margin: 10px;
}
/***************************************/

.article-wrapper {
  padding: 0 1vw;
  border-left: var(--cs-main-border);
  font-size: 16px;
}
.article-index-wrapper {
  min-height: 30vh;
}
.article-wrapper :deep(p) {
  line-height: 1.3;
}
.article-wrapper :deep(.article-body) {
  margin: 0 50px;
}
.article-wrapper :deep(.article-body button) {
  display: inline-block;
  max-width: 20px;
  max-height: 20px;
  padding: 0;
  /* a negative top margin to avoid differences
     in line heights in lines that contain a `button`.
     a transform centers the button on the line.
  */
  margin: -15% 0 0 0;
  transform: translateY(15%);
}
@media ( orientation:portrait ) {
  .article-wrapper :deep(.article-body) {
    margin: 0 20px;
  }
}
</style>