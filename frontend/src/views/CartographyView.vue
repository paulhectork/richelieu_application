<!-- CartographyController.vue
     an cartographic interface to explore spatial
     (Places & Cartography tables) and image data (Iconography table).
     based on Marina Hervieu's prototype : https://github.com/MapunaH/code-stage

     page structure:
     * left : CartographyController
        a controller that contains a form that allows to filter
        which places are displayed.
        - its display is controller by `displayLeft`
     * center : this component
     * right : CartographyPlaceInfo
        a block that is displayed when a plot is clicked and shows
        (mostly) the iconography related to it
        - its display depends on `displayRight` and `placeIdUuid`.
           - `placeIdUuid` controls the creation of `CartographyPlaceInfo`
           - `displayRight` (bool) changes the CSS display to allow the
             block to be visible.
     * modal :
        an explanatory modal displayed when opening the map,
        or when clicking on UiButtonQuestion
        - is display is controlled by domStore.cartogrphyModalVisible
          (the advantage of using a store instead of a `ref` is that state
          handling will be done at app level instead of at view level: once
          the modal is closed it won't be displayed until doing a hard reload
          on the whole app)

     lifecycle for updating the map's data:
     * onMounted:
        - the map is defined
        - controllers are added
        - the places geoJSON is fetched from the backend.
          it is stored in 2 refs:
          - `places`, a geoJSON which is never changed after being created,
            stores the initial state of the map.
          - `placesFilter` is a geoJSON that can be modified according to
            user filters. it's this element that's added to the leaflet map.
            onMounted, `placesFilter` is a copy of `places`.
        - `placesFilter` is added to the map as an L.GeoJSON
     * on emit of CartographyController.filterUpdate:
        - `placesFilter` is redefined by filtering `places` using
            the user defined filters, and by fetching/updating its
            geometries from the backend
        - the old leaflet geoJSON is removed from the map.
        - `placesFilter` is added to the map as a geoJSON.

-->

<template>
  <h1 hidden>Cartographie</h1>
  <div class="cartography-outer-wrapper"
       :class="{ 'right-visible': displayRight }"
  >
    <div class="cartography-controller-outer-wrapper"
        :class="{ 'cartography-controller-visible': displayLeft }"
    >
      <CartographyController @close-cartography-controller="closeCartographyController"
                             @filter-update="onFilterUpdate"
                             :places="places"
                             :currentFeatureCount="currentFeatureCount"
                             v-if="placesFilter !== undefined
                                   && Object.keys(placesFilter).length
                                   && places !== undefined
                                   && Object.keys(places).length"
      ></CartographyController>
    </div>

    <div class="cartography-wrapper">
      <div id="map-main"></div>
    </div>

    <!--<Transition name="slideInOut">-->
    <div class="cartography-place-wrapper" v-if="placeIdUuid !== undefined">
      <CartographyPlaceInfo :place-id-uuid="placeIdUuid"
                            :associated-places="currentAssociatedPlaces"
                            @close-place-info="closeCartographyPlaceInfo">
      </CartographyPlaceInfo>
    </div>

    <div class="c-modal-container">
      <Transition name="slideInOut">
        <CartographyModal v-if="domStore.cartographyModalVisible/*displayModal === true*/"
                          @close-cartography-modal="onCloseCartographyModal"
        ></CartographyModal>
      </Transition>
    </div>

  </div>
</template>


<script setup>
import { onMounted, ref, watch, h } from "vue";

import axios from "axios";
import L from "leaflet";
import $ from "jquery";
import _ from "lodash";

import CartographyModal from "@components/CartographyModal.vue";
import CartographyPlaceInfo from "@components/CartographyPlaceInfo.vue";
import CartographyController from "@components/CartographyController.vue";

import { domStore } from "@stores/dom.js";
import { uiButtonPlus, uiButtonFilter, uiButtonQuestion } from "@utils/ui";
import { colorScaleBlue, colorScaleRed } from "@utils/colors";
import { globalDefineMap
       , layerBounds
       , lflDefaultMarker
       , getLayerByName
       , mapCenter } from "@utils/leaflet";

/************************************************************/

// state holders
const placeIdUuid = ref();  // when this is set, an indx of iconography resources of the place with place.id_uuid == placeIdUuid will be displayed
const displayLeft = ref(false);  // when true, the left block (controller) will be displayed
const displayRight = ref(false);  // when true, the right block will be displayed

const currentlyFiltering = ref(false);      // flag to ensure that one `onFilterUpdate` is finished before a new one is started
const loadState = ref("loading");  // loading/loaded/error

// finally handled by `domStore.cartographyModalVisible`
// const displayModal = ref(true);  // when true, display an explanatory modal

// leaflet objects
const lflMap = ref();  // L.Map, defined in onMounted
const lflPlaces = ref();  // L.GeoJSON: the places geoJson as a leaflet L.geoJSON object. this object only contains features that match the user filters defined in `CartographyController`. it is this object that is actually added to the map
const lflInfoHover = ref();  // an L.Controller that displays info on hover
const lflLayerControl = ref();  // L.Control.Layers: used to programatically change background layers
const lflFallBackBounds = ref();  // L.LatLngBounds

// data from the backend
const places                    = ref({});  // the default geoJson describing places, with no filters. not modified after being fetched from the backend
const placesFilter              = ref({});  // the geoJson describing places, with filters
const cartographyForSource      = ref();    // { source: "sourceName", features: [] }. `features` contains all rows of the `Cartography` table with the same "sourceName"
const cartographyForGranularity = ref();    // { granularity: "granularityName", features: [] }. `features` contains all rows of the `Cartography` table with the same "granularityName"
const currentFeatureCount       = ref();    // number of features currently displayed on the map
const currentAssociatedPlaces   = ref();    // a list of the 5 places most frequently associated with the currently clicked on place (targeted by `placeIdUuid`)

// css
const transDur = 500;  // transition duration in JS
const transDurCss = ".5s";  // transition duration in CSS

// [ [min,max], color ]
const colorClasses = [ [[321, Infinity], colorScaleRed(0 / 7)] // marina's color scale: '#000000'
                     , [[161, 320], colorScaleRed(1 / 7)] // marina's color scale: '#4b0082'
                     , [[81, 160], colorScaleRed(2 / 7)] // marina's color scale: '#800080'
                     , [[41, 80], colorScaleRed(3 / 7)] // marina's color scale: '#ff0000'
                     , [[21, 40], colorScaleRed(4 / 7)] // marina's color scale: '#ff4500'
                     , [[11, 20], colorScaleRed(5 / 7)] // marina's color scale: '#ff7f50'
                     , [[6, 10], colorScaleRed(6 / 7)] // marina's color scale: '#ffddc1'
                     , [[0, 5], colorScaleRed(7 / 7)] // marina's color scale: '#ffffff'
                     ];

/************************************************************/
/** ajax stuff */

/**
 * fetch the Place table as a geoJson from the backend.
 * only used in `onMounted()`, after creating the map.
 */
function getInitPlaces() {
  return Promise.all([
    axios.get(new URL("/i/cartography-main/places", __API_URL__))
      .then(r => r.data)
      .then(data => {
        places.value = data;
        placesFilter.value = data;  // by default, no filters are applied
        currentFeatureCount.value = data.features.length;
      })
  ])
}

const getCartographyForSource = (cartographySource) =>
  axios.get(new URL(`/i/cartography-main/cartography/source/${cartographySource}`, __API_URL__))
    .then(r => r.data)
    .then(data => { return { "source": cartographySource, "features": data } });

const getCartographyForGranularity = (cartographyGranularity) =>
  axios.get(new URL(`/i/cartography-main/cartography/granularity/${cartographyGranularity}`, __API_URL__))
    .then(r => r.data)
    .then(data => { return { "granularity": cartographyGranularity, "features": data } });


/************************************************************/
/** DOM manipulation / emit handlers */

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
  setTimeout(() => {              // reset data + remove the sidebar
    placeIdUuid.value = undefined;
    currentAssociatedPlaces.value = [];
  }, transDur);
}

function closeCartographyController() {
  displayLeft.value = false;
}

function onCloseCartographyModal() {
  // displayModal.value = false;
  domStore.cartographyModalVisible = false;
  // zoom on the map when closing the modal.
  // if we have a map and geoJson bounds to zoom to, zoom to the geojson map
  // else, zoom to the default map center.
  if ( lflFallBackBounds.value ) {
    lflMap.value?.flyToBounds(lflFallBackBounds.value, { duration: .5 });
  } else {
    lflMap.value?.flyTo(mapCenter, 15.5, { duration: .5 })
  }
}


/************************************************************/
/** leaflet stuff */

/**
 * a function to disable drag on a control
 *
 * @param {L.Control} control: the leaflet control to modify
 * @param {L.Map} _map: the leaflet map
 */
const handleDragOnControl = (control, _map) => {
  control.getContainer().addEventListener("mouseover", () =>
    _map.dragging.disable() );
  control.getContainer().addEventListener("mouseout", () =>
    _map.dragging.enable() );
}

/**
 * all `add...Control(_map)` functions below add individual functions
 * to the leaflet map `_map`. they are called through `addControls()`,
 * which updates `_map` with new controls and then sets global variables
 * created here. all `add...Control` functions return only the
 * updated `_map`, except `addInfoHoverControl`, which also returns
 * the created control (it needs to be updated globally)
 * @param {L.Map} _map: the leaflet map to add controls to
 * @returns {L.Map}
 */

 /**
  * this button changes the opacity of the places geojson
  *
  * to change the opacity, the global lflPlaces is accessed,
  * which i don't like because all other functions only use local values
  * and global are passed as arguments by `addControls()`, and it's best
  * to avoid mixing local and global scopes.
  * however, the global lflPlaces needs to be accessed
  * here to change the style of the current places geojson layer.
  * since this layer is reactive and may be changed at any time, it's not
  * possible to pass it as an argument (this function is called on map init,
  * but opacity will have to change future versions of the map).
  */
function addOpacityControl(_map) {
  const opacityCtrl = new L.Control({ position: "topright" });

  // create the controls and necessary methods: info listeners, update...
  opacityCtrl.onAdd = function () {
    this._div = L.DomUtil.create("div", "infobox");
    this._div.innerHTML = `
      <h4>Modifier l'opacité (<span id="opacity-to-modif">50%</span>)</h4>
      <div><input type="range"
                  id="opacity-slider"
                  min="0"
                  max="1"
                  step="0.01"
                  value="0.5"
      ></input></div>`;
    return this._div;
  };

  opacityCtrl.addTo(_map);
  handleDragOnControl(opacityCtrl, _map);

  // add event listening through jquery: change the opacity of the geoJsons
  $("#opacity-slider").on("input", (e) => {
    let v = e.target.value;
    $("#opacity-to-modif").html(`${ Math.round(v * 100) }%`);
    if ( lflPlaces.value ) {
      lflPlaces.value.setStyle({ fillOpacity: v });
    }
  })

  return _map;
}

function addColorControl(_map) {
  const colorCtrl = new L.Control({ position: "topright" });

  // this function creates a single row of the html table contained by colorCtrl
  const colorCtrlRow = (colorClass) =>
    "<tr>"
    + `<td style="background-color: ${colorClass[1]}"></td>`
    + (colorClass[0][1] === Infinity
      ? `<td>Plus de ${colorClass[0][0]} ressources</td>`
      : `<td>Entre ${colorClass[0][0]} et ${colorClass[0][1]} ressources</td>`)
    + "</tr>";

  // create the control and add it to the map
  colorCtrl.onAdd = function () {
    this._div = L.DomUtil.create("div", "infobox color-legend");
    this._div.innerHTML = `
      <div class="top-wrapper">
        <h4>Légende</h4>
        <span class="btn-container">${uiButtonPlus}</span>
      </div>
      <table style="display: none">
        ${colorClasses.map(colorCtrlRow).join("")}
      </table>`;  // join.("") turns the  array of strings into a single string
    this._div.innerHTML += `</table>`;
    // effects for this one are fancier and will be done in jQuery after `colorCtrl.addTo(map)`
    return this._div;
  }

  colorCtrl.addTo(_map);
  handleDragOnControl(colorCtrl, _map);

  // for `colorCtrl`, the event listening is a bit complex, so
  // we do it in jQuery. this demands to wait for colorCtrl.addTo(_map).
  let $button = $(".color-legend .btn-container > button"),
    $table = $(".color-legend table");
  $button.on("click", () => {
    let open = $table.css("display");
    $table.css({ display: open === "none" ? "block" : "none" });
    $button.html(open === "none"
      ? $button.find("svg").addClass("rotated")
      : $button.find("svg").removeClass("rotated")
    );
  });

  return _map;
}

function addFilterOpenerControl(_map) {
  const filterOpener = new L.Control({ position: "bottomleft" });

  filterOpener.onAdd = function () {
    this._div = L.DomUtil.create("div", "custom-controller");
    this._div.innerHTML = uiButtonFilter; // pure html, contains the equivalent of `@components/UiButtonFilter.vue`
    L.DomEvent.on(this._div, "click", () => { displayLeft.value = true }, this);
    return this._div;
  }
  filterOpener.onRemove = function () {
    L.DomEvent.off(this._div, "click", context = this);
  }

  filterOpener.addTo(_map);
  handleDragOnControl(filterOpener, _map);
  return _map;
}

function addPresOpenerControl(_map) {
  const presOpener = new L.Control({ position: "bottomleft" });
  presOpener.onAdd = function () {
    this._div = L.DomUtil.create("div", "custom-controller");
    this._div.innerHTML = uiButtonQuestion;
    L.DomEvent.on(this._div, "click", () => {
      /*displayModal.value = true*/
      domStore.cartographyModalVisible = true;
    }, this);
    return this._div
  }
  presOpener.onRemove = function () {
    L.DomEvent.off(this._div, "click", context = this);
  }

  presOpener.addTo(_map);
  handleDragOnControl(presOpener, _map);
  return _map;
}

/**
 * @returns {Array<L.Map, L.Control>}: the control is also returned by this function
 */
function addInfoHoverControl(_map) {
  const infoHover = new L.control({ position: "topright" });

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

  infoHover.addTo(_map);
  handleDragOnControl(infoHover, _map);
  return [_map, infoHover];
}

/**
 * add 5 controls:
 *    - addInfoHoverControl    : a control that displays data when hovering over a geojson feature
 *    - acurrentLayerddColorControl        : a legend for the colors
 *    - addFilterOpenerControl : to display the `CartographyController` component on click,
 *    - addPresOpenerControl   : to display the intro presentation on click.
 *    - addOpacityControl      : a controller that allows to change the opacity of the geoJson.
 */
function addControls() {
  let _map = lflMap.value,
      infoHover;

  [_map, infoHover] = addInfoHoverControl(_map);
  _map = addColorControl(_map);
  _map = addFilterOpenerControl(_map);
  _map = addOpacityControl(_map);
  _map = addPresOpenerControl(_map);

  lflInfoHover.value = infoHover;
  return;
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
    fillColor: colorClasses.find((c) => comparator(c[0], iconographyCount))[1],  // if iconographyCount is in a range defined in `colorClasses`, select the color
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
const onEachLayer = (layer, leafletGeoJson) => {
  const info = lflInfoHover.value,
    _map = lflMap.value;

  // on click, change the opacity of the layer and display a sidebar
  layer.on("click", (e) => {
    // set the data, which will trigger mounting/display of CartographyPlaceInfo
    placeIdUuid.value = undefined;
    displayRight.value = true;
    placeIdUuid.value = layer.feature.properties.id_uuid;

    // revert the style of all layers
    leafletGeoJson.resetStyle();
    var associatedLayers = L.featureGroup();  // all associated layers will be stored here
    // fetch the UUIDs of the 5 places most often associated with the clicked one
    // (that is, places that are connected to iconography resources connected
    // to the clicked place). style those layers
    axios.get(new URL(`/i/association/place-from-place/${placeIdUuid.value}`, __API_URL__))
    .then(r => r.data)
    .then(data => {
      currentAssociatedPlaces.value = data;

      // set the style of the clicked layer
      layer.setStyle({ fillOpacity: 1, fillColor: "var(--cs-duck)" });
      associatedLayers.addLayer(layer);
      // extract all associated layers and set their style
      leafletGeoJson.eachLayer(otherLayer => {
        if ( data.map( i => i.id_uuid ).includes( otherLayer.feature.properties.id_uuid ) ) {
          otherLayer.setStyle({ fillOpacity: 1, fillColor: "var(--cs-seagreen)" })
          associatedLayers.addLayer(otherLayer);
        }
      });
      // zoom to the clicked layer
      //TODO fix yank here ?
      setTimeout(() => _map.fitBounds(associatedLayers.getBounds()),
                 transDur);  // wait for the size animation to complete...
    });
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
function addPlaces(init) {
  let _map = lflMap.value,
    _places = placesFilter.value;

  // remove the old geoJson if it exists
  if (lflPlaces.value) _map.removeLayer(lflPlaces.value);

  // define the geojson
  const leafletPlaces = L.geoJSON(_places, {
    style: styleFeature,
    pointToLayer: (gjPoint, latLng) => lflDefaultMarker(latLng)  // style is defined in the `style` function below
  });
  // add event listeners for each layer (1 layer = 1 feature in the geoJson).
  // this is equivalent to `onEachFeature` inside `L.geoJSON`, but we add the
  // event listeners here because we need to access `leafletPlaces`, and so
  // create the event listeners after `leafletPlaces` has been initialized.
  leafletPlaces.eachLayer((layer) => onEachLayer(layer, leafletPlaces, _map));

  // add to map and set the global variables
  if (init) { lflFallBackBounds.value = leafletPlaces.getBounds() };  // save the bounds of the full original geojson layer, in case we later add a geoJson feature with 0 layers (in which case we won't be able to compute bounds)
  leafletPlaces.addTo(_map);

  // zoom on the layers. if init, the zoom animation is triggered
  // in `onCloseCartographyModal()`
  if (!init) {
    _map.fitBounds( _places.features.length
                ? leafletPlaces.getBounds()
                : lflFallBackBounds.value);
  }

  lflPlaces.value = leafletPlaces;
  // lflMap.value    = _map;
  return;
}

/************************************************************/
/** handler for CartographyController */

/** helper functions */

/**
 * updates the `geoJsonObj` geojson by
 * 1) only keeping features for which we can find a vector in `_cartography`.
 * 2) updating the `vector` of each feature by the matched vector in `_cartography`
 * `_cartography` is a local version of `cartographyForSource`
 * @param {GeoJSON} geoJsonObj: a geoJson describing places
 * @param {Object} _cartography: an object with the structure: { features: [<array of Cartography objects>] }
 */
const updatePlacesByCartography = (geoJsonObj, _cartography) => {
  let features = [];
  geoJsonObj.features.map(f => {
    let v = _cartography.features.find(c =>
      c.place.length === 1
      && c.place[0].id_uuid === f.properties.id_uuid
    )?.vector
    if (v !== undefined) {
      f.vector = v;
      features.push(f);
    }
  })
  geoJsonObj.features = features
  return geoJsonObj;
}
/**
 * only keep the features in `geoJsonObj` with an iconography_count
 * contained in the range `iconographyCount`
 * @param {Object} geoJsonObj: the geoJson to filter
 * @param {Array<Number>} iconographyCount: an array of min,max
 *    allowed iconography counts
 * @returns {Object} geoJsonObj
 */
const updateByIconographyCount = (geoJsonObj, iconographyCount) => {
  // if iconographyCount is null or has no len, this filter is not set
  // => reset back to the original placesGeoJson
  if (iconographyCount != null && iconographyCount.length) {
    geoJsonObj.features = geoJsonObj.features.filter(f =>
      iconographyCount[0] <= f.properties.iconography_count
      && f.properties.iconography_count <= iconographyCount[1]);
  }
  return geoJsonObj
}
/**
 * only keep the features in `geoJsonObj` that have an address contained
 * within `address`
 * @param {Object} geoJsonObj
 * @param {Array<String>} address: the array of address objects to filter by.
 *    structure: [ { id_uuid: String, address: String } ]
 * @returns {Object} geoJsonObj
 */
const updateByAddress = (geoJsonObj, address) => {
  // console.log(newFilter.address);
  if (address != null && address.length) {
    geoJsonObj.features = geoJsonObj.features.filter(f =>
      address.includes(f.properties.address[0].id_uuid));
  }
  return geoJsonObj;
}
/**
 * only keep the features in `geoJsonObj` that can be represented by
 * the source `cartographySource` and update the vector
 * of these features to come from the source `cartographySources`.
 * this function is different than the 2 above because it is async and requires
 * to fetch data from the backend.
 *
 * @param {GeoJson} geoJsonObj: the geoJson to filter
 * @param {bool} changeCartographySource: if `true`,
 *    _cartographyForSource needs to be updated by fetching data
 *    from the backend.
 * @param {string} cartographySource: a string matching a value of
 *    Cartography.map_source on the database
 * @param {Object} _cartographyForSource: an object of
 *    { source: <string>, features: [<array of Cartography objects>] }.
 *    this object corresponds to the global `cartographyForSOurce` and
 *    may be updated depending on the value of `changeCartographySource`
 * @returns {Array<Object> | Promise<Array<Object>>}
 *    geoJsonObj: the geoJson object after filtering
 *    _cartographyForGranularity: the newly fetched cartography
 *      matching the user defined-source
 */
const updateByCartographySource = async (
  geoJsonObj,
  changeCartographySource,
  cartographySource,
  _cartographyForSource
) => {
  // console.log(`for : °${newFilter.cartographySource}°`);
  if (cartographySource == null
    || cartographySource === ""
    || cartographySource.length === 0  // string of length 0
    || cartographySource === "default"
  ) {
    // use the default cartography source => no need to change it
    // console.log("case 1")
    return [geoJsonObj, _cartographyForSource];
  } else if (!changeCartographySource) {
    // a non-default cartography source is used, but it's the same as
    // `_cartographyForSource` so no need to re-fetch it from the backend
    // console.log("case 2");
    geoJsonObj = updatePlacesByCartography(geoJsonObj, _cartographyForSource);
    return [geoJsonObj, _cartographyForSource];
  } else {
    // a non-default cartography source is used and
    // we need to fetch it from the backend
    // console.log("case 3");
    return getCartographyForSource(cartographySource)
      .then(r => {
        _cartographyForSource = r
        geoJsonObj = updatePlacesByCartography(geoJsonObj, _cartographyForSource);
        return [geoJsonObj, _cartographyForSource];
      });
  }
}
/**
 * the same but for Cartography.granuarity instead of Cartography.map_source
 * @param {GeoJson} geoJsonObj: the geoJson to filter
 * @param {bool} changeCartographyGranularity: if `true`,
 *    _cartographyForGranularity needs to be updated by fetching data
 *    from the backend.
 * @param {string} cartographyGranularity: a string matching a value of
 *    Cartography.granularity on the database
 * @param {Object} _cartographyForGranularity: an object of
 *    { granularity: <string>, features: [<array of Cartography objects>] }.
 *    this object corresponds to the global `cartographyForGranularity` and
 *    may be updated depending on the value of changeCartographyGranularity
 * @returns {Array<Object> | Promise<Array<Object>>}:
 *    geoJsonObj: the geoJson object after filtering
 *    _cartographyForGranularity: the newly fetched cartography
 *      matching the user defined-source
 */
const updateByCartographyGranularity = async (
  geoJsonObj,
  changeCartographyGranularity,
  cartographyGranularity,
  _cartographyForGranularity
) => {
  if (cartographyGranularity == null
    || cartographyGranularity === ""
    || cartographyGranularity.length === 0  // string of length 0
    || cartographyGranularity === "default"
  ) {
    // default granularity => return default geojson
    return [geoJsonObj, _cartographyForGranularity]
  } else if (!changeCartographyGranularity) {
    // data has aldready been fetched => no need to refetch it
    geoJsonObj = updatePlacesByCartography(geoJsonObj, _cartographyForGranularity);
    return [geoJsonObj, _cartographyForGranularity];
  } else {
    // granularity has changed => refetch
    return getCartographyForGranularity(cartographyGranularity)
      .then(r => {
        _cartographyForGranularity = r;
        geoJsonObj = updatePlacesByCartography(geoJsonObj, _cartographyForGranularity);
        return [geoJsonObj, _cartographyForGranularity];
      });
  }
}


/** main process */

/**
 * when the `CartographyController` form emits a new
 * user-defined filter (`newFilter`),
 * 1) generate a new geoJson for places matching `newFilter`.
 *    this includes filtering `places.value` to match `newFilter`
 *    and modifying each the feature's geometries to match
 *    `newFilter.cartographySource`, if necessary
 * 2) add the new geoJson to the map.
 * @param {Object} newFilter: the filter emitted by CartographyController.
 */
function onFilterUpdate(newFilter) {

  if (!currentlyFiltering.value) {
    currentlyFiltering.value = true;

    console.log("onFilterUpdate");

    // 1) variables
    let placesGeoJson = _.cloneDeep(places.value),  // without _.cloneDeep(), the modifications done to placesGeoJson below would be repercuted to `places.value`, which would break everything
      _cartographyForSource = cartographyForSource.value,
      _cartographyForGranularity = cartographyForGranularity.value,
      changeCartographySource = _cartographyForSource?.source !== newFilter.cartographySource,
      changeCartographyGranularity = _cartographyForGranularity?.granularity !== newFilter.cartographyGranularity;

    //TODO find a way to avoid rerunning this function all the time ?

    // 2) run the process, update the map and update globals.
    // all 3 `updateBy` functions are run: verifications are done within each
    // of them to check if there's a need to re-filter the data.
    // console.log("> 0 :", placesGeoJson.features.length);
    updateByCartographySource( placesGeoJson
                             , changeCartographySource
                             , newFilter.cartographySource
                             , _cartographyForSource )
      .then(r => {
        [placesGeoJson, _cartographyForSource] = r;
        updateByCartographyGranularity( placesGeoJson
                                      , changeCartographyGranularity
                                      , newFilter.cartographyGranularity
                                      , _cartographyForGranularity )
          .then(r => {
            [placesGeoJson, _cartographyForGranularity] = r;
            // console.log("> 1 :", placesGeoJson.features.length);
            placesGeoJson = updateByIconographyCount(placesGeoJson, newFilter.iconographyCount);
            // console.log("> 2 :", placesGeoJson.features.length);
            placesGeoJson = updateByAddress(placesGeoJson, newFilter.address);
            // console.log("> 3 :", placesGeoJson.features.length);

            // if we're switching to "parcellaire1900" or "vasserot",
            // programatically update the background tile layer.
            if (changeCartographySource
              && ["parcellaire1900", "vasserot"].includes(newFilter.cartographySource)
            ) {
              // remove all the background layers
              lflLayerControl.value._layers.forEach(l => lflMap.value.removeLayer(l.layer));
              // add the one corresponding to newFilter.cartographySource
              let mapper = {
                vasserot: "Atlas Vasserot (1810-1836)",
                parcellaire1900: "Cadastre municipal (1900)"
              };
              let l = getLayerByName(lflLayerControl.value, mapper[newFilter.cartographySource]);
              lflMap.value.addLayer(l);
            }

            placesFilter.value = placesGeoJson;
            currentFeatureCount.value = placesGeoJson.features.length;
            cartographyForGranularity.value = _cartographyForGranularity;
            cartographyForSource.value = _cartographyForSource;
            addPlaces(false);
            currentlyFiltering.value = false;
          })
      });
  }
}

/************************************************************/

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
  oldId !== undefined && newId === undefined && lflMap.value !== undefined    // unmount
    ? lflMap.value.invalidateSize()
    : oldId === undefined && newId !== undefined && lflMap.value !== undefined  // mount
      ? setTimeout(() => lflMap.value.invalidateSize(), transDur)  // the setTimeout is to wait for the transition to complete
      : ''
)

/************************************************************/

onMounted(() => {
  [lflMap.value, lflLayerControl.value] = globalDefineMap("map-main");  // synchronous
  lflMap.value.setView(mapCenter, 14);
  addControls(lflMap.value);
  getInitPlaces().then(() => addPlaces(true))
})

</script>


<style scoped>
/**
 * about the style:
 *
 * the page is contained by .cartography-outer-wrapper
 * which is divided in 3 hztl blocks. by default, the
 * center block is visible, left and right are hidden.
 *
 * to display the left, block, `transform: translateX()`
 * is used to make the left block visible
 *
 * to display the right block, the whole `.cartography-outer-wrapper`'s
 * grid-template-column is updated:
 * - block 1 (CartographyController) is not changed
 * - block 2 (#map-main): width is reduced
 * - block 2 (CartographyPlaceInfo): width is augmented to make it visible.
 */
.cartography-outer-wrapper {
  height: calc(100vh - var(--cs-navbar-height) - var(--cs-portrait-sidebar-height));
  width: 100%;
  display: grid;
  grid-template-rows: 100%;
  grid-template-columns: 100% 100% 100%;

  transform: translateX(-100%);
  transition: grid-template-columns v-bind("transDurCss");
}

.cartography-outer-wrapper.right-visible {
  grid-template-columns: 100% 0% 100%;
}

.cartography-place-wrapper {
  z-index: 400;
  height: 100%;
  width: 100%;
}

@media (orientation:landscape) {
  .cartography-outer-wrapper {
    height: calc(100vh - var(--cs-navbar-height));
    grid-template-columns: 30% 100% 30%;
    transform: translateX(-30%);
  }

  .cartography-outer-wrapper.right-visible {
    grid-template-columns: 30% 70% 30%;
  }
}

/**************************************/

#map-main {
  height: calc(100vh - var(--cs-navbar-height) - var(--cs-portrait-sidebar-height));
  width: 100%;
  overflow-y: hidden;
}

@media (orientation:landscape) {
  #map-main {
    height: calc(100vh - var(--cs-navbar-height));
  }
}

#map-main :deep(.infobox) {
  padding: 6px 8px;
  color: black;
  font-family: var(--cs-font-sans-serif);
  background-color: var(--cs-main-default-bg);
  border: var(--cs-main-border);
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.2);
  z-index: 999;
}

#map-main :deep(.leaflet-control) {
  border-radius: 0;
  border: var(--cs-main-border);
  margin-left: 10ox;
  margin-right: 10px;
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
  width: max(4vh, 50px);
}

#map-main :deep(.infobox h4) {
  margin: 0;
  font-family: var(--cs-font-serif);
  font-variant-caps: small-caps;
  color: #777;
  font-size: 120%;
}

#map-main :deep(.color-legend) {
  width: 250px;
}

#map-main :deep(.color-legend .top-wrapper) {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
}

#map-main :deep(.color-legend .btn-container > button) {
  width: max(40px, 4vh);
  height: max(40px, 4vh);
}

#map-main :deep(.color-legend svg) {
  transition: transform var(--animate-duration);
}

#map-main :deep(.color-legend svg.rotated) {
  transform: rotate(45deg);
}

#map-main :deep(.color-legend table) {
  max-width: fit-content;
}

#map-main :deep(.color-legend table tr) {
  display: grid;
  grid-template-columns: 15% auto;
  grid-template-rows: 100%;
  border: none;
  margin: 5px;
}

#map-main :deep(.color-legend td) {
  border: none;
  padding: 5;
}

#map-main :deep(.color-legend td:first-child) {
  margin: 3px;
}

#map-main :deep(.color-legend td:last-child) {
  text-wrap: nowrap;
}

/**************************************/

.cartography-controller-outer-wrapper {
  z-index: 1001;
  background-color: var(--cs-main-default-bg);
  color: var(--cs-main-default);
  border-right: var(--cs-main-border);
  transition: transform v-bind(transDurCss);
}

.cartography-controller-visible {
  transform: translateX(100%);
  height: 100%;
  width: 100%;
}
</style>