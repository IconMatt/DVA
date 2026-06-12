# vetwell-design — Tailwind v4

Front-end build for the Veteran and Family Wellbeing Agency site: HTML templates + Tailwind v4 CSS + minimal vanilla JS, designed for Drupal / GovCMS handoff via Single Directory Components (SDC). Started life as a parallel `tw4/` build of the SCSS project; now promoted to the repo root. The legacy `scss/` tree is kept for cross-checking only — the build does not consume it.

## Layout

```
├── src/                # CSS source
│   ├── main.css        # entry — imports theme, base, utilities, components
│   ├── theme/          # @theme tokens (colors, typography, spacing, radius, breakpoints, motion)
│   ├── base/           # reset, typography defaults, prose wrapper
│   ├── components/     # BEM components, one block per file
│   └── utilities/      # container, scroll-animations, page-specific overrides
├── templates/          # 11 HTML page templates
├── assets/             # images, icons
├── css/main.css        # build output (minified)
├── docs/               # working conventions + Drupal handoff docs
├── accessibility/      # Lighthouse audit reports (12 Jun 2026, GovCMS staging)
├── scss/               # legacy SCSS — reference only, not built
├── _tools/             # clamp-calculator (fluid scale tooling)
└── index.html          # menu page
```

## Develop / build

```sh
npm install
npm run dev      # watch mode → css/main.css (UNMINIFIED — never commit this output)
npm run build    # one-shot, minified — always run before committing css/main.css
```

See `LESSONS.md` for why the dev/build distinction matters when committing.

## Conventions

The working rules live in `AGENTS.md` and `docs/` — read those first. The short version:

- Tailwind v4 is **primarily a token system** here. Tokens enter through `@theme` blocks in `src/theme/*.css` (no `tailwind.config.js`); components are BEM, authored as plain CSS against `var(--token)`.
- Seven breakpoints (`xs:360`, `sm:560`, `md:840`, `lg:1120`, `xl:1440`, `2xl:1680`, `wide:1920`) mirrored between CSS and Tailwind variants.
- Fluid Utopia-style clamp scales for type and spacing, with legacy `--step-*` / `--space-*` mirrors in `:root`.
- No hex / rgb / hsl outside `src/theme/colors.css`.
- Accessibility target: WCAG 2.2 AA. See `docs/accessibility-checklist.md` and the audit reports in `accessibility/`.

## Parity with the legacy SCSS build

- Token values were ported verbatim from `scss/tokens/` and `scss/abstracts/_tokens.scss`; cross-check there when in doubt.
- Every legacy `scss/components/_*.scss` has a 1:1 sibling under `src/components/`. Sass `$vars` became `var(--*)`, `@include respond-to("md")` became `@media (min-width: 840px)`, mixins were inlined.
- Same root font-size scaling above 1440px (`src/base/reset.css`), same reduced-motion guards, same inline `<script>` behaviour and `data-*` hooks, same BEM class names.

## Drupal handoff

The CSS ports as-is into the Mercury-derived theme; templates are rebuilt as thin SDC Twig. See `docs/drupal-handoff.md`, `docs/drupal-mapping-pattern.md`, and `docs/drupal-a11y-actions.md` (open accessibility actions for the Drupal team).
