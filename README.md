# Deglem Landing

Static Astro landing page for the Deglem app. Bilingual (EN/MN), Tailwind v4, deployed on Vercel. Package manager: pnpm.

## Develop
```bash
pnpm install
pnpm dev      # http://localhost:4321
pnpm build    # static output to dist/
```

## Swap-in checklist before launch
- Replace `public/screenshots/{dashboard,camera,progress}.png` with real app screenshots (same names).
- Replace `public/badges/{app-store,google-play}.svg` with official store badges.
- Set `APP_STORE_URL` and `PLAY_STORE_URL` in `src/config.ts`.
- Replace `privacy.body` in `src/i18n/{en,mn}.json` with the real policy.
- Update `site` in `astro.config.mjs` and the Sitemap URL in `public/robots.txt` to the final domain.
- Replace `public/og-image.png`.

## i18n
Copy lives in `src/i18n/en.json` + `mn.json` (identical keys).
