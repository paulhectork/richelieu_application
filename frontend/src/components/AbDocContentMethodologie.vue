<template>
  <div class="textpage-text-wrapper">
    <h3 id="abdoc-richdata">
      <i>Rich.Data</i>, un écosystème numérique pour
      l'histoire urbaine</h3>

    <p><i>RICH.DATA</i>, le volet numérique du projet, permet de
      répondre à aux questionnements scientifiques grâce
      à une approche protéiforme des données.
    </p>
    <p>La colonne vertébrale des développements numériques
      du projet consiste en une chaîne de traitement de la
      donnée, depuis des corpus de recherche vers la présente
      application Web.
    </p>
    <ol>
      <li>Les corpus iconographique et cartographique
        ont été produits <q>&nbsp;manuellement&nbsp;</q>. Le corpus
        des bottins et annuaires du XIX<sup>e</sup> a été produit
        en utilisant des technologies d'apprentissage machine et
        de reconnaissance optique de caractères (OCR). Ce corpus,
        constitué avant 2022 sous la supervision d'Isabella
        Di Lenardo, n'est pas accessible depuis la présente plateforme.
      </li>
      <li>À partir ce ces corpus de recherche, il s'agit d'automatiser
        la création d'une base de données, via un processus de traitement,
        de croisement et d'hybridation des données.</li>
      <li>Enfin, la présente plateforme est à la fois une plateforme
        d'exploration et de valorisation des données et un objet éditorial,
        visant à permettre le croisement entre recherche en humanités, données
        et analyses compoutationnelles.
      </li>
      <li>Autour de cette colonne vertébrale, de nombreux autres outils ont
        pu être développées. Parmi eux se trouvent des modèles 3D produits à partir de
        sources historiques ainsi que des
        <a href="https://gitlab.inha.fr/snr/rich.data/auxiliaires/networks">
          analyses de réseaux</a>.
      </li>
    </ol>
    <StaticImageDisplay :imgUrl="pipUrl"
                        imgAlt="Schéma représentant la chaîne de traitement du projet. Celle-ci est composée de 3 étapes: production, migration et exposition des données."
                        imgLegend="Chaîne de traitement du projet <i>Richelieu</i>"
    ></StaticImageDisplay>
    <p>Pour mieux comprendre l'évolution du parcellaire
      du quartier, un système d'information géographique
      (SIG) a été utilisé afin de spatialiser différentes
      sources cartographiques produites au cours du long
      XIX<sup>e</sup> siècle. Ce travail a permis d'identifier
      et de géo-référencer un corpus de plans cadastraux
      de Paris (1809-1854, Archives nationales, CP/F/31/3
      à CP/F/31/14). Un découpage vectoriel de ces sources
      a permis de retracer à l'échelle de la parcelle les
      évolutions du bâti parisien des rues que nous avons
      sélectionnées. Cette approche géohistorique permet
      d'appréhender le quartier comme une succession de couches
      historiques dont il est possible de retracer l'évolution.
    </p>
    <p>Ce corpus cartographique comprend 495 parcelles issues
      de 5 sources cartographiques différentes et correspond
      à 331 lieux, eux-mêmes connectés avec les 4217 documents
      iconographiques. Ces deux corpus complémentaires sont
      croisés à l'aide d'une base de données relationnelle
      (PostgreSQL). Ces sources ont été intégrées dans une
      base de données composée de 23 tables et plus de 100
      000 lignes, dans l'objectif de proposer au public une
      lecture des résultats du projet sous différents angles.
      Afin de garantir l'interopérabilité de nos données,
      le modèle de données utilisé est compatible avec le
      Dublin Core.
    </p>
    <StaticImageDisplay :imgUrl="dbUrl"
                        imgAlt="Schéma représentant le modèle de données de
                          la base de données du projet Richelieu. Histoire du quartier"
                        imgLegend="Schéma du modèle de données du projet <i>Richelieu</i>
                          (crédits&nbsp;: Marina Hervieu)."
    ></StaticImageDisplay>
    <p>Plus qu'une interface de consultation de la base de données du projet,
      la présente plateforme est conçu comme un objet éditorial hybrique, croisant
      l'exposition numérique de sources et la recherche et l'analyse historique
      de celles-ci. Le site propose plusieurs lectures du quartier, en accord
      avec les axes de recherches développés. On y trouve&nbsp;:
    </p>
    <ul>
      <li>Un accès guidé au travers
        <RouterLink to="/cartographie">d'une carte</RouterLink>&nbsp;,
        <RouterLink to="/article">d'articles thématiques</RouterLink>
        rédigés par les membres du projet&nbsp,
        <RouterLink to="/entite-nommee">des entités nommées</RouterLink>
        et <RouterLink to="/theme">des thèmes</RouterLink>
        identifiés dans chaque image.
      </li>
      <li>Un accès aux données grâce à un
        <RouterLink to="/recherche">moteur de recherche avancée</RouterLink>.
      </li>
      <li>Un accès à la donnée brute, à l'aide d'une
        <RouterLink to="/documentation/api">API REST</RouterLink>,
        qui facilite la réutilisation de l'ensemble de
        nos productions dans une démarche de science ouverte.
      </li>
    </ul>
    <p>Dans une démarche de science ouverte, l'intégralité
      des images est accessible en
      <a href="https://iiif.io/"><i>IIIF (International Image
      Interoperability Framework)</i></a>, un ensemble de standards
      visant à uniformiser les modalités de partage des images
      patrimoniales afin d'encourager leur réutilisation&nbsp;;
      le site centralise donc des ressources issues de plusieurs
      entrepôts de données institutionnels afin de privilégier
      la réutilisation des ressources, tout en garantissant
      la traçabilité des données vers les institutions conservant
      les images. A ce titre, le projet a été récompensé
      en 2023 par le prix
      <a href="https://www.enseignementsup-recherche.gouv.fr/fr/remise-des-prix-science-ouverte-des-donnees-de-la-recherche-93729">
        <q>&nbsp;Science ouverte des données de recherche&nbsp;</q></a>
      dans la catégorie
      <q>&nbsp;réutilisation de données&nbsp;</q>
      du Ministère de l'enseignement supérieur et de la Recherche.
    </p>
    <p>La plateforme est développée à l'aide des <i>frameworks</i> Flask (Python)
      et Vue.JS (JavaScript). Elle est composée d'un <i>backend</i> chargé de communiquer
      avec la base de donnée, de mettre en forme les données renvoyées par celles-ci et
      de les envoyer au <i>frontend</i>. Celui-ci consiste en l'interface graphique
      de l'application&nbsp;: c'est avec lui qu'est composée l'interface utilisateur.
      Il est aussi chargé de mettre en forme les données brutes reçues du <i>backend</i>.
      Afin de permettre la réutilisation des données produites
      par le projet, cette plateforme dispose d'une
      <RouterLink to="/documentation/api">API ouverte au public</RouterLink>. Le code
      source de l'application est disponible sur le
      <a href="https://gitlab.inha.fr/snr/rich.data/application">
        GitLab de l'Institut national d'histoire de l'art</a>.
    </p>
    <StaticImageDisplay :img-url="archUrl"
                        img-alt="Architecture du site Quartier Richelieu"
                        img-legend="Architecture du site <i>Quartier Richelieu</i>"
    ></StaticImageDisplay>
  </div>

  <div class="textpage-text-wrapper">
    <h3 id="abdoc-3D">
      Du corpus d'images à la modélisation 3D</h3>
    <h4>Par Colin Prudhomme</h4>
    <p>Le rapport au lieu qu'entretient le vaste corpus
      de sources recueillies dans le cadre du projet Richelieu
      présente une grande diversité, non seulement due aux
      différents modes de production utilisés par leurs auteurs
      et autrices mais aussi par la façon dont ils ont choisi
      de lui faire porter l'éventuel message qu'ils souhaitent
      transmettre. Ainsi, si certaines sources se réfèrent
      au lieu de manière textuelle, par la mention d'une
      adresse, la description d'une place ou la commémoration
      d'un évènement par exemple, d'autres vont figurer des
      perspectives, des élévations, voire des vues géométrales
      obtenues grâce à une caméra.
    </p>
    <p>Ces dernières permettent ainsi d'appréhender des
      informations sur la deuxième et troisième dimension
      du lieu. On peut alors envisager de modéliser leur
      lien avec celui-ci non seulement en connectant la source
      aux entités nommées qu'elle représente dans une base
      de données mais aussi au travers de divers modes de
      spatialisation, en positionnant la source dans une
      représentation tridimensionnelle de l'espace. Afin
      d'explorer cette représentation nous avons choisi de
      nous concentrer sur la place de la Bourse, avec un
      corpus de près de 700 images afférentes.
    </p>
    <p>La première façon choisie au sein du projet pour
      mettre en lien ces éléments a été de positionner les
      sources dans une représentation cartographique de l'espace,
      au moyen d'un Système d'Information Géographique (SIG).
      Les SIG sont un type de système d'information permettant
      de stocker, représenter, analyser et visualiser des
      données relatives à l'espace dans un référentiel généralement
      2D choisi par l'utilisateur. On peut y modéliser l'information
      géographique sous forme d'objets ponctuels, linéaires
      ou polygonaux, regroupés dans des couches et associés
      à une table attributaire au sein de laquelle chaque
      ligne permet de renseigner les métadonnées associées
      à ces objets.
    </p>
    <p>L'étape initiale de cette spatialisation des sources
      iconographiques représentant l'espace a donc été la
      projection des plans parcellaires présents dans les
      sources du projet Richelieu au sein de ce référentiel,
      puis de modéliser à partir de ceux-ci les parcelles
      sous forme de couches de polygones. Une fois ces différentes
      strates chronologiques représentées, il est possible
      d'y positionner de façon approximative les sources,
      en leur donnant un emplacement et une orientation.
      Ce processus est rendu complexe par le fait que certaines
      sources, des caricatures par exemple, présentent une
      vision schématisée ou déformée de l'espace qui ne permet
      pas toujours d'attribuer un emplacement même si un
      lieu est représenté.
    </p>
    <p>Ce processus demande un travail de reconstitution
      de la chronologie, à la fois pour situer une source
      dans le temps et à la fois parce que situer les sources
      relativement au bâti permet de constater des évolutions
      des élévations ou de l'espace urbain qui ne se reflètent
      pas forcément dans celle des emprises au sol. Une fois
      constitué, ce SIG permet de faire émerger un certain
      nombre de caractéristiques du corpus, en particulier
      la présence de compositions communes à différents auteurs
      dans le temps et les choix d'objets représentés.
    </p>
    <StaticImageDisplay :imgUrl="col1Url"
                        imgAlt="Capture d'écran du SIG localisant les
                                prises de vue des différents documents
                                cartographiques sur la place de la Bourse,
                                au dessus de la couche de polygones correspondant
                                au parcellaire de 1897, avec en fond une carte
                                représentant le percement de la rue du Quatre Septembre"
                        imgLegend="Documents iconographiques positionnés
                                  dans le SIG au dessus de la couche de polygones du
                                  parcellaire de 1897, au dessus du plan du percement
                                  de la rue du Quatre Septembre
                                  (crédits&nbsp;: Colin Prudhomme)"
    ></StaticImageDisplay>
    <p>A la suite de la constitution de ce SIG, nous nous
      sommes intéressés à la troisième dimension contenue
      dans ces images en envisageant la construction d'un
      SIG tridimensionnel sur la base du positionnement de
      ces sources, en utilisant non plus seulement les sources
      cartographiques mais aussi un relevé 3D que nous avons
      effectué de la place de la Bourse au moyen d'un scanner
      lasergrammétrique, qui permet d'obtenir un relevé de
      points très précis de cet espace.
    </p>
    <p>Celui-ci nous a ensuite servi à repositionner certains
      documents du corpus iconographique, sur la base des
      emplacements déterminés sur le SIG. En effet, pour
      replacer le plus grand nombre de documents possible,
      nous avons envisagé de positionner en priorité les
      documents représentant assez de bâti actuel pour que
      cette étape soit facile, mais aussi assez de bâti ancien
      pour nous permettre de modéliser approximativement
      celui-ci, afin que ce modèle puisse à son tour servir
      de référence pour placer d'autres documents.
      Un algorithme tenant compte de ces deux contraintes
      a donc été développé pour identifier l'ordre de repositionnement
      des documents.
    </p>
    <StaticImageDisplay :imgUrl="col2Url"
                        imgAlt="Capture d'écran du logiciel de modélisation 3D
                                montrant le processus de reconstruction du Palais
                                de Cristal à partir d'une photographie ancienne
                                repositionnée"
                        imgLegend="Processus de reconstruction des bâtiments du
                                  Palais de Cristal à partir d'une photographie
                                  ancienne repositionnée (crédits&nbsp;:
                                  Colin Prudhomme)"
    ></StaticImageDisplay>
    <p>Nous nous sommes prioritairement focalisés sur les
      archives photographiques, étant donné que leurs caractéristiques
      optiques facilitent le positionnement. En utilisant
      un logiciel de modélisation 3D, nous avons spatialisé
      le modèle 3D extrait du nuage de points, puis nous
      y avons positionné des objets reproduisant les caractéristiques
      optiques des caméras, pour ensuite pouvoir modéliser
      certains éléments disparus. Cette dernière étape s'est
      avérée extrêmement complexe, du fait de la difficulté
      de retrouver précisément les caractéristiques optiques
      des appareils (c'est-à-dire, la manière dont ces appareils
      déforment l'espace). Elle a toutefois permis de superposer
      la vue actuelle à une vue plus ancienne pour certaines
      images (Fig. 3). Cette étape permet ensuite d'obtenir
      encore plus d'informations sur les choix réalisés par
      les artistes, mais aussi sur les méthodes techniques
      employées pour les prises de vues, et révéler des aspects
      méconnus d'un paysage urbain profondément transformé
      depuis l'époque à laquelle il a été dépeint.
    </p>
    <StaticImageDisplay :imgUrl="col3Url"
                        imgAlt="Capture d'écran du logiciel de modélisation 3D
                                illustrant le recadrage d'une photographie de groupe
                                prise depuis les escaliers du Palais Brongniart sur
                                un scan 3D de la place de la Bourse dans son
                                état actuel"
                        imgLegend="Recalage d'une photographie de groupe prise
                                  depuis les escaliers du Palais Brongniart sur
                                  un scan 3D de la place de la Bourse dans son
                                  état actuel (crédits&nbsp;: Colin Prudhomme)"
    ></StaticImageDisplay>
  </div>

</template>


<script setup>
import { onMounted } from "vue";

import StaticImageDisplay from "@components/StaticImageDisplay.vue";

/****************************************/

const dbUrl   = new URL("other/richelieu_db_model_bg.png", __STATICS_URL__);
const pipUrl  = new URL("other/pipeline_main.png", __STATICS_URL__);
const archUrl = new URL("other/application_architecture_fr.png", __STATICS_URL__);
const col1Url = new URL("other/colin_article3d_image1.jpeg", __STATICS_URL__)
const col2Url = new URL("other/colin_article3d_image2.jpeg", __STATICS_URL__)
const col3Url = new URL("other/colin_article3d_image3.jpeg", __STATICS_URL__)

const emit     = defineEmits(["h2"]);
const subtitle = "Méthodologie numérique";

/****************************************/

onMounted(() => emit("h2", subtitle))
</script>


<style scoped>

</style>
