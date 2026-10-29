import { defineConfig } from 'astro/config';

export default defineConfig({
  site: process.env.SITE_URL || 'https://santoshshinde2012.github.io',
  base: process.env.BASE_PATH ?? '/ai-ml-ground-truth',
  output: 'static',
  trailingSlash: 'always',
  build: { inlineStylesheets: 'auto' },
  devToolbar: { enabled: false },
});
