# Animation

This project uses two animation systems. Use each for the right purpose — they are not interchangeable.

---

## 1. Scroll-entrance animations (`data-animate`)

**What it does:** Fades elements in from slightly below as they scroll into the viewport.

**Where the code lives:**
- CSS: `scss/utilities/_scroll-animations.scss`
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

1. On page load, every `[data-animate]` element is invisible (`opacity: 0; transform: translateY(12px)`)
2. An `IntersectionObserver` watches each element
3. When the element enters the viewport, `.is-visible` is added → CSS transitions it to `opacity: 1; transform: none`
4. Stagger containers (`data-animate-stagger`) receive incremental `--animate-delay` values (50ms apart) automatically across their direct `[data-animate]` children

### Fallback

If `IntersectionObserver` is not available (very old browsers), all `[data-animate]` elements are immediately shown with `.is-visible` so nothing stays invisible.

### Reduced motion

All transitions are disabled when the user has `prefers-reduced-motion: reduce` set. Elements show immediately with no animation.

```scss
@media (prefers-reduced-motion: reduce) {
  [data-animate] {
    opacity: 1;
    transform: none;
    transition: none;
  }
}
```

---

## 2. Parallax (vanilla JS, scroll-based)

**What it does:** Moves decorative SVG elements at a slower rate than the scroll, creating a depth effect.

**Where the code lives:** Inline `<script>` blocks in individual templates (not shared). Look for `// Parallax` or `requestAnimationFrame`.

### Current parallax instances

| Template | Element | Speed factor | Notes |
|---|---|---|---|
| `home.html` | `.hero__device-grid--right` | `−0.12` | Moves up at 12% of scroll speed |
| `home.html` | `.hero__device-grid--left` | `−0.08` | Slower, different base transform |
| `topic-landing.html` | `.hero__banner-image` | varies | Banner image + device SVG |
| `content.html` | `.hero__device-grid--right` | `−0.12` | Content page hero SVG only |
| `resource-library.html` | `.hero__device-grid--right` | `−0.12` | Same pattern |

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

The JS only applies a scroll delta. The starting CSS position is set in SCSS (`top`, `right`, etc. on `__device-grid--right`). Do not add a `calc(-50% + ...)` base in the JS — this causes a visible jump when the first scroll event fires.

---

## Rules

1. **Use `data-animate` for all scroll-entrance animations.** Don't write custom IntersectionObserver code per-component.
2. **Keep parallax to decorative hero SVGs only.** Do not apply parallax to content, cards, or anything the user needs to read.
3. **Always pair CSS animations with a `prefers-reduced-motion` reset.**
4. **Parallax JS uses the `ticking` rAF pattern.** Always throttle scroll listeners with `requestAnimationFrame` — never bind expensive work directly to the scroll event.
5. **Don't use JS to animate things CSS can handle** (hover states, focus rings, transitions). JS animation is for scroll-driven or mount-driven effects only.
