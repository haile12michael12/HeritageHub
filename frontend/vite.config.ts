import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

export default defineConfig({
  plugins: [vue(), vueDevTools()],
  resolve: { alias: { '@': fileURLToPath(new URL('./src', import.meta.url)) } },
  server: {
    host: '0.0.0.0',
    port: 5173,
    strictPort: true,
    cors: true,
    hmr: { clientPort: 443 },
    allowedHosts: true,
    proxy: {
      '/api': { target: 'http://localhost:8084', changeOrigin: true },
    },
  },
  preview: { host: '0.0.0.0', port: 4173 },
})
