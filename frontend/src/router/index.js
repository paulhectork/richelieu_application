import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
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
      component: () => import('../views/IconographieView.vue')
    }, {
      path: '/cartographie',
      name: 'Cartographie',
      component: () => import('../views/CartographieView.vue')
    }
  ]
})

export default router
