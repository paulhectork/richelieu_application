<template>
  <button>
    <svg width="100%"
         height="100%"
         viewBox="0 0 24 24" fil
         l="none"
         xmlns="http://www.w3.org/2000/svg"

         transform-box="fill-box"
         transform-origin="center"
         :transform="rotateOnOrient()"
    >
      <path d="M12 5V19M12 5L6 11M12 5L18 11"
            stroke="none"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
      />
    </svg>
  </button>
</template>

<script setup>
import { onMounted } from 'vue';

/**
 * an arrow button that can be rotated based on
 * the value of `props.orient` ("up", "down", "left", "right")
 */

const props = defineProps([ "orient" ]);

function rotateOnOrient() {
  const allowed = ["up", "down", "left", "right"];
  const orient = props.orient;

  if ( !allowed.includes(orient) ) {
    throw new Error(`ButtonArrow.vue: value of orient must be one of '${allowed}', got '${orient}'`)
  } else {
    switch (orient) {
      case "up":
        return "rotate(0 0 0)";
      case "right":
        return "rotate(90 0 0)";
      case "down":
        return "rotate(180 0 0)";
      case "left":
        return "rotate(270 0 0)";
    }
  }
}

</script>

<style>
button {
  padding: 3px;
}
</style>