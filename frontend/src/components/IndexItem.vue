<template>
  <RouterLink v-if="display==='resource'"
     class="index-item index-item-resource"
     :to="item.href"
  >
    <img :src="item.img"
         class="fill-parent"
         loading="lazy"
         >
    <p v-html="item.text"></p>
  </RouterLink>

  <RouterLink v-if="display==='concept'"
     class="index-item index-item-concept"
     :to="item.href"
     :style="{ 'background-image': `url(${item.img})` }"
  >
    <p v-html="item.text"></p>
  </RouterLink>

  <RouterLink v-if="display==='cartography'"
     class="index-item index-item-cartography"
     :to="item.href"
  ></RouterLink>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
// import $ from "jquery";

import { manifestToThumbnail } from "@utils/iiif.js";

const props = defineProps(["item", "display"]);
// const selector = `#iiif-thumbnail-${props.item.idUuid}`;

onMounted(() => {
  /*
  if ( props.item.iiif ) {
    (async () => {
      manifestToThumbnail(props.item.iiif, props.item.img)
      .then((thumbnailUrl) => {
        // console.log( thumbnailUrl );
        // $(selector).attr("src", thumbnailUrl);
        $(selector).attr("src", props.item.img)
      })
      .catch((e) => {
        console.error("ERROR IN INDEXITEM", e);
      });
    })()
  }
  */

})

</script>


<style scoped>
.index-item {
  font-family: var(--cs-font-sans-serif-accentuate);
  border: var(--cs-border);
  margin: 7px;
}
img {
  object-fit: cover;
}
a {
  text-decoration-line: none;
  color: var(--cs-main-default);
}
p {
  margin: 0;
}
.index-item:hover p {
  background-color: var(--cs-main-second-bg);
  color: var(--cs-main-second);
}


/**
 * ressource view
 */
.index-item-resource {
  display: grid;
  grid-template-columns: 100%;
  grid-template-rows: 2fr auto;
  text-align: center;
}
.index-item-resource .img-container {
  /*width: 100%;
  height: 100%;*/
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}
.index-item-resource p {
  padding: 5px;
  height: min-content;
  border-top: var(--cs-border);
}

/**
 * concept view
 */
.index-item-concept {
  display: flex;
  align-items: flex-end;
  justify-content: center;

  background-size: cover;
  background-position: center center;

  text-align: start;
}
.index-item-concept p {
  width: 100%;
  padding: 3px 3px 0px 3px;

  background-color: var(--cs-main-default-bg);
  border-top: var(--cs-border);
  font-variant: small-caps;

  display: flex;
  justify-content: space-between;
  align-items: center;

}
/*
.index-item-concept :deep(span:last-child) {
  font-family: var(--cs-font-sans-serif);
}
*/
</style>