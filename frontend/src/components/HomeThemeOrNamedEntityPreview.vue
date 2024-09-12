<!-- HomeThemeOrNamedEntity.vue

     props:
      resource (Object):
        a theme or named entity with the structure:
        ```
        {
          "category_name": "<category name>",
          "count"        : <number of associated themes or named entities>,
          "preview"      : [ <Array<string> of a few themes or named entities
                             of that resource> ],
          "thumbnail"    : [ <filename> ]
        }
        ```
      tableName (string):
        "theme" or "named_entity"
-->

<template>
  <div v-if="resource != null"
       class="preview-wrapper main-default"
       :id="htmlId"
  >
    <RouterLink :to="tableName === 'named_entity'
                     ? urlToFrontendNamedEntityCategory(resource.category_name).pathname
                     : urlToFrontendThemeCategory(resource.category_name).pathname"
    >
    <div class="preview-inner-wrapper">
      <div class="resource-main">
        <span class="resource-main-text">
          {{ resource.category_name }}
          <span class="resource-count">&mdash; {{ resource.count }}</span>
        </span>
      </div>
      <div class="resource-preview negative-default">
        <span v-html="resource.preview"></span>
        </div>
    </div>
    </RouterLink>
  </div>
</template>


<script setup>
import { ref, onMounted, computed, setBlockTracking } from "vue";

import $ from "jquery";

import { urlToFrontendNamedEntityCategory
       , urlToFrontendThemeCategory } from "@utils/url";

/*************************************************/

const props = defineProps(["resource", "tableName"]);
const resource = ref();
const tableName = ref("");
const htmlId = `home-theme-or-named-entity-preview-${window.crypto.randomUUID()}`;

const dirtyResize = () => {
  const selector = `#${htmlId}`;
  if ( $(selector).length ) {
    $(selector).width( $(`${selector} .resource-main-text`).width() + 10 );  // +10 accounts for margins
}}

onMounted(() => {
  if ( !["named_entity", "theme"].includes(props.tableName) ) {
    console.error(`HomeThemeOrNamedEntityPreview.onMounted: got "${props.tableName}" for "props.tableName", expected one of "named_entity", "theme"]`)
  }
  tableName.value = props.tableName;
  resource.value = props.resource;

  // create a string representation of `resource.preview` (Array<str>).
  // we use a regex to set the string's content so that it's about the
  // same length (visually) as that of `resource.value.category_name`
  let p   = resource.value.preview.sort((a,b) => a.length - b.length)   // shorter elements of `preview` first
                                  .join(" &mdash; " ),
      len = Math.round(resource.value.category_name.length * 0.8),      // maximum allowed string size
      rgx = new RegExp(`^.{${len}}.+?((?=\\s*&mdash;)|(?=$))`);         // match until the next &mdash; or end of line
  resource.value.preview = p.match(rgx) !== null ? p.match(rgx)[0] : p;

})


</script>


<style scoped>
.preview-wrapper {
  border: var(--cs-border);
  background-color: var(--cs-main-default-bg);

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
  font-size: max(min(3vh, 3vw), 16px);
  white-space: nowrap;
  /*padding: 5px;*/
}
.resource-main > span {
  /*background-color: red;*/
}
.resource-main-text {
  display: block;
  padding: 5px 5px 3px 5px;
}
.resource-count {
  color: var(--cs-contrast-default)
}
.resource-preview {
  font-size: 80%;
  padding: 3px;
}
</style>