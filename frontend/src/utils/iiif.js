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
 * @param {string} manifestUrl: the URL to the `manifest.json` file
 * @returns {URL}: the URL object pointing to a thumbnail
 */
export function manifestToThumbnail(manifestUrl, callBackImgUrl) {
  axios.get(manifestUrl)
       .then((r) => {
        const manifest = r.data;
        const imgUrl = manifest.sequences[0]
                               .canvases[0]
                               .images[0]
                               .resource
                               ["@id"];

        //return imgUrl
        console.log(imgUrl);
        return imgUrl.includes("/full/full/")
               ? imgUrl.replace("/full/full/", "/full/500/")  // redimension to 500px
               : callBackImgUrl                               // can't create a thumbnail => return the callback
       })
  /*
  manifestUrl.pathname = manifestUrl
                         .pathname
                         .replace( manifestUrl.pathname.split("/").at(-1)
                                 , "f1/full/200/0/native.jpg");
  */
  //return manifestUrl;
  //return "";
}