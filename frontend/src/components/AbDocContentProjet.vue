<template>

  <div class="textpage-text-wrapper">
    <p>Le projet de recherche <i>Richelieu. Histoire du quartier</i>
      (1750-1950) est né de la collaboration de plusieurs
      institutions publiques situées au cœur du II<sup>e</sup>
      arrondissement de Paris&nbsp;:
      <a href="https://www.bnf.fr/fr">la Bibliothèque nationale de France</a>,
      <a href="https://www.dfk-paris.org/">le Centre allemand d'histoire de l'art</a>,
      <a href="https://www.centrechastel.sorbonne-universite.fr/">le centre Chastel</a>,
      <a href="https://www.chartes.psl.eu/">l'École nationale des chartes&mdash;PSL</a>,
      <a href="https://www.inha.fr/">l'Institut national d'histoire de l'art</a> et
      <a href="https://www.epfl.ch/fr/">l'École polytechnique fédérale de Lausanne</a>.
      Ce projet étudie le quartier
      communément désigné sous le nom de <q>&nbsp;Richelieu&nbsp;</q>,
      à travers ses dynamiques architecturales, humaines
      et économiques et en croisant des sources iconographiques
      et cartographiques, à l'échelle du long XIX<sup>e</sup>
      siècle.
    </p>
    <p>Cet ensemble de rues se situe entre le I<sup>er</sup> et le
      II<sup>e</sup> arrondissement, d'est en ouest de la
      place des Victoires à l'avenue de l'Opéra, et du sud
      au nord du Palais-Royal aux Grands Boulevards. Elles
      englobent des lieux et des monuments qui, par leur
      histoire commune, sont représentatifs de Paris en tant
      que capitale culturelle. Ces espaces sont également
      liés par des réseaux professionnels et interpersonnels,
      ainsi que par des effets de proximités révélés par
      l'étude des sources visuelles.
    </p>
    <p>Le projet prend pour axe principal le tracé nord-sud
      reliant le Palais-Royal et la Bourse par la rue Vivienne,
      incluant l'îlot occupé par le siège de la Banque de
      France entre la rue Croix-des-Petits-Champs et la rue
      de Valois. Cet échantillon de quatre types d'espaces
      urbains adjacents, est documenté à partir d'un premier
      corpus de cartes et de cadastres permettant de retracer
      précisément l'évolution du tissu urbain et de
      <RouterLink to="/iconographie">spatialiser les 4217 documents
        iconographiques</RouterLink> numérisés réunis.
      Cet ensemble allant des dessins et photographies aux
      jetons de commerces et cartes de visite, a été constitué
      à partir de collections numérisées d'institutions publiques
      telles que la Bibliothèque nationale de France, le
      British Museum, les Archives nationales, ou encore
      les Archives, bibliothèques spécialisées et musées
      de la Ville de Paris. Dès la fin du XVIII<sup>e</sup>
      siècle, avec l'essor de l'imprimé, Paris suscite en
      effet une prolifération d'images offrant un témoignage
      précieux de ses transformations. Au-delà de leur valeur
      documentaire, la prolifération de ces images permet
      d'esquisser les prémices de la mise en place d'une
      culture de masse.
    </p>
    <p>Chaque bâtiment, commerce, lieux de production, ou
      évènement représenté a été localisé sur une ou plusieurs
      parcelles dans la <RouterLink to="/cartographie">cartographie
        numérique</RouterLink>. Ce corpus
      varié a été ainsi systématiquement identifié, daté
      et localisé. Tous les documents ont été intégrés à
      un ou plusieurs sous-corpus thématiques
      (<RouterLink to="/theme/qr1bc9332b2db5f45ee9dec8433307f8e7f">espace public</RouterLink>,
      <RouterLink to="/theme/qr119ea3994f787479095683b7da89ccd69">jardin</RouterLink>,
      <RouterLink to="/theme/qr1257e5a9d3d474555a8ea470d0decacd0">chantier</RouterLink>,
      <RouterLink to="/theme/qr1d8b0b911dd7b43ff825c908263e1fcc1">mœurs</RouterLink>,
      <RouterLink to="/theme/qr1ce0a74ab786b4b52832f0abd0c9de4ce">argent</RouterLink>,
      <RouterLink to="/theme/qr144818ee48b4f42b881c820577f1b4740">Révolution française</RouterLink>,
      etc.), et rattachés
      à des sujets spécifiques
      (<RouterLink to="/entite-nommee/qr166e8678c2aa8473ea134e722bff13611">Palais Brongniart</RouterLink>,
      <RouterLink to="/entite-nommee/qr17195ba42b91846dfa62756ab9b36e220">bureau d'omnibus</RouterLink>,
      <RouterLink to="/entite-nommee/qr19529e0fdc0d340b39f34a4c48f364f9f">Palais de Cristal</RouterLink>
      etc.).
    </p>
    <p>L'analyse
      inédite de ce vaste ensemble de sources hétérogènes
      fait apparaître les relations, matérielles et immatérielles
      entre architecture et histoire sociale, histoire culturelle,
      activités économiques et histoire des mentalités, à
      travers <RouterLink to="/article">14 articles illustrés</RouterLink>. et grâce
      aux renvois créés entre les documents. Les interactions
      entre photographes et actrices, commerces et réseaux
      de transports, ainsi que l'influence réciproque entre
      les formes architecturales, les parcours de flâneries,
      l'espace public et les représentations visuelles, émergent
      pour signifier le dynamisme d'une capitale moderne.
    </p>
    <p>Enfin, <RouterLink to="/recherche">la base de données</RouterLink>
      permet d'explorer ces modes
      de fonctionnement sous un angle plus ciblé en offrant
      la possibilité d'analyser de manière locale et concrète
      la réalité de cette production, par parcelle, par nom,
      par commerce, etc.
    </p>
  </div>

</template>


<script setup>
import { onMounted } from "vue";

/****************************************/

const emit = defineEmits(["h2"]);
const subtitle = "Le projet de recherche <i>Richelieu. Histoire du quartier</i>";

/****************************************/

onMounted(() => emit("h2", subtitle))
</script>


<style scoped>

</style>
