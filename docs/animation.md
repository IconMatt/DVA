# Animation

This project uses two animation systems. Use each for the right purpose — they are not interchangeable.

---

## 1. Scroll-entrance animations (`data-animate`)

**What it does:** Fades elements in from slightly below as they scroll into the viewport.

**Where the code lives:**
- CSS: `src/utilities/scroll-animations.css`
- JS: Inline `IntersectionObserver` block in every template (look for `// Staggered entrance animations`)

### How to use

Add `data-animate` to any element you want to animate in on scroll:

```html
<h2 data-animate>Heading</h2>
<p data-animate>Body text</p>
```

Wrap a grid or list in `data-animate-stagger` to auto-stagger child delays:

```html
<div data-animate-stagger>
  <article class="card" data-animate>Card 1</article>
  <article class="card" data-animate>Card 2</article>
  <article class="card" data-animate>Card 3</article>
</div>
```

Override the delay on a specific element with `--animate-delay`:

```html
<h1 data-animate>Title</h1>
<p data-animate style="--animate-delay: 100ms">Subtitle</p>
<div data-animate style="--animate-delay: 200ms">Search box</div>
```

### How it works

1. The page sets `.js-animations` on `<html>` (or `<body>`) once JS boots. Before that class lands, `[data-animate]` elements render fully visible — so users with no JS still see the page.
2. With `.js-animations` present, every `[data-animate]` is invisible (`opacity: 0; transform: translateY(12px)`).
3. An `IntersectionObserver` watches each element.
4. When the element enters the viewport, `.is-visible` is added → CSS transitions it to `opacity: 1; transform: none`.
5. Stagger containers (`data-animate-stagger`) receive incremental `--animate-delay` values (50ms apart) automatically across their direct `[data-animate]` children.

### Fallback

If `IntersectionObserver` is unavailable, all `[data-animate]` elements are immediately shown with `.is-visible` so nothing stays invisible.

### Reduced motion

All transitions are disabled under `prefers-reduced-motion: reduce`. Elements show immediately with no animation. The base rule in `src/utilities/scroll-animations.css`:

```css
@media (prefers-reduced-motion: reduce) {
  .js-animations [data-animate] {
    opacity: 1;
    transform: none;
    transition: none;
  }
  [data-parallax],
  [data-parallax-bg],
  [data-parallax-media] {
    transform: none !important;
    will-change: auto;
  }
}
```

---

## 2. Parallax (vanilla JS, scroll-based)

**What it does:** Moves decorative SVG / image elements at a slower rate than the scroll, creating a depth effect.

**Where the code lives:** Inline `<script>` blocks in individual templates (not shared). Look for `// Parallax` or `requestAnimationFrame`.

### Hooks

| Hook | Purpose | Offset source |
|---|---|---|
| `data-parallax` | Foreground SVG / element inside a positioned ancestor | `el.offsetParent` is fine |
| `data-parallax-bg` | Section-level background layer | **MUST** use `el.getBoundingClientRect()` (see LESSONS) |
| `data-parallax-media` | Image inside a clipped/rounded card | Needs a height-based bleed buffer (see LESSONS) |

### How it works

```js
var ticking = false;
window.addEventListener('scroll', function () {
  if (!ticking) {
    requestAnimationFrame(function () {
      right.style.transform = 'translateY(' + (-window.scrollY * 0.12) + 'px)';
      ticking = false;
    });
    ticking = true;
  }
});
```

The `ticking` flag ensures only one `requestAnimationFrame` is queued per scroll event — this keeps performance smooth and avoids layout thrashing.

### Important: don't add a base transform offset

The JS only applies a scroll delta. The starting CSS position is set in the component CSS (`top`, `right`, etc. on `.hero__device-grid--right`). Do not add a `calc(-50% + ...)` base in the JS — this causes a visible jump when the first scroll event fires.

---

## Rules

1. **Use `data-animate` for all scroll-entrance animations.** Don't write custom IntersectionObserver code per-component.
2. **Keep parallax to decorative elements only.** Do not apply parallax to content, cards (the content of the card), or anything the user needs to read.
3. **Always pair CSS animations with a `prefers-reduced-motion` reset.**
4. **Parallax JS uses the `ticking` rAF pattern.** Always throttle scroll listeners with `requestAnimationFrame` — never bind expensive work directly to the scroll event.
5. **Don't use JS to animate things CSS can handle** (hover states, focus rings, simple transitions). JS animation is for scroll-driven or mount-driven effects only.
6. **Enter-animation classes must stay applied for the full keyframe duration.** Removing an `is-entering` class on the next `requestAnimationFrame` collapses the animation into a barely-visible snap. See LESSONS.

---

## Drupal port

When this lands in the Drupal SDC theme:

- The shared `[data-animate]` host CSS lives in the theme's global stylesheet (mirror of `src/utilities/scroll-animations.css`).
- The shared IntersectionObserver wiring moves out of each template and into a single `Drupal.behaviors` attached as `vetwell/global` library.
- Per-component parallax stays in component JS files (one `Drupal.behaviors` per component) so unused components don't ship dead code.
- The Mercury-style `lib/component.js` (`ComponentInstance` / `ComponentType`) is an optional encapsulation layer, not a requirement — small components are fine with plain `Drupal.behaviors`.
