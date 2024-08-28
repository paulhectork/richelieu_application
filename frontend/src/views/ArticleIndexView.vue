<template>
  <h1>Articles</h1>
  <div class="article-index-wrapper">
    <ul class="list-invisible">
      <li v-for="article in articles"
          class="article-item-wrapper"
      >
        <div class="article-item"
             :style="{ backgroundImage: `url(${article.image})` }"
        >
          <RouterLink :to="`/article/${article.urlSlug}`">
            <h2>{{ article.title }}</h2>
            <h3 v-html="article.subtitle"></h3>
          </RouterLink>
          <!--
          <div class="hover-overlay"
               @mouseenter="showOverlayOnMouseEnter"
               @mouseleave="hideOverlayOnMouseLeave"
          ></div>
          -->
        </div>
      </li>
    </ul>
  </div>
</template>


<script setup>
import { ref, onMounted } from "vue";

import $ from "jquery";

/********************************************/

const articles = [ { title    : "La bourse et sa place",
                     subtitle : `Le temple de l'argent en perspective&nbsp;: activités et
                                 représentations au XIX<sup>e</sup> siècle`,
                     image    : "https://gallica.bnf.fr/iiif/ark:/12148/btv1b53150759s/f1/full/2000/0/native.jpg",
                     urlSlug  : "bourse" }
                 , { title    : "Portrait de rue",
                     subtitle : "La rue Vivienne vue par ses contemporains",
                     image    : "https://gallica.bnf.fr/iiif/ark:/12148/btv1b90087110/f1/full/2000/0/native.jpg",
                     urlSlug  : "vivienne" }
                 , { title    : "Mode et architecture",
                     subtitle : `Boutiques et magasins, expérimentations autour de la
                                 vente de <q>&nbsp;nouveautés&nbsp;</q>`,
                     image    : "https://quartier-richelieu-data.inha.fr/statics/iconography/qr15288251e8d6e4c97999a6c225e82d07c.png",
                     urlSlug  : "mode" }
                 , { title    : "Menus et restaurants",
                     subtitle : `Alimentation et culture visuelle des lieux de
                                 restauration du Palais-Royal aux Grands boulevards`,
                     image    : "https://apicollections.parismusees.paris.fr/sites/default/files/styles/4k/collections/atoms/images/CAR/aze_carg002054_001.jpg?itok=ESLjKoNN",
                     urlSlug  : "menu" }
                 , { title    : "La nature en ville",
                     subtitle : "La botanisation autour de la rue Vivienne",
                     image    : "https://quartier-richelieu-data.inha.fr/statics/iconography/qr1e4c791a70c2940ebaf26373c02110007.jpg",
                     urlSlug  : "nature" }
                 , { title    : "Les cafés du Palais-Royal",
                     subtitle : `Consommations dans l'enceinte du Palais-Égalité
                                 à la fin du XVIII<sup>e</sup> siècle`,
                     image    : "https://apicollections.parismusees.paris.fr/sites/default/files/styles/4k/collections/atoms/images/CAR/aze_carg010953_001.jpg?itok=n6xhEvvn",
                     urlSlug  : "cafe" }
                 , { title    : "La ville en chantier",
                     subtitle : "",
                     image    : "https://apicollections.parismusees.paris.fr/sites/default/files/styles/4k/collections/atoms/images/CAR/lpdp_99044-16.jpg?itok=RomYNLfC",
                     urlSlug  : "chantier" }
                 , { title    : "La banque de france",
                     subtitle : `Économie et sociabilités des établissements environnants
                                 l'hôtel de Toulouse`,
                     image    : "https://apicollections.parismusees.paris.fr/sites/default/files/styles/4k/collections/atoms/images/CAR/lpdp_144183-16.jpg?itok=WAjQ3-3i",
                     urlSlug  : "banque" }
                 , { title    : "Hôtels, passages et immeubles à boutiques",
                     subtitle : "Habiter à travers les recueils d'architecture (1820-1830)",
                     image    : "https://apicollections.parismusees.paris.fr/sites/default/files/styles/4k/collections/atoms/images/CAR/aze_card16711_001.jpg?itok=bH0JRhsX",
                     urlSlug  : "habiter" }
                 , { title    : "La patrimonialisation d'un quartier",
                     subtitle : "",
                     image    : "https://apicollections.parismusees.paris.fr/sites/default/files/styles/4k/collections/atoms/images/CAR/aze_carph015719_001.jpg?itok=JAeUjy5H",
                     urlSlug  : "patrimonialisation" }
                 , { title    : "Le mobilier urbain",
                     subtitle : "Reflet d'un quartier et de ses activités",
                     image    : "https://quartier-richelieu-data.inha.fr/statics/iconography/qr1f0c214cc309846228da9f7262144b638_compress.jpg",
                     urlSlug  : "mobilier" }
                 , { title    : "Les théâtres et leurs images",
                     subtitle : `Autour des spectacles&nbsp;: architectures,
                                 affiches et portraits`,
                     image    : "https://quartier-richelieu-data.inha.fr/statics/iconography/qr1359ddcecafb84650a459f1dcc8421e91.jpg",
                     urlSlug  : "theatre" }
                 , { title    : "Prostitutions",
                     subtitle : "Les logiques spatiales du plus vieux métier du monde",
                     image    : "https://quartier-richelieu-data.inha.fr/statics/iconography/qr1f7350ffbb83543fe91938234376444d0.jpg",
                     urlSlug  : "prostitution" }
                 , { title    : "Curiosités et mœurs",
                     subtitle : "",
                     image    : "https://quartier-richelieu-data.inha.fr/statics/iconography/qr1d53e6b37c6334721b476381fec062660.png",
                     urlSlug  : "curiosite" }
                  ]

/*******************************************/

const showOverlayOnMouseEnter = (e) =>
  $(e.target).css({ opacity: 0.5 });

const hideOverlayOnMouseLeave = (e)  =>
  $(e.target).css({ opacity: 0 });

</script>


<style scoped>
@media (orientation:landscape) {
  .article-index-wrapper {
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .article-index-wrapper > ul {
    width: 75%;
  }
}
.article-item {
  border: var(--cs-border);
  margin: 20px 5px;
  background-position: center;
  position: relative;  /* for the article overlays */
}
.article-item > a {
  text-decoration: none;
  color: var(--cs-main-default);
}
h2, h3 {
  background-color: var(--cs-main-default-bg);
  width: fit-content;
  border: var(--cs-border);
  border-left: none;
  padding: 3px 3px 1px 3px;
}
a {
  z-index: 10;
}
.hover-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;

  transition: opacity var(--cs-color-transition);
  background: linear-gradient(50deg, #C78FA5, var(--cs-seagreen));
  opacity: 0;
}
</style>