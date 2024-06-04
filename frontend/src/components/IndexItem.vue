<template>
  <a v-if="display==='resource'"
     class="index-item index-item-resource"
     :href="item.href"
  >
    <div class="img-container">
        <!--<div v-if="item.iiif != null"
             :id="item.uuid"
        ></div>-->
        <img v-if="item.iiif"
             :src="manifestToThumbnail(item.iiif, item.href)">
        <img v-else
             :src="item.img"
             class="fill-parent">
    </div>
    <p v-html="item.text"></p>
  </a>

  <a v-if="display==='concept'"
     class="index-item index-item-concept"
     :href="item.href"
     :style="{ 'background-image': `url(${item.img})` }"
  >
    <p v-html="item.text"></p>
  </a>

  <a v-if="display==='cartography'"
     class="index-item index-item-cartography"
     :href="item.href"
  ></a>
</template>

<script setup>
import { manifestToThumbnail } from "@utils/iiif.js";

const props = defineProps(["item", "display"]);

</script>


<style scoped>
.index-item {
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
/* `>>>` is a deep selector that allows to apply
   style to elts rendered with `v-html` */
.index-item-concept >>> span:last-child {
  font-family: var(--cs-font-sans-serif);
}
/*
svg {
  font-size: var(--cs-fontsize-mobile);
  display: flex;
  justify-content: center;
  align-items: center;
}
text {
  height: 100%;
  width: 100%;
  fill: var(--cs-main-default);
  stroke: var(--cs-main-default-bg);
  stroke-width: .5px;
  stroke-linejoin: round;
  animation: 2s pulsate infinite;
}
@keyframes pulsate {
  50%{ stroke-width:1px }
}

@media( orientation: landscape ) {
  svg {
    font-size: var(--cs-fontsize-main-desktop);
  }
}
*/
</style>