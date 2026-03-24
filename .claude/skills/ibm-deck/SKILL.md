---
name: ibm-deck
description: Build IBM Carbon Design System styled PPTX presentations from scratch using pptxgenjs. Use this skill whenever the user wants to create, build, or generate an IBM-branded slide deck, presentation, or proposal with Carbon design tokens, IBM Plex fonts, and professional light-theme styling. Also triggers when creating any PPTX with IBM corporate styling, Carbon color tokens, or when the user mentions "IBM deck", "Carbon slides", "IBM presentation", or wants to apply IBM branding to slides. If the user is building a PPTX and mentions IBM or Carbon Design System, use this skill.
user-invocable: true
---

# IBM Carbon Deck Builder

Build professional PPTX decks styled with IBM's Carbon Design System using pptxgenjs.

## Architecture

IBM decks combine two rendering approaches:

- **Title & divider slides**: HTML templates captured as 2x PNG screenshots, then embedded as full-bleed images. This produces premium backgrounds with gradient treatments, arc lines, and layered effects that pptxgenjs can't replicate programmatically.
- **Content slides**: Built programmatically with pptxgenjs using Carbon design tokens. This gives precise control over card layouts, bullet lists, metric callouts, and icons.
- **visuals**: Use SVG liberally

Title slides demand visual richness (layered backgrounds, subtle glows) that only HTML/CSS can deliver at high fidelity, while content slides benefit from the programmatic precision of pptxgenjs for consistent spacing and alignment. If HTML capture is not available or desired, use the programmatic title slide pattern below.

## Bundled Assets

This skill is fully self-contained. All assets are in the skill directory:

```
ibm-deck/
├── SKILL.md
├── assets/
│   ├── media/                         ← HashiCorp CY26 Kit extracted assets (100 files)
│   │   ├── hc-gradient-base.png       (light-mode gradient base layer)
│   │   ├── hc-glow-left.png          (left glow overlay)
│   │   ├── hc-glow-right.png         (right glow overlay)
│   │   ├── hc-arc-lines.png          (arc lines overlay)
│   │   ├── hc-alternate-bg.png       (alternate background)
│   │   ├── hashicorp-logo.svg        (HC hexagon logo)
│   │   ├── image1-2,8,20,25.png      (dark gradient arc backgrounds)
│   │   ├── image5,11,26.png          (additional bg/glow variants)
│   │   ├── image21,83,84.png         (HC logo marks — various sizes)
│   │   ├── image35-37.png            (HC + IBM branding lockups)
│   │   ├── image60-68.png            (raw product icons — no bg)
│   │   ├── image69-82.png            (bordered & filled product icons)
│   │   ├── image12-19,28-34.png      (product logos — HC/HCP branded)
│   │   ├── image38-46.png            (product logos — standalone)
│   │   ├── image47-59.png            (product logos — Enterprise/Community)
│   │   ├── image85,87.png            (gradient color reference bars)
│   │   ├── image86.svg,image88.svg   (timeline/roadmap gradient SVGs)
│   │   ├── Hashicorp_Logos-*.png/svg  (compact strap logos)
│   │   └── HashiCorp Full product strap_.svg
│   ├── fonts/                         ← Font files + CSS declarations
│   │   ├── inter.css                  (Inter font-face — HC CY26 Kit brand font)
│   │   ├── ibm-plex-sans.css         (IBM Plex Sans + Mono font-face)
│   │   ├── Inter-*.woff2             (Light, Regular, Medium, SemiBold, Bold)
│   │   ├── IBMPlexSans-*.woff2       (Light, Regular, Medium, SemiBold, Bold)
│   │   └── IBMPlexMono-*.woff2       (Regular, Medium, SemiBold)
│   ├── slide-title-template.html      ← Title slide with HC CY26 Kit background
│   └── slide-divider-template.html    ← Section divider slide
├── scripts/
│   ├── capture-title.mjs              ← Single-command title/divider capture
│   └── setup-workspace.sh             ← Symlinks media/fonts into working dir
└── references/
    ├── pptxgenjs-ibm.md               ← Complete code patterns
    ├── html-capture.md                ← HTML capture pipeline details
    └── asset-catalog.md               ← Full asset inventory with lookup tables
```

### Using Bundled Product Assets

The `assets/media/` directory contains the complete HashiCorp CY26 Kit asset library — product icons, logos, backgrounds, and branding elements. Read `references/asset-catalog.md` for the full categorized inventory with lookup tables.

**Quick product icon reference** (most commonly needed):

| Product | Icon (filled bg) | Icon (bordered) | Logo | Color |
|---------|-----------------|-----------------|------|-------|
| Terraform | image74.png | image70.png | image42.png | `#7B42BC` |
| Vault | image80.png | image82.png | image39.png | `#FFD814` |
| Consul | image79.png | image76.png | image40.png | `#E03875` |
| Nomad | image73.png | — | image38.png | `#06D092` |
| Boundary | image78.png | image77.png | image41.png | `#F24C53` |
| Packer | — | image69.png | image45.png | `#1DAEFF` |
| Vagrant | — | image81.png | image44.png | `#1868F2` |
| Waypoint | — | image72.png | image46.png | `#14C6CB` |

**Embedding a product icon:**

```javascript
const skillDir = "<path-to-ibm-deck-skill>";
slide.addImage({
  path: `${skillDir}/assets/media/image74.png`,  // Terraform filled icon
  x: 0.7, y: 1.5, w: 0.5, h: 0.5,
});
```

**Brand gradient stops** (CY26 Kit signature gradient):
- Dark: `#6C81FF` → `#C08DFF` → `#FF8791` → `#F9B571`
- Light: `#CDD4FF` → `#E5D0FF` → `#FFC2C7` → `#FCDEC4`

## Quick Start

```bash
# 1. Install dependencies (project root)
npm install pptxgenjs react react-dom react-icons sharp

# 2. Capture title slide (single command — no workspace setup needed)
node <skill-dir>/scripts/capture-title.mjs \
  --line1 "Deck Title" --line2 "Second Line" \
  --subtitle "Subtitle Text" \
  --output images/slide-title.png

# 3. Write build script (run from repo root so relative paths resolve)
# 4. Run it
node build-<deck-name>.mjs
```

**Important**: Build scripts must be run from the **repository root**. Image paths in `addImage({ path: ... })` resolve relative to `process.cwd()`, not relative to the script file.

## Color Rules

pptxgenjs and SVG/React icons use hex colors differently. Getting this wrong is the most common error:

| Context | Format | Example |
|---------|--------|---------|
| **pptxgenjs** (fill, color, line) | Bare hex, NO `#` | `color: "0F62FE"` |
| **React icon SVG** rendering | WITH `#` prefix | `iconToBase64Png(Icon, "#" + C.blue60)` |
| **HTML/CSS** | Standard `#` prefix | `color: #0F62FE` |

The `#` prefix in pptxgenjs corrupts the PPTX XML and produces invisible elements.

## Carbon Design Tokens

```javascript
const C = {
  // Backgrounds
  white:    "FFFFFF",
  gray10:   "F4F4F4",  // panels, cards, code blocks

  // Borders
  gray20:   "E0E0E0",  // default border
  gray30:   "C6C6C6",  // strong border

  // Text
  gray100:  "161616",  // primary text
  gray70:   "525252",  // secondary text
  gray50:   "8D8D8D",  // placeholder/muted

  // Accents
  blue60:   "0F62FE",  // primary action
  purple60: "8A3FFC",
  teal60:   "009D9A",
  green60:  "198038",
  magenta60:"D02670",
  red60:    "DA1E28",
  yellow50: "B28600",
};
```

### Gradient Color Triplets (dark → mid → light)

For SVG → PNG gradient bars and gradient text. Use with `#` prefix (SVG context):

| Accent | Dark | Mid | Light |
|--------|------|-----|-------|
| red60 | `#A01520` | `#DA1E28` | `#FF4D55` |
| yellow50 | `#8A6800` | `#B28600` | `#F59E0B` |
| purple60 | `#627EEF` | `#8A3FFC` | `#D946EF` |
| teal60 | `#007D79` | `#009D9A` | `#2DD4BF` |
| green60 | `#0E6027` | `#198038` | `#34D478` |
| blue60 | `#0043CE` | `#0F62FE` | `#4589FF` |
| magenta60 | `#9F1853` | `#D02670` | `#FF7EB6` |

## Typography

| Element | Font | Size | Weight | Color | Max ~chars |
|---------|------|------|--------|-------|-----------|
| Section label | Arial | 10pt | Bold + charSpacing:3 | accent | 30 |
| Slide title | Arial Black | 22-26pt | Bold | gray100 | 45 |
| Subtitle | Arial | 12-13pt | Regular | gray70 | 90 |
| Card title | Arial | 14-16pt | Bold | gray100 | 35 |
| Body / bullets | Arial | 11-12pt | Regular | gray70 | 60 per line |
| Card body (narrow) | Arial | 9-10pt | Regular | gray70 | 40 per line |
| Card description | Arial | 12pt | Regular | gray70 | 120 |
| Step numbers | Arial | 9pt | Bold + charSpacing:2 | accent | 5 |
| Callout bar text | Arial | 10.5-11pt | Mixed | gray70/100 | 90 |
| Metric number | Arial Black | 24-36pt | Bold | accent | 15 |
| Metric label | Arial | 9pt | Bold + charSpacing:2 | gray50 | 20 |

**Minimum 9pt for any text** — anything smaller is unreadable when projected. Section labels and step numbers that were 7-8pt in early builds were invisible on projectors.

Use `"Arial"` and `"Arial Black"` as fontFace values — universally available in PowerPoint. The HTML title/divider templates use **Inter** (the HashiCorp CY26 Kit brand font), loaded from `assets/fonts/inter.css`. IBM Plex Sans is available in `assets/fonts/` for IBM-branded variants.

## Build Script Skeleton

```javascript
import pptxgen from "pptxgenjs";

const pres = new pptxgen();
pres.layout = "LAYOUT_16x9";  // 10" × 5.625"
pres.author = "Author Name";
pres.title = "Deck Title";

// ... add slides ...

await pres.writeFile({ fileName: "output.pptx" });
```

## Title Slides

### Option A: HTML Capture (Recommended)

Premium title slides use the bundled capture script — a single command that loads the HC CY26 Kit HTML template, substitutes your text, captures via Chrome headless at 2x, and outputs a 3840×2160 PNG. No workspace setup or symlinks needed.

```bash
node <skill-dir>/scripts/capture-title.mjs \
  --line1 "Deck Title" \
  --line2 "Second Line" \
  --subtitle "Subtitle Text" \
  --output images/slide-title.png
```

**Arguments:**

| Flag | Default | Description |
|------|---------|-------------|
| `--line1` | `"Title Line 1"` | First line of the title |
| `--line2` | `""` | Second line (optional) |
| `--subtitle` | `""` | Subtitle below title |
| `--footer` | `"© HashiCorp"` | Footer text |
| `--type` | `title` | `title` or `divider` |
| `--output` | `slide-title.png` | Output PNG path |

**Embed as full-bleed image:**

```javascript
const s1 = pres.addSlide();
s1.addImage({
  path: "images/slide-title.png",
  x: 0, y: 0, w: 10, h: 5.625,
});
```

The script resolves all asset paths (media/, fonts/) internally using absolute `file://` URLs, so it works from any directory. Background layers: `hc-gradient-base.png` (gradient), `hc-glow-left.png`, `hc-glow-right.png`, `hc-arc-lines.png`.

### Option B: Programmatic Title (No HTML Capture)

When Chrome headless isn't available, build the title slide directly in pptxgenjs:

```javascript
const s1 = pres.addSlide();
s1.background = { color: C.white };

// Top accent line
s1.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 10, h: 0.06,
  fill: { color: C.blue60 },
});

// Title
s1.addText("Deck Title", {
  x: 0.7, y: 1.8, w: 8.6, h: 1.0,
  fontSize: 40, fontFace: "Arial Black",
  color: C.gray100, bold: true, margin: 0,
});

// Subtitle
s1.addText("Subtitle Text", {
  x: 0.7, y: 2.8, w: 8.6, h: 0.5,
  fontSize: 18, fontFace: "Arial",
  color: C.gray70, margin: 0,
});

// Bottom bar
s1.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 5.125, w: 10, h: 0.5,
  fill: { color: C.gray10 },
});

s1.addText("Organization Name", {
  x: 0.7, y: 5.125, w: 8.6, h: 0.5,
  fontSize: 12, fontFace: "Arial",
  color: C.gray70, valign: "middle", margin: 0,
});
```

## Section Divider Slides

Section dividers use the same capture script with `--type divider`:

```bash
node <skill-dir>/scripts/capture-title.mjs \
  --type divider \
  --line1 "Section Title" \
  --subtitle "Section subtitle" \
  --output images/slide-divider.png
```

Design: white background, 54px Inter SemiBold title, 1750px horizontal rule, 22px Inter Light subtitle in gray `#727274`.

## Slide Header Pattern

Every content slide starts with this structure. **Always set the white background** — pptxgenjs defaults may not be white.

**Title wrapping**: At fontSize 22 in "Arial Black", a single line is ~0.37" tall with leading. Two lines need ~0.74". Use `h=px(90)` (~0.47") for single-line titles, or `h=px(170)` (~0.89") for titles that wrap to two lines — this gives comfortable clearance. Titles over ~45 chars in an 8.6" wide box will wrap. The subtitle y position is always computed relative to the title: `title.y + title.h + px(16)` for clearance. Never hardcode subtitle y — derive it from the title dimensions so it adjusts automatically when the title height changes.

```javascript
const slide = pres.addSlide();
slide.background = { color: C.white };  // REQUIRED on every content slide

// Section label (uppercase, accented, letter-spaced)
slide.addText("SECTION NAME", {
  x: 0.7, y: 0.35, w: 5, h: 0.3,
  fontSize: 10, fontFace: "Arial",
  color: C.teal60,  // varies per slide
  bold: true, charSpacing: 3, margin: 0,
});

// Title — h must account for possible text wrapping:
//   Single-line (short titles):  h = px(90)  ≈ 0.47"
//   Two-line (long titles):      h = px(170) ≈ 0.89"
// At fontSize 22 "Arial Black", each line is ~0.37" with leading.
// Titles over ~45 chars in an 8.6" wide box will wrap to 2 lines.
const titleY = 0.6;
const titleH = px(90);  // increase to px(170) if title may wrap to 2 lines
slide.addText("Slide Title Here", {
  x: 0.7, y: titleY, w: 8.6, h: titleH,
  fontSize: 22, fontFace: "Arial Black",
  color: C.gray100, bold: true, margin: 0,
});

// Subtitle — y derived from title position for automatic clearance
const subtitleY = titleY + titleH + px(16);
slide.addText("Supporting description text", {
  x: 0.7, y: subtitleY, w: 8.6, h: 0.3,
  fontSize: 12, fontFace: "Arial",
  color: C.gray70, margin: 0,
});
```

Content area starts at y ≈ 1.4-1.5. If using a larger 26pt title, push subtitle down accordingly and content to y: 1.5-1.65. When a title wraps to two lines (titleH = px(170)), the subtitle and content area shift down proportionally — always derive positions from the title dimensions rather than hardcoding.

## Key Patterns

Read `references/pptxgenjs-ibm.md` for complete code examples. Read `references/asset-catalog.md` for the complete product icon and asset inventory. Quick reference:

### Shadow Factory (CRITICAL)

pptxgenjs **mutates** option objects after passing them to `addShape()`. Reusing a shadow object across shapes produces corrupted values on the second shape. Always define shadows as factory functions at the top of the file — never write shadow objects inline:

```javascript
const cardShadow = () => ({
  type: "outer", color: "000000", blur: 8,
  offset: 2, angle: 135, opacity: 0.08,
});
```

### Card with Left Accent Bar (Gradient)

```javascript
slide.addShape(pres.shapes.RECTANGLE, {
  x: cx, y: cy, w: cardW, h: cardH,
  fill: { color: C.gray10 },
  shadow: cardShadow(),  // fresh instance every call
});

// Gradient left accent (w: 0.08 minimum for projection visibility)
const vBar = await renderVerticalGradientBar(gradientColors, 8, 260);
slide.addImage({ data: vBar, x: cx, y: cy, w: 0.08, h: cardH });
```

### Card with Top Accent Bar (Gradient)

```javascript
slide.addShape(pres.shapes.RECTANGLE, {
  x: px, y: py, w: pillarW, h: pillarH,
  fill: { color: C.gray10 }, shadow: cardShadow(),
});

// Gradient top accent (h: 0.08 minimum for projection visibility)
const bar = await renderGradientBar(gradientColors, 400, 8, 0);
slide.addImage({ data: bar, x: px, y: py, w: pillarW, h: 0.08 });
```

### Arrow Icons Between Cards

LINE shapes with `endArrowType: "triangle"` are too thin to see when projected. Use FaArrowRight icon images instead:

```javascript
import { FaArrowRight } from "react-icons/fa";

const arrowImg = await iconToBase64Png(FaArrowRight, "#" + arrowColor, 256);
slide.addImage({
  data: arrowImg,
  x: arrowX,  // midpoint between cards
  y: arrowY,  // vertically centered on cards
  w: 0.22,
  h: 0.22,
});
```

### Gradient Hero Title Text

Render large gradient-colored text (e.g., card hero titles like "Establish", "Enable") as SVG→PNG. This is the only way to get gradient text in pptxgenjs:

```javascript
const titleGrad = [
  { offset: 0, color: "#627EEF" },
  { offset: 50, color: "#8A3FFC" },
  { offset: 100, color: "#D946EF" },
];
const titleRW = title.length > 7 ? 900 : 700;  // wider SVG for longer text
const titleImg = await renderGradientTitle(title, titleGrad, titleRW, 120);
const titleW = cardW - px(50);
const titleH = titleW * (120 / titleRW);  // preserve aspect ratio
slide.addImage({ data: titleImg, x: cx + px(30), y: cy + px(78), w: titleW, h: titleH });
```

Adjust `titleRW` based on text length to avoid clipping — longer words need a wider SVG canvas.

### REQUIRED / MANDATORY Badge

A filled pill-shaped badge used to flag mandatory items on prerequisite or checklist cards:

```javascript
// Filled accent badge
slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: cx + cardW - 1.15, y: cy + 0.15, w: 0.95, h: 0.26,
  fill: { color: accentColor }, rectRadius: 0.05,
});
slide.addText("REQUIRED", {
  x: cx + cardW - 1.15, y: cy + 0.15, w: 0.95, h: 0.26,
  fontSize: 8, fontFace: "Arial", color: C.white,
  bold: true, align: "center", valign: "middle", charSpacing: 1.5, margin: 0,
});
```

For mandatory card highlighting, combine a tinted background + colored border:

```javascript
slide.addShape(pres.shapes.RECTANGLE, {
  x: cx, y: cy, w: cardW, h: cardH,
  fill: { color: "E8F7F7" },  // tinted bg instead of gray10
  line: { color: accentColor, width: 1.5 },  // accent border
  shadow: cardShadow(),
});
```

### Pixel-to-Inch Conversion Helper

For precise positioning when translating pixel-based designs to pptxgenjs inches:

```javascript
const px = (v) => v / 192;  // 1920px = 10 inches → 192px per inch
```

This is useful when porting layouts from 1920×1080 HTML slides to pptxgenjs. Use it for all coordinates to maintain exact proportions.

### Reusable Slide Header Helper

Encapsulates the section label + title + subtitle header pattern into a single function call. Handles title-wrap detection automatically:

```javascript
function addSlideHeader(slide, pres, sectionLabel, sectionColor, title, subtitle) {
  slide.background = { color: C.white };
  slide.addText(sectionLabel, {
    x: 0.7, y: 0.35, w: 5, h: 0.3,
    fontSize: 10, fontFace: "Arial", color: sectionColor,
    bold: true, charSpacing: 3, margin: 0,
  });
  const titleY = 0.6;
  const titleH = title.length > 45 ? px(170) : px(90);
  slide.addText(title, {
    x: 0.7, y: titleY, w: 8.6, h: titleH,
    fontSize: 22, fontFace: "Arial Black", color: C.gray100, bold: true, margin: 0,
  });
  if (subtitle) {
    const subtitleY = titleY + titleH + px(16);
    slide.addText(subtitle, {
      x: 0.7, y: subtitleY, w: 8.6, h: 0.3,
      fontSize: 12, fontFace: "Arial", color: C.gray70, margin: 0,
    });
  }
}

// Usage
addSlideHeader(slide, pres, "SECTION NAME", C.teal60,
  "Slide Title Here",
  "Supporting description text that explains the slide content");
```

### XML Entity Escaping for SVG Text

**Critical** when embedding user-provided content in SVG strings. Without this, ampersands and angle brackets in text will corrupt the SVG XML and produce blank images:

```javascript
function escXml(s) {
  return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

// Usage in SVG template literals
const svg = `<text ...>${escXml(userText)}</text>`;
```

### Footer Bar Shadow Factory

Lighter shadow variant for callout/footer bars — improves visual hierarchy vs. using `cardShadow()` on everything:

```javascript
const footerBarShadow = () => ({
  type: "outer", color: "000000", blur: 4,
  offset: 1, angle: 270, opacity: 0.06,
});
```

### Bullet Lists

Bullet text inside cards is the most common source of overflow — text wraps more than expected in narrow columns (2.75" cards have only ~2.35" of usable text width). Keep bullet text short (under 40 chars per bullet) and ensure the text box `h` value leaves room within the card boundary. If the card is `h: 3.0` and bullets start at `y + 1.4`, the bullet text box can be at most `h: 1.45` to stay inside.

`breakLine` adds a paragraph break after each item. Set it to `false` on the last item to avoid trailing whitespace:

```javascript
const bullets = items.map((item, idx) => ({
  text: item,
  options: {
    bullet: { code: "2022" },
    breakLine: idx < items.length - 1,  // false on last item
    fontSize: 11, color: C.gray70,
    paraSpaceAfter: 6,
  },
}));

slide.addText(bullets, {
  x, y, w, h,
  fontFace: "Arial", valign: "top", margin: 0,
});
```

### React Icons → PNG Base64

`iconToBase64Png()` is **async** — always `await` it. Missing `await` produces `[object Promise]` instead of image data:

```javascript
import { renderToStaticMarkup } from "react-dom/server";
import { createElement } from "react";
import sharp from "sharp";

async function iconToBase64Png(Icon, color, size = 256) {
  const svg = renderToStaticMarkup(createElement(Icon, { color, size: String(size) }));
  const pngBuffer = await sharp(Buffer.from(svg)).png().toBuffer();
  return "image/png;base64," + pngBuffer.toString("base64");
}

// MUST await — this is async
const iconData = await iconToBase64Png(FaShieldAlt, "#" + C.green60, 256);
slide.addImage({ data: iconData, x, y, w: 0.38, h: 0.38 });
```

### Bottom Callout Bar

Position at y ≈ 4.5-4.75 depending on content above. Match tint color to slide accent (see Tint Color Guide below):

```javascript
slide.addShape(pres.shapes.RECTANGLE, {
  x: 0.7, y: 4.5, w: 8.6, h: 0.55,
  fill: { color: "F0F5FF" },
  line: { color: C.blue60, width: 1 },
});

slide.addText([
  { text: "Bold prefix: ", options: { bold: true, color: C.gray100 } },
  { text: "Regular description text.", options: { color: C.gray70 } },
], {
  x: 1.4, y: 4.5, w: 7.7, h: 0.55,
  fontSize: 11, fontFace: "Arial", valign: "middle", margin: 0,
});
```

## Charts with Carbon Styling

pptxgenjs v4 has native `addChart()` supporting BAR, LINE, PIE, DOUGHNUT, RADAR, and more. Apply Carbon tokens for consistent styling.

### Chart Color Palette

```javascript
const carbonChartColors = [C.blue60, C.teal60, C.purple60, C.green60, C.magenta60];
```

Colors are bare hex (no `#`) — same rule as all pptxgenjs values.

### Common Chart Options

| Property | Value | Purpose |
|----------|-------|---------|
| `chartColors` | `carbonChartColors` | Series fill colors (bare hex) |
| `chartArea` | `{ fill: { color: C.white }, roundedCorners: false }` | Chart background |
| `catAxisLabelColor` | `C.gray70` | Category axis text |
| `valAxisLabelColor` | `C.gray70` | Value axis text |
| `catAxisLabelFontSize` | `10` | Category axis font size |
| `valAxisLabelFontSize` | `10` | Value axis font size |
| `valGridLine` | `{ color: C.gray20, size: 0.5 }` | Horizontal grid lines |
| `catGridLine` | `{ style: "none" }` | No vertical grid lines |
| `dataLabelColor` | `C.gray100` | Data label text |
| `dataLabelFontSize` | `10` | Data label size |
| `showLegend` | `true` | Show legend below chart |
| `legendColor` | `C.gray70` | Legend text color |
| `legendFontSize` | `10` | Legend font size |

### Chart Types

1. **Column/Bar chart** — KPI comparisons, quarterly data. Use `pres.charts.BAR` with `barDir: "col"` for vertical columns.
2. **Line chart** — trends, time series. Use `pres.charts.LINE` with `lineSmooth: true` for curved lines, `lineSize: 2` for visibility.
3. **Pie/Doughnut chart** — composition breakdowns. Use `pres.charts.DOUGHNUT` with `showPercent: true`, `holeSize: 50` for doughnuts.
4. **Radar chart** — maturity/capability assessments. Use `pres.charts.RADAR` with `radarStyle: "filled"`.

### Chart Positioning

Charts live in the content area below the slide header. Standard placement:

```javascript
slide.addChart(pres.charts.BAR, chartData, {
  x: 0.7, y: 1.5, w: 8.6, h: 3.5,
  // ... Carbon styling options
});
```

For side-by-side chart + callout:
- Chart: `x: 0.7, y: 1.5, w: 5.5, h: 3.2`
- Callout card: `x: 6.5, y: 1.5, w: 3.1, h: 3.2`

See `references/pptxgenjs-ibm.md` for complete chart code examples.

## SVG Data Visualization Helpers

For visualizations that pptxgenjs can't render natively (progress rings, sparklines, gauges), use the same SVG→PNG pipeline as gradient bars: construct an SVG string, convert via `sharp`, and embed as a base64 image.

All helpers follow this pattern:

```javascript
async function renderXxx(...params) {
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" ...>...</svg>`;
  const buf = await sharp(Buffer.from(svg)).png().toBuffer();
  return "image/png;base64," + buf.toString("base64");
}
```

### Available Helpers

| Helper | Default Size | Use Case |
|--------|-------------|----------|
| `renderProgressRing(value, maxValue, colors, size, thickness)` | 200×200 | KPI gauges, completion % |
| `renderRadialGauge(value, min, max, colors, width, height)` | 200×120 | Semi-circular gauges |
| `renderSparkline(dataPoints, color, width, height)` | 200×60 | Inline trend indicators |
| `renderMiniBarChart(data, colors, width, height)` | 200×120 | Compact bar charts in cards |
| `renderDonutChart(segments, size, thickness)` | 200×200 | Composition breakdowns |
| `renderProcessFlow(steps, colors, width, height)` | 800×100 | Horizontal flow diagrams |
| `renderProcessFlowSVG(steps, colors, width, height)` | 900×80 | Horizontal process flows with human gate styling |
| `renderHorizontalBars(data, colors, width, height)` | 400×200 | Horizontal bar comparisons (long labels) |
| `renderTimelineConnector(milestones, colors, width, height)` | 100×400 | Vertical timeline with milestones |
| `renderMatrixHeatmap(matrix, categories, colorScale, width, height)` | 300×300 | Risk/decision heat grids |
| `renderWaterfallChart(categories, values, colors, width, height)` | 500×200 | Cumulative value flows |

### renderProcessFlowSVG (Enhanced)

Enhanced process flow that supports **human gate styling** (dashed red borders), sub-labels, and `escXml()` for safe text rendering. Renders the entire flow as a single SVG image — more compact than building individual pptxgenjs shapes. **Prefer this over the basic `renderProcessFlow` when you need gate indicators or sub-labels.**

```javascript
function escXml(s) { return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); }

async function renderProcessFlowSVG(steps, colors, width = 900, height = 80) {
  const boxCount = steps.length;
  const arrowW = 20, gap = 6;
  const totalArrowSpace = (boxCount - 1) * (arrowW + gap * 2);
  const boxW = (width - totalArrowSpace - gap * 2) / boxCount;
  const boxH = height - 16, boxY = 8, boxR = 8;
  let elements = "";
  for (let i = 0; i < boxCount; i++) {
    const x = gap + i * (boxW + arrowW + gap * 2);
    const color = colors[i % colors.length];
    const isDashed = steps[i].gate;
    elements += `<rect x="${x}" y="${boxY}" width="${boxW}" height="${boxH}" rx="${boxR}"
      fill="${isDashed ? '#FFF0F0' : color}"
      ${isDashed ? `stroke="#DA1E28" stroke-width="2" stroke-dasharray="6 3"` : ''}/>
      <text x="${x + boxW/2}" y="${boxY + boxH/2 - 6}" text-anchor="middle" dominant-baseline="central"
        font-size="11" font-weight="700" font-family="Arial,Helvetica,sans-serif"
        fill="${isDashed ? '#DA1E28' : 'white'}">${escXml(steps[i].label)}</text>
      <text x="${x + boxW/2}" y="${boxY + boxH/2 + 10}" text-anchor="middle" dominant-baseline="central"
        font-size="8" font-family="Arial,Helvetica,sans-serif"
        fill="${isDashed ? '#DA1E28' : 'rgba(255,255,255,0.8)'}">${escXml(steps[i].sub || '')}</text>`;
    if (i < boxCount - 1) {
      const ax = x + boxW + gap;
      const ay = boxY + boxH / 2;
      elements += `<path d="M${ax},${ay} L${ax + arrowW - 6},${ay} L${ax + arrowW - 10},${ay - 4} M${ax + arrowW - 6},${ay} L${ax + arrowW - 10},${ay + 4}"
        fill="none" stroke="#8D8D8D" stroke-width="2" stroke-linecap="round"/>`;
    }
  }
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}" viewBox="0 0 ${width} ${height}">${elements}</svg>`;
  const buf = await sharp(Buffer.from(svg)).png().toBuffer();
  return "image/png;base64," + buf.toString("base64");
}

// Usage — process flow with human approval gate
const flow = await renderProcessFlowSVG([
  { label: "1. Clarify", sub: "Parse & resolve" },
  { label: "2. Design", sub: "Research & spec" },
  { label: "Approve", sub: "Human gate", gate: true },
  { label: "3. Implement", sub: "TDD-first code" },
  { label: "4. Validate", sub: "Full pipeline" },
], ["#0043CE", "#8A3FFC", "#DA1E28", "#009D9A", "#198038"], 900, 80);
slide.addImage({ data: flow, x: 0.5, y: 1.55, w: 9.0, h: 0.83 });
```

**When to use SVG flows vs. shape-based flows**: SVG flows produce a single embedded image — ideal when you need compact rendering, sub-labels, or gate styling. Shape-based flows (individual ROUNDED_RECTANGLE + FaArrowRight) are better when you need native PowerPoint editability or complex per-card content (bullets, metrics, icons inside cards).

### Key Details

- **Colors use `#` prefix** — these are SVG context, not pptxgenjs. Use `"#" + C.blue60`.
- **All helpers are async** — always `await` them.
- Track circles/arcs use `C.gray20` (`#E0E0E0`) for the unfilled portion.
- Center text in rings/gauges uses `C.gray100` (`#161616`).
- Sparkline gradients use the accent color at 20% opacity for the fill area.

See `references/pptxgenjs-ibm.md` for full implementations.

## Tables with Carbon Styling

pptxgenjs `addTable()` creates native PowerPoint tables. Apply Carbon tokens for consistent styling.

### Table Styling Rules

| Element | Style |
|---------|-------|
| Header row | `fill: { color: C.gray100 }`, `color: C.white`, bold, 12pt |
| Odd rows | `fill: { color: C.white }` |
| Even rows | `fill: { color: C.gray10 }` |
| All borders | `{ pt: 0.5, color: C.gray20 }` |
| Body text | 11pt Arial, `color: C.gray70` |
| Status: On Track | `color: C.green60`, bold |
| Status: At Risk | `color: C.red60`, bold |
| Status: In Progress | `color: C.yellow50`, bold |

### Table Positioning

Tables use the standard content area:

```javascript
slide.addTable(rows, {
  x: 0.7, y: 1.5, w: 8.6,
  fontFace: "Arial",
  fontSize: 11,
  border: { pt: 0.5, color: C.gray20 },
  colW: [2.5, 2.0, 2.0, 2.1],  // column widths must sum to table w
  autoPage: false,
});
```

### Per-Cell Formatting

Apply cell-level overrides for status colors, merged cells, and bold labels:

```javascript
const rows = [
  // Header
  [
    { text: "Initiative", options: { fill: { color: C.gray100 }, color: C.white, bold: true, fontSize: 12 } },
    { text: "Status", options: { fill: { color: C.gray100 }, color: C.white, bold: true, fontSize: 12 } },
  ],
  // Data row
  [
    { text: "Cloud Migration", options: { color: C.gray70 } },
    { text: "On Track", options: { color: C.green60, bold: true } },
  ],
];
```

### Risk Matrix Table with Per-Row Heights

For risk/priority matrices with color-coded severity levels and action columns. Uses `rowH` array for per-row height control:

```javascript
const riskRows = [
  [
    { text: "Risk Level", options: { fill: { color: C.gray100 }, color: C.white, bold: true, fontSize: 11 } },
    { text: "Version Type", options: { fill: { color: C.gray100 }, color: C.white, bold: true, fontSize: 11 } },
    { text: "Plan Changes", options: { fill: { color: C.gray100 }, color: C.white, bold: true, fontSize: 11 } },
    { text: "Action", options: { fill: { color: C.gray100 }, color: C.white, bold: true, fontSize: 11 } },
  ],
  [
    { text: "Low", options: { color: C.green60, bold: true, fontSize: 10 } },
    { text: "Patch (x.x.Y)", options: { color: C.gray70, fontSize: 10 } },
    { text: "No destroys", options: { color: C.gray70, fontSize: 10 } },
    { text: "Auto-merge", options: { color: C.green60, bold: true, fontSize: 10 } },
  ],
  [
    { text: "Medium", options: { color: C.yellow50, bold: true, fontSize: 10, fill: { color: C.gray10 } } },
    { text: "Minor (x.Y.0)", options: { color: C.gray70, fontSize: 10, fill: { color: C.gray10 } } },
    { text: "Adds only", options: { color: C.gray70, fontSize: 10, fill: { color: C.gray10 } } },
    { text: "Auto + notify", options: { color: C.yellow50, bold: true, fontSize: 10, fill: { color: C.gray10 } } },
  ],
  [
    { text: "Critical", options: { color: C.red60, bold: true, fontSize: 10 } },
    { text: "Major (Y.0.0)", options: { color: C.gray70, fontSize: 10 } },
    { text: "Destroys", options: { color: C.gray70, fontSize: 10 } },
    { text: "Block + escalate", options: { color: C.red60, bold: true, fontSize: 10 } },
  ],
];

slide.addTable(riskRows, {
  x: 0.7, y: 2.65, w: 8.6,
  fontFace: "Arial", fontSize: 10,
  border: { pt: 0.5, color: C.gray20 },
  colW: [1.6, 2.2, 2.4, 2.4],
  autoPage: false,
  rowH: [0.38, 0.35, 0.35, 0.35],  // per-row height control
});
```

See `references/pptxgenjs-ibm.md` for complete table patterns.

## Layout Recipes

These are starting points — adjust dimensions based on content volume. All values in inches.

### 2×2 Card Grid (4 items)
- Cards: w=4.1, h=1.35, gapX=0.4, gapY=0.2
- Start: x=0.7, y=1.4

### 3-Column Pillars (3 items)
- Pillars: w=2.75, h=2.7-3.0, gap=0.45
- Start: x=0.7, y=1.5-1.65
- Note: Bottom of 3.0-tall pillars reaches y≈4.65 — push callout bar to y≈4.75

### 2-Column Split (list + stats)
- Left column: x=0.7, w=4.5
- Right column: x=5.6, w=4.0

### Metric Callout Cards (3 items)
- Cards: w=2.75, h=3.4, gap=0.45
- Start: x=0.7, y=1.45
- Inset metric box: x+0.15, y+1.75, w-0.3, h=1.4

### Timeline Phase Cards (3 items)
- Cards: w=2.75, h=2.7, gap=0.45
- Start: x=0.7, y=1.5
- Number circle: centered, 0.48×0.48 `pres.shapes.OVAL`
- Arrow connectors between cards (FaArrowRight icon)

### Stacked Horizontal Cards (4 items)
- Cards: w=4.5, h=0.68, gap=0.10
- Start: x=0.7, y=1.45
- Icon: 0.38×0.38 at x+0.15
- Title at x+0.65, desc below

### 4-Column Compounding Value Cards (Strategic Impact)
- **Header**: section label y=px(40) h=px(20), title y=px(64) h=px(170) for wrapping titles (px(90) if single-line), subtitle derived as titleY+titleH+px(16) — always derive positions, never hardcode
- Cards: w≈2.06" (px(396)), h≈2.81" (px(540)), gap calculated from x-offsets
- Use `ROUNDED_RECTANGLE` with `rectRadius: 0.08` and per-card tinted `bgColor`
- Each card: gradient accent bar (borderRadius=16), step number ("01"), gradient hero title (renderGradientTitle), subtitle, divider LINE, 4 items, divider LINE, outcome text
- Arrow connectors (FaArrowRight) between cards
- Start: x=px(102), y=px(250) — use `px = v / 192` helper
- Custom colors per card: `bgColor`, `divColor`, `outcomeColor`, `numColor`, `arrowColor`

### 4-Column Prerequisite / Checklist Cards
- Cards: w=2.0, h=2.95, gap=0.27
- Start: x=0.7, y=1.5
- Last card (or flagged card): tinted bg + colored border + REQUIRED badge
- Badge: ROUNDED_RECTANGLE filled with accent, white "REQUIRED" text, 8pt, charSpacing:1.5
- Mandatory card text uses `gray100` instead of `gray70` for emphasis

### Comparison / Before-After
- Two columns: left x=0.7 w=4.1, right x=5.2 w=4.1
- Left: red-tinted card (`FFF0F0`, `C.red60` top accent), "BEFORE" label
- Right: green-tinted card (`F0FFF4`, `C.green60` top accent), "AFTER" label
- Each column has bullet items below the label

### Quote / Testimonial
- Large SVG quotation mark (rendered via `renderQuoteMark()`, purple60 gradient)
- Quote text: 16-18pt Arial italic, `C.gray100`
- Attribution: em-dash prefix, bold name + regular title in `C.gray70`
- Vertical gradient accent bar on left edge
- Optional: metric stats on right side (big numbers + uppercase labels)

### KPI Dashboard (3 panels)
- Panels: w=2.75, h=3.0, gap=0.45
- Start: x=0.7, y=1.5
- Each panel: card background, progress ring (SVG) centered, metric label below ring, sparkline at bottom
- Composes card pattern + SVG data viz helpers (`renderProgressRing`, `renderSparkline`)

### Icon Grid / Feature Matrix
- Grid: 4×2 or 3×3 with consistent spacing
- Each cell: OVAL colored circle (0.6×0.6) + icon via `iconToBase64Png` + label below
- 4 accent colors cycling per column
- Cell size: ~2.0×1.3, gap: 0.2

### Comparison Matrix
- N columns × M rows grid
- Column headers: gradient accent bar on top, bold title, `C.gray10` bg
- Status icons per cell: FaCheckCircle (`C.green60`), FaExclamationTriangle (`C.yellow50`), FaTimesCircle (`C.red60`)
- Row labels in first column, bold, `C.gray100`

### Process Flow with Human Gate
- 5-step horizontal cards: w=1.6, h=1.8, gap=0.15
- Start: x=0.7, y=1.8
- Step number: OVAL circle (0.36×0.36) above card
- FaArrowRight connectors between cards
- Human gate card: dashed border (`dashType: "dash"`), `C.red60` line color, `FFF0F0` tinted bg, "HUMAN GATE" badge (ROUNDED_RECTANGLE filled red60, white text)

### Donut + Cards + Callout (3-Zone)

SVG donut chart with legend on the left, stacked info cards in the center, and a highlighted callout card on the right. Great for agent architecture, resource distribution, or team composition slides.

- Left zone: SVG donut (1.3×1.3) at x=0.7 y=1.6, legend items below (colored RECTANGLE 0.18×0.18 + label)
- Center zone: 4 stacked cards w=3.4, h=0.72, gap=0.12, starting x=2.5
  - Each card: vertical gradient left accent bar (0.08w), icon, title, description
- Right zone: ROUNDED_RECTANGLE callout card w=3.5 at x=6.2
  - Tinted bg (e.g., F5F0FF), gradient top accent bar, section label, title, bullet items
- Use `renderDonutChart` for the donut, `renderVerticalGradientBar` for card accents

### Document Structure + Principles (Split Visual)

Left side shows a visual representation of a structured document (numbered color-coded sections), right side shows principle/philosophy cards.

- Left: ROUNDED_RECTANGLE container w=4.2 h=3.2 with gray10 bg + gray20 border
  - File icon + filename title at top
  - 7 numbered section rows: OVAL dot (0.2×0.2, filled accent color) + number inside + section title text
  - Rows at 0.36" vertical spacing
- Right: 3 stacked principle cards w=4.4 h=0.95 gap=1.08
  - Each card: vertical gradient left accent, icon, bold title, description
  - Uses `renderVerticalGradientBar` for left bars

### Two-Column Feature Cards + Banner

Two wide cards side by side with a full-width banner bar below. Good for integration/tooling slides.

- Cards: ROUNDED_RECTANGLE w=4.3 h=2.2 at x=0.7 and x=5.4
  - Tinted bg per card, gradient top accent bar, icon + title inline, bullet items below
- Banner: ROUNDED_RECTANGLE w=8.6 h=1.1 at y=4.0
  - Gradient top bar spanning full width, section label, description text
  - Optional: icon row on the right side (6 icons at 0.38" spacing)

### Quote Closing + Stats

Closing slide combining a vertical gradient bar, SVG quote mark, italic quote text, attribution, and summary stats.

- Top: accent strip RECTANGLE h=0.06 full width
- Left: vertical gradient bar (0.08w, 2.4h) via `renderVerticalGradientBar`
- Quote mark: `renderQuoteMark` SVG (0.625×0.625) offset right of bar
- Quote text: 17pt Arial italic gray100, w=6.0
- Attribution: rich text array with bold name + regular title
- Stats row: 4 items at y=3.1, each with `renderProgressRing` (0.7×0.7) + uppercase label below
- Bottom bar: gray10 RECTANGLE h=0.5

### Programmatic Title with Stats Row

Full programmatic title slide (no HTML capture) with accent strip and key stats.

- Top accent: RECTANGLE h=0.06 full width, filled with accent color (e.g., blue60)
- Title: 40pt Arial Black gray100 at y=1.2
- Subtitle: 18pt Arial gray70 at y=2.25
- Gradient accent strip: `renderGradientBar` at y=2.9, w=8.6, h=0.08 — full width below subtitle
- Stats row: 4 items evenly spaced (2.15" apart), starting x=0.7 y=3.3
  - Big number: 28pt Arial Black in accent color
  - Label: 9pt Arial gray50, bold, charSpacing:2
- Bottom bar: gray10 RECTANGLE h=0.5 at y=5.125

### SVG Process Flow (Alternative to Shape-Based)

Renders an entire horizontal process flow as a **single SVG image** via `renderProcessFlowSVG`. More compact than building individual pptxgenjs shapes. Supports human gate styling (dashed red boxes), sub-labels, and XML-safe text.

- SVG flow: w=9.0, h=0.83 at x=0.5 y=1.55
- Below the flow: 4 detail cards in a row (ROUNDED_RECTANGLE w≈2.06, h≈2.1, gap=0.32)
  - Each card: tinted bg, gradient top bar, step number, icon (top-right), title, description
  - FaArrowRight connectors between cards
- **Use SVG flows to visually break up the slide** — a colored flow diagram above detail cards creates visual rhythm and helps audiences follow the narrative

## SVG Visual Strategy

**Use SVG diagrams liberally** to create visual appeal and break up slide flow. SVG-rendered elements (process flows, donut charts, progress rings, sparklines) serve dual purpose:

1. **Visual anchors** — they draw the eye and create focal points on otherwise text-heavy slides
2. **Flow breakers** — placing an SVG diagram between a header and detail cards creates visual rhythm and prevents "wall of cards" monotony

**Recommended patterns for visual variety:**
- **Flow → Cards**: SVG process flow at top, detail cards below (e.g., SDD cycle slide)
- **Donut → Grid**: SVG donut chart left, card grid right (e.g., agent taxonomy slide)
- **Ring → Table**: Progress rings in KPI panels above, data table below
- **Quote → Stats**: SVG quote mark + vertical bar left, progress ring stats right

Every 2-3 slides should include at least one SVG visualization element. This prevents the deck from feeling like a series of identical card layouts.

## Gradient Fills — NOT SUPPORTED in pptxgenjs v4

pptxgenjs v4 `fill.type` only supports `'solid'` or `'none'`. Using `type: "gradient"` with `color1`/`color2` silently produces **corrupted OOXML** — the PPTX will not open in PowerPoint or Keynote. There is no `GradientFill` interface in the v4 type definitions.

### Workaround: SVG → PNG via sharp

Render gradient elements as SVG, convert to PNG, and embed as images. This gives visual gradients while keeping surrounding text/shapes natively editable.

```javascript
import sharp from "sharp";

// Gradient accent bar (e.g., top of a card)
async function renderGradientBar(colors, width = 396, height = 8, borderRadius = 16) {
  const gid = "g" + Math.random().toString(36).slice(2, 8);
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}" viewBox="0 0 ${width} ${height}">
    <defs>
      <linearGradient id="${gid}" x1="0" y1="0" x2="1" y2="0">
        <stop offset="0%" stop-color="${colors[0]}"/>
        <stop offset="50%" stop-color="${colors[1]}"/>
        <stop offset="100%" stop-color="${colors[2]}"/>
      </linearGradient>
    </defs>
    <rect width="${width}" height="${borderRadius > 0 ? borderRadius * 2 : height}" rx="${borderRadius}" fill="url(#${gid})"/>
  </svg>`;
  const buf = await sharp(Buffer.from(svg)).png().toBuffer();
  return "image/png;base64," + buf.toString("base64");
}

// Vertical gradient bar (e.g., left accent on cards)
async function renderVerticalGradientBar(colors, width = 8, height = 260) {
  const gid = "vb" + Math.random().toString(36).slice(2, 8);
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}" viewBox="0 0 ${width} ${height}">
    <defs><linearGradient id="${gid}" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="${colors[0]}"/>
      <stop offset="50%" stop-color="${colors[1]}"/>
      <stop offset="100%" stop-color="${colors[2]}"/>
    </linearGradient></defs>
    <rect width="${width}" height="${height}" fill="url(#${gid})"/>
  </svg>`;
  const buf = await sharp(Buffer.from(svg)).png().toBuffer();
  return "image/png;base64," + buf.toString("base64");
}

// Gradient text (e.g., hero titles)
async function renderGradientTitle(text, stops, width = 700, height = 120) {
  const gid = "g" + Math.random().toString(36).slice(2, 8);
  const stopsSvg = stops.map(s => `<stop offset="${s.offset}%" stop-color="${s.color}"/>`).join("");
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}" viewBox="0 0 ${width} ${height}">
    <defs><linearGradient id="${gid}" x1="0" y1="0" x2="1" y2="0.3">${stopsSvg}</linearGradient></defs>
    <text x="0" y="${height * 0.75}" font-size="${height * 0.82}" font-weight="800"
      font-family="Arial,Helvetica,sans-serif" fill="url(#${gid})">${text}</text>
  </svg>`;
  const buf = await sharp(Buffer.from(svg)).png().toBuffer();
  return "image/png;base64," + buf.toString("base64");
}

// Usage — horizontal top accent bar (h: 0.08 minimum for projection visibility)
const barImg = await renderGradientBar(["#627EEF", "#8A3FFC", "#D946EF"], 400, 8, 0);
slide.addImage({ data: barImg, x: cx, y: cy, w: cardW, h: 0.08 });

// Usage — vertical left accent bar (w: 0.08 minimum for projection visibility)
const vBarImg = await renderVerticalGradientBar(["#627EEF", "#8A3FFC", "#D946EF"], 8, 260);
slide.addImage({ data: vBarImg, x: cx, y: cy, w: 0.08, h: cardH });

// Usage — gradient hero title text
const titleImg = await renderGradientTitle("Establish", [
  { offset: 0, color: "#627EEF" },
  { offset: 50, color: "#8A3FFC" },
  { offset: 100, color: "#D946EF" },
], 700, 120);
slide.addImage({ data: titleImg, x: cx + 0.15, y: cy + 0.4, w: 1.8, h: 0.31 });
```

**Key details**:
- When `borderRadius > 0`, the SVG `<rect>` height must be `borderRadius * 2` (taller than the bar) so rounded corners clip correctly within the viewBox. When `borderRadius = 0`, use the actual `height` value — otherwise `borderRadius * 2 = 0` produces an invisible zero-height rect.
- Minimum visible size when projected: **0.08"** for both horizontal bar height and vertical bar width. Values of 0.05-0.06" are nearly invisible on projectors.

### rectRadius

`rectRadius` on `ROUNDED_RECTANGLE` is a **fraction from 0.0 to 1.0** (not absolute inches). Values above 1.0 produce invalid OOXML.

## Critical Rules

1. **No "#" prefix on pptxgenjs colors** — see Color Rules table above.
2. **Always `await` async functions** — `iconToBase64Png()` returns a Promise. Missing `await` silently breaks images.
3. **Never reuse shadow/option objects** — always use `() => ({...})` factory functions. pptxgenjs **mutates** shadow objects in place during XML generation, converting values to EMU units. On the second use, these already-converted values get converted again, producing values that overflow INT32 and corrupt the PPTX. Never write shadow objects inline.
4. **No gradient fills** — `fill.type` only supports `'solid'` or `'none'` in v4. Use the SVG → PNG workaround above for gradients.
5. **Set `slide.background = { color: C.white }`** on every content slide — don't rely on defaults.
6. **Coordinates are in inches** — LAYOUT_16x9 is 10" wide × 5.625" tall.
7. **Content padding** — start content at y≈1.4 (0.8-1.0" below header). Too tight looks cramped.
8. **Text overflow** — respect the max character counts in the Typography table. Reduce fontSize or increase dimensions if wrapping occurs. **Bounding box overlap check**: for every text element, verify that `y + h` does not exceed the `y` of the next element below it. Leave at least 0.08" clearance. A common mistake is using a height that fits the text tightly but leaves no visual gap — at fontSize 22 "Arial Black", each line including leading is ~0.37", so a single-line title needs at minimum h=0.40" and a two-line title needs h=0.74". Use `px(90)` (~0.47") as a safe single-line default or `px(170)` (~0.89") for wrapping titles, and always derive the subtitle `y` from `title.y + title.h + px(16)` so it shifts automatically with generous clearance.
9. **Footer clearance** — bottom callout bars at y≈4.5-4.75. Taller content layouts (3.0" pillars) push the callout lower.
10. **Working directory** — run build scripts from the repo root. The capture script (`scripts/capture-title.mjs`) resolves all asset paths automatically — no workspace setup needed for title/divider slides.
11. **Title slides are HTML captures** — title slide text lives in the HTML source file, not in `pres.title`. Changing `pres.title` in the build script does NOT update the rendered title slide. To update title text: edit the HTML → recapture via Chrome headless → rebuild PPTX.
12. **Capture from the directory containing assets** — HTML title slides use relative paths to `media/` and `fonts/` folders. Always `cd` into the directory where `media/` and `fonts/` exist, then run Chrome headless from there. Copying the HTML elsewhere without its assets produces a blank white background. **Verify PNG file size after every capture** — the HC CY26 Kit background layers (gradient base, left glow, right glow, arc lines) produce a 3840×2160 PNG around **2–3MB**. If the file is under 2MB, the backgrounds rendered partially or at reduced quality — recapture. Under 200KB means assets failed to load entirely. Compare against a known-good reference if available (e.g., extract `image-1-1.png` from a working PPTX via `unzip` and check its size).
13. **Output filename matches branding** — when rebranding a deck, also update the `fileName` in `pres.writeFile()` to match the new name.
14. **Always rebuild after text changes** — after any edit to the build script, run `node build-<deck>.mjs` to regenerate. Never leave stale PPTX builds.
15. **Case-matching when rebranding** — when replacing branded terms across a deck, match the case of each occurrence: `UPPERCASE` section labels stay uppercase, `Title Case` stays title case, `lowercase` body text stays lowercase.
16. **Visual QA via subagent is mandatory** — never deliver a deck without at least 2 subagent visual review cycles. Never inspect slide images yourself — always spawn a subagent. You wrote the code and will see what you intended, not what rendered. See the QA Pipeline section for the full process.
17. **SVG visuals for variety** — every 2-3 slides should include at least one SVG visualization (process flow, donut chart, progress ring, sparkline). SVG diagrams break up card-heavy layouts and create visual focal points. Use `renderProcessFlowSVG` for workflows, `renderDonutChart` for composition breakdowns, `renderProgressRing` for KPIs, and `renderSparkline` for trends.

## Tint Color Guide

For callout bars and tinted backgrounds — match to the slide's section accent:

| Accent | Tint Background | Border |
|--------|----------------|--------|
| Blue | `"F0F5FF"` | `C.blue60` |
| Green | `"F0FFF4"` | `C.green60` |
| Yellow | `"FFF8F0"` | `C.yellow50` |
| Red | `"FFF0F0"` | `C.red60` |
| Purple | `"F5F0FF"` | `C.purple60` |
| Teal | `"F0FFFC"` | `C.teal60` |

## QA Pipeline — Visual Review via Subagent (MANDATORY)

**You must never deliver a deck without completing this pipeline. No exceptions.**

Your first render is almost never pixel-perfect. Text wraps differently than you expect, cards overflow by a fraction of an inch, callout bars collide with content above them. These issues are invisible in code but obvious in a screenshot. You wrote the code, so you will see what you intended — not what actually rendered. That is why every visual inspection must be done by a subagent, never by you directly.

**Why a subagent, not you?** Confirmation bias. You just wrote the layout code and will unconsciously assume your intent matches the output. A subagent starts with zero context about the code — it only sees the rendered image. This asymmetry is the entire point: subagents catch spatial issues (overlap, alignment, clipping) that the code author consistently misses. In testing, self-review catches ~30% of visual bugs while subagent review catches ~85%.

### Step 1: Build and Convert to Images

After running the build script, convert the PPTX to slide images:

```bash
node build-<deck-name>.mjs
soffice --headless --convert-to pdf output.pptx
pdftoppm -jpeg -r 150 output.pdf slide
```

This produces `slide-1.jpg`, `slide-2.jpg`, etc. If `soffice` is not available, use any other PPTX-to-image conversion method.

### Step 2: Spawn Subagent(s) for Visual Inspection

You must spawn at least one subagent to review the slide images. Do not review the images yourself — delegate all visual inspection to subagents.

For decks with 6+ slides, spawn **multiple subagents in parallel** (e.g., slides 1-3, 4-6, 7-9) to speed up inspection. Each subagent gets a subset of slide images.

Use this prompt template for each QA subagent:

```
Visually inspect these slides. Assume there are issues — your job is to find them.

Check every slide for:
- Overlapping elements (text bleeding through shapes, lines crossing words)
- Text overflow or cut off at card/box boundaries (truncated words, clipped lines)
- Decorative lines or accent bars positioned for single-line text but title wrapped to two lines
- Callout bars or footers colliding with content above them
- Elements too close together (< 0.3" gaps) or cards nearly touching
- Uneven gaps (large empty area in one place, cramped in another)
- Insufficient margin from slide edges (< 0.5")
- Columns or similar elements not aligned consistently
- Low-contrast text (light gray on white, dark on dark)
- Low-contrast icons (icons blending into background without a contrasting circle)
- Text boxes too narrow causing excessive line wrapping
- Bullet text extending beyond its card or column boundary
- Any element that looks visually "off" even if you can't classify it

For each slide, list ALL issues found with specific locations (e.g., "slide 2, top-right card: title text clips below the card boundary by ~10px"). If a slide looks clean, say so — but look hard first.

Read and analyze these images:
1. /path/to/slide-1.jpg (Expected: [brief description of what this slide should show])
2. /path/to/slide-2.jpg (Expected: [brief description])
...
```

### Step 3: Fix Issues and Re-verify via New Subagent

For each issue the subagent found:
1. Fix the code (adjust dimensions, reduce text, increase card height, move elements)
2. Rebuild the PPTX and re-convert to images:
   ```bash
   node build-<deck-name>.mjs
   soffice --headless --convert-to pdf output.pptx
   pdftoppm -jpeg -r 150 output.pdf slide
   ```
3. **Spawn a new subagent** to inspect the fixed slides. Do not inspect them yourself — you made the fix and will assume it worked. A fresh subagent catches regressions that fixes introduce (e.g., a taller card now pushes content into the callout bar, or wider text breaks adjacent column alignment).

Keep cycling (fix → rebuild → spawn new subagent) until a subagent review finds zero issues.

### Step 4: Confirmation Cycle (Required)

After the first clean subagent pass, do one final confirmation cycle:
1. Rebuild the PPTX one more time
2. Re-convert to images
3. Spawn a final subagent to confirm nothing regressed

This catches subtle regressions from the last round of fixes.

### Minimum Requirement

**You must complete at least 2 full subagent review cycles before delivering the deck** — one to catch initial issues, and one to confirm fixes didn't introduce regressions. Each cycle must use a subagent (never self-review). If you find yourself wanting to skip this step because "the code looks right" — that is exactly when bugs hide.

### Common Fixes

| Problem | Fix |
|---------|-----|
| Text clipped at card bottom | Increase card height (`h`) by 0.2-0.3" or reduce bullet count |
| Callout bar overlaps content | Move callout bar down (`y += 0.2`) or shrink content above |
| Text wraps unexpectedly | Reduce `fontSize` by 1-2pt, or increase text box `w` |
| Cards not aligned | Use consistent `y` values; calculate from shared starting point |
| Too tight between elements | Add 0.15-0.2" to gaps; content breathing room matters |

### What "Done" Looks Like

A deck is ready to deliver only when:
- [ ] Build script runs without errors
- [ ] At least 2 subagent visual reviews completed (never self-reviewed)
- [ ] Final subagent review found zero issues
- [ ] No pending fixes that haven't been re-verified by a subagent
