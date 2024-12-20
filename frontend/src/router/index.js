import { createRouter, createWebHistory } from 'vue-router'


/**
 * see:
 * https://router.vuejs.org/guide/essentials/dynamic-matching.html
 */


const router = createRouter({
  // production errors: can only access directly to the root url `/`
  // https://vue-land.github.io/faq/production-page-refresh
  // it's impossible to access to any other url (`/theme`) or
  // reload a page other than the root. otherwise, we get a blank page.
  // however, redirections etc work fine with `createWebHashHistory`:
  //
  // history: createWebHashHistory(import.meta.env.BASE_URL),
  history: createWebHistory(import.meta.env.BASE_URL),

  scrollBehavior(to, from, savedPosition) {  // https://router.vuejs.org/guide/advanced/scroll-behavior.html#Scroll-Behavior
    if ( to.hash ) {
      // very hacky scrollIntoView within a promise:
      // otherwise, there's an error message that anchor `to.hash`
      // could not be found, so we manually do the whole
      // scrollIntoView thing
      return new Promise((res,rej) => {
        setTimeout(() => {
          document.querySelector(to.hash)?.scrollIntoView({ behavior:"smooth" });
          return { el: to.hash,
                    behavior:"smooth" }
        }, 250)
      })
    // } else if ( savedPosition ) {
    //   return savedPosition
    } else {
      return { top: 0 }
    }
  },
  linkExactActiveClass: "selected",  // `.selected` is added to the `a` created using `RouterLink` for the currently active component
  routes: [
    {
      path: '/',
      name: 'intro',
      component: () => import("@views/IntroIiifView.vue")
    }, {
      path: '/accueil',
      name: 'home',
      component: () => import("@views/HomeView.vue")
    }, {
      path: '/recherche',
      component: () => import("@views/AdvancedSearchView.vue")
    }, {
      path: '/recherche-rapide',
      component: () => import("@views/QuickSearchView.vue")
    }, {
      path: '/iconographie',
      component: () => import("@views/IconographyIndexView.vue")
    }, {
      path: '/iconographie/:idUuid',
      component: () => import("@views/IconographyMainView.vue")
    }, {
      path: '/cartographie',
      component: () => import("@views/CartographyView.vue")
    }, {
      path: '/theme',
      component: () => import("@views/ThemeOrNamedEntityCategoryIndexView.vue"),
      props: { tableName: "theme" }  // https://router.vuejs.org/guide/essentials/passing-props.html#Object-mode
    }, {
      // theme and named entities route matching (both work the same):
      //
      // theme/qr1.+
      //    => we're looking for a main theme
      //    => redirect to ThemeMainView. else, the slug after "theme/"
      //       should be a value of the column theme.category_slug (see route below).
      // in practical terms, this means that ThemeMainView and NamedEntityMainView
      // can be reached by 2 URLs:
      // - (theme|entite-nommee)/<category_slug>/<idUuid>
      // - (theme|entite-nommee)/<idUuid>   => the <category_slug> is optional
      // https://router.vuejs.org/guide/essentials/route-matching-syntax.html#Custom-regex-in-params
      path: '/theme/:idUuid(qr1.+)',
      component: () => import("@views/ThemeMainView.vue"),
    }, {
      path: '/theme/:categorySlug',
      component: () => import("@views/ThemeOrNamedEntityIndexView.vue"),
      props: { tableName: "theme" }
    }, {
      path: '/theme/:categorySlug/:idUuid',
      name: 'Thème',
      component: () => import("@views/ThemeMainView.vue")
    }, {
      path: '/entite-nommee',
      component: () => import("@views/ThemeOrNamedEntityCategoryIndexView.vue"),
      props: { tableName: "namedEntity" }
    }, {
      // "entite-nommee/qr1.+"
      //    => we're looking for a main named entity
      //    => redirect to NamedEntityMainView.
      //    else, redirect to ThemeOrNamedEntityIndexView
      path: '/entite-nommee/:idUuid(qr1.+)',
      component: () => import("@views/NamedEntityMainView.vue")
    }, {
      path: '/entite-nommee/:categorySlug',
      component: () => import("@views/ThemeOrNamedEntityIndexView.vue"),
      props: { tableName: "namedEntity" }
    }, {
      path: '/entite-nommee/:categorySlug/:idUuid',
      component: () => import("@views/NamedEntityMainView.vue")
    }, {
      path: '/lieu',
      component: () => import("@views/PlaceIndexView.vue")
    }, {
      path: '/lieu/:idUuid',
      component: () => import("@views/PlaceMainView.vue")
    }, {
      path: '/institution',
      component: () => import("@views/InstitutionIndexView.vue")
    }, {
      path: '/institution/:idUuid',
      component: () => import("@views/InstitutionMainView.vue")
    }, {
      path: '/index-combine',
      component: () => import("@views/AssociationIndexView.vue"),
      props: route => ({ toIdUuid   : route.query.toIdUuid,   // https://router.vuejs.org/guide/essentials/passing-props.html#Function-mode                        fromIdUuid : route.query.fromIdUuid
                         fromIdUuid : route.query.fromIdUuid,
                         fromTable  : route.query.from,
                         toTable    : route.query.to })
    }, {
      path: '/article',
      component: () => import("@views/ArticleIndexView.vue")
    }, {
      path: '/article/:articleName',
      component: () => import("@views/ArticleMainView.vue")
    }, {
      path: '/documentation/:pageName',
      component: () => import("@views/AboutDocumentationView.vue")
    }, {
      path: '/a-propos/:pageName',
      component: () => import("@views/AboutDocumentationView.vue")
    }, {
      path: "/:pathMatch(.*)*",
      component: () => import("@views/ErrNotFoundView.vue")
    }
  ]
})

export default router
