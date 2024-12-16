/**
 * module to export data. `downloadData` is called by components with
 * formatted data, structures it to JSON|CSV, and triggers a client download
 * of the file
 */

import { stringify } from "csv-stringify/browser/esm/sync"

export function download(blob, fileName) {
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.setAttribute("href", url);
    link.setAttribute("download", fileName);
    link.click()
}

export function toJsonBlob(data) {
    return new Blob([JSON.stringify(data, 0, 4)], { type: "application/json" });
}

export function toCsvBlob(data) {
    const output = stringify(data, {header: true});
    return new Blob([output], { type: "text/csv"});
}

function toBlob(data, fileType) {
  if (fileType === "csv") {
    return toCsvBlob(data);
  } else if (fileType === "json") {
    return toJsonBlob(data)
  } else {
    throw new Error(`Unsupported file type '${fileType}'`)
  }
}

export function downloadData(data, fileType, fileName) {
  const blob = toBlob(data, fileType);
  download(blob, `${fileName}.${fileType}`)
}
