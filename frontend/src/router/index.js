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
      path: '/iconographie',
      name: 'Iconographie',
      component: () => import("@views/IconographyView.vue")
    }, {
      path: '/iconographie/:idUuid',
      name: 'Iconographie / main',
      component: () => import("@views/IconographyMainView.vue")
    }, {
      path: '/cartographie',
      name: 'Cartographie',
      component: () => import("@views/CartographyView.vue")
    }, {
      path: '/theme',
      name: 'Thème',
      component: () => import("@views/ThemeView.vue")
    }, {
      path: '/sujet',
      name: 'Sujets',
      component: () => import("@views/NamedEntityView.vue")
    }, {
      path: '/lieu',
      name: 'Lieux',
      component: () => import("@views/PlaceView.vue")
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
