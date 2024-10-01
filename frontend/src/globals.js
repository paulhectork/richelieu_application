import "@plugins/modernizr.js";

import { urlToIconographyFile } from "@utils/url.js";

/**************************************************/

/**
 * static variables that are globally available to the app
 * and that are exposed/usable by th client (=> more permissive
 * than constants defined in `vite.config.js`)
 */


/**
 * list to order `cartography` and `address` items related to a place,
 * based on the value of sql column:
 * `cartography.map_source`, `address.source`, `place.vector_source`.
 * reordering can be done using:
 * >>> arrayToSort.sort((a,b) =>
 * ...   cartographySourcePriority.indexOf(a.source) - sourcePriority.indexOf(b.source) );
 */
export const cartographySourcePriority = [ "parcellaire1900"
                                         , "vasserot"
                                         , "feuille"
                                         , "contemporain" ];

/**
 * values of database columns
 * `cartography.map_source`, `address.source`, `place.vector_source`
 * mapped to a human readable name
 */
export const cartographySourceMapper = {
  vasserot        : "Atlas Vasserot, 1810-1836",
  parcellaire1900 : "Plan parcellaire de Paris, fin XIX<sup>e</sup> s.",
  billaud         : "Plan de la galerie Colbert (années 1830)",
  contemporain    : "Parcellaire contemporain",
  feuille         : "Parcelles <q>&nbsp;à la feuille&nbsp;</q>, 1809-1854"
}

/**
 * is this a touchable browser?
 */
export const hasTouch = Modernizr.touchevents || Modernizr.pointerevents;

/**
 * listen to just click on non-touchscreen,
 * click+touchend on devices with touchscreen.
 *
 * see: https://web.dev/articles/mobile-touchandmouse
 */
export const clickOrTouchEvent = hasTouch ? "click touchend" : "click";

/**
 * a JSON representation of all articles: their title and subtitle,
 * an URL pointing to an image and a slug to build an URL redirecting
 * to the article's main page
 */
export const articles = [
  { title    : "La bourse et sa place",
    subtitle : `Le temple de l'argent en perspective&nbsp;: activités et
                représentations au XIX<sup>e</sup> siècle`,
    image    : "https://gallica.bnf.fr/iiif/ark:/12148/btv1b53150759s/f1/full/2000/0/native.jpg",
    urlSlug  : "bourse" },
  { title    : "Portrait de rue",
    subtitle : "La rue Vivienne vue par ses contemporains",
    image    : "https://gallica.bnf.fr/iiif/ark:/12148/btv1b90087110/f1/full/2000/0/native.jpg",
    urlSlug  : "vivienne" },
  { title    : "Mode et architecture",
    subtitle : `Boutiques et magasins, expérimentations autour de la
                vente de <q>&nbsp;nouveautés&nbsp;</q>`,
    image    : urlToIconographyFile("qr15288251e8d6e4c97999a6c225e82d07c.png"),
    urlSlug  : "mode" },
  { title    : "Menus et restaurants",
    subtitle : `Alimentation et culture visuelle des lieux de
                restauration du Palais-Royal aux Grands boulevards`,
    image    : "https://apicollections.parismusees.paris.fr/sites/default/files/styles/4k/collections/atoms/images/CAR/aze_carg002054_001.jpg?itok=ESLjKoNN",
    urlSlug  : "menu" },
  { title    : "La nature en ville",
    subtitle : "La botanisation autour de la rue Vivienne",
    image    : urlToIconographyFile("qr1e4c791a70c2940ebaf26373c02110007.jpg"),
    urlSlug  : "nature" },
  { title    : "Les cafés du Palais-Royal",
    subtitle : `Consommations dans l'enceinte du Palais-Égalité
                à la fin du XVIII<sup>e</sup> siècle`,
    image    : "https://apicollections.parismusees.paris.fr/sites/default/files/styles/4k/collections/atoms/images/CAR/aze_carg010953_001.jpg?itok=n6xhEvvn",
    urlSlug  : "cafe" },
  { title    : "La Banque de France",
    subtitle : `Économie et sociabilités des établissements environnants
                l'hôtel de Toulouse`,
    image    : "httnps://apicollections.parismusees.paris.fr/sites/default/files/styles/4k/collections/atoms/images/CAR/lpdp_144183-16.jpg?itok=WAjQ3-3i",
    urlSlug  : "banque" },
  { title    : "Hôtels, passages et immeubles à boutiques",
    subtitle : "Habiter à travers les recueils d'architecture (1820-1830)",
    image    : "https://apicollections.parismusees.paris.fr/sites/default/files/styles/4k/collections/atoms/images/CAR/aze_card16711_001.jpg?itok=bH0JRhsX",
    urlSlug  : "habiter" },
  { title    : "Le mobilier urbain",
    subtitle : "Reflet d'un quartier et de ses activités",
    image    : urlToIconographyFile("qr1f0c214cc309846228da9f7262144b638_compress.jpg"),
    urlSlug  : "mobilier" },
  { title    : "Les théâtres et leurs images",
    subtitle : `Autour des spectacles&nbsp;: architectures,
                affiches et portraits`,
    image    : urlToIconographyFile("qr1359ddcecafb84650a459f1dcc8421e91.jpg"),
    urlSlug  : "theatre" },
  { title    : "La patrimonialisation d'un quartier",
    subtitle : "patrimonialisation",
    image    : "https://apicollections.parismusees.paris.fr/sites/default/files/styles/4k/collections/atoms/images/CAR/aze_carph015719_001.jpg?itok=JAeUjy5H",
    urlSlug  : "patrimonialisation" },
  { title    : "Les révolutions et le Palais-Royal",
    subtitle : "Images, imaginaires et mémoires",
    image    : urlToIconographyFile("qr13f4af1da6eee4caabdc8e39f30ac92a6.jpg"),
    urlSlug  : "revolutions" },
  { title    : "Prostitutions",
    subtitle : "Les logiques spatiales du plus vieux métier du monde",
    image    : urlToIconographyFile("qr1f7350ffbb83543fe91938234376444d0.jpg"),
    urlSlug  : "prostitution" },
  { title    : "Les marginaux du Palais-Royal",
    subtitle : "Donner à voir ce que l'on ne souhaite pas voir",
    image    : urlToIconographyFile("qr1d53e6b37c6334721b476381fec062660.png"),
    urlSlug  : "marginaux" }
]