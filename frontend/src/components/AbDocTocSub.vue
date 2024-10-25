<!-- AbDocTocSub.vue
    a small component to display a table of contents
    for the subtitles within a view (all H3s)
-->


<template>

  <Transition name="slideInOut">
    <ol class='toc-lvl3-root'
        v-if="tocElements.length"
    >
      <li v-for="el in tocElements"
          class="toc-lvl3"
      >
        <RouterLink :to="'el.href'"
                    v-html="el.html"
        ></RouterLink>
      </li>
    </ol>
  </Transition>
</template>


<script setup>
import { onMounted, onUnmounted, watch, ref } from "vue";

// TODO ELEMENTS toc-lvl3 DISAPPEAR AFTER APPEARING ONCE

/*********************************************/


// TODO CLEANUP CODE HERE AND IN ABDOCTOC + FIX TRANSITION
// TODO PUSH TO MAIN

const props = defineProps(["tocElements"])
const tocElements = ref([]);

/*********************************************/

function setTocElements(theTocElements) {
  console.log("***", theTocElements);
  tocElements.value = theTocElements;
}

watch(props, (newP, oldP) => {
  setTocElements(newP.tocElements);
})
onMounted(() => {
  console.log("hii");
  setTocElements(props.tocElements);
})
onUnmounted(() => {
  console.log("bye");
})
</script>


<style scoped>
a {
  color: var(--cs-negative-default) !important;
  text-decoration: none;
}
.toc-lvl3 {
  font-variant-caps: normal;
}
</style>
