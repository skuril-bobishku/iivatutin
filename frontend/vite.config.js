import * as dotenv from 'dotenv';
dotenv.config();

import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'
import { getUrl, getPort } from './src/env.js';

export default defineConfig({
  plugins: [
    vue(),
    vueDevTools(),
  ],
  server: {
    host: getUrl('VITE_API_CLIENT_URL', 'localhost'),
    port: getPort('VITE_API_CLIENT_PORT', 5173),
    //https: import.meta.env.VITE_HTTPS === 'true',
  },
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  }
})
