# HTML Title Slide Capture Pipeline

Premium title and divider slides are built as HTML files, captured as high-resolution PNG screenshots, then embedded as full-bleed images in pptxgenjs. This produces visual richness (layered backgrounds, gradient glows, arc treatments) that pptxgenjs alone can't achieve.

## Table of Contents

- [When to Use HTML Capture](#when-to-use-html-capture)
- [HTML Template](#html-template)
- [Layered Background Pattern](#layered-background-pattern)
- [Section Divider Pattern](#section-divider-pattern)
- [Capture Methods](#capture-methods)
- [Embedding in pptxgenjs](#embedding-in-pptxgenjs)
- [Font Setup](#font-setup)

---

## When to Use HTML Capture

Use HTML capture for slides that need:
- **Layered background images** (gradients, glows, arcs)
- **Custom brand backgrounds** from design kits
- **Complex CSS effects** (gradient text, blend modes, SVG filters)
- **Premium visual treatments** that go beyond solid colors and shapes

Use pptxgenjs directly for:
- **Content slides** with cards, bullets, metrics
- **Data-driven layouts** that change per deck
- Anything that benefits from programmatic precision

---

## HTML Template

Every HTML slide follows this structure:

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=1920">
<title>Slide Title</title>
<link rel="stylesheet" href="fonts/ibm-plex-sans.css">
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    width: 1920px; height: 1080px; overflow: hidden;
    font-family: 'IBM Plex Sans', sans-serif;
    color: #161616;
    background: #ffffff;
    position: relative;
  }

  .title-content {
    position: absolute;
    top: 420px; left: 86px;
    z-index: 10;
    max-width: 1200px;
  }
  .title-content h1 {
    font-size: 72px; font-weight: 700; line-height: 1.05;
    color: #161616;
  }
  .title-content .subtitle {
    font-size: 28px; font-weight: 300; color: #525252;
    margin-top: 24px;
  }

  .footer-text {
    position: absolute;
    bottom: 40px; left: 86px;
    z-index: 10;
    font-size: 11px; font-weight: 400; color: #9B9B9B;
  }
</style>
</head>
<body>

<div class="title-content">
  <h1>Deck Title<br>Second Line</h1>
  <div class="subtitle">Subtitle Text</div>
</div>

<div class="footer-text">&copy; Company Name</div>

</body>
</html>
```

Key constraints:
- **Fixed dimensions**: 1920×1080px body, `overflow: hidden`
- **Absolute positioning**: Title at top:420px, left:86px
- **z-index layering**: Background layers (1-4), content (10)

---

## Layered Background Pattern

The HC CY26 Kit uses 4 layered background images stacked with CSS:

```html
<style>
  .bg-layer {
    position: absolute; top: 0; left: 0;
    width: 1920px; height: 1080px;
    pointer-events: none;
  }
  .bg-gradient {
    z-index: 1;
    background: url('media/hc-gradient-base.png') top center / 1920px 1080px no-repeat;
  }
  .bg-glow-left {
    z-index: 2;
    background: url('media/hc-glow-left.png') bottom left / auto 1080px no-repeat;
  }
  .bg-glow-right {
    z-index: 3;
    background: url('media/hc-glow-right.png') top right / auto 1080px no-repeat;
  }
  .bg-arcs {
    z-index: 4;
    background: url('media/hc-arc-lines.png') center right / auto 1080px no-repeat;
  }
</style>

<div class="bg-layer bg-gradient"></div>
<div class="bg-layer bg-glow-left"></div>
<div class="bg-layer bg-glow-right"></div>
<div class="bg-layer bg-arcs"></div>
```

This produces a premium look with depth — each layer adds subtle gradients, glows, and arc lines that compose into a cohesive background.

---

## Section Divider Pattern

Section dividers use a single accent color. The background can use a `radial-gradient` for subtle depth on white:

```css
body {
  background: radial-gradient(ellipse at 70% 30%,
    rgba(237,245,255,0.6) 0%, transparent 60%), #ffffff;
}
```

Title text uses the section accent color:

| Section | Color | Carbon Token |
|---------|-------|-------------|
| Foundations | `#8a3ffc` | purple-60 |
| Guardrails | `#d02670` | magenta-60 |
| SDD | `#009d9a` | teal-60 |
| Workflows | `#198038` | green-60 |
| Getting Started | `#b28600` | yellow-50 |

---

## Capture Methods

### Chrome Headless (Quick, Single Slide)

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless --disable-gpu \
  --screenshot=images/slide-title.png \
  --window-size=1920,1080 \
  --force-device-scale-factor=2 \
  "file://$(pwd)/slide-title.html"
```

This produces a 3840×2160 PNG (2x scale for Retina sharpness).

### Playwright (Batch Capture)

For capturing multiple slides, use a Playwright script:

```javascript
import { chromium } from "playwright";
import { readdirSync } from "fs";
import { resolve } from "path";

const browser = await chromium.launch();
const context = await browser.newContext({
  viewport: { width: 1920, height: 1080 },
  deviceScaleFactor: 2,
});

const files = readdirSync("static").filter(f => f.endsWith(".html"));

for (const file of files) {
  const page = await context.newPage();
  await page.goto(`file://${resolve("static", file)}`);
  await page.waitForTimeout(500);  // Let CSS render
  const name = file.replace(".html", ".png");
  await page.screenshot({ path: `images/${name}` });
  await page.close();
}

await browser.close();
```

Key settings:
- `viewport: { width: 1920, height: 1080 }` — matches HTML body dimensions
- `deviceScaleFactor: 2` — produces 3840×2160 PNG for Retina
- `waitForTimeout(500)` — allows CSS transitions/fonts to load

---

## Embedding in pptxgenjs

Full-bleed image covering the entire slide:

```javascript
const slide = pres.addSlide();
slide.addImage({
  path: "images/slide-title.png",
  x: 0, y: 0, w: 10, h: 5.625,  // full 16:9 dimensions
});
```

---

## Font Setup

### IBM Plex Sans (for HTML slides)

Font files live in `playgrounds/IBM/fonts/`:
- `IBMPlexSans-Light.woff2` (300)
- `IBMPlexSans-Regular.woff2` (400)
- `IBMPlexSans-Medium.woff2` (500)
- `IBMPlexSans-SemiBold.woff2` (600)
- `IBMPlexSans-Bold.woff2` (700)

CSS declaration: `<link rel="stylesheet" href="fonts/ibm-plex-sans.css">`

### Inter (for HashiCorp-branded slides)

Used with the HC CY26 Kit backgrounds:
- `Inter-Light.woff2` through `Inter-Bold.woff2`
- CSS declaration: `<link rel="stylesheet" href="fonts/inter.css">`

### Important

Font files must be accessible from the HTML file's location. Use relative paths in the `<link>` tag. The fonts are only relevant for HTML capture — pptxgenjs content slides use system fonts (`"Arial"`, `"Arial Black"`).
