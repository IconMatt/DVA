# SCSS Architecture

The stylesheet is layered. Each layer consumes only the layers below it — there are no circular dependencies, and nothing in a lower layer references a higher layer by name.

```
tokens      →  design values (colours, spacing, typography, radius, breakpoints)
abstracts   →  variables, mixins, functions, keyframes (no output on their own)
base        →  element resets, global typography, defaults
utilities   →  narrow-purpose helpers (scroll animations, visually-hidden, etc.)
atoms       →  smallest components — buttons, badges, inputs, icons
molecules   →  small compositions — search box, card meta, nav item
organisms   →  full sections — hero, card grid, footer, main nav
pages       →  page-specific composition (minimal; prefer components)
```

---

## What goes in each layer

### `tokens/`

Design values only. No selectors, no mixins. Every number, colour, and font value in the system starts here.

- `_colors.scss` — brand, neutral, UI semantic
- `_spacing.scss` — spacing scale (`$spacing-xs`, `$spacing-sm`, ...)
- `_typography.scss` — font families, sizes, weights, line heights
- `_radius.scss` — border-radius scale
- `_shadows.scss` — elevation levels

All token variables carry `!default` so a sub-theme can override any of them by importing its own `_overrides.scss` before the tokens partial.

### `abstracts/`

Code that produces no CSS output on its own — mixins, functions, keyframes, internal variables.

- `_breakpoints.scss` — `respond-to()` mixin + breakpoint map
- `_mixins.scss` — reusable mixins (`focus-ring`, `container`, `transition`, etc.)
- `_animations.scss` — keyframes and animation mixins
- `_variables.scss` — layout internals (container max-width, z-index scale)

### `base/`

Element-level defaults. No classes. Covers the unstyled-HTML baseline.

- `_reset.scss` — margins, box-sizing, img defaults
- `_typography.scss` — body font, heading defaults
- `_forms.scss` — input, button, select baseline

### `utilities/`

Narrow-purpose helpers that don't belong to any one component. Each file is a single concern.

- `_scroll-animations.scss` — `[data-animate]` fade-in-up behaviour
- `_visually-hidden.scss` — screen-reader-only class
- `_skip-link.scss` — accessibility skip link

Utilities are **not** layout shortcuts. No `.mt-4`, `.text-center`, `.flex`. See `frontend-rules.md` hard rules.

### `atoms/`

The smallest components — can't be broken down further without becoming an element.

- `_button.scss`
- `_badge.scss`
- `_icon.scss`
- `_input.scss`

### `molecules/`

Small compositions of atoms. They have a job, but they're not a full page section.

- `_search-box.scss`
- `_card-meta.scss`
- `_breadcrumb.scss`

### `organisms/`

Full page sections. Usually map 1:1 with Drupal paragraph types.

- `_hero.scss`
- `_card.scss` (the card itself, composed of atoms and molecules)
- `_footer.scss`
- `_main-nav.scss`

### `pages/`

Page-specific composition where absolutely needed. Keep minimal. **Prefer adding a variant to an organism** over a page-level override.

- `_content.scss` — prose wrapper (see `wysiwyg-output.md`)
- `_resource-library.scss` — grid composition specific to that page

---

## Rules

1. **No layer skips a layer upward.** A token file never references a mixin. An atom never references an organism.
2. **Pages are not a dumping ground.** If you find yourself writing page-level overrides to tweak a component, add a modifier to the component instead.
3. **Organisms compose; they don't redefine.** A hero uses `.btn`, doesn't restyle buttons.
4. **One component per file.** `_card.scss` owns everything that starts with `.card`. Split only when variants grow unwieldy (`_card-featured.scss`).
5. **Imports live in `main.scss` in layer order.** Tokens first, pages last. The order is the dependency graph.

---

## main.scss order

```scss
// 1. Tokens (overridable design values)
@import 'tokens/colors';
@import 'tokens/spacing';
@import 'tokens/typography';
@import 'tokens/radius';
@import 'tokens/shadows';

// 2. Abstracts (no output)
@import 'abstracts/breakpoints';
@import 'abstracts/variables';
@import 'abstracts/mixins';
@import 'abstracts/animations';

// 3. Base (element defaults)
@import 'base/reset';
@import 'base/typography';
@import 'base/forms';

// 4. Utilities
@import 'utilities/scroll-animations';
@import 'utilities/visually-hidden';

// 5. Components
@import 'atoms/button';
@import 'atoms/badge';
// ...

@import 'molecules/search-box';
// ...

@import 'organisms/hero';
@import 'organisms/card';
// ...

// 6. Pages
@import 'pages/content';
@import 'pages/resource-library';
```

---

## Sub-theme overrides

Because every token uses `!default`, a Drupal sub-theme can override any design value:

```scss
// subtheme/scss/_overrides.scss
$color-brand-navy: #002a5c;
$spacing-lg: 28px;

// subtheme/scss/main.scss
@import 'overrides';   // must come BEFORE tokens
@import '../../parent-theme/scss/main';
```

The parent theme's tokens only apply if the sub-theme hasn't already defined them.
