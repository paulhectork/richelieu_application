<!-- DownloadButtonGroup.vue
    A button that allows to download viewed content as JSON or CSV.
    The button receives one prop containing json data.
-->
<template>
    <div class="download-button-group">
        Téléchargement&nbsp;:&nbsp;
        <button @click="emit('download', 'json')">
            JSON
        </button>
        <button @click="$emit('download', 'csv')">
            CSV
        </button>
    </div>
</template>

<script setup>

const emit = defineEmits(["download"])
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
