# Front-End Rules

## Principles
- Design for Drupal handoff.
- Prefer simple structures over clever abstractions.
- Components should be portable and easy to re-template in Twig.
- CSS should be layered, predictable, and token-driven.

## Hard rules
- No hex, rgb, or hsl values outside `scss/abstracts/_tokens.scss`.
- No raw `@media` queries. Use the `respond-to()` mixin.
- No utility classes such as `.mt-4`, `.text-center`, or similar one-off helpers.
- No inline styles.
- No new tokens without updating `_tokens.scss` and noting the change.

## Markup
- Use semantic landmarks: `header`, `nav`, `main`, `aside`, `footer`, `section`.
- Maintain a logical heading structure.
- Use buttons for actions and links for navigation.
- Avoid unnecessary wrapper divs.

## CSS architecture
- Use SCSS only.
- Keep tokens centralized.
- Use mixins for breakpoints and repeated patterns.
- Prefer component styles over page-specific overrides.
- Avoid high specificity and deep nesting.
- Do not invent new tokens casually. Reuse existing tokens unless there is a clear design-system need.

## Naming
- Use BEM for components.
- Example: `.feature-card`, `.feature-card__title`, `.feature-card--highlighted`

## Responsive design
- Build mobile-first.
- Ensure spacing, typography, and layout scale smoothly.
- Do not rely on fixed heights unless truly necessary.
- Prevent awkward text columns and oversized gaps.
- Aim for a polished layout at all breakpoints.

## JavaScript
- Use only where needed for interaction.
- Avoid JS for layout, animation polish, or purely visual state.
- Respect reduced-motion preferences.

## Quality bar
- Visually polished at all breakpoints.
- Readable, balanced typography.
- Stable spacing system.
- Accessible focus and keyboard behavior.
