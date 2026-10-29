import path from 'node:path';
import { fileURLToPath } from 'node:url';

// Astro supplies the configured root when this module is bundled for static rendering.
// Direct Node scripts and tests resolve the same directory from this source file.
export const websiteRoot = path.resolve(
  import.meta.env?.WEBSITE_ROOT ?? fileURLToPath(new URL('../../', import.meta.url)),
);
export const repositoryRoot = path.resolve(websiteRoot, '..');
export const fromWebsite = (...segments) => path.join(websiteRoot, ...segments);
export const fromRepository = (...segments) => path.join(repositoryRoot, ...segments);
