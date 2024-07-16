import { reactive } from 'vue';
import $ from "jquery";

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
  /**
   * portrait or landscape display.
   */
  windowOrientation: "portrait",
  setWindowOrientation(val) {
    if ( ! ["portrait", "landscape"].includes(val) ) {
      new Error(`domStore.setWindowOrientation: expected one of ["portrait", "landscape"], got "${val}"`)
    } else {
      this.windowOrientation = val;
    }
  },
  /**
   * flag to show that the sidebar is visible on mobile displays
   */
  sidebarActive: false,
  toggleMobileSidebar() {
    this.sidebarActive = !this.sidebarActive
  }
})