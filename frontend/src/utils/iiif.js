/**
 * globally useful http and api requests
 * string representations
 */

import axios from "axios";

/********************************************/

/**
 * @typedef tileSource
 *    a single resource (or image) within a manifest.
 *    limited version of OpenSeadragon.TileSource
 * @type object
 * @property {String} url: the URL of the data (image)
 * @property {String} type:
 * @property {Number} height: the height in pixels of the image, to build the tile pyramid
 * @property {Number} width: the width in pixels of the image
 */

/**
 * @typedef tileSequence
 *    a sequence of tile sources. the tile sequence is the images
 *    that will be fed to the Openseadragon viewer.
 * @type {tileSource[]}
 */

/********************************************/

/**
 * function to create a tile source from a resource in a manifest
 * @returns {tileSource}
 */
const resourceProcessing = (theResource) => {
  return { url    : theResource["@id"],
           type   : "image",
           height : theResource.height,
           width  : theResource.width }
};
/**
 * build an array of tilesources from a canvas `theCanvas`
 * @returns {tileSequence}
 */
const canvasProcessing = (theCanvas) =>
  theCanvas.images.map((image) =>
    resourceProcessing(image.resource) );
/**
 * extract all images from the IIIF manifest `theManifest`
 * and return them as a tile sequence (array of `tileSource`)
 * @returns {tileSequence}
 */
const manifestProcessing = (theManifest, folioIndexArray) =>
  folioIndexArray && folioIndexArray.length
  ? theManifest.sequences[0].canvases
      .filter((canvas, canvasIdx) => folioIndexArray.includes(canvasIdx))
      .map((canvas) => canvasProcessing(canvas))
      .flat()
  : theManifest.sequences[0].canvases
      .map((canvas) => canvasProcessing(canvas))
      .flat();  // `.flat()` : we get a nested tilesequence and need to flatten it.

/********************************************/

/**
 * process a IIIF manifest to extract tile sources
 * from a IIIF manifest, we must get all `sequences/canvases/images/resource/@id`,
 * and create a tile sequence (array of tileSource).
 * see: https://openseadragon.github.io/examples/tilesource-iiif/
 *
 * during the execution of this function, we use a flag variable
 * `success`, which is turned to `false` if an error occurs. this
 * allow the parent to know when there's been an error, and to
 * handle it (replace the IIIF viewer with a static image).
 * somehow, just using `catch` when this function is called
 * caused more errors than it solved
 *
 * @param {Object} manifest
 *    the IIIF manifest
 * @param {Array<number>?} folio
 *    an array of canvas numbers to display. if `folio` is
 *    not empty, only the pages in `folio` will be shown
 * @returns {Array<tileSequence, bool>}
 *    an array of `[tileSequence, success]`.
 *    the first item is the tile sequence, the second a flag that
 *    will be `false`  if an error has occurred
 */
export async function manifestToTileSequence(manifestUrl, folio=[]) {
  let out     = [],  // the final output array
      success = true;  // switched to false if an error occurs

  const manifest =
    await axios.get(manifestUrl)
          .then((r) => { return r.data })
          .catch((e) => {
           console.error("iiif.manifestToTileSequence: error fetching IIIF manifest", e);
           success = false;
          })

  // assert that we're working with a v2 presentation manifest
  if ( success && manifest["@context"] !== "http://iiif.io/api/presentation/2/context.json" ) {
    console.error(`iiif.manifestToTileSequence: the manifest must follow the IIIF
                   presentation v2 API, on '${manifestUrl}'`);
    success = false;
  }

  // if there's a problem so far, return.
  if (!success) return [ out, success ];

  // build the tilesequence.
  if ( folio && folio.length ) {
    try { out = manifestProcessing(manifest, folio) }
    catch(e) {
      console.error(`@utils.iiif.manifestToTileSequence: error using "folio" parameter with value ${folio}`);
      out = manifestProcessing(manifest);
    }
  } else {
    out = manifestProcessing(manifest);
  }
  return [ out, success ];
}


/**
 * transform a manifest URL into an URL pointing to a thumbnail.
 * launching this repeatedly will cause errors: the IIIF servers
 * block our requests
 *
 * IIIF image format: {base}/{ark}/{vue}/{region}/{size}/{rotation}/{quality}
 *
 * @param {string} manifestUrl: the URL to the `manifest.json` file
 * @param {string} backupImgUrl: the URL of the non-iiif thumbnail, in case there is an error with the IIIF manifest
 * @returns {URL}: the URL object pointing to a thumbnail
 */
export async function manifestToThumbnail(manifestUrl, backupImgUrl) {
  return axios
         .get(manifestUrl)
         .then((r) => {
          const manifest = r.data;
          const imgUrl = manifest.sequences[0]
                                 .canvases[0]
                                 .images[0]
                                 .resource
                                 ["@id"];
          return imgUrl.includes("/full/full/")
                 ? imgUrl.replace("/full/full/", "/full/500/")  // redimension to 500px
                 : backupImgUrl                                 // can't create a thumbnail => return the callback
          // return backupImgUrl
         }).catch((e) => {
          console.error( "iiif.manifestToThumbnail"
                       , ": " + manifestUrl
                       , e
                       , e.config.url);
         })
}

/********************************************/

export const osdNavImages = {
  "zoomIn": {
    "REST": "zoomin_rest.png",
    "GROUP": "zoomin_grouphover.png",
    "HOVER": "zoomin_hover.png",
    "DOWN": "zoomin_pressed.png"
  },
  "zoomOut": {
    "REST": "zoomout_rest.png",
    "GROUP": "zoomout_grouphover.png",
    "HOVER": "zoomout_hover.png",
    "DOWN": "zoomout_pressed.png"
  },
  "home": {
    "REST": "home_rest.png",
    "GROUP": "home_grouphover.png",
    "HOVER": "home_hover.png",
    "DOWN": "home_pressed.png"
  },
  "fullpage": {
    "REST": "fullpage_rest.png",
    "GROUP": "fullpage_grouphover.png",
    "HOVER": "fullpage_hover.png",
    "DOWN": "fullpage_pressed.png"
  },
  "rotateleft": {
    "REST": "rotateleft_rest.png",
    "GROUP": "rotateleft_grouphover.png",
    "HOVER": "rotateleft_hover.png",
    "DOWN": "rotateleft_pressed.png"
  },
  "rotateright": {
    "REST": "rotateright_rest.png",
    "GROUP": "rotateright_grouphover.png",
    "HOVER": "rotateright_hover.png",
    "DOWN": "rotateright_pressed.png"
  },
  "flip": {
    "REST": "flip_rest.png",
    "GROUP": "flip_grouphover.png",
    "HOVER": "flip_hover.png",
    "DOWN": "flip_pressed.png"
  },
  "previous": {
    "REST": "previous_rest.png",
    "GROUP": "previous_grouphover.png",
    "HOVER": "previous_hover.png",
    "DOWN": "previous_pressed.png"
  },
  "next": {
    "REST": "next_rest.png",
    "GROUP": "next_grouphover.png",
    "HOVER": "next_hover.png",
    "DOWN": "next_pressed.png"
  }
}
