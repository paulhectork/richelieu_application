
/**
 * leaflet helper functions
 */

import "leaflet/dist/leaflet.css";
import "leaflet";


/**
 * the neighbourhood as a geoJson
 */
export const gjZone = { "type": "FeatureCollection", "features": [ { "type": "Feature", "properties": {}, "geometry": { "type": "MultiPolygon", "coordinates": [ [ [ [ -9.308577500591156, 51.96179459849796 ], [ -9.308577500591156, 41.03936743552862 ], [ 12.68928919604204, 41.03936743552862 ], [ 12.68928919604204, 51.96179459849796 ], [ -9.308577500591156, 51.96179459849796 ] ], [ [ 2.3431082580363807, 48.87146697188524 ], [ 2.343049573623574, 48.87153642186135 ], [ 2.3417749810140265, 48.871730870621974 ], [ 2.3389640887056373, 48.87219946215572 ], [ 2.3389640887056373, 48.871839256572315 ], [ 2.3368510758635352, 48.87146948531159 ], [ 2.332538257218971, 48.870726880412946 ], [ 2.3327044980904077, 48.87036190760571 ], [ 2.332427716255353, 48.87028099314284 ], [ 2.3355596988145635, 48.863107626297676 ], [ 2.3353691290912764, 48.86274277118474 ], [ 2.33704272217949, 48.86220110912893 ], [ 2.337334006377233, 48.86267888967484 ], [ 2.339136771027114, 48.862188032828584 ], [ 2.3394194667683053, 48.86281913360381 ], [ 2.3397346030054678, 48.86349290873966 ], [ 2.340439024548175, 48.864742874434654 ], [ 2.341055393952786, 48.865492839077234 ], [ 2.3412407728052074, 48.865483693804805 ], [ 2.341379803497688, 48.86553247161277 ], [ 2.3415373716162833, 48.865642221506334 ], [ 2.3415141998338527, 48.86580074870568 ], [ 2.3413983409238313, 48.8659165951876 ], [ 2.34145395320013, 48.86609646156194 ], [ 2.3413149225077063, 48.866297667248915 ], [ 2.340981248845395, 48.866285472987954 ], [ 2.341199063597685, 48.866840308856325 ], [ 2.3419285808616053, 48.868527292535646 ], [ 2.3436527244255387, 48.86816914720873 ], [ 2.34264319299686, 48.87021352566978 ], [ 2.3431082580363807, 48.87146697188524 ] ] ] ] } } ] };


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


/**
 * initialize a map.
 * @param {string} mapId: the html ID of the map container
 * @returns: a leaflet map
 */
export function globalDefineMap(mapId) {
  // generic background tiles. dict of `{ key: [ mapName, layer ] }`
  const backgroundTiles = {
    etatMajor: [
      "Carte de l'etat-major 1&nbsp;: 40 000 (1820-1866)",
      L.layerGroup([ buildWmtsTile( "https://wxs.ign.fr/cartes/geoportail/wmts"
                                  , "GEOGRAPHICALGRIDSYSTEMS.ETATMAJOR40"
                                  , "bgPane"
                                  , 7, 15.5 )
                   , buildWmsTile( "https://wxs.ign.fr/cartes/geoportail/r/wms"
                                 , "GEOGRAPHICALGRIDSYSTEMS.ETATMAJOR40"
                                 , "bgPane"
                                 , 15.5, 17 ) ])
    ],
    paris1906: [
      "Carte de Paris (1906)",
      buildWmtsTile( "https://wxs.ign.fr/cartes/geoportail/wmts"
                   , "GEOGRAPHICALGRIDSYSTEMS.1900TYPEMAPS"
                   // , "bgPane"
                   , 10, 15.5 )
    ],
    vasserot: [
      "Plan Vasserot (début XVIII<sup>e</sup> siècle)",
      L.tileLayer( "https://tile.maps.huma-num.fr/uc2usU/d/Alpage_Vasserot_1830/{z}/{x}/{y}.png"
                 , { // pane: "bgPane",
                     opacity: 0.85,
                     minZoom: 14 })
    ],
    cadastreMunicipal: [
      "Cadastre municipal (1900)",
      L.tileLayer( "https://tile.maps.huma-num.fr/uc2usU/d/MOSA_1900_PARIS/{z}/{x}/{y}.png"
                 , { // pane: "bgPane",
                     opacity: 0.85 })
    ]
  }

  // basic map creation
  const map = L.map(mapId, {
    center: [ 48.8687452, 2.3363674 ],
    maxBounds: L.latLngBounds([ { lat: 48.8856701621242, lng: 2.3092982353700506 }
                              , { lat: 48.829997780023035, lng: 2.3845843750075915 }
    ])
    , inertia: false  // inertia does weird things with the geojson layer
    , maxBoundsViscosity: 1.0
    , scrollWheelZoom: true
    , zoomControl: true
    , minZoom: 13  // 11 for paris + region, 13 for the neighbourhood
    , zoom: 14.7
  });

  // define the panes so that `backgroundTiles` may be added to `map`
  // map.createPane("basePane");  // default map tiles
  // map.getPane("basePane").style.zIndex = "0";
  // map.createPane("bgPane");  // custom background panes retrieved from WMS/WMTS
  // map.getPane("bgPane").style.zIndex = "1";
  // map.createPane("dataPane");  // actual data added on top of the map: raster images, shapes...
  // map.getPane("dataPane").style.zIndex = "2";

  // add background tiles and a controller to enable/disable background tiles
  L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    // pane: "basePane",
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
  }).addTo(map);

  L.geoJSON(gjZone, { style: {
    fillColor: "ffffff",
    fillOpacity: .4,
    stroke: false
   }}).addTo(map);

  const layerControl =  L.control.layers(
    {}, undefined, { hideSingleBase: true, position: "bottomright" }
  );
  layerControl.addTo(map);
  Object.keys(backgroundTiles).forEach((key) => {
    layerControl.addOverlay( backgroundTiles[key][1], backgroundTiles[key][0] );
  })

  // vasserot is selected by default. quick and dirty
  backgroundTiles.vasserot[1].addTo(map);

  return map;
}


/**
 * get layer bounds for a point or another geojson feature
 * returns
 *    the bound of a geojson feature if the feature is not a point
 *    or bounds determined from its LatLng if the feature is a point
 * @param {Object} layer: the leaflet layer corresponding to a geojson feature
 */
export const layerBounds = (layer) => {
  let pointBounds = { lat: 0.0005434656870164645/2, lng: -0.0005838759503453694/2 }  // distances from which to get the points
  return layer.feature.geometry.type !== "Point"
  ? layer.getBounds()
  : [ [ layer.getLatLng().lat - pointBounds.lat, layer.getLatLng().lng - pointBounds.lat ]
    , [ layer.getLatLng().lat + pointBounds.lat, layer.getLatLng().lng + pointBounds.lat ]
    ]
}

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
export const lflDefaultMouseOver = (layer) => {
  console.log(layer);
  layer.setStyle({ color: layer.options.fillColor, weight: 3 })
};
export const lflDefaultMouseOut = (layer) =>
  layer.setStyle({ color: "black", weight: 1 });



