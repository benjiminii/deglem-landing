import path from "node:path";
import { fileURLToPath } from "node:url";
import { mkdir, readFile, unlink, writeFile } from "node:fs/promises";
import { chromium } from "playwright";
import { featureGraphic, screens } from "./screens.mjs";

const SRC = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(SRC, "..", "..");
const TMP = path.join(SRC, ".tmp.html");

const TARGETS = [
  { store: "app-store", width: 1284, height: 2778 },
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
