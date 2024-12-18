<template>
  <!-- DownloadButtonGroup.vue
      a button that allows to download viewed content as JSON or CSV.

      props:
        - disableButtons (bool)
            if `true`, the buttons will have the attribute @disabled
            to block launching extra downloads when one is aldready ongoing.
            (used by IndexIconography, where download takes a lot of time)

      emits
        - download (String "csv"|"json")
            an order to trigger data download
  -->

  <div class="download-button-group">
        Téléchargement&nbsp;:&nbsp;
        <button @click="emit('download', 'json')"
                :disabled="disabled===true"
        >JSON</button>
        <button @click="$emit('download', 'csv')"
                :disabled="disabled===true"
        >CSV</button>
    </div>
</template>

<script setup>
import { onMounted, ref, watch } from "vue";

/************************************/

const props = defineProps([ "disableButtons" ]);
const emit  = defineEmits(["download"])

const disabled = ref();

/************************************/

watch(props, (newP, oldP) => {
  disabled.value = newP.disableButtons;
})

onMounted(() => {
  disabled.value = props.disableButtons;
})

</script>

<style scoped>
    .download-button-group {
        margin: 0 15px;
        display: flex;
        font-size: 1rem;
        justify-content: right;
        align-items: center;
        gap: 0rem;
    }
</style>
