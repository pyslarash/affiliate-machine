/** @type {import('tailwindcss').Config} */
const {nextui} = require("@nextui-org/react");

module.exports = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
    "./node_modules/@nextui-org/theme/dist/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: "class",
  plugins: [
    nextui({
      prefix: "amachine",
      addCommonColors: false,
      defaultTheme: "light",
      defaultExtendTheme: "light",
      themes: {
        light: {
          layout: {},
          colors: {
            "foreground": "#180828",
            "background": "#F2EAFA",
            "primary": "#9353d3",
            "secondary": "#006FEE",
            "danger": "#f31260",
            "warning": "#f5a524",
            "success": "#17c964",
          }
        },
        dark: {
          layout: {},
          colors: {
            "foreground": "#F2EAFA",
            "background": "#180828",
            "primary": "#9353d3",
            "secondary": "#006FEE",
            "danger": "#f31260",
            "warning": "#f5a524",
            "success": "#17c964",
          }
        },
      }
    })
  ],
};
