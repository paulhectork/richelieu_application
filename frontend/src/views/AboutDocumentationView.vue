<template>

  <!-- AboutDocumentationView.vue
      a small component that handles the display of all About / Documentation pages.
  
      for scalability, to be sure that every one of these pages has the same HTML
      markup and offers the same behaviour, `AboutDocumentationView` will serve
      as a parent component that will dynamically import `AbDocContent*`, child
      components containing page-specific HTML and emits based on the current route.
      if the route points to nothing, an `ErrNotFound.vue` will be displayed.
  
      this is loosely based on @views/ArticleMainView.vue.
  
      this parent component handles 2 components:
      - AbDocConent* :
          the "main" part, containing a static HTML page in the ABout/Documentation
          sections, based on the router's path
          (AbDocContentEquipe, AbDocContentMethodologie, AbDocContentProjet, AbDocContentCredits, AbDocContentApi)
      - AbDocToc: a table of contents
  
      2 interactions between those components happen:
      - in portrait mode, AbDocToc can emit a message to hide/show the table
        of contents, when clicking on a button.
      - when the AbDocContent* page is loaded, AboutDocumentationView emits
        a flag to AbDocToc so that AbDocToc, using JQuery, can complete the
        table of contents with H3 headers that are within a single
        AbDocContent component.
  
  -->


  <component v-if="notFoundFlag === true"
             :is="currentComponent"
  ></component>

  <div v-else
       class="textpage-outer-wrapper">
    <div class="textpage-title-wrapper">
      <h1 v-if="pageType === 'about'">À propos</h1>
      <h1 v-else>Documentation technique</h1>
      <h2 v-html="h2Html"></h2>
    </div>

    <div class="textpage-inner-wrapper"
         :class="{ 'toc-visible': domStore.windowOrientation === 'landscape' || expandToc }"
    >

      <div class="textpage-toc-outer-wrapper">
        <AbDocToc @display-toc="toggleDisplayToc"
                  :text-mounted="textMounted"
        ></AbDocToc>
      </div>

      <div class="textpage-text-outer-wrapper">
        <component :is="currentComponent"
                   @h2="(txt) => h2Html = txt"
                   @vue:mounted="(e) => textMounted = e"
        ></component>
      </div>
    </div>
  </div>

</template>


<script setup>
import { onMounted
       , shallowRef
       , ref
       , defineAsyncComponent
       , watch
       } from "vue";
import { useRoute } from "vue-router";

import AbDocToc from "@components/AbDocToc.vue";
import { domStore } from "@stores/dom.js";

/************************************************/

const route            = useRoute();
const currentComponent = shallowRef();
const notFoundFlag     = ref(false);  // true if currentComponent === ErrNotFound.vue
const pageType         = ref(null);  // null|"about"|"documentation" (null if notFoundFlag is true)
const h2Html           = ref("");

const expandToc        = ref(false);
const textMounted      = ref();

// { <props received from router>: [ <page type>, <component name for dynamic import> ] }
const mapper = { projet       : [ "about"         , "AbDocContentProjet" ]
               , equipe       : [ "about"         , "AbDocContentEquipe" ]
               , mentions     : [ "about"         , "AbDocContentCreditsMentions" ]
               , methodologie : [ "documentation" , "AbDocContentMethodologie" ]
               , donnees      : [ "documentation" , "AbDocContentDonnees" ]
               , api          : [ "documentation" , "AbDocContentApi" ]
               , modele       : [ "documentation" , "AbDocContentDataModel" ]
               }

/************************************************/

function toggleDisplayToc(e) {
  expandToc.value = e;
}

/**
 * based on `route.params.pageName`, mount a component defined in `mapper`.
 * if `route.params.pageName` is undefined, then `ErrNotFound` will be displayed.
 */
function componentMounter(pageName) {
  let componentName;
  [ pageType.value, componentName ] = mapper[pageName] || [ null, "ErrNotFound" ];  // if "pageName" is not in mapper, an ErrNotFound will be displayed.
  notFoundFlag.value = componentName === "ErrNotFound";
  currentComponent.value = defineAsyncComponent(() =>
    import(`../components/${componentName}.vue`));
}

/************************************************/

/**
 * when switching routes, load the new AbDocContent.
 */
watch(route, (newRoute, oldRoute) => {
  componentMounter( newRoute.params.pageName );
  toggleDisplayToc(false);  // hide the table of contents when switching views
})

onMounted(() => {
  componentMounter(route.params.pageName);  // mount the component.
})
</script>


<style scoped>
.textpage-outer-wrapper {
  display: grid;
  grid-template-columns: 100%;
  grid-template-rows: auto 2fr;
  height: 100%;
  border-bottom: var(--cs-main-border);
}
.textpage-title-wrapper {
  border-bottom: var(--cs-main-border);
}
.textpage-inner-wrapper {
  display: grid;
  grid-template-rows: 100%;
}
@media ( orientation: portrait ) {
  .textpage-inner-wrapper {
    /*
    mobile grid is kinda fancy: the AbDocToc sidebar
    can be hidden/displayed on click. below is the default
    state, adding .toc-visible to .textpage-inner-walker
    adds a `transform:translateX()` that makes the sidebar visible.
    */
    grid-template-columns: 70vw calc(100vw - 5vh);  /* 5vh to accomodate for button size */
    transform: translateX(-70vw) translateX(5vh);  /* chaining translateX(trans1) translateX(trans2) is equivalent to translateX(trans1+trans2) */
    transition: transform .5s;
    overflow-x: hidden;
    width: calc(70vw + 100vw - 5vh);  /* width also needs to be set and updated to avoid x-overflow scrolling */
  }
}
@media (orientation:portrait) {
  .textpage-inner-wrapper.toc-visible {
    transform: translateX(0);
    width: 100vw;
  }
}
@media ( orientation:landscape ) {
  .textpage-inner-wrapper {
    grid-template-columns: 30% 70%;
    transform: translateX(0);
    width: 100%;
  }
}
.toc-outer-wrapper {
  height: 100%;
  width: 100%;
}
.textpage-text-outer-wrapper {
  height: 100%;
  overflow: scroll;
  padding: 5%;
  font-size: var(----cs-fontsize-article);
}

:deep(.textpage-text-wrapper) {
  border-bottom: var(--cs-main-border);
}
:deep(.textpage-text-wrapper:not(:last-child)) {
  padding-bottom: 4vh;
}
:deep(.textpage-text-wrapper:last-child) {
  border-bottom: none;
}
:deep(.textpage-text-wrapper h3) {
  font-variant-caps: small-caps;
  text-decoration: underline;
  margin-left: 0;
}
:deep(.textpage-text-wrapper h4) {
  text-decoration: underline;
}
:deep(.textpage-text-wrapper dt) {
  font-family: var(--cs-font-serif);
  font-size: 110%;
  font-variant-caps: small-caps;
  margin-top: 5px;
}
:deep(.textpage-text-wrapper dd) {
  margin-bottom: 20px;
}
</style>
