# CSS Architecture

The stylesheet is layered. Each layer consumes only the layers below it. The dependency graph is literally the import order in `src/main.css` — no circular dependencies, nothing in a lower layer references a higher layer by name.

```
theme       →  design tokens (@theme blocks — colours, type, space, radius, breakpoints, motion)
base        →  element resets, global typography, prose wrapper
utilities   →  layout primitives (.u-container, .u-grid), scroll-animation host
components  →  BEM components (32 files, one per block)
page        →  page-specific overrides (kept tiny)
```

Tailwind v4 is the build engine. It runs the `@import "tailwindcss"` core (preflight + utility generation), reads every `@theme` block to know which tokens become utilities, scans the `@source` paths to know which utilities are actually used, then emits the minified CSS to `css/main.css`.

---

## What goes in each layer

### `src/theme/` — tokens

Design values only. Every number, colour, font value, breakpoint, and motion constant in the system starts here. No selectors except `@theme` and `:root`.

- `colors.css` — raw palette + semantic roles + shadows. Hex / rgb / hsl values may only appear in this file.
- `typography.css` — `--font-display`, `--font-body`, `--text-step-*` fluid clamp scale, `:root` legacy aliases (`--step-*`, `--font-size-*`, line-height + weight).
- `spacing.css` — `--spacing-3xs … 3xl` singles plus paired tokens (`--spacing-s-l`), `:root` legacy mirrors (`--space-*`), container + grid layout values.
- `radius.css` — radius scale (`--radius-sm` … `--radius-2xl`, `--radius-pill`).
- `breakpoints.css` — the seven project breakpoints declared as `--breakpoint-*` so Tailwind generates `xs:`, `sm:`, `md:`, `lg:`, `xl:`, `2xl:`, `wide:` variants.
- `motion.css` — `--transition-base`, `--transition-slow`, easing tokens.

Tokens flow through `@theme` so Tailwind utilities derive from them (`bg-brown-900`, `text-step-2`, `gap-l`, `rounded-card`). The `:root` mirrors exist because component CSS authored before the Tailwind port references `--step-*` / `--space-*` directly; do not delete those mirrors unless you also rewrite every component that consumes them.

### `src/base/` — element defaults

Element-level defaults. No classes (except `.headings-serif` opt-in and the `.page-content__section` prose wrapper).

- `reset.css` — margins, box-sizing, image defaults, root font-size scaling above the `xl` breakpoint.
- `typography.css` — heading font, base body, `text-wrap: balance` on `h1`–`h4`, `text-wrap: pretty` on `p`, `li`, `dd`.
- `prose.css` — `.page-content__section` wrapper that styles every element CKEditor can emit. See `wysiwyg-output.md`.

### `src/utilities/` — narrow-purpose helpers

Single-concern helpers that don't belong to any one component.

- `container.css` — `.container`, `.u-container`, `.u-grid`. These are the **only** non-Tailwind utility classes in the system; they're prefixed `u-` to mark them as primitives.
- `scroll-animations.css` — `[data-animate]` host styles, parallax `will-change`, reduced-motion guards. See `animation.md`.
- `home-page.css` — page-specific layout overrides (the one place page-specific CSS is allowed; keep it tiny).

Utilities are **not** layout shortcuts in the Tailwind sense. There is no `.mt-4`, `.text-center`, `.flex` here — Tailwind's own utility generator already covers those when needed in markup.

### `src/components/` — BEM components

One BEM block per file. 32 files. Each file owns everything that starts with that block name. Variants live in the same file unless they grow large enough to justify splitting.

Components author plain CSS against the `var(--token)` API. `@apply` is allowed but rare — most rules read like:

```css
.card__title {
  font-size: var(--font-size-md);
  line-height: var(--line-height-snug);
  color: var(--color-brown-900);
}
```

This makes components portable into the Drupal theme without any Sass / Tailwind-specific syntax.

### Page-specific

Page-specific tweaks live in `src/utilities/home-page.css` (legacy filename — page overrides, not utilities). Prefer adding a modifier to an organism over a page-level override.

---

## Rules

1. **No layer skips a layer upward.** A token file never references a component class. A component never overrides a token value.
2. **Pages are not a dumping ground.** If you find yourself writing page-level CSS to tweak a component, add a modifier to the component instead.
3. **Components compose; they don't redefine.** A hero uses `.button`, doesn't restyle buttons.
4. **One BEM block per file.** `card.css` owns everything starting with `.card`. Split only when variants grow unwieldy.
5. **Imports live in `src/main.css` in layer order.** Tokens first, page-specific last. The order is the dependency graph.

---

## `src/main.css` order

```css
@import "tailwindcss";

@source "../templates";
@source "../index.html";

/* Tokens */
@import "./theme/colors.css";
@import "./theme/typography.css";
@import "./theme/spacing.css";
@import "./theme/radius.css";
@import "./theme/breakpoints.css";
@import "./theme/motion.css";

/* Base */
@import "./base/reset.css";
@import "./base/typography.css";
@import "./base/prose.css";

/* Utilities */
@import "./utilities/container.css";
@import "./utilities/scroll-animations.css";

/* Components — 32 BEM files */
@import "./components/buttons.css";
@import "./components/site-header.css";
/* …etc */

/* Page-specific */
@import "./utilities/home-page.css";
```

---

## Sub-theme overrides (for the Drupal port)

When this lands in a Mercury-derived Drupal theme, editors can retheme by editing `theme.css` and `fonts.css` next to `index.php` — Mercury picks them up without a rebuild. Token definitions written through `@theme` blocks compile into the build; downstream `:root` overrides applied through a runtime `theme.css` file win because they cascade later.

For local rethemes during prototyping, edit `src/theme/colors.css` (or the relevant token file) and let Tailwind regenerate.
