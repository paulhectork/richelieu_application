import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

import { backendUrl } from "./src/utils/constants";

// https://vitejs.dev/config/
/**
 * stuff that could be useful that i don't want to understand now:
 * server config: https://vitejs.dev/config/server-options.html,
 *                https://vitejs.dev/config/server-options.html#server-proxy
 *
 */
export default defineConfig({
  plugins: [
    vue(),
  ],
  define: {
    __API_URL__: JSON.stringify(backendUrl)
  },
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
      "@utils": fileURLToPath(new URL("./src/utils", import.meta.url)),
      "@views": fileURLToPath(new URL("./src/views", import.meta.url)),
      "@router": fileURLToPath(new URL("./src/router", import.meta.url)),
      "@stores": fileURLToPath(new URL("./src/router", import.meta.url)),
      "@assets": fileURLToPath(new URL("./src/assets", import.meta.url)),
      "@components": fileURLToPath(new URL("./src/components", import.meta.url)),
      "@composables": fileURLToPath(new URL("./src/composables", import.meta.url))
    }
  }
})
