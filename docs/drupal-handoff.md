# Drupal / GovCMS Handoff

## Goal
Ensure all front-end work can be translated cleanly into Drupal templates and paragraph-based content structures.

## Template philosophy
- Keep HTML components modular and portable.
- Assume Drupal will output data into thin Twig templates.
- Avoid logic-heavy template assumptions.

## Preferred mapping pattern
For each UI pattern, document:
- Suggested paragraph type or content structure
- Expected fields
- Optional fields
- Variant flags
- Any preprocess variables required

## Example: Hero component
Suggested Drupal structure:
- Paragraph: Hero
- Fields:
  - title
  - summary
  - image
  - cta_link
  - cta_text
  - theme_variant

Preprocess notes:
- Build class list based on theme variant.
- Normalize CTA presence.
- Expose image alt and caption safely.

Twig notes:
- Keep markup thin.
- Avoid transformation logic in Twig.

## Field naming guidance
- Use clear, content-editor-friendly names.
- Avoid front-end-only naming in CMS fields.

## Handoff note block
Every component should include:
- Drupal structure suggestion
- Field list
- Preprocess notes
- Twig notes
- Known implementation risks

## Related docs
- `drupal-mapping-pattern.md` — the three-piece pattern (paragraph type → preprocess → thin Twig) with a worked example.
- `field-naming.md` — BEM-prefixed field machine names (`field_card_title`, `field_hero_eyebrow`).
- `wysiwyg-output.md` — how CKEditor body fields are styled.

## Forward path: Single Directory Components
When this structure moves to Drupal 10.3+, each component can be lifted into a Single Directory Component (SDC). The BEM markup, SCSS partial, and a small `component.yml` manifest live together in one folder, and the three-piece pattern collapses into a single `render component` call from preprocess. The architecture here — BEM + tokens + thin templates — was deliberately built to make that migration trivial.
