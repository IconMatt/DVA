# Tailwind v4 Conventions

Tailwind v4 here is **primarily a token system**, not a markup-utility system. Tokens enter through `@theme`, get exposed as CSS custom properties, and get generated into utilities. Components are still BEM. Utilities are a convenience layer, not a substitute.

This page documents the rules and the small set of conventions that keep the two layers from fighting each other.

---

## No `tailwind.config.js`

Tailwind v4 is CSS-first. Configuration lives in `@theme` blocks inside `src/theme/*.css`. There is **no** JS config file, and adding one is a regression.

If you need to extend the theme, add a token to the relevant `src/theme/*.css` file. Tailwind generates a matching utility automatically.

---

## `@theme` vs `@theme inline`

Two forms appear in the codebase:

- `@theme { --color-brown-900: #4b3928; }` — Tailwind generates the utility (`bg-brown-900`) from the literal value at compile time.
- `@theme inline { --color-foreground: var(--ink); }` — Tailwind emits the utility as `color: var(--ink)`, so swapping the upstream variable at runtime retheme-time changes the rendered colour without a rebuild.

Use `@theme inline` for semantic role tokens that may be overridden at runtime (the Mercury `theme.css` customisation path). Use plain `@theme` for raw palette values.

---

## `@source` directives

Tailwind only generates utilities for classes it can find in source files. `src/main.css` declares:

```css
@source "../templates";
@source "../index.html";
```

If a new directory contains markup using Tailwind utilities (a new `pages/` folder, embedded MDX, etc.), add an `@source` line. Without it, the utilities won't exist at runtime.

---

## When to use a utility vs. a BEM class

| Situation | Use |
|---|---|
| One-off layout (`md:grid-cols-2 gap-l`) on a section wrapper | Tailwind utility |
| Reusable visual style (card, button, hero) | BEM component file in `src/components/` |
| Spacing on a layout grid (`u-grid`, `gap-l`) | Tailwind utility |
| Spacing inside a component (`padding`, `gap`) | Component CSS reading `var(--space-*)` |
| Conditional state class for JS (`is-open`, `is-visible`) | BEM state class — never a Tailwind utility |
| Theming swap (light surface vs dark surface) | BEM modifier (`--dark`, `--inverse`) reading from semantic role tokens |

The mental model: **if the same class would repeat on three or more elements, it belongs in a component file.** Utilities are for the seam between components.

---

## `@apply` rules

`@apply` is allowed but kept rare. Acceptable uses:

- Inside `@layer base` to apply utility-styled defaults to bare elements.
- Inside `@layer components` to compress a long chain of utilities that genuinely don't deserve their own variable.
- Never in markup (Tailwind's `@apply` is a CSS feature, not a markup feature).

Component CSS in this project almost always reads `var(--token)` directly rather than `@apply`. That keeps components portable into the Drupal SDC theme without any Tailwind dependency on the consumer side.

---

## Available utility surface

Because of the `@theme` token set, the following are available in markup alongside BEM classes:

- **Colours** — `bg-brown-900`, `text-ink`, `border-warm`, `bg-sweet-grass`, etc. Slash-opacity works (`bg-brown-900/40`).
- **Typography** — `text-step-0` through `text-step-5`, plus `font-display`, `font-body`.
- **Spacing** — `m-s`, `p-l`, `gap-2xl`, plus paired tokens (`gap-s-l`).
- **Radius** — `rounded-sm`, `rounded-md`, `rounded-lg`, `rounded-xl`, `rounded-2xl`, `rounded-pill`.
- **Shadows** — `shadow-sm`, `shadow-md`, `shadow-lg`.
- **Breakpoints** — variants `xs:`, `sm:`, `md:`, `lg:`, `xl:`, `2xl:`, `wide:`.

If a utility doesn't generate (typo, missing token), check whether the token exists in `src/theme/*.css` and whether the markup is covered by an `@source` path.

---

## Legacy `:root` mirrors

Component CSS authored before the Tailwind port references `--step-*` / `--space-*` / `--font-size-*` directly. These names are mirrored in `:root` inside `src/theme/typography.css` and `src/theme/spacing.css`:

```css
:root {
  --step-0: var(--text-step-0);
  --space-s: var(--spacing-s);
  --font-size-md: var(--step-1);
  /* …etc */
}
```

**Keep these mirrors.** Removing them silently breaks every component file that uses the legacy names. New code should prefer the Tailwind-native token names (`--text-step-0`, `--spacing-s`) where convenient, but consistency inside an existing component file matters more than purity.

---

## CVA (Class Variant Authority)

The reference Mercury theme uses CVA in Twig. **This project does not.** The vetwell-design tw4 system applies BEM class names directly. When this work ports to Drupal:

- Conditional classes are computed in preprocess (`$variables['modifier_class']`) or via plain Twig (`{% set classes = ... %}`).
- `html_cva()` does **not** appear in templates.
- The `cva:cva` Drupal module is **not** a dependency.

See `drupal-mapping-pattern.md`.

---

## What to do when something doesn't fit

If a pattern doesn't fit into BEM + tokens + sparse utilities, stop and ask. Common cases:

- "I need to override Tailwind's preflight" — write a `@layer base` rule in `src/base/` instead.
- "I need a new colour" — add it to `src/theme/colors.css`; Tailwind generates the utility automatically.
- "I need a one-off breakpoint" — first check whether the seven existing breakpoints cover it. If genuinely not, add it to `src/theme/breakpoints.css` rather than hard-coding a pixel value.
- "I need a fluid value not in the scale" — author it as a `clamp()` directly in the component file with a `/* Custom fluid value: <reasoning> */` comment, **or** add a token to `src/theme/spacing.css`.
