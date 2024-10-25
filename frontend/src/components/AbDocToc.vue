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
  >
    <div class="toc-inner-wrapper negative-default">
      <div class="toc-showhide">
        <UiButtonPlus v-if="domStore.windowOrientation === 'portrait'"
                      @click="showOrHideToc"
                      :class="{ 'as-cross': expandToc }"
        ></UiButtonPlus>
      </div>

      <!--
      we use style:display instead of v-if because v-if removes the element
      from the DOM, which messes up the insertion or `.toc-lvl3-root` with jquery
      -->
      <ul class="list-invisible toc-lvl1-root"
          :style="{ display: expandToc ? 'block' : 'none' }"
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
          <ol class="toc-lvl2-root list-invisible"
              :class="{ 'hidden-list': false/*!expandAbout*/ }"
          >
            <li id="toc-item-projet"
                class="toc-lvl2"
            >
              <RouterLink to="/a-propos/projet">Le projet</RouterLink>
              <AbDocTocSub :tocElements="tocSubElements['toc-item-projet']"
              ></AbDocTocSub>
            </li>
            <li id="toc-item-equipe"
                class="toc-lvl2"
            >
              <RouterLink to="/a-propos/equipe">L'équipe</RouterLink>
              <AbDocTocSub :tocElements="tocSubElements['toc-item-equipe']"
              ></AbDocTocSub>
            </li>
            <li id="toc-item-mentions"
                class="toc-lvl2"
            >
              <RouterLink to="/a-propos/mentions">Crédits et mentions légales</RouterLink>
              <AbDocTocSub :tocElements="tocSubElements['toc-item-mentions']">
              </AbDocTocSub>
            </li>
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
          <ol class="toc-lvl2-root list-invisible"
              :class="{ 'hidden-list': false/*!expandDocumentation*/ }"
          >
            <li id="toc-item-methodologie"
                class="toc-lvl2"
            >
              <RouterLink to="/documentation/methodologie">
                Méthodologie du projet</RouterLink>
              <AbDocTocSub :tocElements="tocSubElements['toc-item-methodologie']"
              ></AbDocTocSub>
            </li>
            <li id="toc-item-api"
                class="toc-lvl2"
            >
              <RouterLink to="/documentation/api">Documentation de l'API</RouterLink>
              <AbDocTocSub :tocElements="tocSubElements['toc-item-api']"
              ></AbDocTocSub>
            </li>
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

import AbDocTocSub from "@components/AbDocTocSub.vue";
import UiButtonPlus from "@components/UiButtonPlus.vue";

import { domStore } from "@stores/dom.js";

/*********************************************/

const route = useRoute();
const emit = defineEmits(["displayToc"]);
const props = defineProps(["textMounted"]);

const currentId = ref("");
const expandToc = ref(false);

// { <htmlId of a toc-lvl2 item> : [<array of elements to pass to AbDocTocSub]  }
const tocSubElements = ref({ "toc-item-projet"       : []
                           , "toc-item-equipe"       : []
                           , "toc-item-mentions"     : []
                           , "toc-item-methodologie" : []
                           , "toc-item-api"          : []
                           })

// { route.params.pageName: <htmlid> }
const idMapper = { projet       : "toc-item-projet"
                 , equipe       : "toc-item-equipe"
                 , mentions     : "toc-item-mentions"
                 , methodologie : "toc-item-methodologie"
                 , api          : "toc-item-api"
                 }

/*********************************************/

const resetStateAndHtml = () => {
  currentId.value = "";
  expandToc.value = false;
  $("li.toc-lvl2").removeClass("current-toc-lvl2");
  // $(".toc-lvl3-root").remove();

  Object.keys(tocSubElements.value).map((k) => {
    tocSubElements.value[k] = []
  })
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
  let newList = $("<ol class='toc-lvl3-root animate__animated animate__slideInLeft animate__faster'></ol>");
  let h3Titles = [];
  $(".textpage-text-wrapper h3").each((i, obj) => {
    h3Titles.push({ html: $(obj).html(),
                    href: $(obj).attr("id") || "" })
    // subTocItem[currentId.value] =
    // let newEl = $("<li class='toc-lvl3'></li>").append($(obj).html());
    // newList.append(newEl);
  });
  tocSubElements.value[currentId.value] = h3Titles;
  console.log(h3Titles);

  // if ( newList.children("li").length ) {
  //   console.log(">", currentId.value);
//
  //   // TODO: find out why there's a 750/1000ms waiting time before
  //   // $(`#${currentId.value}`) is added to the dom
  //   // TODO: fix .toc-inner-wrapper flickering when changing views without unmounting
  //   // TODO: fix bug with uppercase `.toc-lvl3`
  //   $(`#${currentId.value}`).append(newList);
  // }
}

function setRefs() {
  let urlSlug = route.path.match(/(?<=^\/)[^\/]+/g)[0];

  // expandDocumentation.value = true;// urlSlug === "documentation";
  // expandAbout.value         = true;// urlSlug === "a-propos";
  currentId.value = idMapper[route.params.pageName];
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
})

onMounted(() => {
  setRefs();
})
onUnmounted(() => {
  resetStateAndHtml();
})
</script>


<style scoped>
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
.toc-inner-wrapper {
  /*
  height: calc(100% - 20px);
  width: calc(100% - 20px);
  */
  height: 100%;
  width: 100%;
  overflow: scroll;
}

/***********************/

.toc-showhide {
  width: 100%;
  display: flex;
  justify-content: flex-end;
}
.button-cross {
  min-height: 4vh;
  min-width:  4vh;
  height:     4vh;
  width:      4vh;
}
.button-cross :deep(svg) {
  transition: transform var(--animate-duration);
}
.button-cross.as-cross :deep(svg) {
  transform: rotate(45deg);
}

/***********************/

.toc-lvl1 {
  margin: 5% 0;
  padding: 3% 3% 3% 5%;
  border-top: var(--cs-negative-border);
  border-bottom: var(--cs-negative-border);
  height: 50%;
}
.toc-lvl1-title {
  height: 10%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: var(--cs-negative-border);
  margin: 0 0% 3% 0;
  padding-bottom: 2%;

  font-variant-caps: small-caps;
  font-size: 130%;
  font-family: var(--cs-font-serif);
}
.toc-lvl2 {
  padding: 1% 0 1% 10%;
}
.current-toc-lvl2 {
  font-variant-caps: small-caps;
  font-family: var(--cs-font-sans-serif-accentuate);
}

.hidden-list {
  display: none;
}
</style>