# Clamp Calculator Spec

This document mirrors the four core Utopia calculator modes in a static-project-friendly way for this repo:

- `Type`
- `Space`
- `Grid`
- `Clamp`

The goal is not to recreate every Utopia UI detail. The goal is to preserve the same mental model, formulas, and token outputs in a way that fits this HTML/SCSS build and future Drupal/GovCMS handoff.

## Shared Model

Each calculator starts with two endpoints:

1. A minimum viewport width
2. A maximum viewport width
3. A minimum value at the small viewport
4. A maximum value at the large viewport

The browser then interpolates a fluid value between those endpoints with `clamp()`.

### Shared Formula

Given:

- `minWidth`
- `maxWidth`
- `minValue`
- `maxValue`

The linear scale is:

```text
slope = (maxValue - minValue) / (maxWidth - minWidth)
preferred = intercept + slope * viewport
intercept = minValue - (slope * minWidth)
```

Converted to CSS:

```css
clamp(min, intercept + slope * 100vw, max)
```

For `rem` output, divide pixel values by `16` before writing the final string.

## Type

The type calculator defines:

- minimum viewport width
- maximum viewport width
- minimum base font size
- maximum base font size
- minimum scale ratio
- maximum scale ratio
- steps above and below the base size

### Formula

For each step:

```text
stepMin = minBase * minRatio^step
stepMax = maxBase * maxRatio^step
stepClamp = clamp(stepMin, stepMax)
```

Negative steps reduce the base size by dividing through the ratio.

### Default Output Shape

```css
:root {
  --step--2: clamp(...);
  --step--1: clamp(...);
  --step-0: clamp(...);
  --step-1: clamp(...);
  --step-2: clamp(...);
  --step-3: clamp(...);
  --step-4: clamp(...);
  --step-5: clamp(...);
}
```

### Project Mapping

This repo can map the generated scale back onto semantic typography tokens instead of exposing raw Utopia names everywhere:

```text
$font-size-sm   -> var(--step--1)
$font-size-base -> var(--step-0)
$font-size-lg   -> var(--step-1)
$font-size-xl   -> var(--step-2)
$font-size-2xl  -> var(--step-3)
$font-size-3xl  -> var(--step-4)
```

## Space

The space calculator is built from the same min/max viewport widths and min/max base font sizes.

Instead of modular-scale steps, it applies named multipliers to the base size.

### Recommended Default Labels

```text
3xs, 2xs, xs, s, m, l, xl, 2xl, 3xl
```

### Recommended Default Multipliers

```text
0.25, 0.5, 0.75, 1, 1.5, 2, 3, 4, 6
```

### Formula

```text
spaceMin = minBase * multiplier
spaceMax = maxBase * multiplier
spaceClamp = clamp(spaceMin, spaceMax)
```

### One-Up Pairs

Adjacent sizes produce more dramatic growth:

```text
--space-xs-s
--space-s-m
--space-m-l
```

Each pair uses the smaller token at the minimum viewport and the larger token at the maximum viewport:

```text
pairMin = smaller.min
pairMax = larger.max
pairClamp = clamp(pairMin, pairMax)
```

### Custom Pairs

Any two named sizes can be paired:

```text
--space-s-l
--space-m-2xl
--space-2xl-xs
```

### Default Output Shape

```css
:root {
  --space-3xs: clamp(...);
  --space-2xs: clamp(...);
  --space-xs: clamp(...);
  --space-s: clamp(...);
  --space-m: clamp(...);
  --space-l: clamp(...);
  --space-xl: clamp(...);
  --space-2xl: clamp(...);
  --space-3xl: clamp(...);

  --space-xs-s: clamp(...);
  --space-s-m: clamp(...);
  --space-m-l: clamp(...);
  --space-s-l: clamp(...);
}
```

### Project Mapping

This repo keeps SCSS spacing aliases on top of the generated tokens:

```text
$spacing-3xs -> var(--space-3xs)
$spacing-2xs -> var(--space-2xs)
$spacing-xs  -> var(--space-xs)
$spacing-sm  -> var(--space-s)
$spacing-md  -> var(--space-m)
$spacing-lg  -> var(--space-l)
$spacing-xl  -> var(--space-xl)
$spacing-2xl -> var(--space-2xl)
$spacing-3xl -> var(--space-3xl)
```

## Grid

The grid calculator consumes responsive space tokens instead of inventing fresh gutter values.

### Inputs

- gutter minimum token
- gutter maximum token
- column max-width token
- number of columns

### Formula

The generated gutter is a fluid pair:

```text
gridGutter = clamp(gutterTokenMin.min, gutterTokenMax.max)
```

The generated container max width uses the maximum column width and the maximum gutter:

```text
gridMaxWidth = (columns * columnMax) + ((columns + 1) * gutterMax)
```

That matches the broad behavior of Utopia’s grid calculator, where the outer container padding is part of the complete width.

### Default Output Shape

```css
:root {
  --grid-max-width: 77.5rem;
  --grid-gutter: var(--space-s-l);
  --grid-columns: 12;
}

.u-container {
  max-width: var(--grid-max-width);
  padding-inline: var(--grid-gutter);
  margin-inline: auto;
}

.u-grid {
  display: grid;
  gap: var(--grid-gutter);
}
```

## Clamp

The generic clamp calculator is the escape hatch for any length token that does not belong in the shared type or space systems.

### Inputs

- token name
- minimum viewport width
- maximum viewport width
- minimum value
- maximum value
- unit: `rem` or `px`
- relative to: `viewport` or `container`

### Output Shape

```css
:root {
  --custom-token: clamp(...);
}
```

If `relative to` is `viewport`, use `vw`.

If `relative to` is `container`, use `cqi`.

## Figma Import (back-solving a modular scale)

The calculator includes a "Fit to Figma values" panel that accepts up to six fixed pixel sizes from a Figma canvas (Body, H5–H1) and back-solves a modular scale from them.

### Algorithm

1. Sort input values ascending.
2. Compute the ratio between each consecutive pair.
3. Take the **median** of those ratios (not the mean — median is robust against outlier values in non-strictly-modular type sets).
4. Clamp the result to a minimum of 1.05.
5. The smallest input value becomes `maxBase` (desktop body size).
6. `minBase` is either user-supplied or auto-suggested as `max(14, maxBase × 0.875)`.
7. `minRatio` is auto-suggested as `max(1.067, maxRatio − 0.04)` — a conventional flatter mobile ratio.

Each Figma value is mapped to its nearest scale step via:

```text
step = round(log(value / maxBase) / log(maxRatio))
```

Delta = Figma value − ideal modular value at that step. Deltas under ±2px are acceptable.

### What "Apply" does

Hitting **Apply to Type & Space** writes the back-solved values directly into the Type and Space calculator inputs, then dispatches a synthetic `input` event to trigger a full recalculation. No page reload is needed.

## Figma Grid Import

The Grid section includes a "Figma grid import" panel that accepts Figma's own grid settings and derives matching token selections.

### Figma Center formula

Figma's "Center" grid type does **not** include outer padding in the container width:

```text
containerPx = (columns × colWidth) + ((columns − 1) × gutter)
```

This is different from the CSS grid formula used by the main calculator, which adds `(columns + 1)` gutters to include outer padding. The Figma-derived container width is stored as `data-figma-container-rem` on the `#grid` element and is used verbatim in the generated prompt output.

### Token matching

The panel parses the live space-scale table to find the space token whose maximum value is closest to the Figma gutter. The mobile gutter suggestion is one step smaller in the scale.

## Generate Prompt

The **Generate** section bundles the live CSS outputs from the three calculators into a single `# Foundations setup` prompt that a UX designer can paste directly into Claude Code.

The prompt contains:
- `_typography.scss` — the fluid type scale CSS custom properties (`--step-*`)
- `_spacing.scss` — the fluid space scale (`--space-*`) plus semantic SCSS aliases (`$spacing-sm` etc.)
- `_grid.scss` — the grid tokens; `--grid-max-width` is overridden with the exact Figma-derived container rem value if the Figma grid panel was used
- A completion checklist

Brand colours, fonts, corner radius, and shadows are intentionally excluded — those are design decisions made separately and do not belong to the clamp/scale tooling.

## Defaults Used In The Demo Page

The static calculator page at `clamp-calculator/clamp-calculator.html` starts with these defaults:

```text
Type
- min viewport: 360
- min base size: 18
- min ratio: 1.2
- max viewport: 1440
- max base size: 20
- max ratio: 1.25
- steps up: 5
- steps down: 2

Space
- labels: 3xs,2xs,xs,s,m,l,xl,2xl,3xl
- multipliers: 0.25,0.5,0.75,1,1.5,2,3,4,6
- custom pair: s -> l

Grid
- gutter min: s
- gutter max: l
- column max: xl
- columns: 12

Clamp
- token: --size-fluid-card
- min viewport: 360
- max viewport: 1440
- min value: 24
- max value: 56
- unit: rem
- relative to: viewport
```

## Drupal / GovCMS Handoff

Suggested Drupal structure:

- This is best treated as a design-system utility page or internal pattern-library page, not a paragraph component.
- If productised inside Drupal, expose the calculator defaults through theme settings or a small configuration form rather than editorial content fields.

Expected fields if this becomes CMS-managed:

- page title
- intro copy
- optional documentation link
- optional default settings JSON

Preprocess notes:

- None are required for the static demo.
- If ported to Drupal, pass configuration values into `drupalSettings` or JSON script data and keep the formulas in attached JS.

Twig notes:

- Keep the template thin.
- Keep calculator math in JavaScript, not Twig.
- Keep output token naming predictable so the result can be pasted into SCSS token files.

Known implementation risks:

- Container-relative `cqi` output is not as universally familiar as viewport-relative `vw`; document support expectations if this moves into production tooling.
- This demo mirrors Utopia’s approach, but it is intentionally lighter than the full Utopia interface.
