/*************************************************
 *     globally useful http and api requests     *
 *        string representations                 *
 *************************************************/

import axios from "axios";


/**
 * process a IIIF manifest to extract an image
 * see: https://openseadragon.github.io/examples/tilesource-iiif/
 */
export function manifestToTileSources(manifestUrl) {
  // TO BE ADAPED FROM : https://gitlab.inha.fr/snr/rich.data/auxiliaires/application_prototype/-/blob/main/frontend/src/app/services/iiif-manifest-processor.service.ts?ref_type=heads
  axios.get(manifestUrl)
       .then((r) => {
        console.log(r);
        const manifest = r.response;

       })
       .catch((e) => {
         console.log("***************\nerror\n");
         console.log("status  : ", e.response.status)
         console.log("headers : ", e.response.headers)
         console.log("data    : ", e.response.data)
         console.log("***************")
         throw new Error(e);
       })
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
                 : backupImgUrl                               // can't create a thumbnail => return the callback
          // return backupImgUrl
         }).catch((e) => {
          console.log( "ERROR IN MANIFESTTOTHUMBNAIL"
                     , ": " + manifestUrl
                     , e
                     , e.config.url);
         })
}