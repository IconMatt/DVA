# The Three-Piece Mapping Pattern

Every reusable component follows the same three-piece pattern when it moves from static HTML into a Drupal theme:

1. **Paragraph type** — owns the data shape (in the Drupal admin).
2. **Preprocess function** — owns the Drupal-specific field lookups (in `THEMENAME.theme`).
3. **Thin Twig template** — owns the markup (a near-copy of the static HTML).

This is the convention used by mature Drupal design systems (CivicTheme, USWDS-Drupal, etc.). Keeping the three pieces separated is the single biggest thing you can do to stop a Drupal theme from rotting.

---

## 1. Define the paragraph type

Create a paragraph (or block / node) with one field per data prop the component needs. **Prefix every field with the BEM block it maps to** — this keeps the field, the markup, and the SCSS aligned by name. See `field-naming.md` for the full rule.

```yaml
paragraph: card_resource
fields:
  field_card_image      (image)
  field_card_badge      (text)
  field_card_title      (text + link)
  field_card_excerpt    (text long)
  field_card_date       (date)
```

Notes:
- One field = one prop the template consumes. If the markup doesn't use it, don't add it.
- Variants (e.g. `card--compact`, `card--featured`) should be a `list_string` field on the paragraph, not a separate paragraph type.
- Keep field labels editor-friendly ("Card image") even though machine names are BEM-prefixed.

## 2. Preprocess: extract field values into clean variables

In the theme's `THEMENAME.theme` file, map raw Drupal field arrays to simple scalar variables that the Twig template can consume without any `.0.value` gymnastics:

```php
function THEMENAME_preprocess_paragraph__card_resource(&$variables) {
  $p = $variables['paragraph'];
  $variables['image']   = $p->get('field_card_image')->entity?->getFileUri();
  $variables['badge']   = $p->get('field_card_badge')->value;
  $variables['title']   = $p->get('field_card_title')->value;
  $variables['url']     = $p->get('field_card_title')->uri;
  $variables['excerpt'] = $p->get('field_card_excerpt')->value;
  $variables['date']    = $p->get('field_card_date')->value;
}
```

Notes:
- Always null-check entity references (`?->`).
- If a variant flag affects CSS classes, compute the class list here and expose it as `$variables['modifier_class']`. Don't build class strings in Twig.
- Run `t()` on any static strings the component outputs (labels like "Published", "Read more").

## 3. Thin Twig template

Paste the static markup from `templates/*.html` and swap in the preprocess variables:

```twig
{# paragraph--card-resource.html.twig #}
<article class="card card--topic-resource">
  <div class="card__image">
    <img src="{{ image }}" alt="">
  </div>
  <div class="card__body">
    <div class="card__meta">
      <span class="badge badge--blue">{{ badge }}</span>
    </div>
    <h2 class="card__title"><a href="{{ url }}">{{ title }}</a></h2>
    <p class="card__excerpt">{{ excerpt }}</p>
    <p class="card__date">Published {{ date|date('j F Y') }}</p>
  </div>
</article>
```

Rules:
- **Don't restructure the DOM.** The SCSS depends on the nesting. If the design needs to change, change it in SCSS, don't patch it in Twig.
- **No business logic in Twig.** If the template contains more than variable output, loops, and `if` checks on presence, the logic belongs in preprocess.
- **Diff against the static HTML.** The Twig template should read like the static template with `{{ vars }}` in place of dummy content — nothing more.

---

## Why three pieces

- **Paragraph type** owns the data shape. Editors see it. Content model decisions live here.
- **Preprocess** owns the Drupal-specific lookups. All the `get('field_x')->value` noise is contained in one file.
- **Twig template** stays thin and readable. You can always compare it to the static reference template.

Merge any two of these and the seams blur: business logic leaks into templates, content-model decisions leak into PHP, and the next developer has to read all three files to change one thing.

---

## Checklist per component

- [ ] Paragraph type defined with BEM-prefixed fields
- [ ] Preprocess function maps fields to clean vars
- [ ] Twig template mirrors the static HTML with `{{ vars }}`
- [ ] No `.0.value` or class-building logic in Twig
- [ ] Variant classes computed in preprocess, passed as `modifier_class`
- [ ] Static HTML reference is kept in sync if the component changes

---

## Forward path: Single Directory Components (SDC)

From Drupal 10.3+, each paragraph component can be lifted into an SDC — the BEM markup, SCSS partial, and a `component.yml` manifest live together in one folder. The three-piece pattern maps cleanly:

- Paragraph type → `component.yml` props schema
- Preprocess → stays in the theme, but shrinks to a single "render component" call
- Twig template → becomes `component.twig` inside the component folder

If you are starting a new build on Drupal 10.3+, go straight to SDC. The three-piece pattern above is the bridge for older codebases.
