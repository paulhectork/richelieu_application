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

/**
 * texts presenting theme categories, with 1 text / category.
 * moved here because the html clogged `ThemeOrNamedEntityIndexView`.
 */
export const themeCategoryPresentation = {
  "s-habiller": `
    La question de l'habillement revêt des significations
    plurielles dans le quartier Richelieu. Elle peut d'abord
    être comprise comme un acte de confection pour autrui,
    en écho avec la forte concentration de tailleurs, de
    marchandes de mode et de nouveautés dans le quartier,
    acteurs majeurs du développement économique de la ville.
    En parallèle, ce savoir-faire, ancré dans ce territoire
    depuis le XVIII<sup>e</sup> siècle, se redouble d'un véritable
    faire-savoir auquel les éditeurs et libraires locaux
    participent en publiant et vendant bon nombre de gravures
    de mode. Haut lieu de la promenade urbaine, mais aussi
    de l'activité salariale, ce cas d'étude permet de retracer
    l'essor et les mutations socio-économiques et matérielles
    de la culture des apparences en milieu urbain. Enfin,
    cette activité, loin de se cantonner aux corps, contribue
    aussi à draper la ville d'un épais et éclectique manteau
    de boutiques, contribuant alors à lier cette notion
    à sa spatialité, son architecture et sa propension
    à faire espace public.`,
  "se-divertir": `
    La densité et la variété des activités de divertissement
    qui ont eu lieu dans le quartier Richelieu se perçoivent
    à travers l'abondante production graphique qu'elles
    ont suscité. Les grands et petits spectacles joués
    dans l'espace public ou derrière les portes de la dizaine
    de salles concentrées à l'échelle de quelques rues,
    sont révélés à l'analyse des affiches promotionnelles,
    des vues et des photographies liées aux représentations.
    Plusieurs gravures et dessins rappellent également
    l'importance de ces lieux en matière de sociabilités
    et plus précisément de mondanités. L'iconographie autour
    du théâtre renforce cette image d'une institution dont
    le rapport au loisir était loin d'être cantonné à la
    seule performance artistique de la scène. La musique,
    notamment sous la forme de partitions publiées chez
    les éditeurs spécialisés installés rue Vivienne, fait
    aussi écho aux salles de concert et aux soirées musicales.
    Enfin, l'activité des théâtres, à travers les tickets
    d'entrée et la production de décors ou de costumes,
    éclaire le parcours de certains acteurs et actrices.`,
  "representer": `
    Ce thème est articulé autour des différents supports
    rendant présent à la vue, mais aussi à l'esprit le
    quartier Richelieu dans toute sa volubilité et sa volatilité.
    Bien avant d'être le réceptacle de l'Agence France-Presse,
    anciennement Havas, les alentours de la place de la
    Bourse et du Palais-Royal sont des espaces où le papier
    règne en maître, rendant ainsi nécessaire d'intégrer
    les éditeurs, imprimeurs et titres de presse à notre
    champ d'étude afin de restituer les réseaux du papier
    dans leur temporalité et leur spatialité. Représenter,
    c'est aussi donner à voir sous la forme d'un substitut,
    leitmotiv des nombreux photographes qui vendent et
    produisent des images du quartier et de ses activités,
    esquissant ainsi des clés de lecture quant à la dimension
    sociale, matérielle et symbolique de ce territoire.
    Représenter est également un moyen d'attirer l'attention
    sur une réalité, parfois peu glorieuse, prérequis des
    caricatures qui, par un humour au vitriol, permettent
    d'infléchir le regard sur les mœurs urbaines. Enfin,
    représenter revient à exprimer matériellement une réalité
    abstraite, voire fantasmée, grand œuvre des cartes
    postales dont les angles de vue orientent les perceptions
    du quartier, contribuant à le figer dans son image
    d'Épinal.`,
  "s-informer": `
    L'information est, dans ce cadre thématique, intimement
    liée à la dimension politique et historique des différents
    évènements survenus dans le quartier Richelieu. Si
    l'iconographie constitue une fenêtre presque anecdotique
    et ponctuelle sur certains faits qui se sont déroulés
    dans le quartier, à l'instar de bals ou de rencontres
    sportives, elle contribue aussi à donner une forme,
    une structure signifiante à des moments marquants de
    l'Histoire nationale. Parmi ces épisodes cruciaux,
    on dénombre la Révolution française, la révolution
    de juillet 1830, la révolution de 1848 et enfin, la
    Commune de Paris. Le fait d'informer peut être compris
    comme une transmission ou une communication de renseignements
    dans le cas de la Révolution française, dont nous pouvons
    restituer par l'image une chronologie fine. Mais il
    n'en va pas de même pour d'autres révolutions. Le cas
    de la Commune est emblématique de la façon dont l'iconographie
    se plaît à nourrir la désinformation par l'exagération,
    notamment au sujet de l'incendie du Palais-Royal en
    mai 1871. Ce thème accompagne alors les relectures
    historiographiques du récit national par l'entremise
    d'une approche située de la ville.`,
  "consommer": `
    La notion de consommation fait
    écho à la forte densité des activités économiques recensées dans
    les rues du quartier au XIX<sup>e</sup> siècle. La bourse installée au palais
    Brongniart est l'emblème du dynamisme commercial qui s'empare des
    rues adjacentes où se déroulent diverses transactions&nbsp;:
    banques, alimentation, vente d'objets, ou hygiène et soins du corps.
    Les secteurs sont variés et aisément identifiables à la lecture des
    enseignes, devantures de boutiques, et affiches promotionnelles qui
    abondent dans le corpus iconographique. Si les noms des commerces
    et les marchandises proposées sont parfois au premier plan des
    documents, une analyse plus approfondie des alignements de boutiques
    placés en toile de fond de certaines estampes et photographies
    améliore notre compréhension de la ville commerçante. Les gammes de
    prix et les prestations mises en avant par les commerçants
    fournissent des informations supplémentaires sur les mentalités
    de la réclame publicitaire et sur l'évolution du niveau de vie.
    Les brevets d'invention quant à eux soulignent les innovations à
    l'œuvre et la dimension créatrice du développement économique.`,
  "habiter": `
    Habiter est envisagé au sens
    large, englobant à la fois les espaces privés et publics qui
    composent le cadre de la vie quotidienne des citadins et des
    citadines qui habitent ou fréquentent le quartier. Le dialogue
    entre l'espace public, la nature, et l'évolution des formes
    architecturales, qu'elles soient existantes ou projetés, se révèle
    à travers divers médiums, des estampes aux photographies.
    L'architecture domestique, tout comme celle des monuments, est
    explorée à travers des documents graphiques produits par des
    architectes et des entrepreneurs identifiés et met en lumière
    aussi bien les grands édifices institutionnels que les habitations
    plus modestes. Le laboratoire de l'urbain s'enrichit par une
    attention portée à l'équipement de la ville, à travers la
    modernisation du mobilier urbain, l'amélioration des réseaux et
    moyens de transports, et la représentation de chantiers&nbsp;: un
    dynamisme qui capte l'attention des observateurs. C'est un aperçu
    de la fabrique de la ville, telle qu'elle a été conçue et vécue
    par ses contemporains.`,
}