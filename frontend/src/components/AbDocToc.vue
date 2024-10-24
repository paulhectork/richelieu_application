<!--

  architecture:
  - toc-lvl1-root : the root of the toc
  - toc-lvl1      : À propos / Documentation
  - toc-lvl2-root : list containing all lvl2 items
  - toc-lvl2      : actual view (Le projet, L'équipe...)
  - toc-lvl3-root : list containing all lvl3 items
  - toc-lvl3      : all H3 within the current view, if there are any
-->

<template>
  <div class="toc-outer-wrapper"
       :class="{ 'hidden-toc': ''/*!displayToc*/ }"
  >
    <div class="toc-inner-wrapper negative-default">
      <div class="toc-showhide">
        <UiButtonPlus v-if="domStore.windowOrientation === 'portrait'"
                      @click="showOrHideToc"
                      :class="{ 'as-cross': expandToc }"
        ></UiButtonPlus>
      </div>

      <ul class="list-invisible toc-lvl1-root"
          v-if="expandToc"
      >

        <li class="toc-lvl1">
          <div class="toc-lvl1-title">
            <span>À propos</span>
            <!--
            <UiButtonPlus @click="switchExpandAbout"
                          :class="{ 'as-cross': expandAbout }"
            ></UiButtonPlus>
            -->
          </div>
          <ol class="toc-lvl2-root"
              :class="{ 'hidden-list': false/*!expandAbout*/ }"
          >
            <li id="toc-item-projet"
                class="toc-lvl2"
            ><RouterLink to="/a-propos/projet">
              Le projet</RouterLink></li>
            <li id="toc-item-equipe"
                class="toc-lvl2"
            ><RouterLink to="/a-propos/equipe">
              L'équipe</RouterLink></li>
            <li id="toc-item-mentions"
                class="toc-lvl2"
            ><RouterLink to="/a-propos/mentions">
              Crédits et mentions légales</RouterLink></li>
          </ol>
        </li>

        <li class="toc-lvl1">
          <div class="toc-lvl1-title">
            <span>Documentation technique</span>
            <!--
            <UiButtonPlus @click="switchExpandDocumentation"
                          :class="{ 'as-cross': expandDocumentation }"
            ></UiButtonPlus>
            -->
          </div>
          <ol class="toc-lvl2-root"
              :class="{ 'hidden-list': false/*!expandDocumentation*/ }"
          >
            <li id="toc-item-methodologie"
                class="toc-lvl2"
            ><RouterLink to="/documentation/methodologie">
              Méthodologie du projet</RouterLink></li>
            <li id="toc-item-api"
                class="toc-lvl2"
            ><RouterLink to="/documentation/api">
              Documentation de l'API</RouterLink></li>
          </ol>
        </li>

      </ul>
    </div>
  </div>
</template>


<script setup>
import { onMounted, ref, watch, onUnmounted } from "vue";
import { useRoute } from "vue-router";

import $ from "jquery";

import UiButtonPlus from "@components/UiButtonPlus.vue";
import { domStore } from "@stores/dom.js";

/*********************************************/

const route = useRoute();
const emit = defineEmits(["displayToc"]);
const props = defineProps(["textMounted"]);

const currentId = ref("");
// const expandDocumentation = ref(false);
// const expandAbout         = ref(false);
const expandToc = ref(false);

// { route.params.pageName: html:Id }
const idMapper = { projet         : "toc-item-projet"
                 , equipe         : "toc-item-equipe"
                 , mentions       : "toc-item-mentions"
                 , methodologie   : "toc-item-methodologie"
                 , api            : "toc-item-api"
                 }

/*********************************************/

const resetStateAndHtml = () => {
  currentId.value = "";
  expandToc.value = false;
  $("li.toc-lvl2").removeClass("current-toc-lvl2");
  $(".toc-lvl3-root").remove();
}

const setExpandTocBase = (windowOrientation) => {
  expandToc.value = windowOrientation === "landscape";
}

const showOrHideToc = () => {
  expandToc.value = !expandToc.value;
  emit("displayToc", expandToc.value);
};


// const switchExpandAbout = () => {
//   expandAbout.value = !expandAbout.value };

// const switchExpandDocumentation = () => {
//   expandDocumentation.value = !expandDocumentation.value };

const setCurrentItem = (htmlId) => {
  $("li.toc-lvl2").removeClass("current-toc-lvl2");
  $(`#${htmlId}`).addClass("current-toc-lvl2");
}

function setSubtitles() {
  let newList = $("<ol class='toc-lvl3-root'></ol>");
  $(".textpage-text-wrapper h3").each((i, obj) => {
    let newEl = $("<li class='toc-lvl3'></li>").append($(obj).html());
    newList.append(newEl);
  });

  if ( newList.children("li").length ) {
    console.log(">", currentId.value);

    // TODO: find out why there's a 750/1000ms waiting time before
    // $(`#${currentId.value}`) is added to the dom
    // TODO: fix .toc-inner-wrapper flickering when changing views without unmounting
    // TODO: fix bug with uppercase `.toc-lvl3`
    setTimeout(() => {
      $(`#${currentId.value}`).append(newList);
    }, 1000);
  }
}

function setRefs() {
  let urlSlug = route.path.match(/(?<=^\/)[^\/]+/g)[0];

  // expandDocumentation.value = true;// urlSlug === "documentation";
  // expandAbout.value         = true;// urlSlug === "a-propos";
  currentId.value           = idMapper[route.params.pageName];
  setCurrentItem(currentId.value);
  setExpandTocBase(domStore.windowOrientation);
}

/*********************************************/

watch(props, (newP, oldP) => {
  setSubtitles()
})
watch(domStore, (newDs, oldDs) => {
  setExpandTocBase(newDs.windowOrientation);
});

watch(route, (newRoute, oldRoute) => {
  resetStateAndHtml();
  setRefs();
  $(".toc-lvl3-root").remove();
})

onMounted(() => {
  setRefs();
})
onUnmounted(() => {
  resetStateAndHtml();
})
</script>


<style scoped>
* {
  font-family: var(--cs-font-serif);
  font-size: 102%;
}
a {
  color: var(--cs-negative-default) !important;
  text-decoration: none;
}
a.router-link-active {
  text-decoration: underline;
}

/***********************/

.toc-outer-wrapper {
  border-right: var(--cs-main-border);
  align-self: start;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  /*padding: 5px;*/
}
/*
.toc-outer-wrapper.hidden-toc {
  padding: 0;
}
*/
.toc-inner-wrapper {
  /*
  height: calc(100% - 20px);
  width: calc(100% - 20px);
  */
  height: 100%;
  width: 100%;
  overflow: scroll;
}
.toc-showhide {
  width: 100%;
  display: flex;
  justify-content: flex-end;
}
.current-toc-lvl2 {
  font-variant-caps: small-caps;
}
.toc-lvl1 {
  margin: 5% 0;
  padding: 3%;
  border-top: var(--cs-negative-border);
  border-bottom: var(--cs-negative-border);
}
.toc-lvl1-title {
  height: 10%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: var(--cs-negative-border);
  margin: 0 0% 5% 0;
  padding-bottom: 2%;

  font-variant-caps: small-caps;
  font-size: 130%;
}
.button-cross {
  min-height: max(4vh, 50px);
  min-width: max(4vh, 50px);
  height: max(4vh, 50px);
  width: max(4vh, 50px);
}
.button-cross :deep(svg) {
  transition: transform var(--animate-duration);
}
.button-cross.as-cross :deep(svg) {
  transform: rotate(45deg);
}
.hidden-list {
  display: none;
}
</style>