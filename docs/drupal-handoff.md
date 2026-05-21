# Drupal / GovCMS Handoff

## Goal
Ensure all front-end work can be translated cleanly into a Drupal 11+ theme using **Single Directory Components (SDC)** and paragraph-based content structures.

The target theme is a Mercury-derived custom theme (copied from Mercury's starterkit; **not** subthemed). Tailwind v4 is the build system; BEM is the public class API; CVA is **not** used.

## Template philosophy
- Keep HTML components modular and portable. The 32 BEM components under `src/components/` map 1:1 to SDC components in the theme.
- Assume Drupal will output data into thin Twig templates inside SDC folders.
- Avoid logic-heavy template assumptions. Conditional class lists are computed in preprocess, not in Twig.

## Preferred mapping pattern
For each UI pattern, document:
- Suggested paragraph type or content structure
- Expected fields (BEM-prefixed machine names — see `field-naming.md`)
- Optional fields
- Variant flags (`list_string` field on the paragraph)
- Any preprocess variables required (especially the computed `modifier_class`)

See `drupal-mapping-pattern.md` for the worked three-piece example.

## Example: Hero component
Suggested Drupal structure:
- Paragraph: `paragraph: hero` (or content type if the hero is page-specific)
- Fields:
  - `field_hero_title`
  - `field_hero_eyebrow`
  - `field_hero_summary`
  - `field_hero_image`
  - `field_hero_cta_link`
  - `field_hero_cta_text`
  - `field_hero_variant` (`list_string`: `default`, `inverse`, `compact`)

Preprocess notes:
- Build class list based on the variant field → expose as `$variables['modifier_class']`.
- Normalize CTA presence (one variable, not three).
- Expose image alt and caption safely.
- Run `t()` on any static labels.

Twig notes:
- Markup mirrors `src/components/hero.css` BEM structure (`.hero`, `.hero__inner`, `.hero__title`, `.hero__quick-links`).
- Concatenate `modifier_class` into the root element's class attribute: `<section class="hero {{ modifier_class }}">`.
- No `html_cva()`. No inline conditionals in `class=""`.
- No business logic in Twig.

## Field naming guidance
- Machine names are BEM-prefixed (`field_card_title`, `field_hero_eyebrow`). See `field-naming.md`.
- Labels are editor-friendly ("Card title", "Hero eyebrow"). Editors never see machine names.

## Handoff note block
Every component should include:
- Drupal structure suggestion (paragraph type or SDC)
- Field list with machine names + labels
- Preprocess notes
- Twig notes
- Known implementation risks

## Related docs
- `drupal-mapping-pattern.md` — the three-piece pattern (paragraph type → preprocess → thin Twig inside an SDC folder) with a worked example.
- `field-naming.md` — BEM-prefixed field machine names (`field_card_title`, `field_hero_eyebrow`).
- `wysiwyg-output.md` — how CKEditor body fields are styled by `.page-content__section`.
- `tailwind-conventions.md` — explicit note that CVA is rejected for this theme.

## What ports vs. what is rebuilt

| Layer | Action |
|---|---|
| `src/theme/*.css` (tokens) | Port as-is into the Drupal theme's `src/theme/` directory. |
| `src/base/*.css` | Port as-is. |
| `src/utilities/*.css` | Port as-is. |
| `src/components/*.css` | Port as-is. The BEM names match what the SDC Twig will output. |
| `templates/*.html` | Rebuild as SDC `.twig` templates under `components/<name>/<name>.twig`, plus `.component.yml` schemas. |
| Inline `<script>` blocks in templates | Move into Drupal libraries; attach via `Drupal.behaviors`. |

The CSS doesn't change shape across the port — only the markup gets re-templated as Twig + SDC schemas.
