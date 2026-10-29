import { defineConfig } from 'astro/config';
import { fileURLToPath } from 'node:url';

const root = fileURLToPath(new URL('.', import.meta.url));

export default defineConfig({
  root,
  site: process.env.SITE_URL || 'https://santoshshinde2012.github.io',
  base: process.env.BASE_PATH ?? '/ai-ml-ground-truth',
  output: 'static',
  trailingSlash: 'always',
  build: { inlineStylesheets: 'auto' },
  devToolbar: { enabled: false },
  vite: { define: { 'import.meta.env.WEBSITE_ROOT': JSON.stringify(root) } },
});
