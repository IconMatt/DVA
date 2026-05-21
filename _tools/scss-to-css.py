#!/usr/bin/env python3
"""SCSS -> CSS translator for vetwell-design components.

Converts:
  - $vars to var(--vars)
  - @include respond-to("md") to @media (min-width: 840px)
  - @include focus-ring/visually-hidden/container/bleed-wrap/bleed-content/eyebrow/reduced-motion to inline CSS
  - @include link-underline-animate/grow to inline CSS
  - @use lines stripped

Tailwind v4 supports CSS nesting via Lightning CSS, so nested rules stay nested.
"""
import re
import sys
from pathlib import Path

BREAKPOINTS = {
    "xs": 360,
    "sm": 560,
    "md": 840,
    "lg": 1120,
    "xl": 1440,
    "2xl": 1680,
    "wide": 1920,
}

# Direct $var -> var(--var) replacements. Order matters: longer names first to avoid prefix collisions.
VAR_MAP = [
    # Spacing — note the SCSS aliases ($spacing-sm = var(--space-s) etc.)
    (r"\$spacing-3xs\b", "var(--space-3xs)"),
    (r"\$spacing-2xs\b", "var(--space-2xs)"),
    (r"\$spacing-xs\b", "var(--space-xs)"),
    (r"\$spacing-sm\b", "var(--space-s)"),
    (r"\$spacing-md\b", "var(--space-m)"),
    (r"\$spacing-lg\b", "var(--space-l)"),
    (r"\$spacing-xl\b", "var(--space-xl)"),
    (r"\$spacing-2xl\b", "var(--space-2xl)"),
    (r"\$spacing-3xl\b", "var(--space-3xl)"),
    # Legacy --space-* SCSS aliases
    (r"\$space-3xs\b", "var(--space-3xs)"),
    (r"\$space-2xs\b", "var(--space-2xs)"),
    (r"\$space-xs\b", "var(--space-xs)"),
    (r"\$space-sm\b", "var(--space-s)"),
    (r"\$space-md\b", "var(--space-m)"),
    (r"\$space-lg\b", "var(--space-l)"),
    (r"\$space-xl\b", "var(--space-xl)"),
    (r"\$space-2xl\b", "var(--space-2xl)"),
    (r"\$space-3xl\b", "var(--space-3xl)"),
    (r"\$space-4xl\b", "var(--space-4xl)"),
    # Radii
    (r"\$radius-xs\b", "var(--radius-xs)"),
    (r"\$radius-sm\b", "var(--radius-sm)"),
    (r"\$radius-md\b", "var(--radius-md)"),
    (r"\$radius-lg\b", "var(--radius-lg)"),
    (r"\$radius-xl\b", "var(--radius-xl)"),
    (r"\$radius-2xl\b", "var(--radius-2xl)"),
    (r"\$radius-pill\b", "var(--radius-pill)"),
    (r"\$radius-hero\b", "var(--radius-hero)"),
    (r"\$radius-card\b", "var(--radius-card)"),
    (r"\$radius-quick-link\b", "var(--radius-quick-link)"),
    # Semantic colours -> renamed variables
    (r"\$color-text-muted\b", "var(--color-ink-muted)"),
    (r"\$color-text-inverse\b", "var(--color-ink-inverse)"),
    (r"\$color-text\b", "var(--color-ink)"),
    (r"\$color-link-hover\b", "var(--color-link-hover)"),
    (r"\$color-link\b", "var(--color-link)"),
    (r"\$color-border-strong\b", "var(--color-border-strong)"),
    (r"\$color-border-warm\b", "var(--color-border-warm)"),
    (r"\$color-border\b", "var(--color-border-default)"),
    (r"\$color-bg-page\b", "var(--color-bg-page)"),
    (r"\$color-bg-muted\b", "var(--color-bg-muted)"),
    (r"\$color-bg-dark\b", "var(--color-bg-dark)"),
    (r"\$color-bg-card\b", "var(--color-bg-card)"),
    (r"\$color-accent-hover\b", "var(--color-accent-hover)"),
    (r"\$color-accent\b", "var(--color-accent)"),
    (r"\$color-focus\b", "var(--color-focus)"),
    (r"\$color-emergency-dark\b", "var(--color-emergency-dark)"),
    (r"\$color-emergency\b", "var(--color-emergency)"),
    # Raw palette
    (r"\$color-brown-900\b", "var(--color-brown-900)"),
    (r"\$color-brown-700\b", "var(--color-brown-700)"),
    (r"\$color-brown-500\b", "var(--color-brown-500)"),
    (r"\$color-sand-stone\b", "var(--color-sand-stone)"),
    (r"\$color-sweet-grass-dark\b", "var(--color-sweet-grass-dark)"),
    (r"\$color-sweet-grass\b", "var(--color-sweet-grass)"),
    (r"\$color-white\b", "var(--color-white)"),
    (r"\$color-slate-300\b", "var(--color-slate-300)"),
    (r"\$color-slate-500\b", "var(--color-slate-500)"),
    (r"\$color-slate-700\b", "var(--color-slate-700)"),
    (r"\$color-zest-dark\b", "var(--color-zest-dark)"),
    (r"\$color-zest\b", "var(--color-zest)"),
    # Overlays
    (r"\$overlay-white-02\b", "var(--overlay-white-02)"),
    (r"\$overlay-white-04\b", "var(--overlay-white-04)"),
    (r"\$overlay-white-06\b", "var(--overlay-white-06)"),
    (r"\$overlay-white-08\b", "var(--overlay-white-08)"),
    (r"\$overlay-white-10\b", "var(--overlay-white-10)"),
    (r"\$overlay-white-14\b", "var(--overlay-white-14)"),
    (r"\$overlay-white-16\b", "var(--overlay-white-16)"),
    (r"\$overlay-white-18\b", "var(--overlay-white-18)"),
    (r"\$overlay-white-22\b", "var(--overlay-white-22)"),
    (r"\$overlay-white-25\b", "var(--overlay-white-25)"),
    (r"\$overlay-white-30\b", "var(--overlay-white-30)"),
    (r"\$overlay-white-35\b", "var(--overlay-white-35)"),
    (r"\$overlay-white-45\b", "var(--overlay-white-45)"),
    (r"\$overlay-white-82\b", "var(--overlay-white-82)"),
    (r"\$overlay-white-92\b", "var(--overlay-white-92)"),
    (r"\$overlay-black-18\b", "var(--overlay-black-18)"),
    (r"\$overlay-black-30\b", "var(--overlay-black-30)"),
    (r"\$overlay-gray-10\b", "var(--overlay-gray-10)"),
    (r"\$overlay-gray-18\b", "var(--overlay-gray-18)"),
    (r"\$overlay-gray-55\b", "var(--overlay-gray-55)"),
    (r"\$overlay-sand-stone-30\b", "var(--overlay-sand-stone-30)"),
    (r"\$overlay-brown-92\b", "var(--overlay-brown-92)"),
    (r"\$overlay-brown-60\b", "var(--overlay-brown-60)"),
    (r"\$overlay-brown-40\b", "var(--overlay-brown-40)"),
    (r"\$overlay-brown-20\b", "var(--overlay-brown-20)"),
    (r"\$overlay-shadow-sm\b", "var(--overlay-shadow-sm)"),
    (r"\$overlay-shadow-md\b", "var(--overlay-shadow-md)"),
    (r"\$overlay-shadow-lg\b", "var(--overlay-shadow-lg)"),
    # Typography
    (r"\$font-display\b", "var(--font-display)"),
    (r"\$font-body\b", "var(--font-body)"),
    (r"\$font-size-5xl\b", "var(--font-size-5xl)"),
    (r"\$font-size-4xl\b", "var(--font-size-4xl)"),
    (r"\$font-size-3xl\b", "var(--font-size-3xl)"),
    (r"\$font-size-2xl\b", "var(--font-size-2xl)"),
    (r"\$font-size-2xs\b", "var(--font-size-2xs)"),
    (r"\$font-size-xs\b", "var(--font-size-xs)"),
    (r"\$font-size-sm\b", "var(--font-size-sm)"),
    (r"\$font-size-base\b", "var(--font-size-base)"),
    (r"\$font-size-md\b", "var(--font-size-md)"),
    (r"\$font-size-lg\b", "var(--font-size-lg)"),
    (r"\$font-size-xl\b", "var(--font-size-xl)"),
    (r"\$line-height-tight\b", "var(--line-height-tight)"),
    (r"\$line-height-snug\b", "var(--line-height-snug)"),
    (r"\$line-height-normal\b", "var(--line-height-normal)"),
    (r"\$line-height-loose\b", "var(--line-height-loose)"),
    (r"\$font-weight-regular\b", "var(--font-weight-regular)"),
    (r"\$font-weight-medium\b", "var(--font-weight-medium)"),
    (r"\$font-weight-semibold\b", "var(--font-weight-semibold)"),
    (r"\$font-weight-bold\b", "var(--font-weight-bold)"),
    # Motion
    (r"\$transition-fast\b", "var(--transition-fast)"),
    (r"\$transition-base\b", "var(--transition-base)"),
    (r"\$transition-slow\b", "var(--transition-slow)"),
    # Shadows
    (r"\$shadow-sm\b", "var(--shadow-sm)"),
    (r"\$shadow-md\b", "var(--shadow-md)"),
    (r"\$shadow-lg\b", "var(--shadow-lg)"),
    # Layout
    (r"\$container-padding\b", "var(--container-padding)"),
    # Breakpoint pixel constants used in calc() etc.
    (r"\$bp-xs\b", "360px"),
    (r"\$bp-sm\b", "560px"),
    (r"\$bp-md\b", "840px"),
    (r"\$bp-lg\b", "1120px"),
    (r"\$bp-xl\b", "1440px"),
    (r"\$bp-2xl\b", "1680px"),
    (r"\$bp-wide\b", "1920px"),
]

# Mixin expansions (for `@include foo;` — single-line form, no body)
INLINE_MIXINS = {
    "focus-ring": "outline: 3px solid var(--color-focus); outline-offset: 1px;",
    "visually-hidden": (
        "position: absolute; width: 1px; height: 1px; padding: 0; "
        "margin: -1px; overflow: hidden; clip: rect(0 0 0 0); "
        "white-space: nowrap; border: 0;"
    ),
    "container": (
        "width: 100%; margin-inline: auto; padding-inline: var(--container-padding);"
    ),
    "bleed-wrap": (
        "margin-inline: 0.75rem;\n"
        "  @media (min-width: 840px) { margin-inline: 0.9rem; }"
    ),
    "bleed-content": (
        "padding-inline: calc(var(--container-padding) - 0.75rem);\n"
        "  @media (min-width: 840px) { "
        "padding-inline: calc(var(--container-padding) - 0.9rem); }"
    ),
    "eyebrow": (
        "font-size: var(--step-0); font-weight: var(--font-weight-regular); "
        "color: var(--color-brown-900); letter-spacing: 0.02em; text-wrap: pretty;"
    ),
    "link-underline-animate": (
        "text-decoration: none;\n"
        "  background-image: linear-gradient(currentColor, currentColor);\n"
        "  background-position: 0 100%;\n"
        "  background-repeat: no-repeat;\n"
        "  background-size: 0 1px;\n"
        "  transition: background-size var(--transition-base), color var(--transition-base);\n"
        "  &:hover, &:focus-visible { background-size: 100% 3px; }\n"
        "  @media (prefers-reduced-motion: reduce) { transition: none; }"
    ),
    "link-underline-grow": (
        "text-decoration: none;\n"
        "  background-image: linear-gradient(currentColor, currentColor), linear-gradient(currentColor, currentColor);\n"
        "  background-position: 0 100%, 100% 100%;\n"
        "  background-repeat: no-repeat, no-repeat;\n"
        "  background-size: 0 1px, 100% 1px;\n"
        "  transition: background-size var(--transition-base), color var(--transition-base);\n"
        "  &:hover, &:focus-visible { background-size: 100% 3px, 0 1px; }\n"
        "  @media (prefers-reduced-motion: reduce) { transition: none; }"
    ),
}


def replace_includes(text: str) -> str:
    """Replace @include directives. Block forms first, then inline."""

    # respond-to("X") { ... }
    def respond_to(m):
        name = m.group(1)
        return f'@media (min-width: {BREAKPOINTS[name]}px) {{'

    text = re.sub(r'@include\s+respond-to\(\s*["\'](\w+|2xl|wide)["\']\s*\)\s*\{',
                  respond_to, text)

    def respond_below(m):
        name = m.group(1)
        return f'@media (max-width: {BREAKPOINTS[name] - 1}px) {{'

    text = re.sub(r'@include\s+respond-below\(\s*["\'](\w+|2xl|wide)["\']\s*\)\s*\{',
                  respond_below, text)

    def respond_between(m):
        a, b = m.group(1), m.group(2)
        return (f'@media (min-width: {BREAKPOINTS[a]}px) and '
                f'(max-width: {BREAKPOINTS[b] - 1}px) {{')

    text = re.sub(
        r'@include\s+respond-between\(\s*["\'](\w+|2xl|wide)["\']\s*,\s*["\'](\w+|2xl|wide)["\']\s*\)\s*\{',
        respond_between, text)

    # reduced-motion { ... }
    text = re.sub(r'@include\s+reduced-motion\s*\{',
                  '@media (prefers-reduced-motion: reduce) {', text)

    # Inline mixin includes (single line, ends in `;`)
    def inline_mixin(m):
        name = m.group(1)
        if name in INLINE_MIXINS:
            return INLINE_MIXINS[name]
        return m.group(0)  # leave as-is, will be flagged

    text = re.sub(r'@include\s+([a-z-]+)\s*;', inline_mixin, text)

    return text


def convert_line_comments(text: str) -> str:
    """Convert SCSS // line comments to /* */ block comments.
    Skip lines that contain `//` inside a URL or string literal."""
    out = []
    for line in text.splitlines():
        # crude string-aware scan for `//` outside quotes
        idx = -1
        in_s, in_d = False, False
        i = 0
        while i < len(line) - 1:
            ch = line[i]
            if ch == "'" and not in_d:
                in_s = not in_s
            elif ch == '"' and not in_s:
                in_d = not in_d
            elif ch == '/' and line[i + 1] == '/' and not in_s and not in_d:
                # Skip URL protocol-relative `//` (e.g. `//cdn`) — only treat as
                # comment when preceded by whitespace or start-of-line
                if i == 0 or line[i - 1] in ' \t;{}()':
                    idx = i
                    break
            i += 1
        if idx >= 0:
            before = line[:idx].rstrip()
            comment = line[idx + 2:].strip()
            if before:
                out.append(f"{before} /* {comment} */" if comment else before)
            elif comment:
                # Preserve leading indent
                indent = line[:len(line) - len(line.lstrip())]
                out.append(f"{indent}/* {comment} */")
            else:
                out.append("")
        else:
            out.append(line)
    return "\n".join(out)


def translate(text: str) -> str:
    # Convert // line comments first (before any other regex passes touch them).
    text = convert_line_comments(text)

    # Drop @use, @forward
    text = re.sub(r'^@use\s+.*?;\s*\n', '', text, flags=re.MULTILINE)
    text = re.sub(r'^@forward\s+.*?;\s*\n', '', text, flags=re.MULTILINE)

    # Apply @include translations first (they may reference $vars internally)
    text = replace_includes(text)

    # Then $var -> var(--var)
    for pattern, replacement in VAR_MAP:
        text = re.sub(pattern, replacement, text)

    # Sass interpolation #{...} — strip the wrapper
    text = re.sub(r'#\{([^}]+)\}', r'\1', text)

    # Map.get / map.keys references — not used in components, but warn
    return text


def main():
    src_dir = Path("/Users/frankrecalde/dev/vetwell-design/scss/components")
    dst_dir = Path("/Users/frankrecalde/dev/vetwell-design/tw4/src/components")
    dst_dir.mkdir(parents=True, exist_ok=True)

    issues = []
    for src_file in sorted(src_dir.glob("_*.scss")):
        name = src_file.name[1:].replace(".scss", ".css")  # _foo.scss -> foo.css
        dst_file = dst_dir / name
        scss = src_file.read_text()
        css = translate(scss)

        # Check for any leftover Sass syntax that needs hand attention
        for line_no, line in enumerate(css.splitlines(), 1):
            if re.search(r'\$[a-z]', line) or '@include' in line or '@use' in line:
                issues.append(f"{name}:{line_no}: {line.strip()[:120]}")

        dst_file.write_text(css)
        print(f"  wrote {dst_file.name}  ({len(scss)} -> {len(css)} chars)")

    if issues:
        print("\n--- LEFTOVER SASS SYNTAX (needs manual review) ---")
        for issue in issues:
            print(issue)
    else:
        print("\nAll components translated cleanly.")


if __name__ == "__main__":
    main()
