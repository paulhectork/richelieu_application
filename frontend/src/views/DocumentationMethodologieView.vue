<template>
  <div class="textpage-outer-wrapper">
    <h1>Documentation technique</h1>
    <h2><i>Rich.Data</i>, un écosystème numérique pour l'histoire urbaine</h2>

    <div class="textpage-text-wrapper">
      <p><i>RICH.DATA</i>, le volet numérique du projet, permet de
        répondre à aux questionnements scientifiques grâce
        à une approche protéiforme des données.
      </p>
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
                            (crédits: Marina Hervieu)."
      ></StaticImageDisplay>
      <p>Le site du projet est une interface de consultation
        de sa base de données. Celui-ci propose plusieurs
        lectures du quartier, en accord avec les axes de recherches
        développés. On y trouve&nbsp;:
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
    </div>

    <StaticImageDisplay :img-url="archUrl"
                        img-alt="Architecture du site Quartier Richelieu"
                        img-legend="Architecture du site <i>Quartier Richelieu</i>"
    ></StaticImageDisplay>
  </div>
</template>


<script setup>
import StaticImageDisplay from "@components/StaticImageDisplay.vue";

const archUrl = new URL("/other/application_architecture_fr.png", __STATICS_URL__);
const pipUrl = new URL("/other/pipeline_main.png", __STATICS_URL__);
const dbUrl = new URL("/other/richelieu_db_model_bg.png", __STATICS_URL__);


console.log(archUrl);
</script>


<style scoped>
.textpage-outer-wrapper {
  max-width: 100%;
}
</style>