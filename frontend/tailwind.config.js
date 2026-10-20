/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        heritage: {
          50: '#fef9ec',
          100: '#fdedc8',
          200: '#fbd88d',
          300: '#f8c052',
          400: '#f5a623',
          500: '#e67e00',
          600: '#cc5f00',
          700: '#a63d00',
          800: '#853100',
          900: '#6d2800',
          950: '#3d1400',
        },
        ink: {
          50: '#f8f7f6',
          100: '#e8e6e1',
          200: '#d1ccc4',
          300: '#b8b0a3',
          400: '#9a9286',
          500: '#7d7568',
          600: '#635d53',
          700: '#4a4540',
          800: '#2e2b28',
          900: '#1a1816',
        },
      },
      fontFamily: {
        display: ['Playfair Display', 'serif'],
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      boxShadow: {
        soft: '0 4px 24px rgba(0,0,0,0.06)',
        lifted: '0 12px 40px rgba(0,0,0,0.10)',
        glow: '0 0 20px rgba(230,126,0,0.15)',
      },
      borderRadius: {
        '2xl': '1rem',
        '3xl': '1.5rem',
        '4xl': '2rem',
      },
      animation: {
        'fade-in': 'fadeIn 0.5s ease-out',
        'slide-up': 'slideUp 0.4s ease-out',
        'shimmer': 'shimmer 1.5s infinite',
      },
      keyframes: {
        fadeIn: { '0%': { opacity: '0' }, '100%': { opacity: '1' } },
        slideUp: { '0%': { transform: 'translateY(10px)', opacity: '0' }, '100%': { transform: 'translateY(0)', opacity: '1' } },
        shimmer: { '0%': { transform: 'translateX(-100%)' }, '100%': { transform: 'translateX(100%)' } },
      },
    },
  },
  plugins: [],
}
