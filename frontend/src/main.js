import "./assets/main.css";

import { createApp } from "vue";
import { createPinia } from "pinia";
import { plugin, defaultConfig } from "@formkit/vue";
import config from "../formkit.config.js";
// import { RecycleScroller } from 'vue-virtual-scroller'
// import VueVirtualScroller from "vue-virtual-scroller";
// import 'vue-virtual-scroller/dist/vue-virtual-scroller.css';

import App from "@/App.vue";
import router from "@/router";

const app = createApp(App);

// setup of the app
app// .component('RecycleScroller', RecycleScroller)
   // .use(VueVirtualScroller)
   .use(createPinia())
   .use(router)
   .use(plugin, defaultConfig(config))
   .mount("#app");

