/** @type {import('tailwindcss').Config} */
const plugin = require('tailwindcss/plugin')
module.exports = {
  mode: "jit",
  content: [
    "./templates/**/*.{html,js}"
  ],
  theme: {
    colors: {
      'pink': '#f5c2ee',
      'tan': '#ECD4A9',
      'black': '#000000',
      'white': '#ffffff',
      'button': '#9E129E',
      'button-hover': '#CC35CC',
    },
    extend: {},
  },
  plugins: [
    require('tailwindcss-3d'),
  ],
}
