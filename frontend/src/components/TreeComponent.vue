<!-- TreeComponent.vue

  a tree component to represent a nested list.
  currently, the tree component only allows 2 levels of depth
  (a list of nodes and their children)

  props:
  - data (@typedefs.treeData)
      the data to represent as a tree.
-->

<template>
  <div class="tree-wrapper">
    <ul class="tree-root list-invisible"
        v-if="data && data.length"
    >
      <li v-for="(nodeLvl1, idx) in data"
          class="node-lvl1"
          :class="{ 'node-children-expanded': expandedNodes.includes(htmlIdArray[idx]) }"
          :id="htmlIdArray[idx]"
      >
        <span class="node-lvl1-label">
          <UiButtonPlus @click="() => addOrRemoveToExpanded(htmlIdArray[idx])"
          ></UiButtonPlus>
          <RouterLink v-if="nodeLvl1.nodeUrl"
                      :to="nodeLvl1.nodeUrl"
                      v-html="nodeLvl1.nodeLabel"
          ></RouterLink>
          <span v-else
                v-html="nodeLvl1.nodeLabel"
          ></span>
        </span>
        <div class="node-lvl1-children-wrapper">
          <ul class="node-lvl2-root">
            <li v-for="nodeLvl2 in nodeLvl1.nodeChildren"
                class="node-lvl2"
            >
              <span class="node-lvl2-label">
                <RouterLink v-if="nodeLvl2.nodeUrl"
                            :to="nodeLvl2.nodeUrl.pathname"
                            v-html="nodeLvl2.nodeLabel"
                ></RouterLink>
                <span v-else
                      v-html="nodeLvl2.nodeLabel"
                ></span>
              </span>
            </li>
          </ul>
        </div>
      </li>
    </ul>
  </div>
</template>


<script setup>
import { ref, onMounted, watch } from "vue";

import _ from "lodash";

import UiButtonPlus from "@components/UiButtonPlus.vue";

import "@typedefs";

/*******************************************/

const props = defineProps(["data"]);

/** @type {treeData} */
const data = ref();
/** @type {string[]} */
const htmlIdArray = ref([]);
/** @type {string[]} if an html id is in this array, then nodeChildren will be expanded */
const expandedNodes = ref([]);

/*******************************************/

/**
 * if `htmlId` is in `expandedNodes`, remove it (collapse the children)
 * else, expand it (display the children)
 * @param {string} htmlId
 */
function addOrRemoveToExpanded(htmlId) {
  let expandedNodesCopy = _.clone(expandedNodes.value),
      slugPos           = expandedNodesCopy.indexOf(htmlId);
  slugPos > -1 ? expandedNodesCopy.splice(slugPos, 1)
               : expandedNodesCopy.push(htmlId);
  expandedNodes.value = expandedNodesCopy;
}

/**
 * function to run at init or when props change: sets the start state.
 */
function initHook() {
  data.value = props.data;
  htmlIdArray.value = data.value.map(x => window.crypto.randomUUID());
  expandedNodes.value = [];
}

/*******************************************/

watch(props, (newP, oldP) => {
  initHook();
})

onMounted (() => {
  initHook();
})
</script>


<style scoped>
.tree-wrapper {
  width: auto;
  margin: 0 5%;
  border: var(--cs-main-border);
  display: flex;
  flex-direction: column;
}
ul.tree-root {
  width: 100%;
  max-width: 100%;
}
.tree-wrapper li {
  width: 100%;
}

/**************************/

.node-lvl1 {
  position: relative;
  width: 100%;
  border-top: var(--cs-main-border);
  padding: 10px;
  display: flex;
  flex-direction: column;
  align-items: start;
}
.node-lvl1:first-child {
  border-top: none;
}
.node-lvl1-label {
  display: flex;
  flex-direction: row;
  align-items: center;
}

.node-lvl1-label > button {
  height: max(4vh, 40px);
  width: max(4vh, 40px);
}
.node-lvl1-label > button :deep(svg) {
  transition: transform var(--animate-duration);
}
.node-children-expanded button :deep(svg) {
  transform: rotate(45deg);
}

/**************************/

/** height animation:
 * https://keithjgrant.com/posts/2023/04/transitioning-to-height-auto/#with-grid
 */
.node-lvl1-children-wrapper {
  display: grid;
  grid-template-rows: 0fr;
  transition: grid-template-rows var(--animate-duration) ease-in-out;
}
.node-children-expanded .node-lvl1-children-wrapper {
  grid-template-rows: 1fr;
}
.node-lvl2-root {
  overflow: hidden;
}
</style>