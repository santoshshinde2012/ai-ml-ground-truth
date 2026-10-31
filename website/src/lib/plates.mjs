// Which plate each page shows. The web pages, the print edition and the EPUB share this,
// so every edition carries the same illustrations.
/** @typedef {'start' | 'guide' | 'causal' | 'offer' | 'price' | 'churn' | 'delivery' | 'lab' | 'publish'} PlateKind */
/** @type {Record<string, PlateKind>} */
const kinds = {
  'start-here': 'start',
  'reader-guide': 'guide',
  publishing: 'publish',
  'reference-lab': 'lab',
  'reference-lab/data-card': 'lab',
  'reference-lab/incident-report': 'lab',
  'reference-lab/model-card': 'lab',
  'reference-lab/evaluation': 'lab',
  '09-business-machine-learning/causal-primer': 'causal',
  '09-business-machine-learning/offer-recommendation': 'offer',
  '09-business-machine-learning/price-recommendation': 'price',
  '09-business-machine-learning/churn': 'churn',
  '09-business-machine-learning/delivery-plan': 'delivery',
};
const labStages = {
  'reference-lab/data-card': 0,
  'reference-lab/incident-report': 1,
  'reference-lab/model-card': 2,
  'reference-lab/evaluation': 3,
};

/**
 * @param {{ slug: string, category: string, chapter?: number, parentSlug?: string }} page
 * @returns {{ chapter: number } | { kind: PlateKind, stage: number } | null}
 */
export function plateFor(page) {
  if (page.parentSlug) return null;
  if (page.category === 'Chapter' && page.chapter) return { chapter: page.chapter };
  const kind = kinds[page.slug];
  return kind ? { kind, stage: labStages[page.slug] ?? -1 } : null;
}
