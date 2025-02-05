/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./src/**/*.{html,ts,tsx}",
    "./src/**/**/*.{html,ts,tsx}",
    "./index.html",
    "../templates/*.html",
  ],
  theme: {
    extend: {
      colors: {
        "red-orange": "#FF5733",
        "bold-yellow": "#FFC300",
        "rich-green": "#28A745",
      },
      animation: {
        fadeIn: "fadeIn 1s ease-out",
        slideIn: "slideIn 1s ease-out",
      },
      keyframes: {
        fadeIn: {
          "0%": { opacity: "0", transform: "translateY(10px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
        slideIn: {
          "0%": { opacity: "0", transform: "translateX(-30px)" },
          "100%": { opacity: "1", transform: "translateX(0)" },
        },
      },
    },
  },
  plugins: [],
};
