import "./assets/main.css";

import { createApp } from "vue";
import { createPinia } from "pinia";

import App from "@/App.vue";
import router from "@/router";

const app = createApp(App);

// setup of the app
app.use(createPinia())
   .use(router)
   .mount("#app");

