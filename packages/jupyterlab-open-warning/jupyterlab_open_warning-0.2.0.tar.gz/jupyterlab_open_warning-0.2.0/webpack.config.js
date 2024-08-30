/* eslint-disable @typescript-eslint/no-require-imports */

const path = require("path");
const {
  WPPlugin: { JSONLicenseWebpackPlugin },
} = require("@jupyterlab/builder");

module.exports = {
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "lib"),
    },
  },
  plugins: [
    new JSONLicenseWebpackPlugin({
      licenseFileOverrides: {
        "@jupyter/collaboration": "LICENSE-downloaded",
      },
    }),
  ],
};
