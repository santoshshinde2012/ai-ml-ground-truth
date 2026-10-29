import { basePath } from '../lib/book.mjs';
export function GET({ site }: { site: URL }) {
  return new Response(
    `User-agent: *\nAllow: /\nSitemap: ${new URL(`${basePath()}/sitemap.xml`, site).href}\n`,
    { headers: { 'Content-Type': 'text/plain' } },
  );
}
