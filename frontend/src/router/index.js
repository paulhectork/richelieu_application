import { createRouter, createWebHistory } from 'vue-router'


/**
 * see:
 * https://router.vuejs.org/guide/essentials/dynamic-matching.html
 */


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  linkExactActiveClass: "selected",  // `.selected` is added to the `a` created using `RouterLink` for the currently active component
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import("@views/HomeView.vue")
    }, {
      path: '/recherche',
      name: 'Recherche',
      component: () => import("@views/AdvancedSearchView.vue")
    }, {
      path: '/iconographie',
      name: 'Index iconographique',
      component: () => import("@views/IconographyIndexView.vue")
    }, {
      path: '/iconographie/:idUuid',
      name: 'Ressource iconographique',
      component: () => import("@views/IconographyMainView.vue")
    }, {
      path: '/cartographie',
      name: 'Index cartographique',
      component: () => import("@views/CartographyView.vue")
    }, {
      path: '/theme',
      name: 'Index des thèmes',
      component: () => import("@views/ThemeIndexView.vue")
    }, {
      path: '/theme/:idUuid',
      name: 'Thème',
      component: () => import("@views/ThemeMainView.vue")
    }, {
      path: '/sujet',
      name: 'Index des sujets',
      component: () => import("@views/NamedEntityIndexView.vue")
    }, {
      path: '/sujet/:idUuid',
      name: 'Sujet',
      component: () => import("@views/NamedEntityMainView.vue")
    }, {
      path: '/lieu',
      name: 'Index des lieux',
      component: () => import("@views/PlaceIndexView.vue")
    }, {
      path: '/lieu/:idUuid',
      name: 'Lieu',
      component: () => import("@views/PlaceMainView.vue")
    }, {
      path: '/article',
      name: 'Articles',
      component: () => import("@views/ArticleIndexView.vue")
    }, {
      path: '/article/:articleName',
      name: 'Article',
      component: () => import("@views/ArticleMainView.vue")
    }, {
      path: '/table-viewer',
      name: 'Voir les tables',
      component: () => import("@views/TableViewerView.vue")
    }, {
      path: "/:pathMatch(.*)*",
      name: "404",
      component: () => import("@views/NotFoundView.vue")
    }
  ]
})

export default router
