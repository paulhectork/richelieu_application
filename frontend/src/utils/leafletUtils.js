import "leaflet/dist/leaflet.css";
import "leaflet";

/*******************************
 * leaflet helper functions
 *******************************/

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
      minZoom : minZoom,
      maxZoom : maxZoom,
      version: "1.3.0",
      uppercase: true,
      attribution : "<a href='https://www.geoportail.gouv.fr/'>IGN-F/Geoportail</a>",
    }
  )
}


/**
 * initialize a map.
 * @param {string} mapId: the html ID of the map container
 * @returns: a leaflet map
 */
export function globalDefineMap(mapId) {
  // generic background tiles. dict of `{ mapName: layer }`
  const backgroundTiles = {
    "Carte de l'etat-major 1&nbsp;: 40 000 (1820-1866)": L.layerGroup([
      buildWmtsTile( "https://wxs.ign.fr/cartes/geoportail/wmts"
                   , "GEOGRAPHICALGRIDSYSTEMS.ETATMAJOR40", "bgPane", 7, 15.5
      ), buildWmsTile( "https://wxs.ign.fr/cartes/geoportail/r/wms"
                     , "GEOGRAPHICALGRIDSYSTEMS.ETATMAJOR40", "bgPane", 15.5, 17
      )
    ]),
    "Carte de Paris (1906)": buildWmtsTile( "https://wxs.ign.fr/cartes/geoportail/wmts"
                     , "GEOGRAPHICALGRIDSYSTEMS.1900TYPEMAPS", "bgPane", 10, 15.5
    ),
    "Plan Vasserot (début XVIII<sup>e</sup> siècle)": L.tileLayer(
      "https://tile.maps.huma-num.fr/uc2usU/d/Alpage_Vasserot_1830/{z}/{x}/{y}.png", {
        pane: "bgPane",
        opacity: 0.85,
        minZoom: 14
    }),
    "Cadastre municipal (1900)": L.tileLayer(
      "https://tile.maps.huma-num.fr/uc2usU/d/MOSA_1900_PARIS/{z}/{x}/{y}.png", {
        pane: "bgPane",
        opacity: 0.85
    })
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
  map.createPane("basePane");  // default map tiles
  map.getPane("basePane").style.zIndex = "0";
  map.createPane("bgPane");  // custom background panes retrieved from WMS/WMTS
  map.getPane("bgPane").style.zIndex = "1";
  map.createPane("dataPane");  // actual data added on top of the map: raster images, shapes...
  map.getPane("dataPane").style.zIndex = "2";

  // add background tiles and a controller to enable/disable background tiles
  L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    pane: "basePane",
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
  }).addTo(map);

  const layerControl =  L.control.layers(
    {}, undefined, { hideSingleBase: true, position: "bottomright" }
  );
  layerControl.addTo(map);
  Object.keys(backgroundTiles).forEach((key) => {
    layerControl.addOverlay( backgroundTiles[key], key );
  })

  return map;
}






