<!-- HomeThemeOrNamedEntity.vue

     props:
        resource (Object). see below for its structure.
        display (string): one of 'article'|'category',
          to set HTML style classes

     resource data model:
     {
      title_main   : <string. the main item to be displayed>,
      title_second : <string. an item that will be displayed next to title_main, in gray>,
      title_sub    : <string. a secondary item that will be displayed below, in white on back>,
      href         : <URL. an URL to make redirections>,
      thumbnail    : <string. an URL to an optional image to be displayed on the background of this component>
     }

     html structure:
     +-----------------------------------------+
     | +--------------------+ +--------------+ |
     | | title_main         | | title_second | |
     | +--------------------+ +--------------+ |
     |                                         |
     | +-------------------------------------+ |
     | | title_sub                           | |
     | +-------------------------------------+ |
     +-----------------------------------------+
-->

<template>
  <div v-if="resource != null"
       class="preview-wrapper main-default"
       :id="htmlId"
       :style="{ backgroundImage: resource.thumbnail
                                  ? `url(${resource.thumbnail})`
                                  : 'inherit' }"
  >
    <RouterLink :to="resource.href.pathname">
      <div class="preview-inner-wrapper">
        <div class="resource-main"
             :class="props.display === 'category'
                     ? 'resource-main-category'
                     : 'resource-main-article'"
        >
          <span class="title-main"
          >{{ resource.title_main }}</span>
          <span v-if="resource.title_second"
                class="title-second"
          >&nbsp;&mdash; {{ resource.title_second }}</span>
        </div>
        <div v-if="resource.title_sub"
             class="resource-sub negative-default">
          <span v-html="resource.title_sub"></span>
        </div>
      </div>
    </RouterLink>
  </div>
</template>


<script setup>
import { ref, onMounted } from "vue";

/*************************************************/

const props = defineProps(["resource", "display"]);
const resource = ref();
const htmlId = `home-item-preview-${window.crypto.randomUUID()}`;

/*************************************************/


onMounted(() => {
  resource.value = props.resource;
})


</script>


<style scoped>
.preview-wrapper {
  border: var(--cs-border);
  background-color: var(--cs-main-default-bg);
  background-size: 150%;
  background-position: center;
}
.preview-inner-wrapper {
  display: grid;
  grid-template-columns: 100%;
  grid-template-rows: 60% 40%;
}
.preview-wrapper a {
  text-decoration: unset;
  color: unset;
}
.resource-main {
  font-size: 100%;
  font-size: max(min(4vh, 4vw), 16px);
  display: flex;
  align-items: center;
  padding: 5px 5px 3px 5px;
  background-color: var(--cs-main-default-bg);
  transition: background-color .5s;
}
.resource-main-article {
  margin: 5px;
  border: var(--cs-border);
}
.title-second {
  color: var(--cs-contrast-default);
}
.resource-sub {
  font-size: max(min(2.3vh, 2.3vw), 70%);
  padding: 3px;
}

/*****************************************/

.preview-wrapper:hover .resource-main {
  background-color: var(--cs-main-second-bg);
}
.preview-wrapper:hover .resource-main,
.preview-wrapper:hover .title-second,
.preview-wrapper:active .resource-main,
.preview-wrapper:active .title-second {
  color: var(--cs-main-second);
}
.preview-wrapper:active .resource-main,
.preview-wrapper:active .title-second {
  background-color: var(--cs-contrast-active-bg);
}
</style>