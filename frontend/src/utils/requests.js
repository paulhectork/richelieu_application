/*************************************************
 *     globally useful http and api requests     *
 *        string representations                 *
 *************************************************/

import axios from "axios";


export function manifestToTileSources(manifestUrl) {
  /**
   * process a IIIF manifest to extract an image
   */

  // TO BE ADAPED FROM : https://gitlab.inha.fr/snr/rich.data/auxiliaires/application_prototype/-/blob/main/frontend/src/app/services/iiif-manifest-processor.service.ts?ref_type=heads
  // see               : https://openseadragon.github.io/examples/tilesource-iiif/
  axios.get(manifestUrl, { responseType: "json" })
       .then((r) => {

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

export function _manifestToThumbnail(manifestUrl) {
  /**
   * extract a thumbnail image from a IIIF manifest
   */
  axios.get(manifestUrl, { responseType: "json" })
       .then((r) => {
        r = JSON.parse(r.request.response);
        if ( r.thumbnail && r.thumbnail["@id"] ) {
          return r.thumbnail["@id"]
        } else {
          // console.log(r);
        }
  }).catch ((e) => {
    if (e.response) {
      console.log("response")
    } else if (e.request) {
      // JE CROIS QUE ON SE FAIT BLOQUER PAR LA BNF AVANT
      // MÊME D'AVOIR LANCÉ LA REQUÊTE PARCE QU'ON REFRESH TROP.
      console.log(`request on ${manifestUrl}`);
      console.log("complete log", e);
      console.log("resquest log", e.request);
      console.log("config log", e.config);
      console.log("**************************************************************");
    }
  })
}

export function manifestToThumbnail(manifestUrl) {
  /**
   * transform a manifest URL into an URL pointing to a thumbnail
   *
   * IIIF image format: {base}/{ark}/{vue}/{region}/{size}/{rotation}/{quality}
   * - base     : https://gallica.bnf.fr/iiif : {str}
   * - ark      : ark:/12148/btv1b53016210r   : {str}
   * - vue      : f1                          : {str}, "identification de l'image numérique, p.ex. le folio"
   * - region   : full                        : {int,int,int,int | full}
   * - size     : 200                         : {int,int | int}
   * - rotation : 0                           : {0..360}
   * - quality  : native.jpg                  : {native|gray|bitonal|color}
   * (`|` == `or`, `a,b,b` == multiple comma-separated values, `a..b` == range from `a` to `b)
   *
   * @param {str} manifestUrl: the URL to the `manifest.json` file
   * @returns {URL}: the URL object pointing to a thumbnail
   */
  manifestUrl = new URL(manifestUrl)
  manifestUrl.pathname = manifestUrl.pathname
                                    .replace(manifestUrl.pathname.split("/").at(-1)
                                             , "f1/full/200/0/native.jpg") ;
  return manifestUrl;
}