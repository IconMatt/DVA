# CKEditor / WYSIWYG Output

Every Drupal site ends up with a rich-text body field somewhere. Editors fill it with an unpredictable mix of `<h2>`, `<h3>`, paragraphs, lists, blockquotes, tables, figures, and links — often all on the same page.

This doc covers how we style that output without letting it leak across the rest of the design system.

---

## The rule

**All prose styling lives inside a single wrapper class.** In this project that wrapper is `.page-content__section` (see `scss/pages/_content.scss`). On other projects it's often `.prose`, `.wysiwyg`, or `.rich-text`.

Render any CKEditor / body field inside that wrapper and it styles correctly with no extra CSS per component:

```twig
<div class="page-content__section">
  {{ content.body }}
</div>
```

---

## Why a wrapper, not global element styles

If you style `h2`, `ul`, `blockquote` globally, those styles will clash with every component that uses those elements (cards, heroes, nav, etc.). Scoping everything inside a wrapper class:

- Keeps component styles predictable (a `.card__title` that happens to be an `h2` isn't affected).
- Gives editors a safe sandbox — they can drop any valid HTML into the body and it will be styled.
- Makes it trivial to move the wrapper onto a different field later (sidebars, alerts, etc.).

---

## What the wrapper should style

At minimum, the wrapper needs opinionated styles for every element CKEditor can emit:

- `h2`, `h3`, `h4`, `h5`, `h6` — sized using typography tokens, with consistent `margin-top` rhythm
- `p` — line-height, spacing
- `ul`, `ol`, `li` — list markers, nested lists, spacing
- `blockquote` — visual treatment, attribution
- `a` — link colour, hover, focus ring
- `strong`, `em`, `code`
- `pre`, `code` — monospace block and inline
- `table`, `thead`, `tbody`, `tr`, `th`, `td` — borders, padding, zebra if needed
- `figure`, `figcaption`, `img` — max-width, alignment
- `hr` — divider treatment
- First- and last-child margin resets (so the wrapper doesn't introduce unwanted gaps)

Always use design tokens for colours, spacing, and typography — never hard-coded values. See `frontend-rules.md`.

---

## CKEditor configuration should match

Whatever elements the wrapper styles, the CKEditor toolbar should allow — no more. Otherwise editors will insert elements that don't have a style, or produce inline markup (colours, font sizes) that breaks the design system.

- Strip inline styles via the text format filter (`filter_html` or an equivalent).
- Disable the "Font size" and "Font colour" plugins.
- Allow heading levels the wrapper styles (typically `h2`–`h4`, not `h1`).
- Allow `<table>` only if the wrapper styles tables.

---

## Full-bleed elements inside prose

Sometimes the design calls for an image, pull-quote, or callout to break out of the prose column. Two clean approaches:

1. **Nested component**: CKEditor-embedded entity (e.g. `entity_embed`) rendered as its own paragraph component — styled by its own BEM class, not the prose wrapper.
2. **Max-width reset**: give the wrapper a constrained `max-width`, then selectively reset it on figures with a modifier class (`.page-content__section figure.is-wide`).

Prefer option 1 for anything non-trivial. CKEditor is not a layout tool.

---

## Accessibility

- Ensure heading levels inside prose start at `h2` (the page owns `h1`).
- Use `scope` on table headers when tables are data-bearing.
- Don't rely on colour alone for link styling — underline or weight must also differ.
- Blockquotes should use `<blockquote>` with a `<cite>`, not just italic paragraphs.

---

## Checklist

- [ ] One wrapper class owns all prose styling
- [ ] Wrapper uses design tokens, not hard-coded values
- [ ] First/last-child margins are reset
- [ ] Every element CKEditor can emit has a style
- [ ] CKEditor toolbar matches what the wrapper supports
- [ ] Heading levels start at `h2`
- [ ] Table headers use `scope`
- [ ] Links are distinguishable without colour alone
