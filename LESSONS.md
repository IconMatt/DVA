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
