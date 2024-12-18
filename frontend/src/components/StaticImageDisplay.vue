<template>
  <!-- StaticImageDisplay.vue
      a component that displays a non-IIIF image with a legend and full-page-view
      option, to be used inside the "/a-propos/" or "documentation/" pages

      props:
      - imgUrl (string)
          the URL to fetch the image from
      - imgAlt (string)
          the @alt attribute of the <img>
      - imgLegend (string)
          the HTML string to use as a legend for the image
  -->
  <div class="id-outer-wrapper">
    <figure class="id-wrapper">
      <div class="id-img-wrapper">
        <img :src="props.imgUrl"
             :alt="props.imgAlt || props.imgLegend"
        />
      </div>
      <figcaption class="id-legend-wrapper">
        <span v-html="imgLegend"></span>
      </figcaption>
    </figure>
  </div>

</template>


<script setup>
// import { onMounted } from "vue";

/********************************************/

const props = defineProps(["imgUrl", "imgAlt", "imgLegend"]);

/********************************************/


/********************************************/

</script>


<style scoped>
.id-outer-wrapper {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 4vh 0;
  max-height: 50vh;
}
.id-wrapper {
  width: fit-content;
  max-height: 60vh;
  max-width: 70%;
  border: var(--cs-main-border);
  /* apparently, display:grid seems useless when working with figcaption */
  /*
  display: grid;
  grid-template-rows: 85% 15%;
  grid-template-columns: 100%;
  */
}
.id-img-wrapper, .id-legend-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
}
.id-legend-wrapper {
  text-align: center;
  border-top: var(--cs-main-border);
  padding: 5px;
}
img {
  object-fit: contain;
  width: 100%;
  max-height: calc(0.85 * 50vh);  /* img has a maximum size of 85% 50vh */
}
</style>