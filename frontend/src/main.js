import "./assets/main.css";

import { createApp } from "vue";
import { createPinia } from "pinia";
import { plugin, defaultConfig } from "@formkit/vue";
import config from "../formkit.config.js";

import App from "@/App.vue";
import router from "@/router";

const app = createApp(App);

// setup of the app
app.use(createPinia())
   .use(router)
   // .use(Vueform, vueformConfig)
   .use(plugin, defaultConfig(config))
   .mount("#app");

