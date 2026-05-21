# vetwell-design — Tailwind v4 alternate

Parallel build of the parent project using **Tailwind v4** instead of Sass. Same six templates, same markup, same visual output, same JavaScript.

## Layout

```
tw4/
├── src/                # CSS source
│   ├── main.css        # entry — imports theme, base, utilities, components
│   ├── theme/          # @theme tokens (colors, typography, spacing, radius, breakpoints, motion)
│   ├── base/           # reset, typography defaults, prose wrapper
│   ├── components/     # 32 components (1:1 with /scss/components)
│   └── utilities/      # container, scroll-animations, page-specific overrides
├── templates/          # 6 HTML templates (copied verbatim from /templates)
├── assets -> ../assets # symlink to parent project's assets
├── css/main.css        # build output
└── index.html          # menu page
```

## Develop / build

```sh
cd tw4
npm install
npm run dev      # watch mode → css/main.css
npm run build    # one-shot, minified
```

## Behavioural parity

- Same tokens (fluid clamp typography, spacing, radii). Token values copied verbatim from `/scss/tokens/` and `/scss/abstracts/_tokens.scss`.
- Same breakpoints (xs:360, sm:560, md:840, lg:1120, xl:1440, 2xl:1680, wide:1920) → Tailwind variants `xs:`, `sm:`, etc.
- Same component CSS — every `/scss/components/_*.scss` has a 1:1 sibling at `src/components/*.css`. Sass `$vars` became `var(--*)`, `@include respond-to("md")` became `@media (min-width: 840px)`, mixins were inlined.
- Same root font-size scaling above 1440px (in `src/base/reset.css`).
- Same reduced-motion guards on every animated component plus a global strip rule.
- Same JavaScript — templates' inline `<script>` blocks copied verbatim, `data-*` hooks unchanged.
- BEM class names preserved in HTML.

## What's different

- No Sass dependency — Tailwind v4's Lightning CSS handles nesting, `@import`, and CSS variables natively.
- `bg-brown-900/40` slash-opacity replaces the explicit `--overlay-*` tokens (the legacy names are kept in `:root` for component CSS).
- Tokens flow through `@theme`, so utilities like `bg-brown-900`, `text-step-2`, `rounded-card`, `gap-s-l`, `md:grid-cols-2` are available alongside the BEM classes.
- Build output is one minified CSS file at `css/main.css` (mirrors the original SCSS output path so templates' `<base href="../" />` + `href="css/main.css"` work unchanged).
