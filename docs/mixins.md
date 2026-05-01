# Mixin Catalog

Reusable SCSS mixins live in `scss/abstracts/_mixins.scss` (layout + utilities), `scss/abstracts/_breakpoints.scss` (media queries), and `scss/abstracts/_animations.scss` (keyframes + animation mixins).

**Rule:** reach for a mixin before writing raw CSS for anything on this list. Don't write `@media (min-width: 1024px)` by hand. Don't hand-roll a focus ring. Don't re-implement `visually-hidden`.

---

## Breakpoints

### `respond-to($name)`

The only way to write a media query. Accepts named breakpoints (`sm`, `md`, `lg`, `xl`).

```scss
.card {
  padding: $spacing-md;

  @include respond-to('lg') {
    padding: $spacing-xl;
  }
}
```

Never write `@media` directly. If you need a breakpoint that doesn't exist, add it to the breakpoints token map, don't hard-code the pixel value.

---

## Accessibility

### `focus-ring($color, $offset)`

WCAG 2.4.11-compliant focus ring (3:1 contrast on light and dark backgrounds). Apply to every interactive element's `:focus-visible` state.

```scss
.btn:focus-visible {
  @include focus-ring;
}

// Custom colour for dark backgrounds
.btn--on-dark:focus-visible {
  @include focus-ring($color-brand-mint);
}
```

Defaults: `$color-ui-focus`, `2px` offset.

### `visually-hidden` / `sr-only`

Hide an element from sighted users but keep it available to screen readers. Use for skip-link targets, form labels on icon-only controls, etc.

```scss
.skip-link {
  @include visually-hidden;

  &:focus {
    // restore on keyboard focus
    position: fixed;
    // ...
  }
}
```

`sr-only` is an alias for `visually-hidden`.

---

## Layout

### `container`

Page-width wrapper with responsive padding. Use on top-level section wrappers.

```scss
.page-content {
  @include container;
}
```

Produces: `max-width`, `margin-inline: auto`, `padding-inline` that scales with breakpoint.

### `flex-row($gap, $align, $justify)` / `flex-col($gap)`

Shorthand for common flex compositions. Defaults: `$gap: $spacing-md`, `$align: center`, `$justify: flex-start`.

```scss
.card__meta { @include flex-row($spacing-sm); }
.card__body { @include flex-col($spacing-md); }
```

### `auto-grid($min, $gap)`

CSS Grid with `auto-fit` columns. Defaults: `$min: 280px`, `$gap: $spacing-xl`.

```scss
.card-grid { @include auto-grid(320px, $spacing-lg); }
```

### `aspect-ratio($width, $height)`

Reserve space at a fixed ratio and clip overflow. Default: `16:9`.

```scss
.card__image { @include aspect-ratio(4, 3); }
```

---

## Typography

### `truncate`

Single-line truncation with ellipsis.

```scss
.card__title { @include truncate; }
```

### `line-clamp($lines)`

Multi-line truncation (webkit). Default: `2` lines.

```scss
.card__excerpt { @include line-clamp(3); }
```

### `fluid-type($min, $max, $min-vw, $max-vw)`

Clamp-based responsive typography. Scales smoothly between viewport widths.

```scss
.hero__heading { @include fluid-type(2rem, 3.5rem); }
```

Defaults: `$min-vw: 375px`, `$max-vw: 1280px`.

---

## Components

### `button-reset`

Strip all browser defaults from a `<button>`. Use as the first line of any custom button style.

```scss
.btn-ghost {
  @include button-reset;
  // custom styles...
}
```

### `surface($bg, $radius)`

Card / panel base — background, border, radius. Defaults: `$color-ui-surface`, `$radius-lg`.

```scss
.panel { @include surface; }
.panel--dark { @include surface($color-brand-navy, $radius-md); }
```

### `transition($props, $duration, $easing)`

Shorthand for a standard transition. Defaults: `all`, `0.2s`, `ease-in-out`.

```scss
.btn { @include transition(background-color); }
```

Use over raw `transition:` so durations stay consistent across components.

---

## Animation

See `animation.md` for scroll-entrance and parallax patterns. For mount-driven fades, use these mixins from `scss/abstracts/_animations.scss`:

### `anim-fade-in-up($duration, $easing, $delay, $fill)`

Fade in while rising 10px. Hidden until animation runs.

```scss
.menu__item {
  @include anim-fade-in-up($delay: 100ms);
}
```

### `anim-fade-in-down($duration, $easing, $delay, $fill)`

Fade in while descending 10px. Used in the mobile-menu stagger.

### `anim-fade-in($duration, $easing, $delay, $fill)`

Plain opacity fade, no translate.

All three defaults: `0.22s` (or `0.2s` for plain fade), `ease`, `0ms`, `forwards`.

---

## When to write a new mixin

Add a mixin when:

- A pattern appears in 3+ components and would otherwise be copy-pasted.
- The pattern has parameters (sizes, colours) that vary across usages.
- The pattern is hard to remember or easy to get wrong (focus ring, visually-hidden).

Don't add a mixin for a one-off. The SCSS should read like a description of the component, not a series of opaque `@include` calls.
