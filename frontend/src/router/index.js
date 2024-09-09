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
      component: () => import("@views/AdvancedSearchView.vue")
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
      path: '/theme/:categoryName',
      component: () => import("@views/ThemeOrNamedEntityIndexView.vue"),
      props: { tableName: "theme" }
    }, {
      path: '/theme/:categoryName/:idUuid',
      name: 'Thème',
      component: () => import("@views/ThemeMainView.vue")
    }, {
      path: '/entite-nommee',
      component: () => import("@views/ThemeOrNamedEntityCategoryIndexView.vue"),
      props: { tableName: "namedEntity" }
    }, {
      path: '/entite-nommee/:categoryName',
      component: () => import("@views/ThemeOrNamedEntityIndexView.vue"),
      props: { tableName: "namedEntity" }
    }, {
      path: '/entite-nommee/:categoryName/:idUuid',
      component: () => import("@views/NamedEntityMainView.vue")
    }, {
      path: '/lieu',
      component: () => import("@views/PlaceIndexView.vue")
    }, {
      path: '/lieu/:idUuid',
      component: () => import("@views/PlaceMainView.vue")
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
      path: '/table-viewer',
      component: () => import("@views/TableViewerView.vue")
    }, {
      path: "/:pathMatch(.*)*",
      component: () => import("@views/ErrNotFoundView.vue")
    }
  ]
})

export default router
