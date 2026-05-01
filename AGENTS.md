# AGENTS.md

## What this project is
This is a front-end build intended for later Drupal/GovCMS integration.

## Core constraints
- Use plain HTML, SCSS, and minimal JavaScript.
- Prefer semantic HTML and progressive enhancement.
- Keep JavaScript out of purely presentational behavior.
- Do not introduce React, Tailwind, CSS-in-JS, inline styles, or utility-class sprawl.
- Follow BEM naming for components.
- Use design tokens for spacing, typography, color, radius, shadows, and breakpoints.
- Build with accessibility as a default requirement, not a later enhancement.

## Read these files first
- `/docs/frontend-rules.md`
- `/docs/scss-architecture.md`
- `/docs/mixins.md`
- `/docs/drupal-handoff.md`
- `/docs/drupal-mapping-pattern.md`
- `/docs/field-naming.md`
- `/docs/wysiwyg-output.md`
- `/docs/accessibility-checklist.md`
- `/docs/content-rhythm.md`
- `/docs/animation.md`
- `/docs/definition-of-done.md`
- `/LESSONS.md`

## Planning rule
Before writing code for any new component, page, or multi-file change, propose a short implementation plan, list affected files, and wait for approval.

For single-file tweaks, small fixes, or copy changes, proceed directly.

Keep plans brief: 3–6 bullets maximum.

## Working style
- Reuse existing patterns before creating new ones.
- Keep templates thin and styles predictable.
- When creating a component, document where it maps to Drupal.
- Read `LESSONS.md` before starting work and avoid repeating known mistakes.
- When unsure, choose the simplest implementation that supports GovCMS handoff.

## Output expectations
- Clean, readable markup.
- SCSS organized by abstracts, base, layout, components, and pages.
- Responsive behavior that works well at mobile, tablet, desktop, and wide layouts.
- Good keyboard and focus behavior.
- Balanced line lengths and stable spacing rhythm.

## Foundations setup (when you receive a calculator-generated prompt)

The tool at `clamp-calculator/clamp-calculator.html` generates a `# Foundations setup` prompt for Claude Code to act on.

When you receive a prompt with that heading:
- **Trust all token values.** They were back-solved from real Figma measurements or derived from modular-scale math. Do not invent alternatives or recalculate.
- **Your job is accurate file creation, not design decisions.** Create every file listed in the prompt.
- **Follow the import order exactly** as shown in the prompt's `main.scss` section.
- Add `!default` to every SCSS variable unless the prompt already includes it.
- Do not add hex values in any file other than `scss/tokens/_colors.scss`.
- After writing all files, run `npm run verify` if it exists.

## Before finishing
- Validate against `/docs/definition-of-done.md`.
- Note any Drupal preprocess or paragraph-type assumptions.
- Flag anything that should be confirmed by a Drupal developer.
