# Accessibility Checklist

## Structure
- Page has one clear `<main>` landmark.
- Landmarks (`header`, `nav`, `main`, `aside`, `footer`) used appropriately.
- Heading order is logical — page owns `h1`, prose starts at `h2`.
- Lists are real lists when content is list-like.

## Keyboard
- All interactive elements are keyboard reachable.
- Focus order is logical.
- No keyboard traps.
- Skip link is present and visible on focus.

## Focus
- Focus indicators are clearly visible.
- The project focus ring is `3px solid var(--color-focus)` (zest yellow) with `outline-offset: 1px` by default. Override only when the default would be invisible on a particular background — then bump offset or invert the colour.
- Focus is never removed without replacement.
- Hover-only behaviour has a keyboard equivalent (use `:focus-visible` siblings of every `:hover` rule).

## Motion
- Respect `prefers-reduced-motion`. The shared rule in `src/utilities/scroll-animations.css` cancels scroll-entrance and parallax transforms. Component-level transitions also need a reduced-motion guard.
- Avoid unnecessary animation.
- Motion is never required to understand content.

## Content
- Link text is meaningful (no "click here").
- No two links on a page share an accessible name while pointing at different destinations. Repeated card CTAs ("Read more", "View service details") get a visually-hidden suffix naming the target: `View service details<span class="visually-hidden"> for [service]</span>`. Entities sharing a title need a qualifier (e.g. suburb). Same rule for repeated buttons (`aria-label="Save [title]"`).
- Buttons describe the action.
- Images have an alt-text strategy. Decorative images take `alt=""`.
- Contrast meets WCAG AA. The brand palette (`--color-brown-900` on `--color-sand-stone`, `--color-brown-900` on `--color-zest`) was checked at design time; verify when introducing new colour pairings.

## Forms and interactive patterns
- Labels are present (visible or `sr-only` via Tailwind's built-in `sr-only` utility).
- Errors are understandable.
- Instructions are clear and precede the field they describe.

## WCAG 2.2 specifics
The project targets WCAG 2.2 AA. Criteria new in 2.2 that automated tools largely miss:
- Target size minimum (2.5.8): interactive targets ≥ 24×24 px — check pills, filter chips, carousel controls.
- Consistent help (3.2.6): the urgent-help banner/link sits in the same place on every screen of a flow.
- Focus not obscured (2.4.11): the sticky header must not cover the focused element when tabbing.
- Redundant entry (3.3.7): multi-step forms re-use previously entered data (draft persistence covers this).
- 4.1.1 Parsing was removed in 2.2 — disregard legacy audit findings about parsing errors.

## Testing
- Keyboard test (Tab through, Enter / Space on interactive elements, Esc on overlays).
- Reduced-motion check (toggle the OS setting, reload).
- Zoom and reflow check (200% zoom, narrow viewport).
- Basic screen-reader sanity check (VoiceOver on macOS, NVDA on Windows).
- Automated accessibility scan (pa11y or axe via the browser extension).
- Automated scans are a floor, not a certificate — Lighthouse/axe detect roughly a third of WCAG failures. The manual checks above are what validate AA.
