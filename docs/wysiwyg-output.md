# CKEditor / WYSIWYG Output

Every Drupal site ends up with a rich-text body field. Editors fill it with an unpredictable mix of `<h2>`, `<h3>`, paragraphs, lists, blockquotes, tables, figures, and links — often all on the same page.

This doc covers how prose is styled in this project without letting CKEditor output leak across the rest of the design system.

---

## The rule

**All prose styling lives inside the `.page-content__section` wrapper.** The wrapper is defined in `src/base/prose.css`. Render any CKEditor / body field inside it and it styles correctly with no extra CSS per component:

```twig
<div class="page-content">
  <div class="page-content__section">
    {{ content.body }}
  </div>
</div>
```

The wrapper clamps to a comfortable reading column (`clamp(36rem, 50vw + 8rem, 56rem)`) and owns every element CKEditor can emit. The base `src/base/typography.css` rules apply at the element level too, but the prose wrapper overrides them in the contexts where editors are producing arbitrary HTML.

---

## Why a wrapper, not global element styles only

The base layer (`src/base/typography.css`) gives `h1`–`h5` a default font-size, weight, and `text-wrap: balance`. That covers unstyled HTML correctly. But editors produce *contextual* prose with vertical rhythm, list indentation, link decoration, table borders, and so on — applying all of that at the element level would clash with every component that uses `<h2>` or `<ul>` (cards, heroes, nav).

So the system splits cleanly:

- **Bare element defaults** live in `src/base/typography.css` (one-line heading sizes, body text-wrap).
- **Prose rhythm and contextual treatment** live in `src/base/prose.css` scoped under `.page-content__section`.

This gives editors a safe sandbox while keeping component styles predictable.

---

## What the wrapper styles

The wrapper has opinionated styles for every element CKEditor can emit. From `src/base/prose.css`:

- `h2`, `h3`, `h4`, `h5`, `h6` — sized from `--step-*` tokens with consistent `margin-block-start` rhythm using `--space-xl` / `--space-s`.
- `p` (no class) — `margin-block: 0 var(--space-s)`.
- `ul`, `ol`, `li` — list markers, nested lists, spacing with `--space-l` indent and `--space-2xs` between items. Nested lists demote markers (`disc → circle → square`, `decimal → lower-alpha`).
- `blockquote` — Halant serif with hanging punctuation, attribution via `<cite>`.
- `a` (no class) — animated underline-grow on `--color-zest`; focus ring on `--color-focus`.
- `strong`, `em`, `code` — semantic emphasis with token colours.
- `pre`, `code` — monospace block on `--color-sand-stone`, `--radius-md` corners.
- `table`, `thead`, `tbody`, `tr`, `th`, `td` — `border-bottom` borders, `--space-2xs / --space-s` padding, header weight.
- `figure`, `figcaption`, `img` — full-width image with `--radius-md` corners, caption typography from the `--step--1` size.
- `hr` — `--space-xl` margin, faint `border-top`.
- First- and last-child margin resets so the wrapper introduces no unwanted gaps.

All values come from design tokens — no hard-coded values inside `prose.css`.

---

## Embedded components inside prose

Editors can also place page-builder components inside the body field (quick-links, callouts, downloads). When they do:

1. The component keeps its own BEM block scope (`.quick-links`, `.downloads`).
2. `prose.css` only styles **bare** elements (selectors with `:not([class])`) so it never overrides component styles.
3. For specific cases where the editor-embedded component needs a layout adjustment inside the prose column, scope an override under `.page-content__section .component-name` (see `.quick-links--results-top` in `prose.css` for the pattern).

Prefer entity-embed components for anything non-trivial. CKEditor is not a layout tool.

---

## CKEditor configuration should match

Whatever elements the wrapper styles, the CKEditor toolbar should allow — no more. Otherwise editors will insert elements that don't have a style, or produce inline markup (colours, font sizes) that breaks the design system.

- Strip inline styles via the text format filter (`filter_html` or equivalent).
- Disable the "Font size" and "Font colour" plugins.
- Allow heading levels the wrapper styles (typically `h2`–`h4`, not `h1` — the page owns `h1`).
- Allow `<table>` only if the wrapper styles tables (it does).

---

## Accessibility

- Heading levels inside prose start at `h2` (the page owns `h1`).
- Use `scope` on table headers when tables are data-bearing.
- Don't rely on colour alone for link styling — the underline-grow effect changes weight as well as colour.
- Blockquotes use `<blockquote>` with optional `<cite>`, not just italic paragraphs.
- Reduced-motion: link underline transitions are removed inside `@media (prefers-reduced-motion: reduce)`.

---

## Drupal port

When this lands in the Drupal SDC theme:

- The wrapper is rendered by a `field--body` Twig template (or a `paragraph--text` SDC component depending on the content model).
- `src/base/prose.css` is loaded as part of the global stylesheet — no per-component prose styles needed.
- Editor toolbars are configured per text format in Drupal admin; mirror the toolbar to the wrapper's supported elements.

---

## Checklist

- [ ] `.page-content__section` wraps all CKEditor body field output
- [ ] Wrapper uses design tokens only — no hard-coded values
- [ ] First/last-child margins are reset
- [ ] Every element CKEditor can emit has a style
- [ ] CKEditor toolbar matches what the wrapper supports
- [ ] Heading levels start at `h2` inside prose
- [ ] Table headers use `scope`
- [ ] Links are distinguishable without colour alone
