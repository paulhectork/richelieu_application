<template>
  <div :id="props.footnoteHtmlId"
       class="footnote-outer-wrapper">
    <div class="footnote-inner-wrapper">
      <p v-html="props.footnoteContent"
      ></p>
      <ButtonCross @click="sendUnmount"
      ></ButtonCross>
    </div>
  </div>
</template>


<script setup>
import { onMounted, onUnmounted } from "vue";

import $ from "jquery";

import ButtonCross from "@components/ui/ButtonCross.vue";

/************************************************/

const props = defineProps([ "footnoteContent"
                          // , "footnotePosition"
                          , "footnoteHtmlId" ]);
const emit = defineEmits(["unmount-footnote"]);

/************************************************/

/**
 * emit the `unmount-footnote` event to the parent,
 * which will trigger the unmounting of this footnote.
 */
const sendUnmount = () => emit("unmount-footnote", true);

/**
 * when clicking outside of the footnote element, close it
 * @param {JQueryEventObject} e
 */
const closeOnClick = (e) => {
  if ( $(e.target).closest(`#${props.footnoteHtmlId}`).length === 0 ) {
    emit("unmount-footnote", true);
  }
}

/**
 * close the footnote when pressing the `Escape` key
 * @param {JQueryEventObject} e
 */
const closeOnEsc = (e) =>
  ( e.key === "Escape" )
  ? emit("unmount-footnote", true)
  : false ;

onMounted(() => {
  // position the element: center of the window.
  let maxWidth = $(".article-main-wrapper").width() * 0.8
  let topOffset = ($(window).height() - $(`#${props.footnoteHtmlId}`).height()) / 2;
  $(`#${props.footnoteHtmlId}`).css({ maxWidth : maxWidth,
                                      top      : topOffset });

  let leftOffset = ($(".article-main-wrapper").width() - $(`#${props.footnoteHtmlId}`).width()) / 2
  $(`#${props.footnoteHtmlId}`).css({ left: leftOffset });

  // register events. without setTimout, clicking on the `.button-ellipsis`
  // to display the footnote would also close it, because it would trigger
  // `closeOnClick`.
  setTimeout(() => {
    $(window).on("click", closeOnClick);
    $(window).on("touchend", closeOnClick);
    $(window).on("keyup", closeOnEsc)
  }, 1000)
})
onUnmounted(() => {
  $(window).off("click", closeOnClick);
  $(window).off("touchend", closeOnClick);
  $(window).off("keyup", closeOnEsc)
})

</script>


<style scoped>
.footnote-outer-wrapper {
  position: fixed;
  left: 50px;
  top: 50px;
  background-color: var(--cs-main-default-bg);
  border: var(--cs-border)
}
.footnote-outer-wrapper p {
  margin: 5px;
}
.footnote-inner-wrapper {
  display: grid;
  grid-template-rows: 100%;
  grid-template-columns: 2fr auto;
  justify-items: center;
  align-items: center;
}
.button-cross {
  margin: 5px;
  height: max(3vh, 30px);
}

</style>