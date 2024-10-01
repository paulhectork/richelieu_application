<!-- WaitingToComeToLife.vue
     just a simple modal window for when a page
     doesn't yet exist, but will shortly.
-->

<template>
  <div class="warn-wrapper">
    <div class="warn">
      <p>Cette page est encore en développement :^(</p>
    </div>
  </div>
</template>


<style scoped>
.warn-wrapper {
  position: absolute;
  top: 0;
  height: 100%;
  width: 100%;
  z-index: 999;
  display: grid;
  align-items: center;
  justify-content: center;
  background-color: rgba(113,5,81,.5);
}
.warn {
  opacity: 1;
  background-color: white;
  border: var(--cs-main-border);
}
.warn > p {
  margin: 30px;
}
</style>