# Design System — Deglem Landing (Astro / Tailwind v4)

The marketing site shares the Deglem app's brand: warm cream background, near-black charcoal text, the D-spoon glyph, and Roboto. All styling uses Tailwind v4 utility classes. Tokens are defined CSS-first in `src/styles/global.css` under `@theme` — there is **no** `tailwind.config` file.

---

## 1. Visual Theme & Atmosphere

Warm, approachable, analog — like a well-crafted food journal, not a sterile health tracker. The cream background separates Deglem from clinical white SaaS pages. Charcoal-on-cream gives soft, readable contrast; a single charcoal section (the download CTA) provides one strong dark anchor.

**Key characteristics:**
- Warm parchment background (`#faf9f6`) — never pure white
- **Roboto** as the only typeface (weights 400 / 500 / 700)
- Secondary text via the dedicated `muted` token (not opacity guesses)
- Borders over shadows for cards (`#e7e2d6`)
- One inverted section (charcoal CTA) for download emphasis
- Phone mockups in charcoal frames carry the product imagery

---

## 2. Color Palette

### Tailwind v4 tokens (`src/styles/global.css`)

```css
@theme {
  --color-cream: #faf9f6;
  --color-charcoal: #1c1c1c;
  --color-muted: #5f5f5d;
  --color-cream-border: #e7e2d6;
  --font-sans: 'Roboto', system-ui, sans-serif;
}
```

Defining `--color-cream` auto-generates `bg-cream`, `text-cream`, `border-cream`, and opacity modifiers like `bg-cream/90`, `text-cream/70`.

### Roles

| Token | Value | Class | Use |
|-------|-------|-------|-----|
| Cream | `#faf9f6` | `bg-cream` | Page background, card surfaces, logo/text on charcoal |
| Charcoal | `#1c1c1c` | `bg-charcoal` / `text-charcoal` | Primary text, dark buttons, CTA section, phone frames |
| Muted | `#5f5f5d` | `text-muted` | Secondary text, captions — **only on light backgrounds** |
| Cream Border | `#e7e2d6` | `border-cream-border` | Card borders, dividers, section tint (`bg-cream-border/30`) |
| Cream 70% | `rgb(250 249 246 / .7)` | `text-cream/70` | Secondary text **on charcoal** (passes WCAG AA) |
| Cream 90% | `rgb(250 249 246 / .9)` | `bg-cream/90` | Sticky nav backdrop (with `backdrop-blur`) |

**Contrast rule:** Never put `text-muted` on `bg-charcoal` (≈2.66:1, fails AA). Use `text-cream/70` for secondary text on dark.

---

## 3. Typography

Roboto via `@fontsource/roboto` (imported in `global.css`). `--font-sans` maps `font-sans` to Roboto.

### Type scale (as used)

| Role | Classes | Use |
|------|---------|-----|
| Hero | `text-4xl sm:text-5xl font-bold leading-tight` | `<h1>` page headline |
| Section heading | `text-3xl font-bold` | `<h2>` section titles |
| Card / step title | `text-lg font-semibold` | FeatureCard, HowItWorks step |
| Lead | `text-lg text-muted` | Hero subtitle |
| Body | `text-base` / `text-sm` | Descriptions, footer |
| Nav / button | `text-sm font-medium` | Nav links, Download button |

**Rules:**
- Weights: 400 (regular), 500 (`font-medium`), 700 (`font-bold`) — `font-semibold` (600) is used for titles and is acceptable.
- Headings use `font-bold`; body stays regular. No letter-spacing tweaks.
- One `<h1>` per page; sections use `<h2>`; cards/steps use `<h3>`.

---

## 4. Spacing & Layout

Base unit 4px (Tailwind default). Common rhythm:

| Class | px | Use |
|-------|----|-----|
| `gap-2` / `gap-3` | 8 / 12 | Inline groups (logo+wordmark, badge rows) |
| `px-5` | 20 | **Standard horizontal page padding** (every section) |
| `p-6` | 24 | Card inner padding |
| `py-16` | 64 | Standard section vertical padding |
| `py-20` / `sm:py-24` | 80 / 96 | CTA / hero vertical padding |
| `mt-10` | 40 | Heading-to-content / content-to-badges |

- Content width capped at `max-w-5xl` (sections) / `max-w-3xl` (CTA, privacy body), centered with `mx-auto`.
- Responsive: single column on mobile, `sm:grid-cols-3` for features/steps; gallery side phones are `hidden … sm:block`.

---

## 5. Border Radius

| Class | px | Use |
|-------|----|-----|
| `rounded-lg` | 8 | Buttons |
| `rounded-xl` | 12 | Cards (FeatureCard) |
| `rounded-full` | pill | Numbered step badges, language pills |
| `rounded-[2rem]` / `rounded-[1.5rem]` | 32 / 24 | Phone mockup outer frame / inner screen |

Cards use `border border-cream-border` — **not** shadows. Only phone mockups use a shadow (`shadow-2xl`) to lift product imagery off the page.

---

## 6. Component Patterns

### Primary button (Download)
```html
<a href="#download" class="rounded-lg bg-charcoal px-4 py-2 text-sm font-medium text-cream transition-opacity hover:opacity-80">Download</a>
```

### Card
```html
<div class="rounded-xl border border-cream-border bg-cream p-6 text-left">…</div>
```

### Sticky nav
```html
<header class="sticky top-0 z-10 border-b border-cream-border bg-cream/90 backdrop-blur">…</header>
```

### Inverted CTA section
```html
<section id="download" class="bg-charcoal py-20">
  <h2 class="text-3xl font-bold text-cream">…</h2>
  <p class="text-cream/70">…</p>
</section>
```

### Phone mockup
Charcoal frame + inner cream screen, optional `rotate` for the gallery:
```html
<div class="rounded-[2rem] bg-charcoal p-2 shadow-2xl" style="transform: rotate(-6deg)">
  <div class="overflow-hidden rounded-[1.5rem] bg-cream">
    <img src="/screenshots/dashboard.png" alt="Deglem dashboard" class="block h-full w-full object-cover" loading="lazy" />
  </div>
</div>
```

### Logo lockup
Glyph + wordmark. Glyph color follows background:
- On cream (nav, footer): `deglem-glyph-dark.png`
- On charcoal: `deglem-glyph-light.png`
```html
<a href="/" class="flex items-center gap-2 transition-opacity hover:opacity-80">
  <img src="/logo/deglem-glyph-dark.png" alt="" width="28" height="28" class="h-7 w-7" />
  <span class="text-xl font-bold text-charcoal">Deglem</span>
</a>
```
The glyph `<img>` uses empty `alt=""` (decorative) because the adjacent "Deglem" text already names the brand.

---

## 7. Imagery & Brand Assets

- **Logo:** glyph-only D-spoon mark (no wordmark in the image). Pair with the text "Deglem". Source: `../calorie-tracker-ai/assets/images/logos/` → copied into `public/logo/`.
- **Screenshots:** shown inside `PhoneMockup`. Placeholders are solid-tone PNGs (360×720) generated by `scripts/make-placeholders.mjs`; swap with real captures at the same paths.
- **Store badges:** placeholder charcoal SVGs; replace with the official Apple / Google badge artwork before launch (brand guideline compliance).
- **Social preview:** `public/og-image.png` (1200×630) — currently a solid cream placeholder.

---

## 8. Accessibility

- Color contrast: charcoal-on-cream and cream-on-charcoal pass AA; never `text-muted` on charcoal.
- Every `<img>` has meaningful `alt`, or `alt=""` when decorative (logo beside text).
- Store badge links carry `aria-label`; emoji feature icons are `aria-hidden="true"`.
- Heading order: one `<h1>`, then `<h2>` sections, `<h3>` cards.
- Touch/click targets: buttons and nav links use generous padding (`px-4 py-2`).

---

## 9. Do's and Don'ts

### Do
- Use `bg-cream` for backgrounds — never `bg-white`
- Use `border border-cream-border` for cards — not shadows
- Use `text-cream/70` for secondary text on charcoal; `text-muted` only on light
- Add `transition-opacity hover:opacity-80` to every link/button
- Use `px-5` as standard horizontal padding and `max-w-5xl` for section width
- Add new design tokens under `@theme` in `global.css` (Tailwind v4 way)
- Match the glyph variant (dark/light) to its background

### Don't
- Don't create a `tailwind.config` file — this is Tailwind v4 CSS-first
- Don't use `bg-white` or `bg-gray-*` — derive from cream / charcoal
- Don't put `text-muted` on charcoal (fails contrast)
- Don't add shadows to cards — borders only (phone mockups are the one exception)
- Don't hardcode user-facing copy — route everything through `t()` with matching keys in both locales
- Don't use saturated accent colors — the palette is intentionally warm-neutral
