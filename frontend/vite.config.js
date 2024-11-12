import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'


// https://vitejs.dev/config/
/**
 * stuff that could be useful that i don't want to understand now:
 * server config: https://vitejs.dev/config/server-options.html,
 *                https://vitejs.dev/config/server-options.html#server-proxy
 *                https://vitejs.dev/guide/env-and-mode#modes
 */
export default defineConfig(({ command, mode, isSsrBuild, isPreview }) => {

  // exit if `--mode` was not provided or
  // if it isn't one of `allowedModes`
  const allowedModes = [ "backend-server", "backend-local" ];
  if ( mode==null || !allowedModes.includes(mode) ) {
    console.log("INVALID PARAMETERS\n",
                `  please provide '--mode' with one of [${allowedModes.map(e => "'"+e+"'")}] and start again.\n`,
                "  exiting...\n")
    process.exit(1)
  }

  // choose the configuration based on `mode`
  let configVariables;
  switch (mode) {
    case "backend-server":
      configVariables = {
        __MODE__       : JSON.stringify("PROD"),
        __API_URL__    : JSON.stringify("https://quartier-richelieu.inha.fr/i"),
        __STATICS_URL__: JSON.stringify("https://quartier-richelieu.inha.fr/statics/")
      };
      break;
    case "backend-local":
      configVariables = {
        __MODE__       : JSON.stringify("DEV"),
        __API_URL__    : JSON.stringify("http://localhost:5001/i"),
        __STATICS_URL__: JSON.stringify("http://localhost:9999/")
      };
      break;
  };

  return {
    plugins: [ vue() ],
    //  server: {
    //   	hmr: {
		//      clientPort: 443  // https://github.com/vitejs/vite/issues/1653. deletes the websocket error but resources still don't load (without errors). le back ne reçoit pas la requête.
	  //    }
    // },
    define: configVariables,
    resolve: {
      alias: {
        "@": fileURLToPath(new URL('./src', import.meta.url)),
        "@utils": fileURLToPath(new URL("./src/utils", import.meta.url)),
        "@views": fileURLToPath(new URL("./src/views", import.meta.url)),
        "@router": fileURLToPath(new URL("./src/router", import.meta.url)),
        "@stores": fileURLToPath(new URL("./src/stores", import.meta.url)),
        "@assets": fileURLToPath(new URL("./src/assets", import.meta.url)),
        "@modules": fileURLToPath(new URL("./src/modules", import.meta.url)),
        "@globals": fileURLToPath(new URL("./src/globals.js", import.meta.url)),
        "@plugins": fileURLToPath(new URL("./src/plugins", import.meta.url)),
        "@components": fileURLToPath(new URL("./src/components", import.meta.url)),
        "@composables": fileURLToPath(new URL("./src/composables", import.meta.url))
      }
    }
  }
})
