<template>
  <h1>Articles</h1>
  <div class="article-index-wrapper">
    <ul class="list-invisible">
      <li v-for="article in articles"
          class="article-item-wrapper"
      >
        <div class="article-item"
             :style="{ backgroundImage: `url(${article.image})` }"
        >
          <RouterLink :to="`/article/${article.urlSlug}`">
            <h2>{{ article.title }}</h2>
            <h3 v-html="article.subtitle"></h3>
          </RouterLink>
          <!--
          <div class="hover-overlay"
               @mouseenter="showOverlayOnMouseEnter"
               @mouseleave="hideOverlayOnMouseLeave"
          ></div>
          -->
        </div>
      </li>
    </ul>
  </div>
</template>


<script setup>
import { ref, onMounted, onUnmounted } from "vue";

import $ from "jquery";

import { articles } from "@globals";

/*******************************************/

const onMouseEnter = (e) => {
  $(e.currentTarget).addClass("selected") };

const onMouseOut = (e)  =>
  $(".article-item").removeClass("selected");

onMounted(() =>
  $(".article-item").on("mouseover", onMouseEnter)
                    .on("mouseout", onMouseOut)
)

</script>


<style scoped>
@media (orientation:landscape) {
  .article-index-wrapper {
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .article-index-wrapper > ul {
    width: 75%;
  }
}
.article-item {
  border: var(--cs-main-border);
  margin: 20px 5px;
  background-position: center;
  position: relative;  /* for the article overlays */
  transform: translateX(0);
  transition: transform .3s;
}
.article-item.selected {
  border: solid var(--cs-plum) 4px;
  transform: translateX(3%);
}
.article-item > a {
  text-decoration: none;
  color: var(--cs-main-default);
}
h2, h3 {
  background-color: var(--cs-main-default-bg);
  width: fit-content;
  border: var(--cs-main-border);
  border-left: none;
  padding: 3px 3px 1px 3px;
}
a {
  z-index: 10;
}
.hover-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;

  transition: opacity var(--cs-color-transition);
  background: linear-gradient(50deg, #C78FA5, var(--cs-seagreen));
  opacity: 0;
}
</style>