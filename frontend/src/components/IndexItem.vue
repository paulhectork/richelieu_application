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

  display: grid;
  grid-template-columns: 100%;
  grid-template-rows: 2fr auto;
  text-align: center;

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
  padding: 5px;
  width: 100%;
  border-top: var(--cs-border);
  height: min-content;
}
.index-item:hover p {
  background-color: var(--cs-main-second-bg);
  color: var(--cs-main-second);
}

/* ressource view */
.index-item-resource p {
  text-align: center;
}

/* concept view */
.index-item-concept p {
  font-variant: small-caps;
  text-align: start;

  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>