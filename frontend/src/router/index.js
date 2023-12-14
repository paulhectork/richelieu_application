import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  linkExactActiveClass: "selected",  // `.selected` is added to the `a` created using `RouterLink` for the currently active component
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    }, {
      path: '/iconographie',
      name: 'Iconographie',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('@views/IconographyView.vue')
    }, {
      path: '/cartographie',
      name: 'Cartographie',
      component: () => import('@views/CartographyView.vue')
    }
  ]
})

export default router
