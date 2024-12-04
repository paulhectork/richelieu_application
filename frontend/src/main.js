import "./assets/main.css";

import { createApp } from "vue";
import { createPinia } from "pinia";
import { plugin, defaultConfig } from "@formkit/vue";

import config from "../formkit.config.js";

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

