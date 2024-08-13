<template>

  <div class="article-header">
    <h1>Le mobilier urbain</h1>
    <h2>Reflet d'un quartier et de ses mobilités</h2>
  </div>

  <div class="article-body">
    <p>Depuis le XIX<sup>e</sup> siècle, le quartier Richelieu fait office d'épicentre
      des politiques urbaines relatives au mobilier urbain. Popularisée par JC Decaux
      dans les années 1960, cette notion revêt une définition administrative, soit
      <q>&nbsp;l'ensemble des objets ou dispositifs publics installés dans l'espace public
        <ButtonEllipsis data-footnote="1" class="footnote-pointer"></ButtonEllipsis>&nbsp;
      </q>.
      À cette définition se superposent un volet légal, comme vecteur de normes, et un
      aspect symbolique, comme témoin et faiseur d'urbanité.
    </p>
    <p>Centre névralgique de la capitale, ce quartier a la particularité d'être
      autant fréquenté de jour que de nuit, conférant de ce fait à l'éclairage
      une grande importance. La rue Vivienne fait partie des trois premières rues
      dotées de lanternes au gaz à la fin des années 1820
      <ButtonEllipsis data-footnote="2" class="footnote-pointer"></ButtonEllipsis>.
      L'effet de ces lanternes se voit démultiplié par la pose
      de candélabres dans les années 1840 <ButtonEye data-image="1"></ButtonEye>.
      La volonté d'assurer un confort visuel optimal et un sentiment de sécurité
      nocturne aux citadins demeure une priorité municipale jusqu'à la fin des
      années 1920
      <ButtonEllipsis data-footnote="3" class="footnote-pointer"></ButtonEllipsis>.
    </p>
    <p>Une autre activité phare du quartier exerce une influence sur le
      mobilier de rue&nbsp;: le théâtre. Le préfet Rambuteau (1781-1869)
      choisit d'implanter les premières colonnes urinoirs à proximité des
      théâtres parisiens, le long du boulevard des Italiens et du boulevard
      Montmartre. Loin d'être de simples lieux d'aisance, elles servent aussi
      de support pour la publicité, en atteste une lithographie de F. Bouchot
      <ButtonEye data-image="2"></ButtonEye>.
      Rapidement jugées incongrues, elles laissent place, à partir
      de 1868, aux colonnes Morris. Ces dernières sont légion dans ce quartier
      propice au divertissement. Initialement conçues pour la réclame théâtrale,
      elles présentent également des affiches en lien avec l'alimentation
      <ButtonEye data-image="3"></ButtonEye>&nbsp;
      <a :href="rootUrl + '/article/menu'">
        <ButtonArrow orient="right"></ButtonArrow>
      </a>.
    </p>
    <p>Le jardin du Palais-Royal sert aussi de moteur en matière d'équipement
      public. Ce lien étroit entre l'aménagement des rues et des espaces verts
      est principalement le fait de l'architecte Gabriel Davioud (1824-1881).
      Il a impulsé, par son travail sur les promenades
      <ButtonEye data-image="4"></ButtonEye>, toute une série
      de modifications, notamment au sujet des urinoirs. Cet architecte dote les
      pissotières de stalles multiples et d'écrans afin de masquer ce que la destination
      a de vulgaire. On retrouve alors place de la Bourse un urinoir grillagé
      à six stalles
      <ButtonEye data-image="5"></ButtonEye>,
      immortalisé par Charles Marville (1813-1879). Parangon
      de la modernité haussmannienne, cet édicule permet de retracer l'histoire
      des mœurs de ce quartier. Il est définitivement fermé en 1903
      <ButtonEllipsis data-footnote="4" class="footnote-pointer"></ButtonEllipsis>
      à cause de sa réputation interlope. Haut lieu des amours homosexuelles,
      encore prohibées à l'époque, les témoignages abondants
      <ButtonEllipsis data-footnote="5" class="footnote-pointer"></ButtonEllipsis>
      confèrent à ce quartier une place de choix dans la géographie queer
      parisienne de la seconde moitié du XIXe siècle.
    </p>
    <p>Enfin, l'étude du mobilier urbain contribue à décliner la figure du flâneur
      au féminin. Des femmes de tous milieux se côtoient dans ce quartier, principalement
      sur la place de la Bourse. Si elles s'y rendent pour des raisons variées
      (travail, achat, divertissement, etc.), toutes sont égales face à l'urgence
      d'un besoin vésical. Les femmes voient leur prière exaucée lors de l'inauguration
      du premier chalet de nécessité
      <ButtonEye data-image="6"></ButtonEye>
      le 26 septembre 1873, place de la Bourse
      <ButtonEllipsis data-footnote="6" class="footnote-pointer"></ButtonEllipsis>.
      Malgré de timides débuts, les chalets finissent par être un succès
      populaire, si bien qu'on en dénombre plus d'une centaine dans Paris au début
      du XXe siècle.</p>
    <p>Le mobilier urbain, loin de se cantonner à <q>&nbsp;un vieux réverbère à souvenirs
      au coin d'une rue où il ne passe déjà presque plus personne
      <ButtonEllipsis data-footnote="7" class="footnote-pointer"></ButtonEllipsis>&nbsp;
    </q>, pour reprendre
      les termes de L-F. Céline, enfant maudit du quartier, est un excellent indicateur
      des mutations d'une ville et dans le cas présent, d'un quartier.
    </p>
  </div>

  <div class="article-footer">
    <p>Louise Thiroux</p>
  </div>

</template>


<script setup>
import { onMounted, ref } from "vue";

import ButtonEllipsis from "@components/ui/ButtonEllipsis.vue";
import ButtonArrow from "@components/ui/ButtonArrow.vue";
import ButtonEye from "@components/ui/ButtonEye.vue";

/************************************************/

const rootUrl     = window.location.origin;
const emit        = defineEmits(["queryParams", "iiifIdUuid", "footnotes"]);
const queryParams = { theme: [ "espace public"
                             , "mobilier urbain"
                             , "affiche"
                             , "théâtre"
                             , "publicité"
                             , "mœurs"
                             ],
                      themeBooleanOp: "or" };
const iiifIdUuid = [ "qr116f7dbcdb2884ccd8ea4160c07202ad3"  // MC55
                   , "qr14be40957a31c4767b80c3de152d094a0"  // MC315
                   , "qr1d15d16273e194973a295b618fb812540"  // BHVP23
                   , "qr1df69056471584f02bf3200a819d3d7cb"  // MAK1
                   , "qr17ecadb767ccf4f80a131f84daea1696b"  // PRBNF24
                   , "qr1a98e4dd3d2b7432da0971c604bf34cc1"  // BDFPM119
                   ]
const footnotes   = [];


/************************************************/

/**
 *
 */
function loadIiifRessources() {

}

/************************************************/

// when the component is mounted, send base emits to parent
onMounted(() => {
  emit("queryParams", queryParams);
  emit("iiifIdUuid", iiifIdUuid);
})
</script>


<style scoped>
q {
  quotes: "«" "»" "‹" "›";
}
.article-body {
  line-height: 15px;
}
.article-body button {
  display: inline;
  max-width: 16px;
  max-height: 16px;
  padding: 0;
  margin: 0;
  transform: translateY(15%);
}
</style>
