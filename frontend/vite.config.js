import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  envDir: '../',
  server: {
    proxy: {
      // Forwards frontend calls like fetch("/api/departments") to the
      // FastAPI backend, so the browser never sees a cross-origin request
      // (avoids CORS errors). Target comes from VITE_BACKEND_URL in your
      // root .env — falls back to localhost:8000 if that's not set.
      "/api": {
        target: process.env.VITE_BACKEND_URL || "http://192.168.1.22:8000",
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ""),
      },
    },
  },
})