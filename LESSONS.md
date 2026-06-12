# LESSONS.md

Running log of corrections. Each entry prevents a future mistake.
Read before starting work. Append (don't edit) when something goes wrong.

- Headings get `text-wrap: balance`; body copy gets `text-wrap: pretty`.
- Wire text wrapping into base typography or a shared mixin. Do not re-apply it per component.
- Raster images must ship with `srcset` + `sizes`. The page scales fluidly above the `wide` breakpoint (clamp on root font-size, container max grows to 1600px), so single-resolution images will look soft on large displays.
- Hero (and any rounded, full-bleed panel with a GPU-composited pseudo-element): use `overflow: hidden`, not `overflow: clip`. `overflow: clip` skips the Block Formatting Context so the compositor is not guaranteed to clip the promoted layer flush with the edge during resize repaints — a sub-pixel strip of the gradient background bleeds through on the right. Also give the `::before` a small horizontal overbleed (`inset: … -2px`) as insurance against fractional-pixel hero widths.
- Background parallax layers (`data-parallax-bg`) must compute their viewport offset from `el.getBoundingClientRect()` directly — **never** via `el.offsetParent`. The hero section has no positioned ancestor, so `offsetParent` resolves to `<body>` (full page height ~4800 px), producing an offset ~20× too large that overshoots the parallax buffer and exposes the gradient background at the bottom of the hero. Foreground layers (`data-parallax`) are `position: absolute` inside a positioned container, so `offsetParent` is correct for those.
- Cropped image parallax needs a height-based bleed buffer. If the image itself moves inside a rounded/hidden container, extend it beyond the mask before translating so card or panel background cannot show at the crop edge.
- Enter animation classes must stay applied for the full keyframe duration. Removing an `is-entering` class on the next `requestAnimationFrame` collapses a fade/scale/slide animation into a barely visible snap.
- Tailwind v4's `@import "tailwindcss"` registers a built-in `.container` utility that emits `max-width: <breakpoint>` inside `@media (min-width: <breakpoint>)` for every breakpoint (360, 560, 840, 1120, 1440, 1680, 1920). Combined with `margin-inline: auto`, this clamps content to the breakpoint floor and centres it — producing big flanking whitespace next to anything using `class="container"`. The project's `.container` in `src/utilities/container.css` must set `max-width: none` explicitly to neutralise Tailwind's caps; otherwise hero panels, resource grids, and any other component using the BEM `.container` will look inset compared to the SCSS source. (Diagnose by grepping the built `css/main.css` for `.container{` — if multiple `max-width: <breakpoint>` rules appear, the override is missing.)
- Tailwind v4's `--minify` (Lightning CSS) drops the FIRST of a vendor-prefixed/unprefixed pair when both appear in the same declaration block. So this source order:
  ```css
  backdrop-filter: blur(14px) saturate(140%);
  -webkit-backdrop-filter: blur(14px) saturate(140%);
  ```
  ships as `-webkit-backdrop-filter: …` only. Modern Chrome/Firefox use the unprefixed form, so the property has no effect. **Fix:** declare the prefixed form FIRST so the unprefixed survives:
  ```css
  -webkit-backdrop-filter: blur(14px) saturate(140%);
  backdrop-filter: blur(14px) saturate(140%);
  ```
  Affects backdrop-filter and likely every `-webkit-` paired property.
- Tailwind v4's `--minify` also strips the whitespace SEPARATOR between space-separated filter-function lists, emitting `blur(14px)saturate(140%)` — invalid syntax, declaration ignored. **Fix:** wrap multi-function values in a custom property; the minifier doesn't touch custom-property contents.
  ```css
  --site-header-backdrop: blur(14px) saturate(140%);
  -webkit-backdrop-filter: var(--site-header-backdrop);
  backdrop-filter: var(--site-header-backdrop);
  ```
  Single-function values (`blur(6px)`) aren't affected — only multi-function `backdrop-filter` / `filter` / `transform` lists need the var() workaround.
- `getComputedStyle` traps when verifying styles in the preview browser: (1) `transform` resolves to `none` for any element without a layout box — e.g. inside a `hidden` form screen — even when the declaration is correct and every sibling property reads fine. Make the element visible before concluding the transform is broken. (2) A backgrounded tab freezes CSS transitions at `currentTime: 0`, so a transitioned property (e.g. an error border-color) reads its *start* value indefinitely; `el.getAnimations().forEach(a => a.finish())` fast-forwards them for verification.
