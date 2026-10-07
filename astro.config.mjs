// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import vercel from '@astrojs/vercel';
import tailwindcss from '@tailwindcss/vite';
import { SITE_URL } from './src/config.ts';

export default defineConfig({
  site: SITE_URL,
  output: 'static',
  adapter: vercel(),
  // /get and the legacy /mn/* stubs are redirect helpers, not content — keep them out of the sitemap.
  integrations: [sitemap({ filter: (page) => !/\/get\/?$|\/mn(\/|$)/.test(page) })],
  vite: { plugins: [tailwindcss()] },
  i18n: {
    defaultLocale: 'mn',
    locales: ['mn', 'en'],
    routing: { prefixDefaultLocale: false },
  },
});
