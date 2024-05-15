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
    <svg>
      <text v-html="item.text"
            x="50%"
            y="50%"
      ></text>
    </svg>
  </a>

</template>

<script setup>
const props = defineProps(["item", "display"]);
</script>


<style scoped>
.catalog-item {
  border: var(--cs-border);
}

/**
 * ressource view
 */
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
  object-fit: cover;
}
a {
  text-decoration-line: none;
  color: var(--cs-main-default);
}
p {
  margin: 5px;
  height: min-content;
}

/**
 * concept view
 */
.catalog-item-concept {
  display: flex;
  align-items: center;
  justify-content: center;

  background-size: cover;
  background-position: center center;
}
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
</style>