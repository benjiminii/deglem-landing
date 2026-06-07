# CLAUDE.md

This file guides Claude Code (claude.ai/code) when working in this repository.

# Deglem Landing — Claude Code Guide

## Project Overview

Static marketing landing page for **Deglem**, an AI calorie-tracking mobile app (the app lives in the sibling repo `../calorie-tracker-ai`). The page sells the app and drives downloads to the App Store and Google Play. Bilingual: English (default) and Mongolian. Built to ship near-zero JavaScript and to let real screenshots / store URLs / privacy copy drop in later with **zero code change**.

This is a separate project from the app — it shares no code, only the brand (palette, logo, Roboto font).

## Tech Stack

| Layer | Choice |
|-------|--------|
| Framework | **Astro** (static output, near-zero JS) |
| Styling | **Tailwind CSS v4** — CSS-first, configured in `src/styles/global.css` via `@theme` (there is **no** `tailwind.config` file) |
| i18n | Astro built-in i18n routing — `/` = EN (default), `/mn/` = Mongolian; `prefixDefaultLocale: false` |
| Fonts | **Roboto** via `@fontsource/roboto` (400 / 500 / 700) |
| Hosting | **Vercel** (`@astrojs/vercel` static adapter) |
| Sitemap | `@astrojs/sitemap` |
| Package manager | **pnpm** (not npm) |

## Design System

See `DESIGN.md` for the full system. Key rules:

- **Background**: `bg-cream` (`#faf9f6`) — never `bg-white`
- **Text**: `text-charcoal` (`#1c1c1c`) primary, `text-muted` (`#5f5f5d`) secondary
- **Borders not shadows** on cards: `border border-cream-border` (`#e7e2d6`), `rounded-xl`
- **Dark sections** (CTA): `bg-charcoal` with `text-cream` / `text-cream/70` for secondary (never `text-muted` on charcoal — fails contrast)
- **Interactions**: `transition-opacity hover:opacity-80` on every link/button
- **Font**: Roboto everywhere (`font-sans` token maps to it)

## Project Structure

```
src/
  config.ts              ← APP_STORE_URL, PLAY_STORE_URL, CONTACT_EMAIL, SITE_NAME (swap store URLs here)
  styles/global.css      ← Tailwind v4 entry: @import "tailwindcss" + @theme tokens + Roboto imports + base body
  layouts/
    Base.astro           ← <html> shell: localized <title>/meta, OG tags, hreflang (en/mn/x-default); imports global.css; <slot/>
  components/
    Nav.astro            ← sticky header: glyph logo + wordmark, LanguageToggle, Download button (path-aware href)
    LanguageToggle.astro ← EN / MN switch (links to the mirror route via localizedPath)
    Hero.astro           ← centered headline + subtitle + one PhoneMockup + StoreBadges
    Features.astro       ← 3 FeatureCards (snap / edit / track)
    FeatureCard.astro    ← icon + title + desc card
    HowItWorks.astro     ← 3 numbered steps
    ScreenshotGallery.astro ← 3 angled PhoneMockups (camera / dashboard / progress)
    PhoneMockup.astro    ← charcoal phone frame around a screenshot (props: screenshot, alt, class, rotate)
    StoreBadges.astro    ← App Store + Google Play badge links (reads config URLs)
    DownloadCTA.astro    ← #download anchor section on charcoal + StoreBadges
    Footer.astro         ← glyph + wordmark, privacy link, contact, LanguageToggle, copyright
  pages/
    index.astro          ← EN landing (lang='en', path='/')
    privacy.astro        ← EN privacy (lang='en', path='/privacy')
    mn/index.astro       ← MN landing (lang='mn', path='/')
    mn/privacy.astro     ← MN privacy (lang='mn', path='/privacy')
  i18n/
    en.json, mn.json     ← copy dictionaries — must keep identical key sets
    utils.ts             ← useTranslations(lang) → t(key); localizedPath(path, lang); Lang type; languages map
public/
  logo/                  ← deglem-glyph-dark.png (on light bg), deglem-glyph-light.png (on dark bg)
  screenshots/           ← dashboard.png, camera.png, progress.png — PLACEHOLDERS, swap with real (same names)
  badges/                ← app-store.svg, google-play.svg — stylized (Apple/Play glyph + label); swap official artwork before launch
  og-image.png           ← PLACEHOLDER social preview
  favicon.png            ← copied from the app
  robots.txt
scripts/
  make-placeholders.mjs  ← dependency-free Node PNG generator for placeholder screenshots
  make-og-image.mjs      ← dependency-free Node PNG generator for the placeholder og-image
astro.config.mjs         ← site, output:'static', vercel adapter, sitemap integration, tailwind v4 vite plugin, i18n
```

## Page Composition

Every page wraps content in `Base.astro` and passes `lang` + `path`. `path` is the **locale-agnostic** path (`/` or `/privacy`) — `localizedPath()` derives the EN/MN URLs and hreflang from it. A page sets `lang`/`path` as frontmatter constants and composes the section components in order: `Nav → Hero → Features → HowItWorks → ScreenshotGallery → DownloadCTA → Footer`.

Adding a new locale = add a dictionary in `src/i18n/`, register it in `astro.config.mjs` `i18n.locales` and `src/i18n/utils.ts` `languages`, and add page files under a new `src/pages/<locale>/` folder.

## i18n Rules

- `src/i18n/en.json` and `src/i18n/mn.json` **must have identical keys**. Verify:
  ```bash
  diff <(node -e "console.log(Object.keys(require('./src/i18n/en.json')).sort().join('\n'))") \
       <(node -e "console.log(Object.keys(require('./src/i18n/mn.json')).sort().join('\n'))")
  ```
- Every user-facing string goes through `t('key')` — no hardcoded copy in components.
- `localizedPath` normalizes trailing slashes (`/privacy` → `/privacy/`) so hreflang URLs are consistent.
- EN is the default locale and is served at the root (no `/en/` prefix).

## Swap-in Checklist (before launch)

These are intentional placeholders — replacing them needs **no code change** unless noted:

- Real screenshots → `public/screenshots/{dashboard,camera,progress}.png` (keep the names; ~1:2 ratio)
- Official store badges → `public/badges/{app-store,google-play}.svg`
- Store URLs → `APP_STORE_URL` / `PLAY_STORE_URL` in `src/config.ts`
- Real privacy copy → `privacy.body` in `src/i18n/{en,mn}.json` (multi-paragraph: the privacy page wraps it in `space-y-4 leading-relaxed`)
- Branded social preview → `public/og-image.png`
- Final domain → `site` in `astro.config.mjs` **and** the `Sitemap:` URL in `public/robots.txt`

## Commands

```bash
pnpm install            # install deps
pnpm dev                # dev server → http://localhost:4321
pnpm build              # static build → dist/ (+ .vercel/output for the adapter)
pnpm preview            # preview the production build
pnpm exec astro check   # type-check .astro / .ts (run before considering work done)
```

There are no automated tests. Verification = `astro check` (0 errors) + `pnpm build` (succeeds) + a visual pass in `pnpm dev`.

## Deployment

Vercel auto-detects Astro + the `@astrojs/vercel` adapter — no build config needed. Push to a Git remote, import the repo in Vercel, add a custom domain, then update `site` (`astro.config.mjs`) and the sitemap URL (`public/robots.txt`).

## Key Conventions

- All styling via Tailwind `class` — no inline styles except the dynamic `rotate` transform in `PhoneMockup`.
- Tailwind **v4**: new design tokens are added as `--color-*` / `--font-*` under `@theme` in `global.css`, which auto-generates the utility classes. Do not add a `tailwind.config` file.
- Use `<a>`/`<button>` with `transition-opacity hover:opacity-80` for interactive feedback.
- File names: kebab-case for assets, PascalCase for `.astro` components.
- i18n: every user-facing string through `t()`; both locale JSONs updated together.
- Keep components small and single-purpose; sections compose in the page files, not in each other.
- Brand assets come from the app repo (`../calorie-tracker-ai/assets/images/logos`); copy into `public/`, don't symlink.
