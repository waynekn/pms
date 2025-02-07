import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { resolve } from "path";

// https://vite.dev/config/
export default defineConfig(({ command }) => {
  return {
    plugins: [react()],
    css: {
      postcss: "./postcss.config.js",
    },
    base: command === "build" ? "/static/dist/" : "/",
    build: {
      chunkSizeWarningLimit: 1000,
      rollupOptions: {
        input: {
          main: resolve("./src/main.tsx"),
        },
        output: {
          entryFileNames: "[name].js",
          assetFileNames: (assetInfo) => {
            if (assetInfo.name?.endsWith(".css")) {
              return "style.css";
            }
            return "assets/[name].[ext]";
          },
        },
      },
    },
  };
});
