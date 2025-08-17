import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
  },
  build: {
    rollupOptions: {
      onwarn(warning, warn) {
        // Ignore warnings about unresolved imports starting with #
        if (warning.code === 'UNRESOLVED_IMPORT' && warning.source?.startsWith('#')) {
          return;
        }
        warn(warning);
      }
    }
  }
})
