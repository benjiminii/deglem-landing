import { mkdirSync, writeFileSync } from 'node:fs';
import QRCode from 'qrcode';

import { SITE_URL, GET_PATH } from '../src/config.ts';

// Regenerate the download QR code:  pnpm gen:qr
// One QR → the smart /get link, which routes iOS / Android to the right store.
// The committed SVG lives in public/qr/ and is referenced by DownloadCTA.astro.
const url = `${SITE_URL}${GET_PATH}`;

const svg = await QRCode.toString(url, {
  type: 'svg',
  errorCorrectionLevel: 'M',
  margin: 1,
  color: { dark: '#1c1c1c', light: '#00000000' }, // charcoal on transparent
});

mkdirSync('public/qr', { recursive: true });
writeFileSync('public/qr/get.svg', svg);
console.log(`wrote public/qr/get.svg -> ${url}`);
