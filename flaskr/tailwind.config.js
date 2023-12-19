/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./static/src/**/*.js"
  ],
  theme: {
    extend: {
        fontFamily: {
            'nunito': ['nunito', 'sans-serif'],
        },
    },

  },
  plugins: [],
}
