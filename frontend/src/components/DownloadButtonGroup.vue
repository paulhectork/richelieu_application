<!-- DownloadButtonGroup.vue
    A button that allows to download viewed content as JSON or CSV.
    The button receives one prop containing json data.
-->
<template>
    <div class="download-button-group">
        Téléchargement&nbsp;:&nbsp;
        <button @click="() => downloadJSON(data.json, filename)">
            JSON
        </button>
        <button @click="() => downloadCSV(data.csv, filename)">
            CSV
        </button>
    </div>
</template>

<script setup>
import { defineProps } from "vue";
import { stringify } from "csv-stringify/browser/esm/sync"
defineProps(["data", "filename"]);

function downloadJSON(data, filename) {
    download(new Blob([JSON.stringify(data, 0, 4)], { type: "application/json" }), `${filename}.json`);
}

function downloadCSV(data, filename) {
    const output = stringify(data, {header: true});
    download(new Blob([output], { type: "text/csv"}), `${filename}.csv`);
}

function download(data, filename) {
    const url = URL.createObjectURL(data);
    const link = document.createElement("a");
    link.setAttribute("href", url);
    link.setAttribute("download", filename);
    link.click()

}

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
