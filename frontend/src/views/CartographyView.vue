<!--

     based on: https://github.com/MapunaH/code-stage

     the displaying of the right block (CartographyPlaceInfo) is
     determined by the value of `displayRight` and `placeIdUuid`.
     - `placeIdUuid` controls the creation of `CartographyPlaceInfo`
     - `displayRight` (bool) changes the CSS display to allow the
       block to be visible.
 -->

<template>
  <h1 hidden>Cartographie</h1>
  <div class="cartography-outer-wrapper"
       :class="{ 'right-visible': displayRight }"
  >
    <div class="cartography-controller-outer-wrapper"
         :class="{ 'cartography-controller-visible' : displayLeft }"
    ><CartographyController @close-cartography-controller="closeCartographyController"
                            @filter-address="handleAddress"
                            @filter-iconography-count="handleIconographyCount"
                            @filter-cartography-source="handleCartographySource"
                            :places="places"
                            v-if="displayLeft"
    ></CartographyController></div>

    <div class="cartography-wrapper">
      <div id="map-main"></div>
    </div>

    <!--<Transition name="slideInOut">-->
    <div class="cartography-place-wrapper"
         v-if="placeIdUuid !== undefined"
    >
      <CartographyPlaceInfo :placeIdUuid="placeIdUuid"
                            @close-place-info="closeCartographyPlaceInfo"
      ></CartographyPlaceInfo>
    </div>
    <!--</Transition>-->

  </div>
</template>


<script setup>
import { onMounted, ref, watch } from "vue";

import axios from "axios";
import L from "leaflet";
import $ from "jquery";
import _ from "lodash";

import CartographyPlaceInfo from "@components/CartographyPlaceInfo.vue";
import CartographyController from "@components/CartographyController.vue";

import { globalDefineMap, layerBounds } from "@utils/leaflet";
import { colorScaleBlue, colorScaleRed } from "@utils/colors";

/************************************************************/

const map          = ref();  // defined in onMounted
const places       = ref({});  // the default geoJson with no filters. not modified after being fetched from the backend
const placeIdUuid  = ref();  // when this is set, an indx of iconography resources of the place with place.id_uuid == placeIdUuid will be displayed
const displayLeft  = ref(false);  // when true, the left block (controller) will be displayed
const displayRight = ref(false);  // when true, the right block will be displayed
const loadState    = ref("loading");  // loading/loaded/error

const lflPlaces    = ref();     // the places geoJson as a leaflet L.geoJSON object. this object only contains features that match the user filters defined in `CartographyController`. it is this object that is actually added to the map
const lflHoverInfo = ref();     // an L.controller that displays info on hover

const currentFilters = ref({
  address           : [],        // Array<string>: the selected addresses. display all if empty
  iconographyCount  : [],        // Array<integer>: the min/max range of iconographies to display
  cartographySource : "default"  // string: which cartography source to use. if "default", show all that's in the `Place` database, regardless of source
});

const transDur     = 500;  // transition duration in JS
const transDurCss  = ".5s";  // transition duration in CSS

// [ [min,max], color ]
const colorClasses = [ [ [321, Infinity], colorScaleRed(0/7) ] // marina's color scale: '#000000'
                     , [ [161, 320]     , colorScaleRed(1/7) ] // marina's color scale: '#4b0082'
                     , [ [81, 160]      , colorScaleRed(2/7) ] // marina's color scale: '#800080'
                     , [ [41, 80]       , colorScaleRed(3/7) ] // marina's color scale: '#ff0000'
                     , [ [21, 40]       , colorScaleRed(4/7) ] // marina's color scale: '#ff4500'
                     , [ [11, 20]       , colorScaleRed(5/7) ] // marina's color scale: '#ff7f50'
                     , [ [6, 10]        , colorScaleRed(6/7) ] // marina's color scale: '#ffddc1'
                     , [ [0, 5]         , colorScaleRed(7/7) ] // marina's color scale: '#ffffff'
                     ];

/************************************************************/

/**
 * when receiving a `closePlaceInfo` event from CartographyPlaceInfo,
 * hide the `.cartography-place-wrapper` before unmounting
 * the `CartographyPlaceInfo`. the setTimeout allows to be
 * sure that `.cartography-place-wrapper` has been hidden before
 * unmounting
 */
function closeCartographyPlaceInfo() {
  displayRight.value = false;  // trigger the animation slideout of the sidebar
  setTimeout(() => { placeIdUuid.value = undefined }, transDur);  // remove the sidebar
}

function closeCartographyController() {
  displayLeft.value = false;
  console.log("closing");
}

function getData() {
  return Promise.all([
    axios.get(new URL("/i/cartography-main/places", __API_URL__))
    .then(r => r.data)
    .then(data => { places.value = data;
                    // lflPlaces.value = data;
     })
  ])
}

/**
 * add 3 controls:
 *    - infoHover  : a control that displays data when hovering over a geojson feature
 *    - ctrlOpener : to display the `CartographyController` component on click,
 *    - presOpener : to display the intro presentation on click.
 */
function addControls(_map) {

  const infoHover  = new L.control({ position: "topright" }),
        ctrlOpener = new L.Control({ position: "bottomleft" }),
        presOpener = new L.Control({ position: "bottomleft" });

  // create the controls and necessary methods: info listeners, update...
  infoHover.onAdd = function () {
    this._div = L.DomUtil.create("div", "infobox");
    this.update();
    return this._div;
  }
  infoHover.update = function (props) {  // when the content of infoHover changes
    this._div.innerHTML =
      `<h4>Nombre de ressources iconographiques associées&nbsp:</h4>
      ${props && props.iconography_count
        ? props.iconography_count
        : "Passer la souris au dessus d'une parcelle"}`;
  }
  ctrlOpener.onAdd = function () {
    this._div = L.DomUtil.create("div", "custom-controller");
    this._div.innerHTML = // pure html, contains the equivalent of `@components/UiButtonFilter.vue`
      `<button>
        <svg width="80%"
             height="80%"
             viewBox="-2 -2 27 27"
             fill="none"
             xmlns="http://www.w3.org/2000/svg"
             aria-label="Filtrer les données. En cliquant ce bouton, il sera possible de cliquer les données. Le dessin vectoriel représente un filtre."
        >
          <title>Filtrer les données></title>
          <desc>En cliquant ce bouton, il sera possible de cliquer les données.
            Le dessin vectoriel représente un filtre.</desc>
          <path fill-rule="evenodd"
                clip-rule="evenodd"
                d="M15 10.5A3.502 3.502 0 0 0 18.355 8H21a1 1 0 1 0 0-2h-2.645a3.502 3.502 0 0 0-6.71 0H3a1 1 0 0 0 0 2h8.645A3.502 3.502 0 0 0 15 10.5zM3 16a1 1 0 1 0 0 2h2.145a3.502 3.502 0 0 0 6.71 0H21a1 1 0 1 0 0-2h-9.145a3.502 3.502 0 0 0-6.71 0H3z"
                fill="#000000"
          />
        </svg>
      </button>`;
    L.DomEvent.on(this._div, "click", () => { displayLeft.value = true }, this);
    return this._div;
  }
  presOpener.onAdd = function () {
    this._div = L.DomUtil.create("div", "custom-controller");
    this._div.innerHTML = `<button>pres</button>`;
    return this._div
  }

  // when removing the elements, remove the event listeners
  ctrlOpener.onRemove = function() {
    L.DomEvent.off(this._div, "click", context=this); }
  presOpener.onRemove = function() {
    L.DomEvent.off(this._div, "click", context=this); }

  ctrlOpener.addTo(_map);
  presOpener.addTo(_map);
  infoHover.addTo(_map);

  return[ _map, infoHover ];
}

/**
 * add the places as a geoJson to the map
 */
function addPlaces(_map, _places) {
  const info = lflHoverInfo.value;

  const leafletPlaces = L.geoJSON(_places, {
    pointToLayer:  (gjPoint, latLng) =>
      L.circleMarker(latLng, { radius: 6, pane: "markerPane" }),  // style is defined in the `style` function below
    style: (feature) => {
      // set color based on iconography count
      const iconographyCount = feature.properties.iconography_count,
            comparator = (range, num) => range[0] <= num && num <= range[1];
      return {
        fillColor: colorClasses.find( (c) => comparator(c[0], iconographyCount) )[1],  // if iconographyCount is in a range defined in `colorClasses`, select the color
        fillOpacity: feature.geometry.type === "Point"
                     ? 1
                     : 0.5,
        color: "black",
        weight: 1
      }
    },

    onEachFeature: (feature, layer) => {
      // on click, change the opacity of the layer and display a sidebar
      layer.on("click", (e) => {
        // set the data, which will trigger mounting/display of CartographyPlaceInfo
        placeIdUuid.value = undefined;
        displayRight.value = true;
        placeIdUuid.value = feature.properties.id_uuid;
        // set the style: opacity of 1 on the clicked layer
        leafletPlaces.resetStyle();  // revert the opacity for all layers
        layer.setStyle({ fillOpacity:1 });
        // zoom to the clicked layer
        //TODO fix yank here ?
        setTimeout(() => _map.fitBounds(layerBounds(layer)), transDur);  // wait for the size animation to complete...
      });

      // on hover, change the color and weight of the border
      layer.on("mouseover", (e) => {
        layer.setStyle({ color: layer.options.fillColor, weight: 3 })
        info.update(layer.feature.properties);
      });
      layer.on("mouseout", (e) => {
        layer.setStyle({ color: "black", weight: 1 });
        info.update();
      })
    }
  });
  leafletPlaces.addTo(_map);
  _map.fitBounds(leafletPlaces.getBounds());
  return [ _map, leafletPlaces ];
}


/**
 * the 3 handle* functions update `currentFilters` with newly filtered
 * data from `CartographyController`. this will trigger the `watch(currentFilters)`
 * below to update the places geoJson and add it to the map.
 * in the `handle*` functions, the whole `currentFilters` is redefined
 * because just setting a new value for a property won't trigger the `watch()`
 */
 function handleAddress(newAddress) {
  currentFilters.value = {
    address: newAddress,
    iconographyCount: currentFilters.value.iconographyCount,
    cartographySource: currentFilters.value.cartographySource
  };
}

/**
 * handle an iconography count filter change in `CartographyController`
 */
function handleIconographyCount(newIconographyCount) {
  currentFilters.value = {
    address: currentFilters.value.address,
    iconographyCount: newIconographyCount,
    cartographySource: currentFilters.value.cartographySource
  };
}

/**
 * handle a cartography source change in `CartographyController`
 */
function handleCartographySource() {
  console.log(3)
}

/************************************************************/

/**
 * when changing filters in `CartographyController`, update
 * the displayed geoJson.
 */
watch(currentFilters, (newFilters, oldFilters) => {
  // 1) variables
  let _map          = map.value,
      placesGeoJson = _.cloneDeep(places.value),  // without _.cloneDeep(), the modifications done to placesGeoJson below would be repercuted to `places.value`, which would break everything
      placesLeaflet = lflPlaces.value,
      changeAddress           = newFilters.address !== oldFilters.address,
      changeIconographyCount  = newFilters.iconographyCount !== oldFilters.iconographyCount,
      changeCartographySource = newFilters.cartographySource !== oldFilters.cartographySource;

  // 2) define functions for each individual filter
  const updateByIconographyCount = (geoJsonObj) => {
    if ( newFilters.iconographyCount != null    // if newFilters.iconographyCount is null or has no len, this filter is not set => reset back to the original placesGeoJson
         && newFilters.iconographyCount.length
    ) {
      geoJsonObj.features = geoJsonObj.features.filter(f =>
      newFilters.iconographyCount[0] <= f.properties.iconography_count
      && f.properties.iconography_count <= newFilters.iconographyCount[1]);
    }
    return geoJsonObj
  }
  const updateByAddress = (geoJsonObj) => {
    console.log(newFilters.address);
    if ( newFilters.address != null && newFilters.address.length ) {
      geoJsonObj.features = geoJsonObj.features.filter(f =>
        newFilters.address.includes(f.properties.address[0].id_uuid));
    }
    return geoJsonObj;
  }

  console.log(0, placesGeoJson.features.length);

  // 3) pass placesGeoJson through all the filters
  //TODO find a way to combine the different filters
  if ( changeIconographyCount ) {
    placesGeoJson = updateByIconographyCount(placesGeoJson);
    console.log(1, placesGeoJson.features.length);
  }
  if ( changeAddress ) {
    placesGeoJson = updateByAddress(placesGeoJson);
    console.log(2, placesGeoJson.features.length);
  }

  // 4) update the map
  _map.removeLayer(placesLeaflet);
  [ map.value, lflPlaces.value ] = addPlaces( _map, placesGeoJson );
})

/**
 * when (un)mounting `CartographyPlaceInfo`, the size of the map changes.
 * leaflet doesn't take this into account. this causes:
 * - on mount: buggy zooms
 * - on unmount: data positionned where `CartographyPlaceInfo` used to be
 *   is not displayed.
 * so, when (un)mounting, call `map.invalidateSize()` to force the redraw.
 * it's supposed to be possible to use `map.on(resize)` to do this,
 * but it doesn't work.
 */
watch(placeIdUuid, (newId, oldId) =>
  oldId !== undefined && newId === undefined && map.value != undefined    // unmount
  ? map.value.invalidateSize()
  : oldId === undefined && newId !== undefined && map.value != undefined  // mount
  ? setTimeout(() => map.value.invalidateSize(), transDur)  // the setTimeout is to wait for the transition to complete
  : ''
)

onMounted(() => {
  map.value = globalDefineMap("map-main");  // synchronous
  [ map.value, lflHoverInfo.value ] = addControls(map.value);
  getData().then(() => {
    [ map.value, lflPlaces.value ] = addPlaces( map.value, places.value ) });
})
</script>


<style scoped>
.cartography-outer-wrapper {
  height: 100%;
  width: 100%;

  display: grid;
  grid-template-columns: 30% 100% 30%;

  transform: translateX(-30%);
  transition: grid-template-columns v-bind("transDurCss");
}
.cartography-outer-wrapper.right-visible {
  grid-template-columns: 30% 70% 30%;
}
.cartography-place-wrapper {
  z-index: 400;
  height: 100%;
  width: 100%;
}

/**************************************/

#map-main {
  height: 100%;
  width: 100%;
}
#map-main :deep(.infobox) {
  padding: 6px 8px;
  color: black;
  font-family: var(--cs-font-sans-serif);
  background-color: var(--cs-main-default-bg);
  border: var(--cs-main-border);
  box-shadow: 0 0 15px rgba(0,0,0,0.2);
  z-index: 999;
}
#map-main :deep(.leaflet-control) {
  border-radius: 0;
  border: var(--cs-main-border);
}
#map-main :deep(.infobox h4) {
  margin: 0;
  font-family: var(--cs-font-serif);
  font-variant-caps: small-caps;
  color: #777;
  font-size: 120%;
}
#map-main :deep(.leaflet-bottom.leaflet-left) {
  display: flex;
  flex-direction: row;
}
#map-main :deep(.leaflet-bottom.leaflet-left .leaflet-control) {
  border: none;
}
#map-main :deep(.leaflet-bottom.leaflet-left button) {
  height: max(4vh, 50px);
  width: max(4vh, 50px) ;
}

/**************************************/

.cartography-controller-outer-wrapper {
  z-index: 1001;
  background-color: var(--cs-main-default-bg);
  color: var(--cs-main-default);
  border-right: var(--cs-main-border);
}
.cartography-controller-visible {
  transform: translateX(100%);
  height: 100%;
  width: 100%;
}

</style>