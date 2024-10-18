
/**
 * leaflet helper functions
 */

import "leaflet/dist/leaflet.css";
import L from "leaflet";



/** default values and settings for styling geojsons */

/**
 * the neighbourhood as a geoJson
 */
export const gjZone = { "type": "FeatureCollection", "features": [ { "type": "Feature", "properties": {}, "geometry": { "coordinates": [ [ [ [ 7.875627259060394, 43.03546151241537 ], [ 7.875627259060394, 50.76402288707351 ], [ -3.684393492754367, 50.76402288707351 ], [ -3.684393492754367, 43.03546151241537 ], [ 7.875627259060394, 43.03546151241537 ] ], [ [ 2.3352932, 48.8627152 ], [ 2.3389757, 48.8615218 ], [ 2.339239, 48.8620325 ], [ 2.3393462, 48.862265 ], [ 2.3396953, 48.8631739 ], [ 2.3403676, 48.8643848 ], [ 2.3410387, 48.8654223 ], [ 2.3410387, 48.8654223 ], [ 2.3410929, 48.8654117 ], [ 2.3411609, 48.8654056 ], [ 2.3412233, 48.8654051 ], [ 2.3413023, 48.865411 ], [ 2.3413839, 48.8654289 ], [ 2.3414488, 48.8654503 ], [ 2.3415094, 48.8654799 ], [ 2.3415644, 48.8655132 ], [ 2.341618, 48.8655537 ], [ 2.3416753, 48.8656116 ], [ 2.3417126, 48.8656643 ], [ 2.3417189, 48.8657099 ], [ 2.3417215, 48.8657759 ], [ 2.3417017, 48.8658258 ], [ 2.3416778, 48.8658749 ], [ 2.341625, 48.8659681 ], [ 2.341342, 48.8662782 ], [ 2.3412624, 48.8663425 ], [ 2.3410705, 48.866414 ], [ 2.3415556, 48.86758 ], [ 2.3418484, 48.8683194 ], [ 2.3418913, 48.868437 ], [ 2.3419684, 48.8684414 ], [ 2.3433257, 48.8685294 ], [ 2.3435519, 48.8685366 ], [ 2.3433281, 48.8690421 ], [ 2.3430427, 48.8696637 ], [ 2.342961, 48.8698345 ], [ 2.3428535, 48.8699591 ], [ 2.3428042, 48.8703424 ], [ 2.3429409, 48.8707775 ], [ 2.3431148, 48.871317 ], [ 2.343176, 48.871499 ], [ 2.3400333, 48.8720206 ], [ 2.331957, 48.8706121 ], [ 2.3319792, 48.8704067 ], [ 2.332057, 48.8702261 ], [ 2.332364, 48.8700299 ], [ 2.3333911, 48.8676717 ], [ 2.3349788, 48.8639742 ], [ 2.3352707, 48.8632564 ], [ 2.335341, 48.8630898 ], [ 2.3351508, 48.8627482 ], [ 2.3352932, 48.8627152 ] ] ] ], "type": "MultiPolygon" } } ] }
// old geoJson
// export const gjZone = { "type": "FeatureCollection", "features": [ { "type": "Feature", "properties": {}, "geometry": { "type": "MultiPolygon", "coordinates": [ [ [ [ -9.308577500591156, 51.96179459849796 ], [ -9.308577500591156, 41.03936743552862 ], [ 12.68928919604204, 41.03936743552862 ], [ 12.68928919604204, 51.96179459849796 ], [ -9.308577500591156, 51.96179459849796 ] ], [ [ 2.3431082580363807, 48.87146697188524 ], [ 2.343049573623574, 48.87153642186135 ], [ 2.3417749810140265, 48.871730870621974 ], [ 2.3389640887056373, 48.87219946215572 ], [ 2.3389640887056373, 48.871839256572315 ], [ 2.3368510758635352, 48.87146948531159 ], [ 2.332538257218971, 48.870726880412946 ], [ 2.3327044980904077, 48.87036190760571 ], [ 2.332427716255353, 48.87028099314284 ], [ 2.3355596988145635, 48.863107626297676 ], [ 2.3353691290912764, 48.86274277118474 ], [ 2.33704272217949, 48.86220110912893 ], [ 2.337334006377233, 48.86267888967484 ], [ 2.339136771027114, 48.862188032828584 ], [ 2.3394194667683053, 48.86281913360381 ], [ 2.3397346030054678, 48.86349290873966 ], [ 2.340439024548175, 48.864742874434654 ], [ 2.341055393952786, 48.865492839077234 ], [ 2.3412407728052074, 48.865483693804805 ], [ 2.341379803497688, 48.86553247161277 ], [ 2.3415373716162833, 48.865642221506334 ], [ 2.3415141998338527, 48.86580074870568 ], [ 2.3413983409238313, 48.8659165951876 ], [ 2.34145395320013, 48.86609646156194 ], [ 2.3413149225077063, 48.866297667248915 ], [ 2.340981248845395, 48.866285472987954 ], [ 2.341199063597685, 48.866840308856325 ], [ 2.3419285808616053, 48.868527292535646 ], [ 2.3436527244255387, 48.86816914720873 ], [ 2.34264319299686, 48.87021352566978 ], [ 2.3431082580363807, 48.87146697188524 ] ] ] ] } } ] };

/**
 * the center of the map, that is, the center of the bounding box
 * of the neighbourhood's outline
 *
 * if `g` is a geojson representing the outline, `mapCenter` is obtained using:
 * L.geoJSON(g).getBounds().getCenter()
 */
export const mapCenter = { "lat": 48.8667712, "lng": 2.3377544500000003 };


/**
 * generates a default marker at position `latLng`
 * @example in an L.geoJSON's options:
 *    pointToLayer: (gjPoint, latLng) => lflDefaultMarker(latLng);
 * @param {<Array<Array<Number>>> | L.LatLng} latLng: point to place the map on
 * @returns
 */
export const lflDefaultMarker = (latLng) =>
  L.circleMarker(latLng, { radius: 6, pane: "markerPane" });

/**
 * default `style` function for a geoGson.
 * see:
 *  https://leafletjs.com/reference.html#path
 * @param {L.Feature} feature: the feature we're styling
 * @returns {Object}
 */
export const lflDefaultStyle = (feature) => {
  return { stroke: true,
           color: "var(--cs-main-default)",
           weight: 1,
           fillColor: "var(--cs-plum)",
           fillOpacity: 0.5,
           className: "place-gj"
         }
}

/**
 * default mouseover and mouseout actions on a layer
 * @param {L.Layer} layer
 */
export const lflDefaultMouseOver = (layer) =>
  layer.setStyle({ color: layer.options.fillColor, weight: 3 });
export const lflDefaultMouseOut = (layer) =>
  layer.setStyle({ color: "black", weight: 1 });

/*********************************************************/

/**
 * build a WMS tile (used by the IGN to serve custom maps) using the WMTS protocol
 * based on this tutorial: https://geoservices.ign.fr/documentation/services/utilisation-web/affichage-wmts/leaflet-et-wmts
 *
 * @param serverUrl: the url of the WMTS server
 * @param layer: the name of the layer on the WMTS server
 * @param pane: the pane a layer belongs to. defaults to `tilePane`, the default leaflet value
 * @param minZoom: the minimum zoom
 * @param maxZoom: the maximum zoom
 */
export function buildWmtsTile( serverUrl, layer
                             , pane=undefined, minZoom=7, maxZoom=16 ) {
  return L.tileLayer(
    `${serverUrl}?`
    + "&REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0"
    + "&STYLE=normal"
    + "&TILEMATRIXSET=PM"
    + "&FORMAT=image/jpeg"
    + `&LAYER=${layer}`
    + "&TILEMATRIX={z}"
    + "&TILEROW={y}"
    + "&TILECOL={x}",
    {
      pane: pane != null ? pane : "tilePane",  // if no pane is defined, add the default value
      minZoom : minZoom,
      maxZoom : maxZoom,
      attribution : "<a href='https://www.geoportail.gouv.fr/'>IGN-F/Geoportail</a>",
      tileSize : 256 // les tuiles du Géooportail font 256x256px
    }
  )
}

/**
 * build a WMS tile layer (used by the IGN to serve custom maps)
 * based on this tutorial: https://leafletjs.com/examples/wms/wms.html
 *
 * @param serverUrl: the url of the WMS server
 * @param layer: the name of the layer on the WMS server
 * @param pane: the pane a layer belongs to. defaults to `tilePane`, the default leaflet value
 * @param minZoom: the minimum zoom
 * @param maxZoom: the maximum zoom
 */
export function buildWmsTile(serverUrl, layer, pane=undefined, minZoom=7, maxZoom=16) {
  return L.tileLayer.wms(
    `${serverUrl}?`,
    {
      pane: pane !== undefined && pane !== "" ? pane : "tilePane",  // if no pane is defined, add the default value
      layers: layer,
      minZoom: minZoom,
      maxZoom: maxZoom,
      version: "1.3.0",
      uppercase: true,
      attribution: "<a href='https://www.geoportail.gouv.fr/'>IGN-F/Geoportail</a>",
    }
  )
}

/*********************************************************/

/**
 * initialize a map.
 * @param {string} mapId: the html ID of the map container
 * @returns {Array<L.Map, L.Control.Layers>}:
 *    - a leaflet map
 *    - the leaflet layer control (useful to programatically change
 *        background tilelayers, as done in @components/CartographyView)
 */
export function globalDefineMap(mapId) {
  const baseLayers = {
    // basic vector layers
    "Fond de carte OpenStreetMap":
      L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
      }),
    "Fond de carte Stamen":
      L.tileLayer('https://tiles.stadiamaps.com/tiles/stamen_toner/{z}/{x}/{y}{r}.{ext}', {
        minZoom: 0,
        maxZoom: 20,
        attribution: '&copy; <a href="https://www.stadiamaps.com/" target="_blank">Stadia Maps</a> &copy; <a href="https://www.stamen.com/" target="_blank">Stamen Design</a> &copy; <a href="https://openmaptiles.org/" target="_blank">OpenMapTiles</a> &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        ext: 'png'
      }),
    // historical background tiles.  { layerName: L.Layer }
    "Plan Verniquet (1791)":
      L.tileLayer( 'https://tile.ptm.huma-num.fr/tiles/ark/highres/12148/btv1b55013275x/{z}/{x}/{y}.webp'
                 , { opacity: .85, maxZoom: 17.5,
                     attribution: "<a href='https://ptm.huma-num.fr/'>Projets Time Machine</a> | <a href='https://www.huma-num.fr/'>Huma-Num</a>" }),
    "Atlas Vasserot (1810-1836)":
      L.tileLayer( "https://tile.maps.huma-num.fr/uc2usU/d/Alpage_Vasserot_1830/{z}/{x}/{y}.png"
                 , { opacity: 0.85, minZoom: 14, maxZoom: 18,
                     attribution: "<a href='https://ptm.huma-num.fr/'>Projets Time Machine</a> | <a href='https://www.huma-num.fr/'>Huma-Num</a>" }),
    "Plan de 1812":
      L.tileLayer( 'https://tile.ptm.huma-num.fr/tiles/ark/highres/12148/btv1b530851375/{z}/{x}/{y}.webp'
                 , { opacity: .85, maxZoom: 17.5,
                     attribution: "<a href='https://ptm.huma-num.fr/'>Projets Time Machine</a> | <a href='https://www.huma-num.fr/'>Huma-Num</a>" }),
    "Cadastre municipal (1900)":
      L.tileLayer( "https://tile.maps.huma-num.fr/uc2usU/d/MOSA_1900_PARIS/{z}/{x}/{y}.png"
                 , { opacity: 0.85,
                     attribution: "<a href='https://ptm.huma-num.fr/'>Projets Time Machine</a> | <a href='https://www.huma-num.fr/'>Huma-Num</a>" }),
    "Plan de 1943":
      L.tileLayer( 'https://tile.ptm.huma-num.fr/tiles/ark/highres/12148/btv1b53121232b/{z}/{x}/{y}.webp'
                 , { opacity: .85, maxZoom: 16.5,
                     attribution: "<a href='https://ptm.huma-num.fr/'>Projets Time Machine</a> | <a href='https://www.huma-num.fr/'>Huma-Num</a>" }),
    // "Carte de Paris (1906)":
    //   buildWmtsTile( "https://wxs.ign.fr/cartes/geoportail/wmts"
    //                , "GEOGRAPHICALGRIDSYSTEMS.1900TYPEMAPS"
    //                , 10, 15.5 ),
  };

  // basic map creation
  const map = L.map(mapId, {
    center: mapCenter,
    maxBounds: L.latLngBounds([ { lat: mapCenter.lat + 0.01, lng: mapCenter.lng + 0.03 }
                              , { lat: mapCenter.lat - 0.01, lng: mapCenter.lng - 0.03 }
      // L.latLngBounds([ { lat: 48.8856701621242, lng: 2.3092982353700506 }
      //                , { lat: 48.829997780023035, lng: 2.3845843750075915 }
    ]),
    inertia: false,  // inertia does weird things with the geojson layer
    maxBoundsViscosity: 1.0,
    scrollWheelZoom: true,
    zoomControl: true,
    minZoom: 12,  // 11 for paris + region, 13 for the neighbourhood
    zoom: 15
  });

  // bounds geojson
  L.geoJSON(gjZone, { style: {
    fillColor: "ffffff",
    fillOpacity: .4,
    stroke: false
   }}).addTo(map);

  // other historical tile layers are controlled through the L.Layer.Control
  const layerControl = L.control.layers( baseLayers, undefined
                                       , { hideSingleBase: true, position: "bottomright" })
  layerControl.addTo(map);

  // set the default layer
  map.addLayer( getLayerByName(layerControl, "Cadastre municipal (1900)") );

  return [ map, layerControl ];
}


/*********************************************************/
/** helper functions */

/**
 * get layer bounds for a point or another geojson feature
 * returns
 *    the bound of a geojson feature if the feature is not a point
 *    or bounds determined from its LatLng if the feature is a point
 * @param {Object} layer: the leaflet layer corresponding to a geojson feature
 */
export const layerBounds = (layer) => {
  let pointBounds = { lat: 0.0005434656870164645/2, lng: -0.0005838759503453694/2 }  // distances from which to get the points. determined experimentally
  return layer.feature.geometry.type !== "Point"
         ? layer.getBounds()
         : [ [ layer.getLatLng().lat - pointBounds.lat, layer.getLatLng().lng - pointBounds.lat ]
           , [ layer.getLatLng().lat + pointBounds.lat, layer.getLatLng().lng + pointBounds.lat ]
           ]
}

/**
 * in a layer control, get a layer by its "name". it's kind of a dirty function
 * @param {L.Control.Layers} layerControl: the layer control
 * @param {string} layerName: the name to find the layer
 * @returns {L.Layer | undefined} : undefined if no layer is found
 */
export const getLayerByName = (layerControl, layerName) =>
  layerControl._layers.find(l => l.name === layerName)?.layer;
