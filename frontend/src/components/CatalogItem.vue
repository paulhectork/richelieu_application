<template>
  <a v-if="display==='resource'"
     class="catalog-item catalog-item-resource"
     :href="item.href"
  >
    <div class="img-container">
        <img :src="item.img"
             class="fill-parent">
    </div>
    <p v-html="item.text"></p>
  </a>

  <a v-if="display==='concept'"
     class="catalog-item catalog-item-concept"
     :href="item.href"
     :style="{ 'background-image': `url(${item.img})` }"
  >
    <p v-html="item.text"></p>
  </a>

</template>

<script setup>
const props = defineProps(["item", "display"]);
</script>


<style scoped>
.catalog-item {
  border: var(--cs-border);
}

.catalog-item-resource {
  display: grid;
  grid-template-columns: 100%;
  grid-template-rows: 2fr auto;
}
.img-container {
  /*width: 100%;
  height: 100%;*/
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}
img {
  height: auto;
  min-width: 120%;
}
a {
  text-decoration-line: none;
  color: var(--cs-main-default);
}
p {
  margin: 5px;
  height: min-content;
}

.catalog-item-concept {
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>