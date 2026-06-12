# Drupal team — accessibility fix action list

From the 12 Jun 2026 Lighthouse audits of staging (reports in `/accessibility`).
Source of truth: the static templates and CSS in this repo (branch `main`, as of
commit `ae092d1` — "a11y: fix Lighthouse audit failures"). Each item below has
already been applied to the prototype — your job is to mirror it.

## 1. Pull the updated CSS

- [ ] Re-import the prototype's theme CSS (token change in `src/theme/colors.css`,
      component changes in `search-overlay.css` and `feedback-form.css`), or copy
      the rebuilt `css/main.css` if you consume the compiled file.
- [ ] Do **not** re-apply colour overrides locally in the Drupal theme — inherit
      them, or the next sync reverts your fix.
- ✅ Accept when: search field labels and the inactive Search button compute to
  `#66615b`, not `#817f7d`.

## 2. Service directory — bridging heading

- [ ] Add `<h2 class="visually-hidden">Search results</h2>` above the results
      list, emitted from the view header (global text area plugin on the
      `service_directory` view, or `views-view--service-directory.html.twig`).
- [ ] Run the string through `t()`.
- ✅ Accept when: the rendered heading outline reads h1 "Find a service" →
  h2 "Search results" → h3 card titles. No skips.

## 3. Service card — unique link/button names

In `THEMENAME_preprocess_node__service__list_card`:

- [ ] Build the CTA name: visible "View service details" plus a visually-hidden
      `for [node title]` suffix in a `<span class="visually-hidden">`, through
      `t()` with `@title`.
- [ ] Build the Save button `aria-label` the same way ("Save [title]").
- [ ] Disambiguate services sharing a title: append the suburb from
      `field_service_address` (e.g. "Mental Health Services, Collingwood").
      Apply to both CTA and Save.
- ✅ Accept when: no two links or buttons in a results page share an accessible
  name.

## 4. Map pin popup

- [ ] In the map JS (Drupal library port), the popup CTA template includes
      `<span class="visually-hidden map-pin-detail__cta-name"></span>`, and the
      populate function sets it to `' for ' + point.title`. Copy from the inline
      script in `templates/services-directory.html`.
- ✅ Accept when: clicking a pin yields a CTA accessible name of
  "View service details for [service]".

## 5. Listing "More" links (homepage, about, articles)

- [ ] `paragraph--resource-listing`: header link text "More" → **"More resources"**.
- [ ] `paragraph--news-listing`: header link text "More" → **"More news"**.
- [ ] If the link text is an editor-entered field, set the new defaults and
      update existing content.
- ✅ Accept when: no two links on the homepage share a name while pointing at
  different URLs.

## 6. News cards — "Read more" CTAs

- [ ] In the `card_news` view-mode preprocess: append a visually-hidden
      `: [node title]` suffix to `field_card_cta_text` output.
- ✅ Accept when: each card CTA announces "Read more: [article title]".

## 7. Wellbeing resources — restore dropped h2s (Drupal-only bug)

- [ ] The staging page renders `h3.heading--level-3` with no preceding h2 — the
      port dropped the visually-hidden bridging h2s present in the static
      `resources-landing.html` (the "Choose the collection that best describes
      you" and "Browse resources by wellbeing area" headings).
- [ ] Restore them in the page's Twig, or set those Mercury heading components
      to level 2.
- ✅ Accept when: heading order on `/wellbeing-resources` has no skips.

## 8. Verify

- [ ] Re-run Lighthouse **in an incognito window** (the 12 Jun runs all carried
      an IndexedDB warning): homepage, guided pathway, service directory
      results, wellbeing resources × desktop + mobile. Target 100 × 8.
- [ ] One manual pass per page: keyboard only (search overlay open/close,
      carousels, map toggle), screen reader spot check, 200% zoom, OS
      reduced-motion toggle.
- [ ] WCAG 2.2-specific: 24px target size on pills/chips, urgent-help banner in
      a consistent position on every screen, sticky header doesn't obscure
      focused elements. See `accessibility-checklist.md`.

Items 2, 3, 5, 6 are also documented as comments in the static templates next
to the markup they describe (`templates/services-directory.html`,
`templates/home.html`). A Lighthouse score of 100 is a floor, not a certificate
— the manual pass in item 8 is what validates WCAG 2.2 AA.
