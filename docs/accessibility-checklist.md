# Accessibility Checklist

## Structure
- Page has one clear main landmark.
- Landmarks are used appropriately.
- Heading order is logical.
- Lists are real lists when content is list-like.

## Keyboard
- All interactive elements are keyboard reachable.
- Focus order is logical.
- No keyboard traps.
- Skip link is present and visible on focus.

## Focus
- Focus indicators are clearly visible.
- Focus is not removed without replacement.
- Hover-only behavior has a keyboard equivalent.

## Motion
- Respect `prefers-reduced-motion`.
- Avoid unnecessary animation.
- Motion should never be required to understand content.

## Content
- Link text is meaningful.
- Buttons describe the action.
- Images have an alt text strategy.
- Contrast meets requirements.

## Forms and interactive patterns
- Labels are present.
- Errors are understandable.
- Instructions are clear.

## Testing
- Keyboard test
- Reduced-motion check
- Zoom and reflow check
- Basic screen reader sanity check
- Automated accessibility scan
