<!-- MapPlaceMain.vue
     a cartographic interface for places, displayed on a place's main page.

     props:
     * place: the place, containing all necessary data
-->

<template>
<div class="mpm-wrapper">
  <div class="mpm-left-wrapper">
    <div class="mpm-map-wrapper">
      <div id="mpm-map"></div>
    </div>
    <div v-if="currentAddress"
         class="mpm-address-wrapper"
    >
      <!--
        Adresse (<span class="source-desc"
                       v-html="cartographySourceMapper[currentAddress.source]"
        ></span>)&nbsp;: {{currentAddress.address}}
      -->
      <span class="mpm-address-cartel">
        <span class="source-intro">Adresse</span> <br/>
        <span class="source-desc"
               v-html="cartographySourceMapper[currentAddress.source]"
        ></span>
      </span>
      <span v-html="currentAddress.address"
            class="source-address"
      ></span>
    </div>
  </div>
  <div class="mpm-right-wrapper">
    <span>Fonds cartographiques représentant la parcelle</span>
    <ul class="mpm-address-switch list-invisible"
    >
      <li v-for="c in sortedCartography">
        <button v-html="cartographySourceMapper[c.map_source]"
                :class="c.map_source === source ? 'button-activated' : ''"
                :value="c.map_source"
                @click="sourceHook($event.target.value)"
        ></button>
      </li>
    </ul>
  </div>
</div>

</template>


<script setup>
import { onMounted, ref, computed } from "vue";

import L from "leaflet";
import $ from "jquery";

import { globalDefineMap
       , lflDefaultMarker
       , lflDefaultStyle
       , lflDefaultMouseOver
       , lflDefaultMouseOut } from "@utils/leaflet.js";
import { cartographySourceMapper, cartographySourcePriority } from "@globals";
import { sortCartographyBySource, sortAddressBySource } from "@utils/array.js";
import { urlToCartographyFile } from "@utils/url.js";

/************************************************************/

const props  = defineProps(["place"]);
const place  = props.place;
const map    = ref();  // defined in onMounted()
const source = ref();
const currentAddress = ref();
// const currentCartography = ref();
const sortedCartography = sortCartographyBySource(place.cartography);
const sortedAddress     = sortAddressBySource(place.address);

/************************************************************/

/**
 * select the current address object to be displayed.
 * value changes in `onMounted` and when clicking one of the
 * `mpm-address-switch > li > button` objects
 *
 * the address is matched in 3 steps:
 * 1) try to get an address matching the newly selected `source`
 * 2) if that fails, get the first address in `sortedAddress`.
 * 4) if really nothing works, return undefined
 *
 * @param {String} _source: the newly defined source
 * @returns {undefined | Object}: the address if it's been found, undefined otherwise
 */
function getCurrentAddress(_source) {
  let matchedAddr = undefined;
  if ( _source != null && place != null ) {
    // 1)
    matchedAddr = place.address.find(a => a.source===_source);
    return matchedAddr !== undefined
           ? matchedAddr       // 1)
           : sortedAddress[0]  // 2)
  }
  return undefined             // 3)
}

/**
 * display contents on the map according to the newly selected source
 */
function updateMap(_map, _source, _currentCartography) {
  // define the new vector (GeoJSON) and raster layers (ImageOverlay)
  let vector, raster;
  vector = L.geoJSON(_currentCartography.vector, {
    style: lflDefaultStyle, //{ className: "place-gj" },
    className: "to-remove",
    pointToLayer: (gjPoint, latLng) => lflDefaultMarker(latLng),
    onEachFeature: (feature, layer) => {
      layer.toRemove = true;  // flag to make sure that the layer will be removed
      layer.on({
        // interactive style
        mouseover: (e) => lflDefaultMouseOver(layer),
        mouseout : (e) => lflDefaultMouseOut(layer),
      })
    }
  });
  if ( _currentCartography.filename.length ) {
    raster = L.imageOverlay(
      urlToCartographyFile(_currentCartography.filename[0].url),
      _currentCartography.filename[0].latlngbounds,
      {
        alt: `Image montrant la parcelle sur le fond de carte: ${cartographySourceMapper[_currentCartography.map_source]}`,
        className: "to-remove"  // this class will be used to make sure to delete the layer
      });
  }

  // remove the previous geojson+raster layers
  _map.eachLayer((layer) =>
    layer.toRemove || layer.options.className === "to-remove"
    ? _map.removeLayer(layer)
    : false )

  // append the new vector + raster layer
  if ( raster ) { raster.addTo(_map) };
  vector.addTo(_map);
  _map.fitBounds(vector.getBounds());

  return _map
}

/**
 * complete hook of events for when we set a new source to be displayed:
 * - update the ref `source` with the newly selected source
 * - update the `currentAddress` ref
 * - change the map's contents
 * @param {String} _source: the new `source`, as a string
 */
function sourceHook(_source) {
  if ( _source != source.value ) {
    source.value = _source;
    currentAddress.value = getCurrentAddress(source.value);
    //TODO: SOMETIMES, THERE'S A PROBLEM HERE (HARD TO REPRODUCE).
    // POSSIBLY LINKED TO LIFECYCLE ISSUES ?
    // OR THE `$event.target.value` is something other than the `button`?
    let currentCartography = place.cartography.find(c => c.map_source === source.value);
    map.value = updateMap(map.value, source.value, currentCartography);
  }
}

/************************************************************/

onMounted(() => {
  map.value = globalDefineMap("mpm-map")[0];
  let _source = sortCartographyBySource(props.place.cartography)[0].map_source
  sourceHook(_source);
})
</script>


<style scoped>
/**
 * global css styling:
 * - in landscape mode, `.mpm-wrapper`
 *   has a display:grid with 2 horizontal columns,
 *   `mpm-left-wrapper` and `mpm-right-wrapper`.
 * - in portrait mode, `.mpm-wrapper` has
 *   a `display:flex` with `flex-direction:column-reverse`:
 *   `mpm-right-wrapper` is on top of `mpm-left-wrapper`
 */
.mpm-wrapper {
  height: 100%;
  /*display: grid;
  grid-template-rows: 100%;
  grid-template-columns: 70% 30%;
  border: var(--cs-main-border);
  */
  display: flex;
  flex-direction: column-reverse;
  width: 100%;
  border: var(--cs-main-border);
}

@media ( orientation:landscape ) {
  .mpm-wrapper {
    display: grid;
    grid-template-rows: 100%;
    grid-template-columns: 70% 30%;
  }
}

.negative-default .mpm-wrapper {
  border: var(--cs-negative-border);
}

/***********************************************/

.mpm-left-wrapper {
  display: grid;
  grid-template-columns: 100%;
  grid-template-rows: 2fr auto;
  border-right: var(--cs-main-border);
  height: 100%;
}
#mpm-map {
  height: 100%;
  width: 100%;
  border-bottom: var(--cs-main-border);
  border-top: var(--cs-main-border);
}
.mpm-address-wrapper {
  padding: 5px;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
}
.source-intro {
  text-decoration: underline;
}
.source-desc {
  font-style: italic;
}
.source-address {
  font-weight: bold;
}

.negative-default .mpm-left-wrapper {
  border-right: var(--cs-negative-border);
}
.negative-default #mpm-map {
  border-bottom: var(--cs-negative-border);
  border-top: var(--cs-negative-border);
}
@media ( orientation:landscape ) {
  #mpm-map, .negative-default #mpm-map {
    border-top: none;
  }
}

/***********************************************/

.mpm-right-wrapper {
  display: grid;
  grid-template-rows: auto 2fr;
  max-height: 100%;
  margin: 5px;
}
.mpm-right-wrapper > *:first-child {
  margin: 5px;
}
.mpm-address-switch {
  display: flex;
  height: 100%;
  flex-direction: row;
}
@media ( orientation: landscape ) {
  .mpm-address-switch {
    flex-direction: column;
  }
}
.mpm-address-switch > li {
  flex: 1 1 0px;
  margin: 0 3px 3px 0;
}
.mpm-address-switch button {
  height: 100%;
  width: 100%;
}
</style>