<template>
  <!-- AbDocTocSub.vue
      a small component to display a table of contents
      for the subtitles within a view (all H3s)

      props:
      - tocElements (Array)
          an array of table of content items, that are h3
          titles within a single AbDocContent component.
          structure of each item:
          `{ html: <html to display>, href: <Url to redirect to> }`
  -->

  <ol :id="htmlId"
      class='toc-lvl3-root animate__animated animate__fadeInLeft'
      style="animation-duration: .75s"
      v-if="tocElements.length"
  >
    <li v-for="el in tocElements"
        class="toc-lvl3">
      <RouterLink :to="el.href"
                  v-html="el.html"
      ></RouterLink>
    </li>
  </ol>

</template>


<script setup>
import { onMounted, watch, ref } from "vue";

/*********************************************/

const props = defineProps(["tocElements"]);
const tocElements = ref([]);
const htmlId = `ab-doc-toc-sub-${window.crypto.randomUUID()}`;

/*********************************************/

function setTocElements(theTocElements) {
  tocElements.value = theTocElements;
}

watch(props, (newP, oldP) => {
  setTocElements(newP.tocElements);
})
onMounted(() => {
  setTocElements(props.tocElements);
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
.toc-lvl3-root {
  height: 100%;
}
</style>
