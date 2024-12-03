<!-- TheQuickSearchBar.vue

  a search bar placed in the navbar to run a quick search
  (on the website and on backend data)
-->

<template>
  <div class="qsb-outer-wrapper">
    <div class="qsb-inner-wrapper">
      <FormKit type="search"
               id="quick-search-bar"
               name="quickSearchBar"
               placeholder="Recherche rapide"
               value=""
               validation="textValidator"
               @submit="onSubmit"
      ></FormKit>
    </div>
  </div>
</template>


<script setup>
function onSubmit (e) {

}
</script>

<style scoped>
.qsb-outer-wrapper {
  height: 100%;
  min-width: 200px;
  display: grid;
  align-items: center;
  justify-content: center;
}
.qsb-inner-wrapper {
  width: 100%;
  min-width: 200px;
}
.formkit-outer {
  margin: 0;
}

</style>