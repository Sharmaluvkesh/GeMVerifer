/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        gov: {
          navy: '#0F2942',
          blue: '#1E3A8A',
          lightBlue: '#E0F2FE',
          saffron: '#FF671F',
          green: '#046A38',
          bg: '#F8FAFC',
          card: '#FFFFFF',
          border: '#CBD5E1',
        },
      },
    },
  },
  plugins: [],
}
