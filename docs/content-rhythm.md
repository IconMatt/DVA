# Content Rhythm

## Typography
- Use the fluid type scale defined in `src/theme/typography.css` (`--text-step--2` through `--text-step-5`, mirrored as `--step-*`).
- Keep line length comfortable for reading. Base paragraphs cap at `max-width: 70ch` in `src/base/typography.css`.
- Avoid oversized headings that dominate smaller screens — the clamp scale already handles graceful growth.
- Two type families: `--font-display` (Halant, serif) for opted-in headings via `.headings-serif`, `--font-body` (Figtree, sans) for everything else.

## Spacing
- Use token-based spacing only. Reach for `var(--space-s)` through `var(--space-3xl)` in component CSS; reach for `gap-s`, `p-l`, `m-xl` Tailwind utilities in markup.
- Maintain consistent vertical rhythm between sections and elements via the paired tokens (`--space-s-l`, `--space-m-l`) for rhythmic transitions.
- Avoid one-off spacing overrides unless documented inline with a `/* Custom value: <why> */` comment.

## Readability
- Maintain comfortable measure in text-heavy sections. The prose wrapper (`.page-content__section`) clamps to `clamp(36rem, 50vw + 8rem, 56rem)` for that reason.

## Text wrapping
- Headings (`h1`–`h4`) get `text-wrap: balance` globally in `src/base/typography.css`.
- Body copy (`p`, `li`, `dd`) gets `text-wrap: pretty` globally in `src/base/typography.css`.
- Both are progressive enhancements; no fallback required.
- **Do not re-apply per component.** The base rule covers every element. Component CSS that adds `text-wrap` is duplicative and a maintenance risk.

## Dense government content
- Break long content into digestible sections.
- Use lists, callouts, tables, and summaries carefully.
- Prioritize scanning without losing formality.
- For rich-text body fields rendered through CKEditor, all rhythm is owned by the `.page-content__section` wrapper in `src/base/prose.css`. See `wysiwyg-output.md`.
