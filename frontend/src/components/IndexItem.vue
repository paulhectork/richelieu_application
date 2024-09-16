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

  <!--<RouterLink v-if="display==='concept'"
     class="index-item index-item-concept"
     :to="item.href"
     :style="{ 'background-image': `url(${item.img})` }"
  >-->
  <RouterLink v-if="display==='concept'"
     class="index-item index-item-concept"
     :to="item.href"
  >
    <img :src="item.img"
         class="fill-parent"
         loading="lazy"
    >
    <p v-html="item.text"></p>
  </RouterLink>

  <RouterLink v-if="display==='cartography'"
     class="index-item index-item-cartography"
     :to="item.href"
  ></RouterLink>
</template>

<script setup>

/**************************************************************/

const props = defineProps(["item", "display"]);

</script>


<style scoped>
.index-item {
  font-family: var(--cs-font-sans-serif-accentuate);
  border: var(--cs-border);
  margin: 7px;
}
img {
  object-fit: cover;
  overflow: hidden;
  object-position: center;
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
/*
.index-item-resource .img-container {
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}
*/
.index-item-resource p {
  padding: 5px;
  height: min-content;
  border-top: var(--cs-border);
}

/**
 * concept view
 */
.index-item-concept {
  display: grid;
  grid-template-columns: 100%;
  grid-template-rows: 2fr auto;
  text-align: center;

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