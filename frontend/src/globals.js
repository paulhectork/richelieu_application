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
    image    : urlToIconographyFile("qr1737e8b6cae934559b27126c02a034ba9_compress.jpg"),
    urlSlug  : "bourse"
  },
  { title    : "Portrait de rue",
    subtitle : "La rue Vivienne vue par ses contemporains",
    image    : urlToIconographyFile("qr1e88f013439424a58abe0ea8e9a3c9a2d_compress.jpg"),
    urlSlug  : "vivienne"
  },
  { title    : "Mode et architecture",
    subtitle : `Boutiques et magasins, expérimentations autour de la
                vente de <q>&nbsp;nouveautés&nbsp;</q>`,
    image    : urlToIconographyFile("qr15288251e8d6e4c97999a6c225e82d07c_compress.png"),
    urlSlug  : "mode"
  },
  { title    : "Menus et restaurants",
    subtitle : `Alimentation et culture visuelle des lieux de
                restauration du Palais-Royal aux Grands boulevards`,
    image    : urlToIconographyFile("qr183ed41474751443e8906971a5c905fd4_compress.jpg"),
    urlSlug  : "menu"
  },
  { title    : "La nature en ville",
    subtitle : "La botanisation autour de la rue Vivienne",
    image    : urlToIconographyFile("qr1e4c791a70c2940ebaf26373c02110007_compress.jpg"),
    urlSlug  : "nature"
  },
  { title    : "Les cafés du Palais-Royal",
    subtitle : `Consommations dans l'enceinte du Palais-Égalité
                à la fin du XVIII<sup>e</sup> siècle`,
    image    : urlToIconographyFile("qr122b4108b0d294b0c970ce518362abe70_compress.jpg"),
    urlSlug  : "cafe"
  },
  { title    : "La Banque de France",
    subtitle : `Économie et sociabilités des établissements environnants
                l'hôtel de Toulouse`,
    image    : urlToIconographyFile("qr1a9e147e32aae45abb15910b7601096f7_compress.jpg"),
    urlSlug  : "banque"
  },
  { title    : "Hôtels, passages et immeubles à boutiques",
    subtitle : "Habiter à travers les recueils d'architecture (1820-1830)",
    image    : urlToIconographyFile("qr1c53bb41a40be4f3dbe474a0dcb373c69_compress.jpg"),
    urlSlug  : "habiter"
  },
  { title    : "Le mobilier urbain",
    subtitle : "Reflet d'un quartier et de ses activités",
    image    : urlToIconographyFile("qr1a9a823e79d324dcdada5a7eb1b761de3_compress.jpg"),
    urlSlug  : "mobilier"
  },
  { title    : "Les théâtres et leurs images",
    subtitle : `Autour des spectacles&nbsp;: architectures,
                affiches et portraits`,
    image    : urlToIconographyFile("qr1359ddcecafb84650a459f1dcc8421e91_compress.jpg"),
    urlSlug  : "theatre"
  },
  { title    : "La patrimonialisation d'un quartier",
    subtitle : "Les protections des institutions au titre des Monuments historiques",
    image    : urlToIconographyFile("qr11eed3f6ea17f49a18cf6747a24a719f4_compress.png"),
    urlSlug  : "patrimonialisation"
  },
  { title    : "Les révolutions et le Palais-Royal",
    subtitle : "Images, imaginaires et mémoires",
    image    : urlToIconographyFile("qr13f4af1da6eee4caabdc8e39f30ac92a6_compress.jpg"),
    urlSlug  : "revolutions"
  },
  { title    : "Prostitutions",
    subtitle : "Les logiques spatiales du plus vieux métier du monde",
    image    : urlToIconographyFile("qr1f7350ffbb83543fe91938234376444d0_compress.jpg"),
    urlSlug  : "prostitution"
  },
  { title    : "Les marginaux du Palais-Royal",
    subtitle : "Donner à voir ce que l'on ne souhaite pas voir",
    image    : urlToIconographyFile("qr1d53e6b37c6334721b476381fec062660_compress.png"),
    urlSlug  : "marginaux" }
]