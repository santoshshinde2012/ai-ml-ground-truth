export interface Heading {
  depth: number;
  text: string;
  id: string;
}
export interface BookPage {
  file: string;
  slug: string;
  title: string;
  description: string;
  category: string;
  chapter?: number;
  lab?: string | null;
  html: string;
  headings: Heading[];
  words: number;
  minutes: number;
  markdown: string;
  parentSlug?: string;
  lessonIndex?: number;
  lessonCount?: number;
  lessons?: { slug: string; title: string; minutes: number }[];
}
export interface SourceInventory {
  edition: string;
  updated: string;
  sources: {
    url: string;
    label: string;
    locations: { title: string; href: string; file: string }[];
  }[];
}
