// see: https://cli.vuejs.org/config/#vue-config-js

import { backendUrl } from "./src/utils/constants";

module.exports = {
  configureWebpack: {
    devServer: {
      proxy: backendUrl  // base URL for the devserver
      /*
      "^/api": {
        target: backendUrl,
        ws: true,
        changeOrigin: true
      }
      */
    }
  }
};

