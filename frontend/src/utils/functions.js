/**********************************************
 *         globally useful functions          *
 **********************************************/

export function fnToCartographyFile(fn) {
  /**
   * create an URL to an image on the remote server
   * from the cartography table.
   * @param {str} fn : the filename to the image
   * @returns        : the URL to that image
   */
  return new URL(`/richelieu/imagefiles/cartography/${fn}`, __SERVER_URL__);
}