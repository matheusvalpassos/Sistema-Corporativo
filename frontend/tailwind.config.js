/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html", // Removemos o 'frontend/'
    "./static/**/*.js",      // Se tiver JS na pasta static
    "./src/**/*.js"          // Se tiver JS na pasta src
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}