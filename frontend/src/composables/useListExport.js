import {toValue, toRaw, computed, watchEffect} from "vue";

/**
 * @typedef {Object} DataExport
 * @prop {string} json
 * @prop {string} csv
 */

/**
 * @template {T}
 * @param {Array<T>} data
 * @param { {toJSON?: (item: T) => unknown; toCSV?: (item: T) => Record<string, string | number | null>} }
 * @param {Array<string>} selection Filtered list of uuids to export.
 * @return {DataExport}
 */
export function useListExport(data, selection, {toJSON, toCSV}) {
  const idToJSON = computed(() =>
    toJSON
      ? Object.fromEntries(toValue(data).map(item => [item.id_uuid, toJSON(item)]))
      : null
  );

  const idToCSV = computed(() =>
    toCSV
      ? Object.fromEntries(toValue(data).map(item => [item.id_uuid, toCSV(item)]))
      : null
  );

  const jsonExport = computed(() => idToJSON.value ? toValue(selection).map((item) => idToJSON.value[item]) : null)
  const csvExport = computed(() => idToJSON.value ? toValue(selection).map((item) => idToCSV.value[item]) : null)

  return {
    json: jsonExport,
    csv: csvExport
  }
}
