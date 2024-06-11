import "./assets/main.css";

import { createApp } from "vue";
import { createPinia } from "pinia";
import Vueform from '@vueform/vueform';
import vueformConfig from './../vueform.config';

import App from "@/App.vue";
import router from "@/router";

const app = createApp(App);

// setup of the app
app.use(createPinia())
   .use(router)
   .use(Vueform, vueformConfig)
   .mount("#app");

