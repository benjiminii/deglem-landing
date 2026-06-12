# Store Assets v2 — Design

**Date:** 2026-06-12
**Status:** Approved (brainstorm with user)

## Goal

Replace the current generated store images in `store-assets/` with a higher-quality set that matches the Deglem brand system, uses Mongolian captions (matching the Mongolian app screenshots), and is regenerated from a maintainable HTML + Playwright pipeline instead of the hand-drawn Pillow script.

## Decisions (made during brainstorm)

1. **Locale:** Mongolian captions only — screenshots are MN UI; one asset set.
2. **Lineup:** Keep 5 screens, sharpened story order: snap → macros → dashboard → progress → profile. Plus the Google Play feature graphic.
3. **Visual direction:** Cream minimal, brand-true — the landing page system (cream background, charcoal Roboto headlines, hairline borders, green only as accent).
4. **Series composition:** Alternating tilt with hero opener — screen 1 is a hero (food-photo band + overlapping phone); screens 2–5 are single phones with alternating tilt and left/right anchor.
5. **Tooling:** HTML/CSS templates screenshotted by Playwright (headless Chromium) at exact pixel sizes. The Python Pillow script is deleted.

## Output Spec

Filenames unchanged — drop-in replacement for the current files.

| File | Size (px) |
|---|---|
| `store-assets/app-store/01-snap.png` … `05-profile.png` | 1284 × 2778 (6.5-inch portrait) |
| `store-assets/google-play/01-snap.png` … `05-profile.png` | 1080 × 1920 |
| `store-assets/google-play/feature-graphic.png` | 1024 × 500 |

11 PNGs total.

## Visual Template

- **Background:** cream gradient `#fefefe → #faf9f6`, subtle hairline border vignette. No dot grid, no fake/drawn UI cards — real screenshots carry the content.
- **Type:** Roboto 700 charcoal (`#1c1c1c`) headline, ~2 lines, large; Roboto 400 muted (`#5f5f5d`) subhead. Loaded from `node_modules/@fontsource/roboto` (no network at generation time).
- **Brand row:** `public/logo/deglem-glyph-dark.png` + «Дэглэм» wordmark, top-left.
- **Phone frame:** charcoal CSS frame mirroring `PhoneMockup.astro` (rounded charcoal bezel), soft CSS shadow.
- **Green accent:** thin green (`#22c55e`) underline under one headline keyword; otherwise green appears only inside screenshots.
- **Screen 01 (hero):** food-photo band cropped from the top of `macro.png`, with the macro phone overlapping it, tilted +4°.
- **Screens 02–05:** single phone, tilt alternating −4° / +4°, anchored right / left / right / left.
- **Feature graphic (1024×500):** brand row + headline left, two phones right (dashboard behind, macro front), same cream system.

## Mongolian Copy

| Screen | Screenshot | Headline | Subhead |
|---|---|---|---|
| 01 snap | macro.png | Зураг ав. Илчлэгээ мэд. | Хоолныхоо зургийг авахад л илчлэг, макро секундын дотор гарна. |
| 02 macros | macro.png | Илчлэг, макро — агшин зуур. | Уураг, нүүрс ус, өөх тосыг бүртгэхээсээ өмнө хар. |
| 03 dashboard | dashboard.png | Өдрөө нэг дороос хяна. | Өдрийн илчлэг, макро зорилт, хоолны бүртгэл — нэг дэлгэцэнд. |
| 04 progress | progress.png | Ахиц өдөр бүр харагдана. | Жингийн хандлага, илчлэг, BMI-г хялбар ажигла. |
| 05 profile | profile.png | Зорилгоо өөрөө тодорхойл. | Зорилтот жин, өдрийн илчлэгээ уян хатан тохируул. |
| Feature graphic | dashboard + macro | Нэг зургаас илчлэг | Зураг ав — илчлэг, макро секундын дотор. |

Copy is a draft written during brainstorm; user (native speaker) may revise wording at review time without affecting layout.

## Pipeline

New files under `store-assets/source/`:

- `template.html` — single layout template; per-screen values injected via CSS variables / DOM. Handles all three canvas sizes via viewport.
- `screens.mjs` — per-screen data: headline, subhead, screenshot file, tilt angle, anchor side, hero flag.
- `generate.mjs` — Playwright script: for each (store × screen), set viewport to exact output size with `deviceScaleFactor: 1`, load template, inject data, screenshot to PNG into `store-assets/app-store/` and `store-assets/google-play/`.

Project changes:

- `playwright` added as devDependency (pnpm); Chromium installed via `pnpm exec playwright install chromium`.
- `package.json` script: `"gen:store": "node store-assets/source/generate.mjs"`.
- `store-assets/source/generate-store-assets.py` deleted (replaced).

Inputs read from `public/screenshots/{macro,dashboard,progress,profile}.png` and `public/logo/deglem-glyph-dark.png`.

## Verification

There are no automated tests for this. Verification:

1. `pnpm gen:store` produces all 11 PNGs at exact spec sizes.
2. Visual pass on every PNG: no clipped text, correct fonts (Roboto, not fallback), correct captions per screen, phone/photo alignment, contrast.
3. User reviews final images.

## Out of Scope

- English asset set (can be added later by extending `screens.mjs` with an EN copy table).
- Changes to the landing page itself, `public/screenshots/`, or store listing metadata.
