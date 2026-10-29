import { getBook, bookHref, homeHref, basePath } from '../lib/book.mjs';
export async function GET({ site }: { site: URL }) {
  const paths = [
    homeHref(),
    `${basePath()}/laboratory/`,
    `${basePath()}/sources/`,
    ...(await getBook()).map((p) => bookHref(p.slug)),
  ];
  const xml = `<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">${paths.map((p) => `<url><loc>${new URL(p, site).href}</loc></url>`).join('')}</urlset>`;
  return new Response(xml, { headers: { 'Content-Type': 'application/xml; charset=utf-8' } });
}
