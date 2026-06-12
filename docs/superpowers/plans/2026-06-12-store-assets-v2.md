# Store Assets v2 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Regenerate all 11 store images (5 App Store + 5 Google Play + 1 feature graphic) in the cream-minimal brand style with Mongolian captions, from an HTML + Playwright pipeline replacing the Pillow script.

**Architecture:** One HTML template for the tall screenshots (per-screen data injected via `{{token}}` replacement, layout in `vw` units so both canvas sizes share it) plus one fixed-size template for the 1024×500 feature graphic. A Node ESM script writes a filled temp HTML file, loads it in headless Chromium via `file://` (so relative paths reach `public/` and `node_modules/@fontsource/roboto`), and screenshots at exact pixel sizes.

**Tech Stack:** Node ESM, Playwright (Chromium), @fontsource/roboto (already a dependency), pnpm.

**Spec:** `docs/superpowers/specs/2026-06-12-store-assets-v2-design.md`

**Testing note:** This repo has no automated tests by convention (CLAUDE.md). Verification is: generation succeeds, output dimensions exact, visual pass on every PNG (no clipped text, Roboto rendering, correct captions). Steps below encode those checks as commands instead of unit tests.

---

## File Structure

- Create: `store-assets/source/screens.mjs` — per-screen copy + layout data (the only file to touch for copy edits)
- Create: `store-assets/source/template.html` — tall screenshot layout (both store sizes)
- Create: `store-assets/source/feature.html` — 1024×500 feature graphic layout
- Create: `store-assets/source/generate.mjs` — Playwright render script
- Modify: `package.json` — add `playwright` devDependency, `gen:store` script
- Modify: `.gitignore` — ignore the render temp file
- Delete: `store-assets/source/generate-store-assets.py` — replaced
- Overwrite (generated): `store-assets/app-store/*.png`, `store-assets/google-play/*.png`

---

### Task 1: Install Playwright

**Files:**
- Modify: `package.json`, `pnpm-lock.yaml` (via pnpm)
- Modify: `.gitignore`

- [ ] **Step 1: Add devDependency**

Run from repo root (`/Users/benjiminii/Developer/side-projects/deglem-landing`):

```bash
pnpm add -D playwright
```

Expected: `playwright` appears under `devDependencies` in `package.json`.

- [ ] **Step 2: Install Chromium browser**

```bash
pnpm exec playwright install chromium
```

Expected: downloads Chromium (or no-op if cached). Exit code 0.

- [ ] **Step 3: Ignore render temp file**

Append to `.gitignore`:

```
store-assets/source/.tmp.html
```

> **No git commits anywhere in this plan** — user reviews and commits manually.

---

### Task 2: Screen data module

**Files:**
- Create: `store-assets/source/screens.mjs`

- [ ] **Step 1: Write `screens.mjs`**

Copy comes from the approved spec. `headline` is HTML (`<br>` line break, `.accent` = green underline keyword). `anchor` is the phone's horizontal side; `tilt` is degrees.

```js
export const screens = [
  {
    id: "01-snap",
    hero: true,
    screenshot: "macro.png",
    tilt: 4,
    anchor: "right",
    headline: 'Зураг ав.<br><span class="accent">Илчлэгээ мэд.</span>',
    subhead: "Хоолныхоо зургийг авахад л илчлэг, макро секундын дотор гарна.",
  },
  {
    id: "02-macros",
    hero: false,
    screenshot: "macro.png",
    tilt: -4,
    anchor: "right",
    headline: 'Илчлэг, макро —<br><span class="accent">агшин зуур.</span>',
    subhead: "Уураг, нүүрс ус, өөх тосыг бүртгэхээсээ өмнө хар.",
  },
  {
    id: "03-dashboard",
    hero: false,
    screenshot: "dashboard.png",
    tilt: 4,
    anchor: "left",
    headline: 'Өдрөө <span class="accent">нэг дороос</span><br>хяна.',
    subhead: "Өдрийн илчлэг, макро зорилт, хоолны бүртгэл — нэг дэлгэцэнд.",
  },
  {
    id: "04-progress",
    hero: false,
    screenshot: "progress.png",
    tilt: -4,
    anchor: "right",
    headline: 'Ахиц <span class="accent">өдөр бүр</span><br>харагдана.',
    subhead: "Жингийн хандлага, илчлэг, BMI-г хялбар ажигла.",
  },
  {
    id: "05-profile",
    hero: false,
    screenshot: "profile.png",
    tilt: 4,
    anchor: "left",
    headline: 'Зорилгоо <span class="accent">өөрөө</span><br>тодорхойл.',
    subhead: "Зорилтот жин, өдрийн илчлэгээ уян хатан тохируул.",
  },
];

export const featureGraphic = {
  headline: 'Нэг зургаас<br><span class="accent">илчлэг</span>',
  subhead: "Зураг ав — илчлэг, макро секундын дотор.",
};
```

- [ ] **Step 2: Syntax check**

```bash
node -e "import('./store-assets/source/screens.mjs').then(m => console.log(m.screens.length, 'screens'))"
```

Expected: `5 screens`

---

### Task 3: Tall screenshot template

**Files:**
- Create: `store-assets/source/template.html`

- [ ] **Step 1: Write `template.html`**

All layout in `vw`/`vh` so the same template renders 1290×2796 and 1080×1920. Tokens: `{{anchor}}`, `{{heroClass}}`, `{{headline}}`, `{{subhead}}`, `{{screenshot}}`, `{{tilt}}`. Relative paths resolve from `store-assets/source/` (the temp file is written next to this template).

```html
<!DOCTYPE html>
<html lang="mn">
<head>
<meta charset="utf-8">
<link rel="stylesheet" href="../../node_modules/@fontsource/roboto/400.css">
<link rel="stylesheet" href="../../node_modules/@fontsource/roboto/700.css">
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  html, body { width: 100vw; height: 100vh; }
  body {
    font-family: "Roboto", sans-serif;
    background: linear-gradient(180deg, #fefefe 0%, #faf9f6 100%);
    color: #1c1c1c;
    position: relative;
    overflow: hidden;
  }
  .vignette {
    position: absolute; inset: 2.4vw;
    border: 1px solid #e9e9e6; border-radius: 3vw;
    z-index: 0;
  }
  header { position: relative; z-index: 2; padding: 7vw 7.5vw 0; }
  .brand { display: flex; align-items: center; gap: 2vw; }
  .brand img { width: 4.8vw; height: 4.8vw; }
  .brand span { font-size: 3.5vw; font-weight: 700; letter-spacing: -0.01em; }
  h1 {
    margin-top: 5.5vw;
    font-size: 8.8vw; font-weight: 700;
    line-height: 1.14; letter-spacing: -0.02em;
  }
  h1 .accent {
    text-decoration: underline;
    text-decoration-color: #22c55e;
    text-decoration-thickness: 0.55vw;
    text-underline-offset: 1.1vw;
  }
  .subhead {
    margin-top: 3.2vw;
    font-size: 3.1vw; font-weight: 400; line-height: 1.55;
    color: #5f5f5d; max-width: 82vw;
  }
  .food { display: none; }
  body.hero .food {
    display: block; position: absolute; z-index: 1;
    left: 7.5vw; right: 7.5vw; top: 36vh; height: 22vh;
    border-radius: 3vw; border: 1px solid #e9e9e6;
    background-image: url("../../public/screenshots/macro.png");
    background-size: cover; background-position: 50% 4%;
  }
  .phone {
    position: absolute; z-index: 2;
    width: 62vw; aspect-ratio: 1 / 2.05;
    background: #1c1c1c; border-radius: 9vw; padding: 2vw;
    box-shadow: 0 2.5vw 7vw rgba(0, 0, 0, 0.18);
    bottom: -7vh;
  }
  body.left .phone { left: 7.5vw; }
  body.right .phone { right: 7.5vw; }
  body.hero .phone { width: 54vw; top: 46vh; bottom: auto; }
  .phone img {
    width: 100%; height: 100%;
    object-fit: cover; object-position: top;
    border-radius: 7.2vw; display: block;
  }
</style>
</head>
<body class="{{anchor}} {{heroClass}}">
  <div class="vignette"></div>
  <header>
    <div class="brand">
      <img src="../../public/logo/deglem-glyph-dark.png" alt="">
      <span>Дэглэм</span>
    </div>
    <h1>{{headline}}</h1>
    <p class="subhead">{{subhead}}</p>
  </header>
  <div class="food"></div>
  <div class="phone" style="transform: rotate({{tilt}}deg)">
    <img src="../../public/screenshots/{{screenshot}}" alt="">
  </div>
</body>
</html>
```

---

### Task 4: Feature graphic template

**Files:**
- Create: `store-assets/source/feature.html`

- [ ] **Step 1: Write `feature.html`**

Fixed 1024×500, px units. Tokens: `{{headline}}`, `{{subhead}}`. Two phones right (dashboard behind, macro front) per spec.

```html
<!DOCTYPE html>
<html lang="mn">
<head>
<meta charset="utf-8">
<link rel="stylesheet" href="../../node_modules/@fontsource/roboto/400.css">
<link rel="stylesheet" href="../../node_modules/@fontsource/roboto/700.css">
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  html, body { width: 1024px; height: 500px; }
  body {
    font-family: "Roboto", sans-serif;
    background: linear-gradient(180deg, #fefefe 0%, #faf9f6 100%);
    color: #1c1c1c;
    position: relative; overflow: hidden;
  }
  .vignette {
    position: absolute; inset: 18px;
    border: 1px solid #e9e9e6; border-radius: 24px;
    z-index: 0;
  }
  header { position: relative; z-index: 2; padding: 64px 0 0 64px; max-width: 520px; }
  .brand { display: flex; align-items: center; gap: 14px; }
  .brand img { width: 40px; height: 40px; }
  .brand span { font-size: 28px; font-weight: 700; }
  h1 { margin-top: 36px; font-size: 64px; font-weight: 700; line-height: 1.1; letter-spacing: -0.02em; }
  h1 .accent {
    text-decoration: underline;
    text-decoration-color: #22c55e;
    text-decoration-thickness: 5px;
    text-underline-offset: 9px;
  }
  .subhead { margin-top: 24px; font-size: 22px; line-height: 1.5; color: #5f5f5d; }
  .phone {
    position: absolute;
    width: 200px; aspect-ratio: 1 / 2.05;
    background: #1c1c1c; border-radius: 30px; padding: 7px;
    box-shadow: 0 18px 40px rgba(0, 0, 0, 0.18);
    z-index: 1;
  }
  .phone img {
    width: 100%; height: 100%;
    object-fit: cover; object-position: top;
    border-radius: 24px; display: block;
  }
  .phone.back { right: 250px; top: 70px; transform: rotate(-7deg); }
  .phone.front { right: 80px; top: 40px; transform: rotate(5deg); z-index: 2; }
</style>
</head>
<body>
  <div class="vignette"></div>
  <header>
    <div class="brand">
      <img src="../../public/logo/deglem-glyph-dark.png" alt="">
      <span>Дэглэм</span>
    </div>
    <h1>{{headline}}</h1>
    <p class="subhead">{{subhead}}</p>
  </header>
  <div class="phone back"><img src="../../public/screenshots/dashboard.png" alt=""></div>
  <div class="phone front"><img src="../../public/screenshots/macro.png" alt=""></div>
</body>
</html>
```

---

### Task 5: Generator script + npm script

**Files:**
- Create: `store-assets/source/generate.mjs`
- Modify: `package.json` (scripts)

- [ ] **Step 1: Write `generate.mjs`**

```js
import path from "node:path";
import { fileURLToPath } from "node:url";
import { mkdir, readFile, unlink, writeFile } from "node:fs/promises";
import { chromium } from "playwright";
import { featureGraphic, screens } from "./screens.mjs";

const SRC = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(SRC, "..", "..");
const TMP = path.join(SRC, ".tmp.html");

const TARGETS = [
  { store: "app-store", width: 1290, height: 2796 },
  { store: "google-play", width: 1080, height: 1920 },
];

function fill(template, data) {
  return template.replace(/\{\{(\w+)\}\}/g, (_, key) => String(data[key] ?? ""));
}

async function shoot(page, html, width, height, outPath) {
  await writeFile(TMP, html);
  await page.setViewportSize({ width, height });
  await page.goto("file://" + TMP, { waitUntil: "networkidle" });
  await page.evaluate(() => document.fonts.ready);
  await page.screenshot({ path: outPath });
  console.log("wrote", path.relative(ROOT, outPath));
}

const tallTemplate = await readFile(path.join(SRC, "template.html"), "utf8");
const featureTemplate = await readFile(path.join(SRC, "feature.html"), "utf8");

const browser = await chromium.launch();
const page = await browser.newPage({ deviceScaleFactor: 1 });

for (const { store, width, height } of TARGETS) {
  await mkdir(path.join(ROOT, "store-assets", store), { recursive: true });
  for (const screen of screens) {
    const html = fill(tallTemplate, { ...screen, heroClass: screen.hero ? "hero" : "" });
    await shoot(page, html, width, height, path.join(ROOT, "store-assets", store, `${screen.id}.png`));
  }
}

await shoot(
  page,
  fill(featureTemplate, featureGraphic),
  1024,
  500,
  path.join(ROOT, "store-assets", "google-play", "feature-graphic.png"),
);

await unlink(TMP);
await browser.close();
```

- [ ] **Step 2: Add npm script**

In `package.json` `"scripts"`, add:

```json
"gen:store": "node store-assets/source/generate.mjs"
```

- [ ] **Step 3: Run generation**

```bash
pnpm gen:store
```

Expected: 11 `wrote …` lines, exit 0. Failure modes: missing Chromium → rerun Task 1 Step 2; blank fonts → check the two `@fontsource/roboto` CSS paths exist.

- [ ] **Step 4: Verify exact dimensions**

```bash
for f in store-assets/app-store/*.png store-assets/google-play/*.png; do
  echo "$f: $(sips -g pixelWidth -g pixelHeight "$f" | awk '/pixel/{printf "%s ", $2}')"
done
```

Expected: app-store all `1290 2796`, google-play screens `1080 1920`, feature-graphic `1024 500`.

---

### Task 6: Visual pass and polish

**Files:**
- Modify (as needed): `store-assets/source/template.html`, `store-assets/source/feature.html`, `store-assets/source/screens.mjs`
- Overwrite (generated): `store-assets/app-store/*.png`, `store-assets/google-play/*.png`

- [ ] **Step 1: Read every generated PNG**

Use the Read tool on all 11 PNGs. Check each against this list:

1. No clipped/overflowing text (headline, subhead fit; Cyrillic renders in Roboto, not serif fallback).
2. Headline/subhead don't collide with food band or phone.
3. Green `.accent` underline visible on every headline.
4. Phone frame looks like the site's `PhoneMockup` (charcoal bezel, rounded), screenshot not distorted.
5. Hero (01): food band shows the meal photo (not UI chrome), phone overlaps band.
6. Anchor/tilt pattern: 01 right +4°, 02 right −4°, 03 left +4°, 04 right −4°, 05 left +4°.
7. Feature graphic: both phones inside canvas, no text/phone overlap.
8. Both canvas sizes acceptable (Play 1080×1920 is squatter — verify phone bleed isn't excessive).

- [ ] **Step 2: Fix and regenerate (iterate)**

For each defect, adjust the relevant `vw`/`vh` value or copy, rerun `pnpm gen:store`, re-read the affected PNGs. Repeat until the checklist passes.

- [ ] **Step 3: Leave everything uncommitted for user review**

---

### Task 7: Remove replaced Pillow script

**Files:**
- Delete: `store-assets/source/generate-store-assets.py`

- [ ] **Step 1: Delete**

```bash
rm store-assets/source/generate-store-assets.py
```

- [ ] **Step 2: Confirm nothing references it**

```bash
grep -rn "generate-store-assets" --exclude-dir=node_modules --exclude-dir=.git . || echo "no references"
```

Expected: only matches inside `docs/superpowers/` (spec/plan history) or `no references`.

---

## Final Verification

- [ ] `pnpm gen:store` runs clean end-to-end.
- [ ] Dimension check (Task 5 Step 4) passes for all 11 files.
- [ ] User reviews the final images.
