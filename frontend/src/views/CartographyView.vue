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
                            :currentFeatureCount="currentFeatureCount"
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

// state holders
const placeIdUuid  = ref();  // when this is set, an indx of iconography resources of the place with place.id_uuid == placeIdUuid will be displayed
const displayLeft  = ref(false);  // when true, the left block (controller) will be displayed
const displayRight = ref(false);  // when true, the right block will be displayed
const loadState    = ref("loading");  // loading/loaded/error

// leaflet objects
const lflMap            = ref();  // L.Map, defined in onMounted
const lflPlaces         = ref();  // L.GeoJSON: the places geoJson as a leaflet L.geoJSON object. this object only contains features that match the user filters defined in `CartographyController`. it is this object that is actually added to the map
const lflHoverInfo      = ref();  // an L.Controller that displays info on hover
const lflFallBackBounds = ref();  // L.LatLngBounds

// data from the backend
const places               = ref({});  // the default geoJson with no filters. not modified after being fetched from the backend
const cartographyForSource = ref();  // { source: "sourceName", features: [] }
const currentFeatureCount = ref();  // number of features currently displayed on the map

// user filters defined in CartographyCOntroller
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
/** ajax stuff */

function getPlaces() {
  return Promise.all([
    axios.get(new URL("/i/cartography-main/places", __API_URL__))
    .then(r => r.data)
    .then(data => { places.value = data; })
  ])
}

const getCartographyForSource = (cartographySource) =>
  axios.get(new URL(`/i/cartography-main/cartography/${cartographySource}`, __API_URL__))
  .then(r => r.data)
  .then(data => { return { "source": cartographySource, "features": data } });


/************************************************************/
/** leaflet stuff */

/**
 * when receiving a `closePlaceInfo` event from CartographyPlaceInfo,
 * hide the `.cartography-place-wrapper` before unmounting
 * the `CartographyPlaceInfo`. the setTimeout allows to be
 * sure that `.cartography-place-wrapper` has been hidden before
 * unmounting
 */
function closeCartographyPlaceInfo() {
  displayRight.value = false;  // trigger the animation slideout of the sidebar
  lflPlaces.value.resetStyle();  // switch the opacity back to its original state
  setTimeout(() => { placeIdUuid.value = undefined }, transDur);  // remove the sidebar
}

function closeCartographyController() {
  displayLeft.value = false;
  console.log("closing");
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

  return [ _map, infoHover ];
}

/**
 * set the style for a geoJson feature, mostly setting its color based o,n
 * `feature.properties.iconography_count`.
 * @param {Object} feature: a geoJson feature
 */
const styleFeature = (feature) => {
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
}

/**
 * set events for each layer / feature of the geojson leafletGeoJson
 * @param {L.Layer} layer: the layer we're adding events to
 * @param {L.GeoJSON} leafletGeoJson: the geoJson the layer belongs to
 * @param {L.Map} _map: the leaflet map the geoJson is on.
 */
const onEachLayer = (layer, leafletGeoJson, _map) => {
  const info = lflHoverInfo.value;

  // on click, change the opacity of the layer and display a sidebar
  layer.on("click", (e) => {
    // set the data, which will trigger mounting/display of CartographyPlaceInfo
    placeIdUuid.value = undefined;
    displayRight.value = true;
    placeIdUuid.value = layer.feature.properties.id_uuid;
    // set the style: opacity of 1 on the clicked layer
    leafletGeoJson.resetStyle();  // revert the opacity for all layers
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

/**
 * add the geoJson `places` to the map `_map`
 * @param {L.Map} _map: the leaflet map
 * @param {Object} _places: the geoJson data to add to the map
 * @param {bool} init: is it the first time this function is called ?
 */
function addPlaces(_map, _places, init) {
  // define the geojson
  const leafletPlaces = L.geoJSON(_places, {
    style: styleFeature,
    pointToLayer:  (gjPoint, latLng) => L.circleMarker( latLng, { radius: 6, pane: "markerPane" })  // style is defined in the `style` function below
  });
  // add event listeners for each layer (1 layer = 1 feature in the geoJson).
  // this is equivalent to `onEachFeature` inside `L.geoJSON`, but we add the
  // event listeners here because we need to access `leafletPlaces`, and so
  // create the event listeners after `leafletPlaces` has been initialized.
  leafletPlaces.eachLayer((layer) => onEachLayer(layer, leafletPlaces, _map));

  // add to map and set the global variables
  if ( init ) { lflFallBackBounds.value = leafletPlaces.getBounds() };  // save the bounds of the full original geojson layer, in case we later add a geoJson feature with 0 layers (in which case we won't be able to compute bounds)
  leafletPlaces.addTo(_map);
  _map.fitBounds( _places.features.length
                ? leafletPlaces.getBounds()
                : lflFallBackBounds.value );
  return [ _map, leafletPlaces ];
}

/**
 * add data to the map and set the global variables
 * @param {L.Map} _map: the leaflet map
 * @param {Object} _places: the geoJson data to add to the map
 * @param {bool} init: is it the first time this function is called ?
 * @param {undefined | Object}: data to update `_cartographyForSource` with. if undefined, it won't be updated
 */
function mapSetter(_map, placesGeoJson, init, _cartographyForSource) {
  if ( _cartographyForSource != null ) {
    cartographyForSource.value = _cartographyForSource;
  }
  currentFeatureCount.value = placesGeoJson.features.length;
  [ lflMap.value, lflPlaces.value ] = addPlaces( _map, placesGeoJson, init );
}

/************************************************************/
/** handers for CartographyControllers */

//TODO see if the entire formkit form can listen to changes on its components
// to centralize definition of currentFilters.

/**
 * the 3 handle* functions update `currentFilters` with newly filtered
 * data from `CartographyController`. this will trigger the `watch(currentFilters)`
 * below to update the places geoJson and add it to the map.
 * in the `handle*` functions, the whole `currentFilters` is redefined
 * because just setting a new value for a property won't trigger the `watch()`
 */
 function handleAddress(newAddress) {
  currentFilters.value = {
    address           : newAddress,
    iconographyCount  : currentFilters.value.iconographyCount,
    cartographySource : currentFilters.value.cartographySource
  };
}
function handleIconographyCount(newIconographyCount) {
  currentFilters.value = {
    address           : currentFilters.value.address,
    iconographyCount  : newIconographyCount,
    cartographySource : currentFilters.value.cartographySource
  };
}
function handleCartographySource(newCartographySource) {
  currentFilters.value = {
    address           : currentFilters.value.address,
    iconographyCount  : currentFilters.value.iconographyCount,
    cartographySource : newCartographySource
  }
}

/************************************************************/

/**
 * when changing filters in `CartographyController`, update
 * the displayed geoJson.
 */
watch(currentFilters, async (newFilters, oldFilters) => {
  // 1) variables
  let _map                  = lflMap.value,
      placesGeoJson         = _.cloneDeep(places.value),  // without _.cloneDeep(), the modifications done to placesGeoJson below would be repercuted to `places.value`, which would break everything
      placesLeaflet         = lflPlaces.value,
      _cartographyForSource = cartographyForSource.value,
      // changeAddress           = newFilters.address !== oldFilters.address
      //changeIconographyCount  = newFilters.iconographyCount !== oldFilters.iconographyCount,
      changeCartographySource = newFilters.cartographySource !== oldFilters.cartographySource;

  /**
   * this function updates the `_places` geojson by
   * 1) only keeping features for which we can find a vector in `_cartography`.
   * 2) updating the `vector` of each feature by the matched vector in `_cartography`
   * `_cartography` is a local version of `cartographyForSource`
   */
  const updatePlacesByCartography = (_places, _cartography) => {
    let features = [];
    _places.features.map(f => {
      let v = _cartography.features.find(c =>
        c.place.length === 1
        && c.place[0].id_uuid === f.properties.id_uuid
      )?.vector
      if ( v !== undefined ) {
        f.vector = v;
        features.push(f);
      }
    })
    _places.features = features
    return _places;
  }

  // 2) define functions for each individual filter
  /**
   * only keep the features in `geoJsonObj` with an iconography_count
   * contained in the range `newFilters.iconographyCount`
   */
  const updateByIconographyCount = (geoJsonObj) => {
    // if newFilters.iconographyCount is null or has no len, this filter is not set => reset back to the original placesGeoJson
    if ( newFilters.iconographyCount != null && newFilters.iconographyCount.length ) {
      geoJsonObj.features = geoJsonObj.features.filter(f =>
        newFilters.iconographyCount[0] <= f.properties.iconography_count
        && f.properties.iconography_count <= newFilters.iconographyCount[1]);
    }
    return geoJsonObj
  }
  /**
   * only keep the features in `geoJsonObj` that have an address contained
   * within `newFilters.address`
   */
  const updateByAddress = (geoJsonObj) => {
    // console.log(newFilters.address);
    if ( newFilters.address != null && newFilters.address.length ) {
      geoJsonObj.features = geoJsonObj.features.filter(f =>
        newFilters.address.includes(f.properties.address[0].id_uuid));
    }
    return geoJsonObj;
  }
  /**
   * only keep the features in `geoJsonObj` that can be represented by
   * the source `newFilters.cartographySource` and update the vector
   * of these features to come from the source `newFilters.cartographySources`.
   * this function is different than the 2 above because it is async and requires
   * to fetch data from the backend.
   */
  const updateByCartographySource = async (geoJsonObj) => {
    console.log(`for : °${newFilters.cartographySource}°`);
    if (  newFilters.cartographySource == null
       || newFilters.cartographySource === ""
       || newFilters.cartographySource.length === 0  // string of length 0
       || newFilters.cartographySource === "default"
    ) {
      // use the default cartography source => no need to change it
      console.log("case 1")
      return [ geoJsonObj, _cartographyForSource ];
    } else if ( !changeCartographySource ) {
      // a non-default cartography source is used, but it's the same as
      // `_cartographyForSource` so no need to re-fetch it from the backend
      console.log("case 2");
      geoJsonObj = updatePlacesByCartography(geoJsonObj, _cartographyForSource);
      return [ geoJsonObj , _cartographyForSource ];
    } else {
      // a non-default cartography source is used and
      // we need to fetch it from the backend
      console.log("case 3");
      return getCartographyForSource(newFilters.cartographySource)
             .then(r => {
              _cartographyForSource = r
              geoJsonObj = updatePlacesByCartography(geoJsonObj, _cartographyForSource);
              return [ geoJsonObj, _cartographyForSource ];
            });
    }
  }

  // 3) run the process and update globals (done in an if...else because
  // all 3 `updateBy` functions are run: verifications are done within each
  // of them to check if there's a need to re-filter the data.
  updateByCartographySource(placesGeoJson)
  .then(r => {
    [ placesGeoJson, _cartographyForSource ] = r;
    console.log("°°°", placesGeoJson.features.length);
    console.log("> 1 :", placesGeoJson.features.length);
    placesGeoJson = updateByIconographyCount(placesGeoJson);
    console.log("> 2 :", placesGeoJson.features.length);
    placesGeoJson = updateByAddress(placesGeoJson);
    _map.removeLayer(placesLeaflet);

    mapSetter(_map, placesGeoJson, false, _cartographyForSource);
  });
})

/**
 * when (un)mounting `CartographyPlaceInfo`, the size of the map changes.
 * leaflet doesn't take this into account. this causes:
 * - on mount: buggy zooms
 * - on unmount: data positionned where `CartographyPlaceInfo` used to be
 *   is not displayed.
 * so, when (un)mounting, call `lflMap.invalidateSize()` to force the redraw.
 * it's supposed to be possible to use `lflMap.on(resize)` to do this,
 * but it doesn't work.
 */
watch(placeIdUuid, (newId, oldId) =>
  oldId!==undefined && newId===undefined && lflMap.value!==undefined    // unmount
  ? lflMap.value.invalidateSize()
  : oldId===undefined && newId!==undefined && lflMap.value!==undefined  // mount
  ? setTimeout(() => lflMap.value.invalidateSize(), transDur)  // the setTimeout is to wait for the transition to complete
  : ''
)

onMounted(() => {
  lflMap.value = globalDefineMap("map-main");  // synchronous
  [ lflMap.value, lflHoverInfo.value ] = addControls( lflMap.value );
  getPlaces().then(() =>
    mapSetter(lflMap.value, places.value, true, undefined) );

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