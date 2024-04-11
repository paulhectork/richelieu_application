import { reactive } from 'vue';

/**
 * store relative to DOM manipulation
 *
 * on stores, see: https://vuejs.org/guide/essentials/reactivity-fundamentals.html
 * and:            https://vuejs.org/guide/scaling-up/state-management.html
 *
 * to listen to changes on stores and refs, see the link below and the `watch()` function
 * https://blog.logrocket.com/reactivity-vue-3-composition-api-ref-reactive/#watching-refs-change-watch-function
 */


export const domStore = reactive({
  sidebarHidden: false,  // the sidebar has been hidden
  toggleSidebar() {
    this.sidebarHidden = !this.sidebarHidden
  }
})