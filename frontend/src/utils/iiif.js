/*************************************************
 *     globally useful http and api requests     *
 *        string representations                 *
 *************************************************/

import axios, { AxiosError } from "axios";


/**
 * process a IIIF manifest to extract tile sources
 * from a IIIF manifest, we must get all `sequences/canvases/images/resource/@id`,
 * and create an array of tile sequences with the structure:
 * `[{ type: "image",
 *     url: <url in the resource/@id>,
 *     height: 1
 *  }]`
 * see: https://openseadragon.github.io/examples/tilesource-iiif/
 *
 * @param {string} manifestUrl: the URL to the IIIF manifest
 * @param {Array} folio: an array of canvas numbers to display.
 *                       if `folio` is not empty, only the pages
 *                       in `folio` will be shown
 */
export async function manifestToTileSequence(manifestUrl, folio=[]) {

  /* HELPER FUNCTIONS */
  // function to create a tile source from a resource in a manifest
  // returns an object (`{}`)
  const resourceProcessing = (theResource) => {
    return { url:theResource["@id"], type:"image", height: 1 }
  };
  // build an array of tilesources from a canvas `theCanvas`
  // returns an array (`[]`)
  const canvasProcessing = (theCanvas) => {
    let outputArr = [];
    theCanvas.images.forEach((image) => {
      outputArr.push( resourceProcessing(image.resource) );
    })
    return outputArr;
  }
  // extract all images from the IIIF manifest `theManifest`
  // and add them to the array of tile sources `outputArr`.
  // returns a tile sequence as an array (`[]`)
  const manifestProcessing = (theManifest) => {
    let outputArr = [];
    theManifest.sequences[0].canvases.forEach((canvas) => {
      outputArr = outputArr.concat( canvasProcessing(canvas) );
    })
    return outputArr;
  }

  /* LOGIC */
  // the final output array
  let out = [];

  // fetch the manifest. we use `await` + `catch` to have specific
  // handling of this error and another handling of other errors below
  const manifest = await axios
                         .get(manifestUrl)
                         .then((r) => { return r.data })
                         .catch((e) => {
                          console.log("iiif.manifestToTileSequence: error fetching IIIF manifest", e); });

  // assert that we're working with a v2 presentation manifest
  if ( manifest["@context"] !== "http://iiif.io/api/presentation/2/context.json" ) {
    throw new Error(`iiif.manifestToTileSequence: the manifest must follow the IIIF
                     presentation v2 API, on '${manifestUrl}'`) }

                     // extract the images.
  // if extraction using folios fails, switch back to normal extraction
  if ( folio.length ) {
    try {
      folio.forEach((idx) => {
        out = out.concat( canvasProcessing( manifest.sequences[0].canvases[idx] ) );
      })
    } catch(e) {
      console.log(`iiif.manifestToTileSequence: error using "folio" parameter
                   with value ${folio} on ${manifestUrl}`)
      out = manifestProcessing(manifest, out);
    }
  } else {
    out = manifestProcessing(manifest, out);
  }
  console.log(out);
  return out;
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
          // console.log(r);
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
          console.log( "ERROR IN MANIFESTTOTHUMBNAIL"
                     , ": " + manifestUrl
                     , e
                     , e.config.url);
         })
}