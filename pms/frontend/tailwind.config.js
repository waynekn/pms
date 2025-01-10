/** @type {import('tailwindcss').Config} */
export default {
  content: ["./src/**/*.{html,ts,tsx}", "./index.html", "../templates/*.html"],
  theme: {
    extend: {
      colors: {
        "red-orange": "#FF5733",
        "bold-yellow": "#FFC300",
        "rich-green": "#28A745",
      },
    },
  },
  plugins: [],
};
