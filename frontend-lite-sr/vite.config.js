import { defineConfig } from 'vite';
import { viteStaticCopy } from 'vite-plugin-static-copy';

export default defineConfig({
  plugins: [
    viteStaticCopy({
      watch: true,  // important for dev mode
      targets: [
        {
          src: 'src/app/assets/*',
          dest: 'assets'
        }
      ]
    })
  ],
  esbuild: {
      minifyIdentifiers: false
  }
});