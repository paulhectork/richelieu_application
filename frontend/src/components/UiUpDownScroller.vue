<!--
  UiUpDownScroller.vue : a component to add Up/Down
  buttons to a page. buttons are visible when the
  user has scrolled past `0.75 * windowHeight`,
  but is further than `0.75 * windowHeight`
  from the end of the document.
-->

<template>
  <div id="scroll-buttons">
    <TransitionGroup>
      <UiButtonArrow orient="up"
                   v-if="displayButtons"
                   @click="scroller('up')"
      ></UiButtonArrow>
      <UiButtonArrow orient="down"
                   v-if="displayButtons"
                   @click="scroller('down')"
      ></UiButtonArrow>
    </TransitionGroup>
  </div>
</template>

<script setup>
import { onMounted, onUnmounted, ref } from "vue";
import UiButtonArrow from "@components/UiButtonArrow.vue";

import $ from "jquery";


const margins = 0.75 * $(window).height();  // vertical margins within which to display buttons
const displayButtons = ref(false);          // wether or not to display buttons.

/**
 * scroll to top or bottom of table
 * @param {str} direction: the direction in which to scroll
 */
function scroller(direction) {
  const allowed = ["up", "down"];

  if ( !allowed.includes(direction) ) {
    throw new Error(`DataTableComponent.scroller: 'direction' must be one of '${allowed}', got '${direction}'`)
  } else if (direction === "up") {
    window.scrollTo({ top:document.querySelector("body")
                                  .getBoundingClientRect()
                                  .top,
                      behavior:"smooth" });
  } else if (direction === "down") {
      window.scrollTo({ top:$(document).height(),
                        behavior:"smooth" });
  }
}

/**
 * calculate wether or not to display Up and Down
 * arrow buttons. triggered on scroll. buttons are
 * visible when the vertical scrolling is contained
 * in a +/- 0.75 * $(window).height()
 */
function calcDisplayButtons() {
  displayButtons.value = (
    $("body")[0].getBoundingClientRect().top                         // top of the document is below `margins`
      < -margins
    &&
    document.documentElement.clientHeight + $(document).scrollTop()  // bottom of the documents is above `margins`
      <= $(document).height() - margins
  )
}


onMounted(() => {
  $(window).on("scroll", calcDisplayButtons)
})

onUnmounted(() => {
  window.removeEventListener("scroll", calcDisplayButtons);
})
</script>

<style scoped>
#scroll-buttons {
  position: fixed;
  top: 90vh;
  left: 0;
  z-index: 1;
  height: 10vh;
  width: 70%;

  display: flex;
  flex-direction: row;
  justify-content: right;
}
#scroll-buttons > button {
  height: 7vh;
  width: 7vh;
}

</style>