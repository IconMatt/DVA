# AGENTS.md

## What this project is
Front-end build (HTML + Tailwind v4 CSS + minimal vanilla JS) for the Veteran and Family Wellbeing Agency site. Intended for later Drupal / GovCMS handoff into a custom Mercury-derived theme. The handoff target uses Single Directory Components (SDC).

## Core constraints
- Tailwind v4 only. No Sass build. No `tailwind.config.js` — configuration lives in `@theme` blocks in CSS.
- Plain CSS authored against `@theme` tokens is the primary mode. Tailwind utilities are available alongside, but BEM components stay BEM components.
- Follow BEM naming for components (`.card`, `.card__title`, `.card--resource`). The design system is BEM-first.
- All design values flow through `@theme` tokens. No hex / rgb / hsl outside `src/theme/colors.css`.
- Semantic HTML, progressive enhancement, accessibility-by-default.
- Keep JavaScript out of purely presentational behaviour. Use it for scroll-driven, mount-driven, or interactive behaviour only.
- Do **not** introduce: a Sass pipeline, React, CSS-in-JS, inline `style=""` attributes, utility-class sprawl in markup, or CVA in Twig templates (the Drupal theme target rejects CVA — apply BEM classes directly).

## Read these files first
- `/docs/frontend-rules.md`
- `/docs/css-architecture.md`
- `/docs/tailwind-conventions.md`
- `/docs/drupal-handoff.md`
- `/docs/drupal-mapping-pattern.md`
- `/docs/field-naming.md`
- `/docs/wysiwyg-output.md`
- `/docs/accessibility-checklist.md`
- `/docs/content-rhythm.md`
- `/docs/animation.md`
- `/docs/clamp.md`
- `/docs/definition-of-done.md`
- `/LESSONS.md`

## Planning rule
Before writing code for any new component, page, or multi-file change, propose a short implementation plan, list affected files, and wait for approval.

For single-file tweaks, small fixes, or copy changes, proceed directly.

Keep plans brief: 3–6 bullets maximum.

## Working style
- Reuse existing patterns before creating new ones. `src/components/` already holds a BEM component for most patterns. Look there first.
- Keep templates thin and styles predictable.
- When creating a component, document where it maps to Drupal (paragraph type → preprocess → SDC).
- Read `LESSONS.md` before starting work and avoid repeating known mistakes.
- When unsure, choose the simplest implementation that supports GovCMS / SDC handoff.

## Output expectations
- Clean, readable, semantic markup.
- CSS organized as `theme` → `base` → `utilities` → `components` → page-specific. Import order in `src/main.css` is the dependency graph.
- Responsive behaviour that works at the seven project breakpoints: `xs:360`, `sm:560`, `md:840`, `lg:1120`, `xl:1440`, `2xl:1680`, `wide:1920`.
- Good keyboard and focus behaviour. Focus ring is `3px solid var(--color-focus)` (zest yellow) with `outline-offset: 1px` by default.
- Balanced line lengths, stable spacing rhythm via the fluid `--space-*` / `--spacing-*` scale.

## Build
- `npm run dev` — Tailwind CLI watch mode → `css/main.css`
- `npm run build` — one-shot, minified → `css/main.css`
- `npm run verify` — alias for `build`

The build is driven by `src/main.css`, which `@import`s the token files, base styles, utilities, and every component file in order. `@source "../templates"` and `@source "../index.html"` tell Tailwind where to scan for utility classes used in markup.

## Foundations setup (clamp-calculator prompts)

The Utopia-style fluid scale lives in `src/theme/typography.css` and `src/theme/spacing.css`. The `clamp-calculator` tool (when present in `_tools/`) generates a `# Foundations setup` prompt for Claude Code to act on.

When you receive a prompt with that heading:
- **Trust all token values.** They were back-solved from real Figma measurements or derived from modular-scale math. Do not invent alternatives or recalculate.
- **Your job is accurate file creation, not design decisions.** Create or update every file listed in the prompt.
- **Targets are the `@theme` blocks** in `src/theme/typography.css` and `src/theme/spacing.css`. Mirror legacy `--step-*` / `--space-*` aliases in `:root` so existing component CSS keeps resolving.
- Hex / rgb / hsl values only live in `src/theme/colors.css`.
- After writing, run `npm run build` to confirm CSS compiles.

## Reference vs. live source
- **Live build source:** `src/`, `templates/`, `index.html`, `package.json`. This is what Tailwind compiles.
- **Reference only:** the legacy `scss/` tree is kept for cross-checking token values (`scss/abstracts/_tokens.scss`) and BEM rules. Do not author new SCSS. The build does not consume it.

## Before finishing
- Validate against `/docs/definition-of-done.md`.
- Note any Drupal preprocess or paragraph-type assumptions for the handoff component.
- Flag anything that should be confirmed by a Drupal developer.
