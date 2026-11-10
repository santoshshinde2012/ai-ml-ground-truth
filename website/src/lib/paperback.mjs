// Prepare a section's HTML for paper, where links cannot be followed.

/** A web address as a reader would type it: no scheme, no "www.", no trailing slash. */
export function displayURL(href) {
  const url = new URL(href);
  const path = `${url.pathname}${url.search}${url.hash}`.replace(/\/$/, '');
  return `${url.host.replace(/^www\./, '')}${path}`;
}

/**
 * Drop paragraphs made only of links to other pages of the book, such as "Previous" and
 * "Next", with a rule just before one. They help on the web but say nothing on paper.
 */
export function stripNavigation(html) {
  const link = String.raw`<a href="/[^"]*">[^<]*</a>`;
  const gap = String.raw`(?:[\s\u00a0·]|&nbsp;)*`;
  const navigation = String.raw`(?:<hr>\s*)?<p>${gap}${link}(?:${gap}${link})*${gap}</p>\s*`;
  return html.replace(new RegExp(navigation, 'g'), '');
}

/** Print each external address after its link, unless the link text already shows it. */
export function showLinkTargets(html) {
  return html.replace(
    /<a href="(https?:\/\/[^"]+)"([^>]*)>([\s\S]*?)<\/a>/g,
    (link, href, attributes, text) => {
      const address = displayURL(href.replaceAll('&amp;', '&'));
      if (text.replace(/<[^>]+>/g, '').includes(address)) return link;
      return `${link}<span class="paperback-url"> ${address.replaceAll('&', '&amp;')}</span>`;
    },
  );
}
