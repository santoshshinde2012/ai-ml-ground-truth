// The paperback's physical rules, from Amazon KDP's help pages on paperback submission
// and cover size, checked November 2026. Lengths are in inches.

/** 7 x 10 inch trim: a common size for technical books, with room for code and tables. */
export const trim = { width: 7, height: 10 };
export const bleed = 0.125;
/** The edition's margins. Inside is the binding edge. */
export const margins = { top: 0.75, bottom: 0.8, inside: 0.875, outside: 0.625 };
/** Black ink on white paper. */
const thicknessPerPage = { white: 0.002252, cream: 0.0025 };
/** KDP prints text on the spine only from this page count. */
export const spineTextMinimumPages = 79;

/** KDP's smallest inside margin for a page count. */
export function minimumInsideMargin(pages) {
  if (pages < 24 || pages > 828) throw new RangeError(`KDP prints 24 to 828 pages, not ${pages}.`);
  if (pages <= 150) return 0.375;
  if (pages <= 300) return 0.5;
  if (pages <= 500) return 0.625;
  if (pages <= 700) return 0.75;
  return 0.875;
}
/** KDP's smallest outside, top and bottom margin without bleed. */
export const minimumOuterMargin = 0.25;

export function spineWidth(pages, paper = 'white') {
  return pages * thicknessPerPage[paper];
}

/** The full cover sheet: back, spine and front, with bleed on every outer edge. */
export function coverSize(pages, paper = 'white') {
  const spine = spineWidth(pages, paper);
  return {
    width: bleed + trim.width + spine + trim.width + bleed,
    height: bleed + trim.height + bleed,
    spine,
  };
}

/** The checks KDP applies to an interior, as a list of problems; empty when it fits. */
export function interiorProblems(pages) {
  const problems = [];
  if (pages < 24 || pages > 828) problems.push(`KDP prints 24 to 828 pages; this has ${pages}.`);
  else if (margins.inside < minimumInsideMargin(pages))
    problems.push(
      `${pages} pages need an inside margin of ${minimumInsideMargin(pages)} in; this edition uses ${margins.inside} in.`,
    );
  for (const side of ['top', 'bottom', 'outside'])
    if (margins[side] < minimumOuterMargin)
      problems.push(`The ${side} margin is below KDP's ${minimumOuterMargin} in.`);
  return problems;
}
