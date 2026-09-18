/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#0b0d0c",
        panel: "#131614",
        line: "#2a3129",
        paper: "#efe7d6",
        mute: "#b7b09f",
        accent: "#d7ff3c",
        bronze: "#c4a574",
        danger: "#ff6b4a",
      },
      fontFamily: {
        display: ["Fraunces", "Georgia", "serif"],
        sans: ["Outfit", "system-ui", "sans-serif"],
      },
      boxShadow: {
        lift: "0 30px 60px -40px rgba(0,0,0,0.7)",
      },
      borderRadius: {
        xl: "1.25rem",
      },
    },
  },
  plugins: [],
};
