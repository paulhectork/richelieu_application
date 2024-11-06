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
  menuActive: false,
  /**
   * flag to display the modal @components/TheHomeModal.vue.
   * this modal is only visible on the home page and when visiting
   * the site for the first time and is hidden afterwards
   */
  homeModalVisible: true,
  /**
   * the same, but for the modal @components/CartographyModal.vue,
   * displayed on @views/CartographyView.vue: once it's been removed,
   * don't show it
   */
  cartographyModalVisible: true,
  /**
   *
   */
  theHomeIiifIntroVisible: true

})