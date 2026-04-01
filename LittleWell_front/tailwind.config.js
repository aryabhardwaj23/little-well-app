/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'littlewell': {
          'green': '#A8D5BA',
          'green-dark': '#8FC2A4',
          'green-text': '#2C5F2D',
          'orange': '#F7B267',
          'orange-text': '#8B4513',
          'blue': '#CDE7F0',
          'blue-text': '#1B4965',
          'beige': '#FAF9F6',
        },
      },
      container: {
        center: true,
        padding: '1.5rem',
      },
    },
  },
  plugins: [],
}
