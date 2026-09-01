import { defineConfig } from 'vite';
import { viteStaticCopy } from 'vite-plugin-static-copy';

export default defineConfig({
  // Keep production asset URLs relative so the build works at /en/ (and in previews).
  base: './',
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
