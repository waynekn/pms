import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { resolve } from "path";

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  css: {
    postcss: "./postcss.config.js",
  },
  build: {
    emptyOutDir: true,
    rollupOptions: {
      input: {
        main: resolve("./src/main.tsx"),
      },
      output: {
        dir: "../static/react/",
        entryFileNames: "[name].js",
      },
    },
  },
});
