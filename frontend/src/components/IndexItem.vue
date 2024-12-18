<template>

  <!-- IndexItem.vue
    a single item in @components/IndexBase
  
    props:
      - item (typedefs.IndexBaseItem)
          the item to format
      - display (String)
          a keyword to switch between display styles
  -->


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
  border: var(--cs-main-border);

  display: grid;
  grid-template-columns: 100%;
  grid-template-rows: 2fr auto;
  text-align: center;
}
a {
  text-decoration-line: none;
  color: var(--cs-main-default);
  height: 100%
}
img {
  object-fit: cover;
  overflow: hidden;
  object-position: center;
}
p {
  margin: 0;
  padding: 5px;
  width: 100%;
  border-top: var(--cs-main-border);
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

/* negative theme */
.negative-default .index-item {
  border: var(--cs-negative-border);
}
.negative-default p {
  border-top: var(--cs-negative-border);
}
.negative-default a {
  color: var(--cs-negative-default);
}
.negative-default .index-item:hover p {
  background-color: var(--cs-negative-second-bg);
  color: var(--cs-negative-second);
}
</style>
