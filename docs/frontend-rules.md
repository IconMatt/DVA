# Front-End Rules

## Principles
- Design for Drupal handoff via Single Directory Components (SDC).
- Prefer simple structures over clever abstractions.
- Components should be portable and easy to re-template in Twig.
- CSS is layered, predictable, and token-driven through `@theme`.
- BEM is the public class API. Tailwind utilities are a convenience layer for layout and spacing, not a substitute for component CSS.

## Hard rules
- **No hex, rgb, or hsl values outside `src/theme/colors.css`.** All colour reaches the rest of the codebase as `var(--color-*)` or generated utilities (`bg-brown-900`, `text-ink`, etc.).
- **No `tailwind.config.js`.** All Tailwind v4 configuration lives in `@theme` blocks inside `src/theme/*.css`.
- **No raw `@media` queries with hard-coded pixel values.** Use the project breakpoints exposed through `@theme` in `src/theme/breakpoints.css`. In CSS, refer to them via `@media (min-width: var(--breakpoint-md))` or write component CSS using existing tokens; in markup, use Tailwind variants (`md:`, `lg:`, `wide:`).
- **No utility-class sprawl in markup.** A handful of layout/spacing utilities are fine (`u-container`, `u-grid`, `md:grid-cols-2`, `gap-l`). Repeated visual styling belongs in a BEM component file under `src/components/`.
- **No inline `style=""` attributes** except for genuinely dynamic values set from JS (parallax offsets, animation delays via CSS custom properties).
- **No new tokens without updating `src/theme/*.css`** and recording the change.
- **No SCSS.** The build does not consume `scss/`; it is reference only.
- **No CVA in Twig.** The Drupal theme target applies BEM class names directly. Conditional classes are computed in preprocess or inline as plain Twig (`{% set classes = ... %}`).

## Project breakpoints
Seven, mirrored 1:1 between SCSS and Tailwind. Defined in `src/theme/breakpoints.css`:

```
xs:   360px
sm:   560px
md:   840px
lg:   1120px
xl:   1440px
2xl:  1680px
wide: 1920px
```

In Tailwind markup these are available as variant prefixes (`md:grid-cols-2`, `wide:max-w-[1600px]`). In hand-written component CSS prefer:

```css
@media (min-width: 840px) { /* md */ }
```

…or reference the custom property (`@media (min-width: var(--breakpoint-md))`) when Lightning CSS can resolve it at build time.

## Markup
- Use semantic landmarks: `header`, `nav`, `main`, `aside`, `footer`, `section`.
- Maintain a logical heading structure.
- Use `<button>` for actions and `<a>` for navigation.
- Avoid wrapper divs that exist only to receive utilities — promote them to a BEM element or block instead.
- BEM names look like `.feature-card`, `.feature-card__title`, `.feature-card--highlighted`.

## CSS architecture
- Layered imports in `src/main.css`: `tailwindcss` → `theme` → `base` → `utilities` → `components` → page-specific. See `css-architecture.md`.
- Components author plain CSS against `var(--token)`; they rarely use `@apply`.
- `@apply` is allowed inside `@layer base` and `@layer components` for compactness — it must not appear in markup.
- Avoid deep nesting and high specificity. Prefer a modifier class (`--variant`) over a context selector.
- Mobile-first: write the small-screen rule plain, layer breakpoints up.

## Naming
- BEM for components — block (`.card`), element (`.card__title`), modifier (`.card--resource`).
- The component file under `src/components/<name>.css` matches the BEM block exactly.
- Utility-primitive helpers are prefixed `u-` (`u-container`, `u-grid`) to mark them as primitives.
- Component variants (e.g. `card--news`, `card--resource`) live in the same component file unless the modifier file grows beyond ~300 lines, in which case split it as `_card-news.css`.

## Responsive design
- Build mobile-first.
- Ensure spacing, typography, and layout scale smoothly through the `clamp()` token scale.
- Do not rely on fixed heights unless truly necessary.
- Prevent awkward text columns and oversized gaps via the fluid space scale and `text-wrap: balance | pretty`.
- Aim for a polished layout at every breakpoint.

## JavaScript
- Use only where needed for interaction, scroll-driven animation, or progressive enhancement.
- Avoid JS for layout, animation polish, or purely visual state.
- Respect `prefers-reduced-motion`.
- Throttle scroll listeners with `requestAnimationFrame` and the `ticking` pattern (see `animation.md`).
- When this work ports to Drupal, hook into `Drupal.behaviors` rather than running on `DOMContentLoaded`. The Mercury-derived `ComponentInstance` / `ComponentType` pattern is optional — useful for components, overkill for one-off page scripts.

## Quality bar
- Visually polished at all seven breakpoints.
- Readable, balanced typography.
- Stable spacing system.
- Accessible focus and keyboard behaviour.
- `npm run build` produces a clean compile with no warnings.
