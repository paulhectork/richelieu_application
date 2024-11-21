<!-- DownloadButtonGroup.vue
    A button that allows to download viewed content as JSON or CSV.
    The button receives one prop containing json data.
-->
<template>
    <div class="download-button-group">
        Téléchargement&nbsp;:&nbsp;
        <button @click="() => downloadJSON()">
            JSON
        </button>
        <button @click="() => downloadCSV()">
            CSV
        </button>
    </div>
</template>

<script setup>
import { toValue, watchEffect}  from "vue";
import { stringify } from "csv-stringify/browser/esm/sync"

const props = defineProps(["data", "filename"]);

function downloadJSON() {
    download(new Blob([JSON.stringify(toValue(props.data.json), 0, 4)], { type: "application/json" }), `${toValue(props.filename)}.json`);
}

function downloadCSV() {
    const output = stringify(toValue(props.data.csv), {header: true});
    download(new Blob([output], { type: "text/csv"}), `${toValue(props.filename)}.csv`);
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
