# Definition of Done

A page or component is done when:

## Code quality
- HTML is semantic and clean.
- SCSS is placed in the correct layer.
- Naming follows project conventions.
- JS is minimal and justified.

## Design quality
- Layout is polished across key breakpoints.
- Spacing feels intentional and consistent.
- Typography is readable and balanced.
- No obvious visual bugs or awkward wraps.

## Accessibility
- Keyboard flow works.
- Focus states are visible.
- Landmarks and headings are correct.
- Reduced-motion behavior is respected.
- Automated accessibility scan shows no serious issues.

## Drupal readiness
- Component can be mapped to a paragraph type or content model.
- Field assumptions are documented.
- Twig handoff is straightforward.
- Preprocess requirements are noted.

## Verification
Run `npm run verify` before marking work done. This should run stylelint, HTML validation, pa11y, and generate breakpoint screenshots.

## Review assets
- Mobile screenshot
- Tablet screenshot
- Desktop screenshot
- Notes for any known compromises
