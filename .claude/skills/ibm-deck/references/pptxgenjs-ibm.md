# pptxgenjs IBM Carbon Patterns

Complete code examples for building IBM Carbon-styled PPTX slides with pptxgenjs. These patterns are extracted from production decks and handle common pitfalls.

## Table of Contents

- [Full Build Script Structure](#full-build-script-structure)
- [Shadow Factories](#shadow-factories)
- [Card with Icon + Accent Bar](#card-with-icon--accent-bar)
- [3-Column Pillar Layout](#3-column-pillar-layout)
- [Metric Callout Cards](#metric-callout-cards)
- [Timeline / Phase Cards](#timeline--phase-cards)
- [2-Column Outcome + Stats Layout](#2-column-outcome--stats-layout)
- [Icon Rendering Pipeline](#icon-rendering-pipeline)
- [Rich Text (Bold + Regular Mix)](#rich-text-bold--regular-mix)
- [Number Circle Badge](#number-circle-badge)
- [Callout Bar with Icon](#callout-bar-with-icon)
- [Tinted Background Boxes](#tinted-background-boxes)

---

## Full Build Script Structure

```javascript
import pptxgen from "pptxgenjs";
import React from "react";
import ReactDOMServer from "react-dom/server";
import sharp from "sharp";
import { FaShieldAlt, FaRocket, FaCogs, FaUsers } from "react-icons/fa";

// --- Icon helper ---
function renderIconSvg(IconComponent, color = "#000000", size = 256) {
  return ReactDOMServer.renderToStaticMarkup(
    React.createElement(IconComponent, { color, size: String(size) })
  );
}

async function iconToBase64Png(IconComponent, color, size = 256) {
  const svg = renderIconSvg(IconComponent, color, size);
  const pngBuffer = await sharp(Buffer.from(svg)).png().toBuffer();
  return "image/png;base64," + pngBuffer.toString("base64");
}

// --- IBM Carbon Design Tokens (NO "#" prefix!) ---
const C = {
  white: "FFFFFF",
  gray10: "F4F4F4",
  gray20: "E0E0E0",
  gray30: "C6C6C6",
  gray50: "8D8D8D",
  gray70: "525252",
  gray100: "161616",
  blue60: "0F62FE",
  purple60: "8A3FFC",
  teal60: "009D9A",
  magenta60: "D02670",
  green60: "198038",
  red60: "DA1E28",
  yellow50: "B28600",
  yellow40: "D2A106",
};

// --- Shadow factories (ALWAYS fresh objects) ---
const cardShadow = () => ({
  type: "outer", color: "000000", blur: 8,
  offset: 2, angle: 135, opacity: 0.08,
});

const footerBarShadow = () => ({
  type: "outer", color: "000000", blur: 4,
  offset: 1, angle: 270, opacity: 0.06,
});

// --- Pixel-to-inch conversion (1920px = 10") ---
const px = (v) => v / 192;

// --- XML entity escaping for SVG text ---
function escXml(s) { return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); }

// --- Reusable slide header ---
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

async function buildPresentation() {
  const pres = new pptxgen();
  pres.layout = "LAYOUT_16x9";  // 10" × 5.625"
  pres.author = "Author";
  pres.title = "Deck Title";

  // ... slides ...

  await pres.writeFile({ fileName: "output.pptx" });
}

buildPresentation().catch(console.error);
```

---

## Shadow Factories

pptxgenjs mutates option objects after they're passed to `addShape()`. This means if you define a shadow object once and reuse it, the second shape gets corrupted values. Always return fresh objects from factory functions.

```javascript
// CORRECT — factory returns a new object each time
const cardShadow = () => ({
  type: "outer", color: "000000", blur: 8,
  offset: 2, angle: 135, opacity: 0.08,
});

// WRONG — same object reused, will be mutated
const shadow = { type: "outer", color: "000000", blur: 8, offset: 2, angle: 135, opacity: 0.08 };
s.addShape(pres.shapes.RECTANGLE, { shadow }); // mutates shadow
s.addShape(pres.shapes.RECTANGLE, { shadow }); // gets corrupted values
```

---

## Card with Icon + Accent Bar

A card with a colored left accent bar, icon, title, and description. Used for challenge/risk cards, outcome lists, etc.

```javascript
const cardW = 4.1, cardH = 1.35;
const cx = 0.7, cy = 1.4;
const accentColor = C.red60;

// Card background
slide.addShape(pres.shapes.RECTANGLE, {
  x: cx, y: cy, w: cardW, h: cardH,
  fill: { color: C.gray10 },
  shadow: cardShadow(),
});

// Left accent bar (0.06" wide)
slide.addShape(pres.shapes.RECTANGLE, {
  x: cx, y: cy, w: 0.06, h: cardH,
  fill: { color: accentColor },
});

// Icon (rendered from react-icons)
const iconData = await iconToBase64Png(FaExclamationTriangle, "#" + C.red60, 256);
slide.addImage({
  data: iconData,
  x: cx + 0.2, y: cy + 0.2, w: 0.38, h: 0.38,
});

// Card title
slide.addText("Security Risks", {
  x: cx + 0.7, y: cy + 0.15, w: cardW - 0.9, h: 0.4,
  fontSize: 15, fontFace: "Arial",
  color: C.gray100, bold: true, valign: "middle", margin: 0,
});

// Card description
slide.addText("Description text here", {
  x: cx + 0.7, y: cy + 0.6, w: cardW - 0.9, h: 0.8,
  fontSize: 12, fontFace: "Arial",
  color: C.gray70, valign: "top", margin: 0,
});
```

### 2×2 Grid Layout

```javascript
const cardW = 4.1, cardH = 1.35;
const cardGapX = 0.4, cardGapY = 0.2;
const gridStartX = 0.7, gridStartY = 1.4;

for (let i = 0; i < 4; i++) {
  const col = i % 2;
  const row = Math.floor(i / 2);
  const cx = gridStartX + col * (cardW + cardGapX);
  const cy = gridStartY + row * (cardH + cardGapY);
  // ... add card elements at (cx, cy) ...
}
```

---

## 3-Column Pillar Layout

Three tall cards side by side, each with a top accent bar, icon, title, and bullet list. Good for value propositions, feature comparisons, timeline phases.

```javascript
const pillarW = 2.75, pillarH = 2.95;
const pillarGap = 0.45;
const startX = 0.7, startY = 1.65;

for (let i = 0; i < 3; i++) {
  const px = startX + i * (pillarW + pillarGap);

  // Card background
  slide.addShape(pres.shapes.RECTANGLE, {
    x: px, y: startY, w: pillarW, h: pillarH,
    fill: { color: C.gray10 }, shadow: cardShadow(),
  });

  // Top accent bar
  slide.addShape(pres.shapes.RECTANGLE, {
    x: px, y: startY, w: pillarW, h: 0.05,
    fill: { color: accentColor },
  });

  // Icon
  const iconData = await iconToBase64Png(icon, "#" + accentColor, 256);
  slide.addImage({
    data: iconData,
    x: px + 0.25, y: startY + 0.25, w: 0.42, h: 0.42,
  });

  // Pillar title
  slide.addText(title, {
    x: px + 0.25, y: startY + 0.78, w: pillarW - 0.5, h: 0.35,
    fontSize: 14, fontFace: "Arial",
    color: C.gray100, bold: true, margin: 0,
  });

  // Bullet items
  const bullets = items.map((item, idx) => ({
    text: item,
    options: {
      bullet: { code: "2022" },
      breakLine: idx < items.length - 1,
      fontSize: 11, color: C.gray70,
      paraSpaceAfter: 6,
    },
  }));

  slide.addText(bullets, {
    x: px + 0.25, y: startY + 1.2, w: pillarW - 0.5, h: 1.8,
    fontFace: "Arial", valign: "top", margin: 0,
  });
}
```

---

## Metric Callout Cards

Cards with a big metric number, label, and optional status badge. Arranged in 3 columns.

```javascript
const ucW = 2.75, ucH = 3.4;
const ucGap = 0.45;
const startX = 0.7, startY = 1.45;

for (let i = 0; i < 3; i++) {
  const ux = startX + i * (ucW + ucGap);

  // Card background + top accent bar (same as pillar)
  slide.addShape(pres.shapes.RECTANGLE, {
    x: ux, y: startY, w: ucW, h: ucH,
    fill: { color: C.gray10 }, shadow: cardShadow(),
  });

  // Persona label (small uppercase)
  slide.addText("APPLICATION TEAM", {
    x: ux + 0.2, y: startY + 0.2, w: ucW - 0.4, h: 0.25,
    fontSize: 9, fontFace: "Arial",
    color: accentColor, bold: true, charSpacing: 2, margin: 0,
  });

  // Title
  slide.addText("Consumer Workflow", {
    x: ux + 0.2, y: startY + 0.5, w: ucW - 0.4, h: 0.35,
    fontSize: 16, fontFace: "Arial",
    color: C.gray100, bold: true, margin: 0,
  });

  // Description
  slide.addText("Description", {
    x: ux + 0.2, y: startY + 0.9, w: ucW - 0.4, h: 0.75,
    fontSize: 11, fontFace: "Arial",
    color: C.gray70, valign: "top", margin: 0,
  });

  // Metric box (inset white box with border)
  slide.addShape(pres.shapes.RECTANGLE, {
    x: ux + 0.15, y: startY + 1.75, w: ucW - 0.3, h: 1.4,
    fill: { color: C.white },
    line: { color: C.gray20, width: 0.5 },
  });

  // Metric label (centered uppercase)
  slide.addText("COMPOSITION TIME", {
    x: ux + 0.2, y: startY + 1.82, w: ucW - 0.4, h: 0.2,
    fontSize: 8, fontFace: "Arial",
    color: C.gray50, bold: true, charSpacing: 2, align: "center", margin: 0,
  });

  // Big metric
  slide.addText("Hours → Minutes", {
    x: ux + 0.2, y: startY + 2.05, w: ucW - 0.4, h: 0.45,
    fontSize: 24, fontFace: "Arial Black",
    color: accentColor, bold: true, align: "center", margin: 0,
  });

  // Status badge (icon + text)
  const checkIcon = await iconToBase64Png(FaCheckCircle, "#" + C.green60, 256);
  slide.addImage({
    data: checkIcon,
    x: ux + ucW/2 - 0.48, y: startY + 2.7, w: 0.22, h: 0.22,
  });
  slide.addText("Validated", {
    x: ux + ucW/2 - 0.2, y: startY + 2.68, w: 1, h: 0.28,
    fontSize: 12, fontFace: "Arial",
    color: C.green60, bold: true, valign: "middle", margin: 0,
  });
}
```

---

## Timeline / Phase Cards

Three phase cards with numbered circles, used for engagement timelines.

```javascript
const tlW = 2.75, tlH = 2.7;
const tlGap = 0.45;
const startX = 0.7, startY = 1.5;

for (let i = 0; i < 3; i++) {
  const tx = startX + i * (tlW + tlGap);

  // Card bg + top accent (standard pattern)
  // ...

  // Number circle (centered)
  slide.addShape(pres.shapes.OVAL, {
    x: tx + tlW/2 - 0.24, y: startY + 0.2, w: 0.48, h: 0.48,
    fill: { color: accentColor },
  });

  slide.addText(String(i + 1), {
    x: tx + tlW/2 - 0.24, y: startY + 0.2, w: 0.48, h: 0.48,
    fontSize: 20, fontFace: "Arial",
    color: C.white, bold: true, align: "center", valign: "middle", margin: 0,
  });

  // Phase title (centered)
  slide.addText("Assess & Establish", {
    x: tx + 0.2, y: startY + 0.8, w: tlW - 0.4, h: 0.35,
    fontSize: 15, fontFace: "Arial",
    color: C.gray100, bold: true, align: "center", margin: 0,
  });

  // Month label (centered, small uppercase)
  slide.addText("MONTH 1", {
    x: tx + 0.2, y: startY + 1.1, w: tlW - 0.4, h: 0.25,
    fontSize: 9, fontFace: "Arial",
    color: C.gray50, bold: true, align: "center", charSpacing: 2, margin: 0,
  });

  // Bullets at y = startY + 1.45
  // ...

  // Arrow connector between cards (except last)
  if (i < 2) {
    const arrowIcon = await iconToBase64Png(FaArrowRight, "#" + accentColor, 256);
    slide.addImage({
      data: arrowIcon,
      x: tx + tlW + tlGap/2 - 0.14, y: startY + tlH/2 - 0.14,
      w: 0.28, h: 0.28,
    });
  }
}
```

---

## 2-Column Outcome + Stats Layout

Left column: stacked outcome cards (icon + text). Right column: big stat callouts.

```javascript
// Left column
const ocCardW = 4.5, ocCardH = 0.68;
const ocGap = 0.1, ocStartX = 0.7, ocStartY = 1.45;

for (let i = 0; i < 4; i++) {
  const oy = ocStartY + i * (ocCardH + ocGap);

  slide.addShape(pres.shapes.RECTANGLE, {
    x: ocStartX, y: oy, w: ocCardW, h: ocCardH,
    fill: { color: C.gray10 }, shadow: cardShadow(),
  });

  // Icon at x+0.15, y+0.12, 0.38×0.38
  // Title at x+0.65, y+0.02, fontSize 12 bold
  // Desc at x+0.65, y+0.32, fontSize 10 gray70
}

// Right column
const statStartX = 5.6, statW = 4.0;
const statH = 0.68, statGap = 0.1, statStartY = 1.45;

for (let i = 0; i < 4; i++) {
  const sy = statStartY + i * (statH + statGap);

  // Card bg with left accent bar
  slide.addShape(pres.shapes.RECTANGLE, {
    x: statStartX, y: sy, w: statW, h: statH,
    fill: { color: C.gray10 }, shadow: cardShadow(),
  });

  slide.addShape(pres.shapes.RECTANGLE, {
    x: statStartX, y: sy, w: 0.06, h: statH,
    fill: { color: statColor },
  });

  // Big number (left)
  slide.addText("10x", {
    x: statStartX + 0.2, y: sy, w: 1.1, h: statH,
    fontSize: 24, fontFace: "Arial Black",
    color: statColor, bold: true, valign: "middle", margin: 0,
  });

  // Label (right of number)
  slide.addText("Faster module delivery", {
    x: statStartX + 1.35, y: sy, w: statW - 1.55, h: statH,
    fontSize: 13, fontFace: "Arial",
    color: C.gray100, bold: true, valign: "middle", margin: 0,
  });
}
```

---

## Icon Rendering Pipeline

React Icons are rendered to SVG markup, then converted to PNG via sharp. The resulting base64 string is embedded in the PPTX.

```javascript
import React from "react";
import ReactDOMServer from "react-dom/server";
import sharp from "sharp";

function renderIconSvg(IconComponent, color = "#000000", size = 256) {
  return ReactDOMServer.renderToStaticMarkup(
    React.createElement(IconComponent, { color, size: String(size) })
  );
}

async function iconToBase64Png(IconComponent, color, size = 256) {
  const svg = renderIconSvg(IconComponent, color, size);
  const pngBuffer = await sharp(Buffer.from(svg)).png().toBuffer();
  return "image/png;base64," + pngBuffer.toString("base64");
}
```

Note: The `color` parameter for icon rendering DOES use `"#"` prefix (`"#" + C.green60`), unlike pptxgenjs shape/text colors which never use `"#"`.

---

## Rich Text (Bold + Regular Mix)

Use an array of text objects with per-segment styling:

```javascript
slide.addText([
  { text: "Bold prefix: ", options: { bold: true, color: C.gray100 } },
  { text: "Regular description.", options: { color: C.gray70 } },
], {
  x: 1.4, y: 4.5, w: 7.7, h: 0.55,
  fontSize: 11, fontFace: "Arial", valign: "middle", margin: 0,
});
```

---

## Number Circle Badge

Colored circle with a number inside, used for timeline phases:

```javascript
slide.addShape(pres.shapes.OVAL, {
  x: tx + tlW/2 - 0.24, y: startY + 0.2,
  w: 0.48, h: 0.48,
  fill: { color: accentColor },
});

slide.addText("1", {
  x: tx + tlW/2 - 0.24, y: startY + 0.2,
  w: 0.48, h: 0.48,
  fontSize: 20, fontFace: "Arial",
  color: C.white, bold: true,
  align: "center", valign: "middle", margin: 0,
});
```

---

## Callout Bar with Icon

Bottom-of-slide callout bar with tinted background, border, icon, and rich text:

```javascript
// Tinted background with border
slide.addShape(pres.shapes.RECTANGLE, {
  x: 0.7, y: 4.5, w: 8.6, h: 0.55,
  fill: { color: "F0F5FF" },   // light blue tint
  line: { color: C.blue60, width: 1 },
});

// Icon
const icon = await iconToBase64Png(FaHandshake, "#" + C.blue60, 256);
slide.addImage({
  data: icon, x: 0.9, y: 4.57, w: 0.35, h: 0.35,
});

// Rich text (positioned after icon)
slide.addText([
  { text: "Label: ", options: { bold: true, color: C.gray100 } },
  { text: "Description text.", options: { color: C.gray70 } },
], {
  x: 1.4, y: 4.5, w: 7.7, h: 0.55,
  fontSize: 11, fontFace: "Arial", valign: "middle", margin: 0,
});
```

### Tint color guide

| Accent | Tint Background | Border |
|--------|----------------|--------|
| Blue | `"F0F5FF"` | `C.blue60` |
| Green | `"F0FFF4"` | `C.green60` |
| Yellow | `"FFF8F0"` | `C.yellow50` |
| Red | `"FFF0F0"` | `C.red60` |
| Purple | `"F5F0FF"` | `C.purple60` |
| Teal | `"F0FFFC"` | `C.teal60` |

---

## Tinted Background Boxes

For metric boxes or inset panels within cards:

```javascript
// White inset with border
slide.addShape(pres.shapes.RECTANGLE, {
  x: ux + 0.15, y: startY + 1.75,
  w: ucW - 0.3, h: 1.4,
  fill: { color: C.white },
  line: { color: C.gray20, width: 0.5 },
});
```

---

## Gradient Hero Title Text

Render large gradient-colored hero text (e.g., "Establish", "Enable", "Accelerate") as SVG→PNG. This is the only way to achieve gradient text in pptxgenjs:

```javascript
async function renderGradientTitle(text, gradientStops, width = 700, height = 120) {
  const gid = "g" + Math.random().toString(36).slice(2, 8);
  const stops = gradientStops
    .map(s => `<stop offset="${s.offset}%" stop-color="${s.color}"/>`)
    .join("");
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}" viewBox="0 0 ${width} ${height}">
    <defs><linearGradient id="${gid}" x1="0" y1="0" x2="1" y2="0.3">${stops}</linearGradient></defs>
    <text x="0" y="${height * 0.75}" font-size="${height * 0.82}" font-weight="800"
      font-family="Arial,Helvetica,sans-serif" fill="url(#${gid})">${text}</text>
  </svg>`;
  const buf = await sharp(Buffer.from(svg)).png().toBuffer();
  return "image/png;base64," + buf.toString("base64");
}

// Usage — adjust width for text length to avoid clipping
const titleRW = title.length > 7 ? 900 : 700;
const titleImg = await renderGradientTitle("Establish", [
  { offset: 0, color: "#627EEF" },
  { offset: 50, color: "#8A3FFC" },
  { offset: 100, color: "#D946EF" },
], titleRW, 120);

// Preserve aspect ratio when placing
const titleW = cardW - px(50);
const titleH = titleW * (120 / titleRW);
slide.addImage({ data: titleImg, x: cx + px(30), y: cy + px(78), w: titleW, h: titleH });
```

---

## Charts with Carbon Styling

Native pptxgenjs charts with Carbon Design System tokens applied. Use `addChart()` with consistent color and typography settings.

### Carbon Chart Color Array

```javascript
// Bare hex — no "#" prefix (pptxgenjs context)
const carbonChartColors = [C.blue60, C.teal60, C.purple60, C.green60, C.magenta60];
```

### Column / Bar Chart

```javascript
const chartData = [
  {
    name: "Q1-Q4 Revenue",
    labels: ["Q1", "Q2", "Q3", "Q4"],
    values: [1200, 1800, 2400, 3100],
  },
];

slide.addChart(pres.charts.BAR, chartData, {
  x: 0.7, y: 1.5, w: 5.5, h: 3.2,
  barDir: "col",
  barGrouping: "clustered",
  chartColors: carbonChartColors,
  chartArea: { fill: { color: C.white }, roundedCorners: false },

  catAxisLabelColor: C.gray70,
  catAxisLabelFontSize: 10,
  catAxisLabelFontFace: "Arial",
  catGridLine: { style: "none" },

  valAxisLabelColor: C.gray70,
  valAxisLabelFontSize: 10,
  valAxisLabelFontFace: "Arial",
  valGridLine: { color: C.gray20, size: 0.5 },

  dataLabelColor: C.gray100,
  dataLabelFontSize: 10,
  dataLabelFontFace: "Arial",
  showValue: true,

  showLegend: false,
});
```

### Line Chart

```javascript
const lineData = [
  {
    name: "Deployments",
    labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
    values: [12, 19, 27, 35, 48, 62],
  },
  {
    name: "Incidents",
    labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
    values: [8, 6, 5, 3, 2, 1],
  },
];

slide.addChart(pres.charts.LINE, lineData, {
  x: 0.7, y: 1.5, w: 8.6, h: 3.5,
  lineSmooth: true,
  lineSize: 2,
  chartColors: [C.blue60, C.red60],
  chartArea: { fill: { color: C.white }, roundedCorners: false },

  catAxisLabelColor: C.gray70,
  catAxisLabelFontSize: 10,
  catAxisLabelFontFace: "Arial",
  catGridLine: { style: "none" },

  valAxisLabelColor: C.gray70,
  valAxisLabelFontSize: 10,
  valAxisLabelFontFace: "Arial",
  valGridLine: { color: C.gray20, size: 0.5 },

  showLegend: true,
  legendPos: "b",
  legendColor: C.gray70,
  legendFontSize: 10,
  legendFontFace: "Arial",
});
```

### Doughnut Chart

```javascript
const doughnutData = [
  {
    name: "Resource Allocation",
    labels: ["Compute", "Storage", "Network", "Security"],
    values: [40, 25, 20, 15],
  },
];

slide.addChart(pres.charts.DOUGHNUT, doughnutData, {
  x: 3.0, y: 1.5, w: 4.0, h: 3.5,
  holeSize: 50,
  showPercent: true,
  chartColors: [C.blue60, C.teal60, C.purple60, C.green60],
  dataLabelColor: C.gray100,
  dataLabelFontSize: 10,
  dataLabelFontFace: "Arial",
  showLegend: true,
  legendPos: "b",
  legendColor: C.gray70,
  legendFontSize: 10,
  legendFontFace: "Arial",
});
```

### Radar Chart

```javascript
const radarData = [
  {
    name: "Current State",
    labels: ["Security", "Automation", "Observability", "Governance", "Scalability"],
    values: [3, 2, 4, 2, 3],
  },
  {
    name: "Target State",
    labels: ["Security", "Automation", "Observability", "Governance", "Scalability"],
    values: [5, 5, 5, 4, 5],
  },
];

slide.addChart(pres.charts.RADAR, radarData, {
  x: 2.0, y: 1.3, w: 6.0, h: 3.8,
  radarStyle: "filled",
  chartColors: [C.blue60, C.teal60],
  catAxisLabelColor: C.gray70,
  catAxisLabelFontSize: 10,
  catAxisLabelFontFace: "Arial",
  valGridLine: { color: C.gray20, size: 0.5 },
  showLegend: true,
  legendPos: "b",
  legendColor: C.gray70,
  legendFontSize: 10,
  legendFontFace: "Arial",
});
```

### Chart + Callout Bar Layout

Pair a chart with a side callout card for key insights:

```javascript
// Chart on left
slide.addChart(pres.charts.BAR, chartData, {
  x: 0.7, y: 1.5, w: 5.5, h: 3.2,
  barDir: "col",
  chartColors: carbonChartColors,
  chartArea: { fill: { color: C.white }, roundedCorners: false },
  catAxisLabelColor: C.gray70, catAxisLabelFontSize: 10,
  valAxisLabelColor: C.gray70, valAxisLabelFontSize: 10,
  valGridLine: { color: C.gray20, size: 0.5 },
  catGridLine: { style: "none" },
  showLegend: false,
});

// Callout card on right
slide.addShape(pres.shapes.RECTANGLE, {
  x: 6.5, y: 1.5, w: 3.1, h: 3.2,
  fill: { color: C.gray10 }, shadow: cardShadow(),
});

const calloutBar = await renderGradientBar(["#0043CE", "#0F62FE", "#4589FF"], 400, 8, 0);
slide.addImage({ data: calloutBar, x: 6.5, y: 1.5, w: 3.1, h: 0.08 });

slide.addText("KEY INSIGHT", {
  x: 6.7, y: 1.7, w: 2.7, h: 0.25,
  fontSize: 9, fontFace: "Arial", color: C.blue60,
  bold: true, charSpacing: 2, margin: 0,
});

slide.addText("158%", {
  x: 6.7, y: 2.0, w: 2.7, h: 0.5,
  fontSize: 36, fontFace: "Arial Black", color: C.blue60,
  bold: true, margin: 0,
});

slide.addText("Year-over-year growth driven by automation investments", {
  x: 6.7, y: 2.6, w: 2.7, h: 1.0,
  fontSize: 12, fontFace: "Arial", color: C.gray70,
  valign: "top", margin: 0,
});
```

---

## SVG Data Visualization Helpers

Custom SVG-rendered visualizations converted to PNG via sharp. These complement native charts for specialized data displays like progress rings, sparklines, and gauges.

### renderProgressRing

Circular progress ring with center percentage text. Uses `stroke-dasharray` / `stroke-dashoffset` for the arc.

```javascript
async function renderProgressRing(value, maxValue, colors, size = 200, thickness = 16) {
  const pct = Math.min(value / maxValue, 1);
  const radius = (size - thickness) / 2;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference * (1 - pct);
  const gid = "pr" + Math.random().toString(36).slice(2, 8);

  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${size}" height="${size}" viewBox="0 0 ${size} ${size}">
    <defs>
      <linearGradient id="${gid}" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0%" stop-color="${colors[0]}"/>
        <stop offset="100%" stop-color="${colors[1] || colors[0]}"/>
      </linearGradient>
    </defs>
    <circle cx="${size/2}" cy="${size/2}" r="${radius}"
      fill="none" stroke="#E0E0E0" stroke-width="${thickness}"/>
    <circle cx="${size/2}" cy="${size/2}" r="${radius}"
      fill="none" stroke="url(#${gid})" stroke-width="${thickness}"
      stroke-dasharray="${circumference}" stroke-dashoffset="${offset}"
      stroke-linecap="round" transform="rotate(-90 ${size/2} ${size/2})"/>
    <text x="${size/2}" y="${size/2}" text-anchor="middle" dominant-baseline="central"
      font-size="${size * 0.22}" font-weight="700" font-family="Arial,Helvetica,sans-serif"
      fill="#161616">${Math.round(pct * 100)}%</text>
  </svg>`;

  const buf = await sharp(Buffer.from(svg)).png().toBuffer();
  return "image/png;base64," + buf.toString("base64");
}

// Usage
const ring = await renderProgressRing(78, 100, ["#0F62FE", "#4589FF"], 200, 16);
slide.addImage({ data: ring, x: cx + 0.4, y: cy + 0.3, w: 1.0, h: 1.0 });
```

### renderRadialGauge

Semi-circular gauge with scale markers and value text.

```javascript
async function renderRadialGauge(value, min, max, colors, width = 200, height = 120) {
  const pct = Math.min((value - min) / (max - min), 1);
  const gid = "rg" + Math.random().toString(36).slice(2, 8);
  const cx = width / 2, cy = height - 10;
  const radius = Math.min(cx - 10, cy - 10);
  const startAngle = Math.PI;
  const endAngle = 0;
  const valueAngle = startAngle - pct * Math.PI;

  const arcX1 = cx + radius * Math.cos(startAngle);
  const arcY1 = cy + radius * Math.sin(startAngle);
  const arcXv = cx + radius * Math.cos(valueAngle);
  const arcYv = cy + radius * Math.sin(valueAngle);
  const arcX2 = cx + radius * Math.cos(endAngle);
  const arcY2 = cy + radius * Math.sin(endAngle);
  const largeArc = pct > 0.5 ? 1 : 0;

  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}" viewBox="0 0 ${width} ${height}">
    <defs>
      <linearGradient id="${gid}" x1="0" y1="0" x2="1" y2="0">
        <stop offset="0%" stop-color="${colors[0]}"/>
        <stop offset="100%" stop-color="${colors[1] || colors[0]}"/>
      </linearGradient>
    </defs>
    <path d="M${arcX1},${arcY1} A${radius},${radius} 0 0,1 ${arcX2},${arcY2}"
      fill="none" stroke="#E0E0E0" stroke-width="12" stroke-linecap="round"/>
    <path d="M${arcX1},${arcY1} A${radius},${radius} 0 ${largeArc},1 ${arcXv},${arcYv}"
      fill="none" stroke="url(#${gid})" stroke-width="12" stroke-linecap="round"/>
    <text x="${cx}" y="${cy - 15}" text-anchor="middle"
      font-size="24" font-weight="700" font-family="Arial,Helvetica,sans-serif"
      fill="#161616">${value}</text>
    <text x="${cx - radius}" y="${cy + 12}" text-anchor="middle"
      font-size="10" font-family="Arial,Helvetica,sans-serif" fill="#8D8D8D">${min}</text>
    <text x="${cx + radius}" y="${cy + 12}" text-anchor="middle"
      font-size="10" font-family="Arial,Helvetica,sans-serif" fill="#8D8D8D">${max}</text>
  </svg>`;

  const buf = await sharp(Buffer.from(svg)).png().toBuffer();
  return "image/png;base64," + buf.toString("base64");
}

// Usage
const gauge = await renderRadialGauge(82, 0, 100, ["#198038", "#34D478"], 200, 120);
slide.addImage({ data: gauge, x: cx + 0.3, y: cy + 0.5, w: 1.04, h: 0.625 });
```

### renderSparkline

Compact trend line for embedding in metric cards. No axes, labels, or grid — just the line and optional gradient fill.

```javascript
async function renderSparkline(dataPoints, color, width = 200, height = 60) {
  const maxVal = Math.max(...dataPoints);
  const minVal = Math.min(...dataPoints);
  const range = maxVal - minVal || 1;
  const pad = 4;
  const usableW = width - pad * 2;
  const usableH = height - pad * 2;

  const points = dataPoints.map((v, i) => {
    const x = pad + (i / (dataPoints.length - 1)) * usableW;
    const y = pad + (1 - (v - minVal) / range) * usableH;
    return `${x},${y}`;
  }).join(" ");

  const gid = "sp" + Math.random().toString(36).slice(2, 8);
  const lastPt = points.split(" ").pop();
  const fillPoints = `${pad},${height - pad} ${points} ${width - pad},${height - pad}`;

  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}" viewBox="0 0 ${width} ${height}">
    <defs>
      <linearGradient id="${gid}" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stop-color="${color}" stop-opacity="0.2"/>
        <stop offset="100%" stop-color="${color}" stop-opacity="0.02"/>
      </linearGradient>
    </defs>
    <polygon points="${fillPoints}" fill="url(#${gid})"/>
    <polyline points="${points}" fill="none" stroke="${color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  </svg>`;

  const buf = await sharp(Buffer.from(svg)).png().toBuffer();
  return "image/png;base64," + buf.toString("base64");
}

// Usage — compact sparkline in a metric card
const spark = await renderSparkline([12, 19, 27, 35, 48, 62], "#0F62FE", 200, 60);
slide.addImage({ data: spark, x: cx + 0.2, y: cy + 2.2, w: 1.2, h: 0.36 });
```

### renderMiniBarChart

Compact vertical bar chart for embedding in cards. No axes — just bars with optional value labels.

```javascript
async function renderMiniBarChart(data, colors, width = 200, height = 120) {
  const maxVal = Math.max(...data.map(d => d.value));
  const barCount = data.length;
  const gap = 6;
  const barW = (width - gap * (barCount + 1)) / barCount;
  const labelH = 16;
  const usableH = height - labelH - 4;

  const bars = data.map((d, i) => {
    const x = gap + i * (barW + gap);
    const barH = (d.value / maxVal) * usableH;
    const y = usableH - barH;
    const color = colors[i % colors.length];
    return `<rect x="${x}" y="${y}" width="${barW}" height="${barH}" rx="2" fill="${color}"/>
      <text x="${x + barW/2}" y="${y - 3}" text-anchor="middle"
        font-size="10" font-weight="600" font-family="Arial,Helvetica,sans-serif"
        fill="#161616">${d.value}</text>
      <text x="${x + barW/2}" y="${height - 2}" text-anchor="middle"
        font-size="9" font-family="Arial,Helvetica,sans-serif"
        fill="#8D8D8D">${d.label || ""}</text>`;
  }).join("\n");

  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}" viewBox="0 0 ${width} ${height}">
    ${bars}
  </svg>`;

  const buf = await sharp(Buffer.from(svg)).png().toBuffer();
  return "image/png;base64," + buf.toString("base64");
}

// Usage
const miniBar = await renderMiniBarChart(
  [{ value: 85, label: "Q1" }, { value: 92, label: "Q2" }, { value: 78, label: "Q3" }, { value: 95, label: "Q4" }],
  ["#0F62FE", "#009D9A", "#8A3FFC", "#198038"],
  200, 120
);
slide.addImage({ data: miniBar, x: cx + 0.2, y: cy + 1.5, w: 1.2, h: 0.72 });
```

### renderDonutChart

SVG donut chart with center metric text. Uses `stroke-dasharray` with rotation offsets per segment.

```javascript
async function renderDonutChart(segments, size = 200, thickness = 28) {
  const total = segments.reduce((sum, s) => sum + s.value, 0);
  const radius = (size - thickness) / 2;
  const circumference = 2 * Math.PI * radius;
  let cumulativeOffset = 0;

  const arcs = segments.map((seg) => {
    const pct = seg.value / total;
    const dashLen = circumference * pct;
    const gapLen = circumference - dashLen;
    const rotation = -90 + (cumulativeOffset / total) * 360;
    cumulativeOffset += seg.value;
    return `<circle cx="${size/2}" cy="${size/2}" r="${radius}"
      fill="none" stroke="${seg.color}" stroke-width="${thickness}"
      stroke-dasharray="${dashLen} ${gapLen}"
      transform="rotate(${rotation} ${size/2} ${size/2})"/>`;
  }).join("\n");

  const centerText = segments[0]?.centerText || "";

  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${size}" height="${size}" viewBox="0 0 ${size} ${size}">
    <circle cx="${size/2}" cy="${size/2}" r="${radius}"
      fill="none" stroke="#E0E0E0" stroke-width="${thickness}"/>
    ${arcs}
    <text x="${size/2}" y="${size/2}" text-anchor="middle" dominant-baseline="central"
      font-size="${size * 0.18}" font-weight="700" font-family="Arial,Helvetica,sans-serif"
      fill="#161616">${centerText}</text>
  </svg>`;

  const buf = await sharp(Buffer.from(svg)).png().toBuffer();
  return "image/png;base64," + buf.toString("base64");
}

// Usage
const donut = await renderDonutChart([
  { value: 40, color: "#0F62FE", centerText: "40%" },
  { value: 25, color: "#009D9A" },
  { value: 20, color: "#8A3FFC" },
  { value: 15, color: "#198038" },
], 200, 28);
slide.addImage({ data: donut, x: cx + 0.5, y: cy + 0.3, w: 1.0, h: 1.0 });
```

### renderProcessFlow

Horizontal flow diagram with labeled boxes and arrows between them.

```javascript
async function renderProcessFlow(steps, colors, width = 800, height = 100) {
  const boxCount = steps.length;
  const arrowW = 24;
  const gap = 8;
  const totalArrowSpace = (boxCount - 1) * (arrowW + gap * 2);
  const boxW = (width - totalArrowSpace - gap * 2) / boxCount;
  const boxH = height - 20;
  const boxY = 10;
  const boxR = 6;

  let elements = "";
  for (let i = 0; i < boxCount; i++) {
    const x = gap + i * (boxW + arrowW + gap * 2);
    const color = colors[i % colors.length];
    elements += `<rect x="${x}" y="${boxY}" width="${boxW}" height="${boxH}" rx="${boxR}" fill="${color}"/>
      <text x="${x + boxW/2}" y="${boxY + boxH/2}" text-anchor="middle" dominant-baseline="central"
        font-size="12" font-weight="600" font-family="Arial,Helvetica,sans-serif"
        fill="white">${steps[i]}</text>`;

    if (i < boxCount - 1) {
      const arrowX = x + boxW + gap;
      const arrowY = boxY + boxH / 2;
      elements += `<path d="M${arrowX},${arrowY} L${arrowX + arrowW - 6},${arrowY} L${arrowX + arrowW - 10},${arrowY - 4} M${arrowX + arrowW - 6},${arrowY} L${arrowX + arrowW - 10},${arrowY + 4}"
        fill="none" stroke="#8D8D8D" stroke-width="2" stroke-linecap="round"/>`;
    }
  }

  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}" viewBox="0 0 ${width} ${height}">
    ${elements}
  </svg>`;

  const buf = await sharp(Buffer.from(svg)).png().toBuffer();
  return "image/png;base64," + buf.toString("base64");
}

// Usage
const flow = await renderProcessFlow(
  ["Plan", "Build", "Test", "Deploy", "Monitor"],
  ["#0F62FE", "#009D9A", "#8A3FFC", "#198038", "#D02670"],
  800, 100
);
slide.addImage({ data: flow, x: 0.7, y: 3.5, w: 8.6, h: 1.08 });
```

### renderProcessFlowSVG (Enhanced with Gate Support)

Enhanced version supporting **human gate styling** (dashed red borders), sub-labels per step, and XML-safe text via `escXml()`. Renders entire flow as a single compact SVG image.

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

// Usage — flow with human approval gate
const flow = await renderProcessFlowSVG([
  { label: "1. Clarify", sub: "Parse & resolve" },
  { label: "2. Design", sub: "Research & spec" },
  { label: "Approve", sub: "Human gate", gate: true },
  { label: "3. Implement", sub: "TDD-first code" },
  { label: "4. Validate", sub: "Full pipeline" },
], ["#0043CE", "#8A3FFC", "#DA1E28", "#009D9A", "#198038"], 900, 80);
slide.addImage({ data: flow, x: 0.5, y: 1.55, w: 9.0, h: 0.83 });
```

**Step data format**: Each step is `{ label: string, sub?: string, gate?: boolean }`. When `gate: true`, the box gets a dashed red border (#DA1E28), light red fill (#FFF0F0), and red text — matching the Human Gate visual pattern.

### renderQuoteMark

Large decorative quotation mark with gradient fill, used for testimonial slides.

```javascript
async function renderQuoteMark(colors, size = 120) {
  const gid = "qm" + Math.random().toString(36).slice(2, 8);
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${size}" height="${size}" viewBox="0 0 ${size} ${size}">
    <defs>
      <linearGradient id="${gid}" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0%" stop-color="${colors[0]}"/>
        <stop offset="100%" stop-color="${colors[1] || colors[0]}"/>
      </linearGradient>
    </defs>
    <text x="0" y="${size * 0.85}" font-size="${size}" font-weight="900"
      font-family="Georgia,serif" fill="url(#${gid})">\u201C</text>
  </svg>`;
  const buf = await sharp(Buffer.from(svg)).png().toBuffer();
  return "image/png;base64," + buf.toString("base64");
}

// Usage
const quote = await renderQuoteMark(["#8A3FFC", "#D946EF"], 120);
slide.addImage({ data: quote, x: 0.7, y: 1.4, w: 0.625, h: 0.625 });
```

### renderHorizontalBars

Horizontal bar chart — better than vertical bars when category names are long (common in enterprise slides).

```javascript
async function renderHorizontalBars(data, colors, width = 400, height = 200, showLabels = true) {
  const maxVal = Math.max(...data.map(d => d.value));
  const barCount = data.length;
  const gap = 6;
  const labelW = showLabels ? 100 : 0;
  const barAreaW = width - labelW - 20;
  const barH = (height - gap * (barCount + 1)) / barCount;

  const bars = data.map((d, i) => {
    const y = gap + i * (barH + gap);
    const barW = (d.value / maxVal) * barAreaW;
    const color = colors[i % colors.length];
    let el = "";
    if (showLabels) {
      el += `<text x="${labelW - 6}" y="${y + barH/2}" text-anchor="end" dominant-baseline="central"
        font-size="11" font-family="Arial,Helvetica,sans-serif" fill="#525252">${d.label || ""}</text>`;
    }
    el += `<rect x="${labelW}" y="${y}" width="${barW}" height="${barH}" rx="3" fill="${color}"/>`;
    el += `<text x="${labelW + barW + 6}" y="${y + barH/2}" dominant-baseline="central"
      font-size="10" font-weight="600" font-family="Arial,Helvetica,sans-serif"
      fill="#161616">${d.value}</text>`;
    return el;
  }).join("\n");

  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}" viewBox="0 0 ${width} ${height}">
    ${bars}
  </svg>`;

  const buf = await sharp(Buffer.from(svg)).png().toBuffer();
  return "image/png;base64," + buf.toString("base64");
}

// Usage — horizontal bars with long category names
const hBars = await renderHorizontalBars(
  [{ value: 92, label: "Platform Engineering" }, { value: 78, label: "Security Ops" }, { value: 65, label: "Data Infrastructure" }],
  ["#0F62FE", "#009D9A", "#8A3FFC"],
  400, 200
);
slide.addImage({ data: hBars, x: 1.0, y: 1.8, w: 4.0, h: 2.0 });
```

### renderTimelineConnector

Vertical timeline with circle markers for milestones — use for roadmaps and phase diagrams where horizontal space is limited.

```javascript
async function renderTimelineConnector(milestones, colors, width = 120, height = 400, highlightIndex = -1) {
  const lineX = 20;
  const textX = 44;
  const markerR = 8;
  const stepH = height / milestones.length;

  let elements = "";
  // Spine line
  elements += `<line x1="${lineX}" y1="${stepH/2}" x2="${lineX}" y2="${height - stepH/2}"
    stroke="#E0E0E0" stroke-width="2"/>`;

  for (let i = 0; i < milestones.length; i++) {
    const cy = stepH/2 + i * stepH;
    const color = colors[i % colors.length];
    const isHighlight = i === highlightIndex;
    const isFuture = i > highlightIndex && highlightIndex >= 0;

    // Marker circle
    if (isFuture) {
      elements += `<circle cx="${lineX}" cy="${cy}" r="${markerR}" fill="none" stroke="${color}" stroke-width="2"/>`;
    } else {
      elements += `<circle cx="${lineX}" cy="${cy}" r="${markerR}" fill="${color}"/>`;
    }

    // Highlight ring
    if (isHighlight) {
      elements += `<circle cx="${lineX}" cy="${cy}" r="${markerR + 4}" fill="none" stroke="${color}" stroke-width="2" stroke-dasharray="4 2"/>`;
    }

    // Label
    const fontWeight = isHighlight ? "700" : "400";
    const fillColor = isHighlight ? "#161616" : "#525252";
    elements += `<text x="${textX}" y="${cy}" dominant-baseline="central"
      font-size="11" font-weight="${fontWeight}" font-family="Arial,Helvetica,sans-serif"
      fill="${fillColor}">${milestones[i]}</text>`;
  }

  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}" viewBox="0 0 ${width} ${height}">
    ${elements}
  </svg>`;

  const buf = await sharp(Buffer.from(svg)).png().toBuffer();
  return "image/png;base64," + buf.toString("base64");
}

// Usage — roadmap timeline
const timeline = await renderTimelineConnector(
  ["Assessment", "Planning", "Migration", "Optimization", "Steady State"],
  ["#0F62FE", "#009D9A", "#8A3FFC", "#198038", "#D02670"],
  120, 400, 2  // highlight index 2 = "Migration"
);
slide.addImage({ data: timeline, x: 0.8, y: 1.5, w: 0.625, h: 2.08 });
```

### renderMatrixHeatmap

NxN heat grid for risk matrices, decision grids, and capability assessments.

```javascript
async function renderMatrixHeatmap(matrix, rowLabels, colLabels, colorScale, width = 300, height = 300, showValues = false) {
  const labelPad = 60;
  const cellW = (width - labelPad) / colLabels.length;
  const cellH = (height - labelPad) / rowLabels.length;
  const maxVal = Math.max(...matrix.flat());
  const minVal = Math.min(...matrix.flat());
  const range = maxVal - minVal || 1;

  function interpolateColor(pct) {
    // colorScale: [lowColor, highColor] — interpolate between them
    const low = colorScale[0], high = colorScale[1];
    const lr = parseInt(low.slice(1,3),16), lg = parseInt(low.slice(3,5),16), lb = parseInt(low.slice(5,7),16);
    const hr = parseInt(high.slice(1,3),16), hg = parseInt(high.slice(3,5),16), hb = parseInt(high.slice(5,7),16);
    const r = Math.round(lr + (hr-lr)*pct), g = Math.round(lg + (hg-lg)*pct), b = Math.round(lb + (hb-lb)*pct);
    return "#" + [r,g,b].map(c => c.toString(16).padStart(2,"0")).join("");
  }

  let elements = "";

  // Column labels
  for (let c = 0; c < colLabels.length; c++) {
    const cx = labelPad + c * cellW + cellW/2;
    elements += `<text x="${cx}" y="${labelPad - 8}" text-anchor="middle"
      font-size="10" font-weight="600" font-family="Arial,Helvetica,sans-serif"
      fill="#161616">${colLabels[c]}</text>`;
  }

  // Row labels + cells
  for (let r = 0; r < rowLabels.length; r++) {
    const ry = labelPad + r * cellH;
    elements += `<text x="${labelPad - 8}" y="${ry + cellH/2}" text-anchor="end" dominant-baseline="central"
      font-size="10" font-weight="600" font-family="Arial,Helvetica,sans-serif"
      fill="#161616">${rowLabels[r]}</text>`;

    for (let c = 0; c < colLabels.length; c++) {
      const cx = labelPad + c * cellW;
      const val = matrix[r][c];
      const pct = (val - minVal) / range;
      const color = interpolateColor(pct);
      const textColor = pct > 0.5 ? "#FFFFFF" : "#161616";

      elements += `<rect x="${cx + 1}" y="${ry + 1}" width="${cellW - 2}" height="${cellH - 2}" rx="3" fill="${color}"/>`;
      if (showValues) {
        elements += `<text x="${cx + cellW/2}" y="${ry + cellH/2}" text-anchor="middle" dominant-baseline="central"
          font-size="11" font-weight="600" font-family="Arial,Helvetica,sans-serif"
          fill="${textColor}">${val}</text>`;
      }
    }
  }

  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}" viewBox="0 0 ${width} ${height}">
    ${elements}
  </svg>`;

  const buf = await sharp(Buffer.from(svg)).png().toBuffer();
  return "image/png;base64," + buf.toString("base64");
}

// Usage — risk heat map
const heatmap = await renderMatrixHeatmap(
  [[1, 2, 3], [2, 3, 4], [3, 4, 5]],
  ["Low", "Medium", "High"],
  ["Impact", "Likelihood", "Priority"],
  ["#F4F4F4", "#DA1E28"],  // light gray → red
  300, 300, true
);
slide.addImage({ data: heatmap, x: 3.5, y: 1.5, w: 1.56, h: 1.56 });
```

### renderWaterfallChart

Waterfall chart showing cumulative value progression — ideal for financial narratives and budget breakdowns.

```javascript
async function renderWaterfallChart(categories, values, colors, width = 500, height = 200, baselineColor = "#E0E0E0") {
  const barW = (width - 40) / categories.length - 10;
  const gap = 10;
  const padX = 20;
  const padY = 25;
  const usableH = height - padY * 2;

  // Calculate cumulative sums
  let cumulative = [0];
  for (let i = 0; i < values.length; i++) {
    cumulative.push(cumulative[i] + values[i]);
  }
  const maxCum = Math.max(...cumulative);
  const minCum = Math.min(...cumulative, 0);
  const range = maxCum - minCum || 1;

  function yForVal(v) { return padY + (1 - (v - minCum) / range) * usableH; }

  let elements = "";

  // Baseline
  const zeroY = yForVal(0);
  elements += `<line x1="${padX}" y1="${zeroY}" x2="${width - padX}" y2="${zeroY}"
    stroke="${baselineColor}" stroke-width="1" stroke-dasharray="4 2"/>`;

  for (let i = 0; i < categories.length; i++) {
    const x = padX + i * (barW + gap);
    const startVal = cumulative[i];
    const endVal = cumulative[i + 1];
    const y1 = yForVal(Math.max(startVal, endVal));
    const barH = Math.abs(yForVal(startVal) - yForVal(endVal));
    const color = colors[i % colors.length];

    // Bar
    elements += `<rect x="${x}" y="${y1}" width="${barW}" height="${Math.max(barH, 2)}" rx="2" fill="${color}"/>`;

    // Value label above
    elements += `<text x="${x + barW/2}" y="${y1 - 4}" text-anchor="middle"
      font-size="10" font-weight="600" font-family="Arial,Helvetica,sans-serif"
      fill="#161616">${values[i] > 0 ? "+" : ""}${values[i]}</text>`;

    // Category label below
    elements += `<text x="${x + barW/2}" y="${height - 4}" text-anchor="middle"
      font-size="9" font-family="Arial,Helvetica,sans-serif"
      fill="#8D8D8D">${categories[i]}</text>`;

    // Connector to next bar
    if (i < categories.length - 1) {
      const connY = yForVal(endVal);
      elements += `<line x1="${x + barW}" y1="${connY}" x2="${x + barW + gap}" y2="${connY}"
        stroke="#8D8D8D" stroke-width="1" stroke-dasharray="3 2"/>`;
    }
  }

  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}" viewBox="0 0 ${width} ${height}">
    ${elements}
  </svg>`;

  const buf = await sharp(Buffer.from(svg)).png().toBuffer();
  return "image/png;base64," + buf.toString("base64");
}

// Usage — budget allocation waterfall
const waterfall = await renderWaterfallChart(
  ["Base", "Compute", "Storage", "Network", "Savings", "Total"],
  [100, 45, 25, 15, -30, 0],
  ["#0F62FE", "#009D9A", "#8A3FFC", "#198038", "#DA1E28", "#0F62FE"],
  500, 200
);
slide.addImage({ data: waterfall, x: 0.7, y: 2.5, w: 5.2, h: 2.08 });
```

---

## Tables with Carbon Styling

Native PowerPoint tables using `addTable()` with Carbon Design System tokens.

### Standard Data Table

```javascript
const headerOpts = {
  fill: { color: C.gray100 },
  color: C.white,
  bold: true,
  fontSize: 12,
  fontFace: "Arial",
  valign: "middle",
};

const bodyOpts = (rowIdx) => ({
  fill: { color: rowIdx % 2 === 0 ? C.white : C.gray10 },
  color: C.gray70,
  fontSize: 11,
  fontFace: "Arial",
  valign: "middle",
});

const statusColor = (status) => {
  if (status === "On Track") return C.green60;
  if (status === "At Risk") return C.red60;
  if (status === "In Progress") return C.yellow50;
  return C.gray70;
};

const rows = [
  // Header row
  [
    { text: "Initiative", options: headerOpts },
    { text: "Owner", options: headerOpts },
    { text: "Timeline", options: headerOpts },
    { text: "Status", options: headerOpts },
  ],
  // Data rows
  ...tableData.map((row, idx) => [
    { text: row.initiative, options: bodyOpts(idx) },
    { text: row.owner, options: bodyOpts(idx) },
    { text: row.timeline, options: bodyOpts(idx) },
    { text: row.status, options: { ...bodyOpts(idx), color: statusColor(row.status), bold: true } },
  ]),
];

slide.addTable(rows, {
  x: 0.7, y: 1.5, w: 8.6,
  fontFace: "Arial",
  fontSize: 11,
  border: { pt: 0.5, color: C.gray20 },
  colW: [2.8, 1.8, 2.0, 2.0],
  autoPage: false,
  rowH: [0.4, ...Array(tableData.length).fill(0.35)],
});
```

### Compact Status Table

For smaller tables within cards or split layouts:

```javascript
const compactRows = [
  [
    { text: "Metric", options: { fill: { color: C.blue60 }, color: C.white, bold: true, fontSize: 10 } },
    { text: "Current", options: { fill: { color: C.blue60 }, color: C.white, bold: true, fontSize: 10 } },
    { text: "Target", options: { fill: { color: C.blue60 }, color: C.white, bold: true, fontSize: 10 } },
  ],
  [
    { text: "Deploy Frequency", options: { color: C.gray70, fontSize: 10 } },
    { text: "Weekly", options: { color: C.gray70, fontSize: 10 } },
    { text: "Daily", options: { color: C.green60, bold: true, fontSize: 10 } },
  ],
  [
    { text: "Lead Time", options: { color: C.gray70, fontSize: 10, fill: { color: C.gray10 } } },
    { text: "2 weeks", options: { color: C.gray70, fontSize: 10, fill: { color: C.gray10 } } },
    { text: "< 1 day", options: { color: C.green60, bold: true, fontSize: 10, fill: { color: C.gray10 } } },
  ],
];

slide.addTable(compactRows, {
  x: 5.5, y: 1.5, w: 4.1,
  fontFace: "Arial",
  border: { pt: 0.5, color: C.gray20 },
  colW: [1.5, 1.3, 1.3],
  autoPage: false,
});
```

### Risk Matrix Table

Color-coded risk/severity table with `rowH` array for per-row height control. Risk levels and actions use accent colors:

```javascript
const riskRows = [
  [
    { text: "Risk Level", options: { fill: { color: C.gray100 }, color: C.white, bold: true, fontSize: 11 } },
    { text: "Version Type", options: { fill: { color: C.gray100 }, color: C.white, bold: true, fontSize: 11 } },
    { text: "Plan Changes", options: { fill: { color: C.gray100 }, color: C.white, bold: true, fontSize: 11 } },
    { text: "Action", options: { fill: { color: C.gray100 }, color: C.white, bold: true, fontSize: 11 } },
  ],
  [
    { text: "Low", options: { color: C.green60, bold: true } },
    { text: "Patch (x.x.Y)", options: { color: C.gray70 } },
    { text: "No destroys", options: { color: C.gray70 } },
    { text: "Auto-merge", options: { color: C.green60, bold: true } },
  ],
  [
    { text: "Medium", options: { color: C.yellow50, bold: true, fill: { color: C.gray10 } } },
    { text: "Minor (x.Y.0)", options: { color: C.gray70, fill: { color: C.gray10 } } },
    { text: "Adds only", options: { color: C.gray70, fill: { color: C.gray10 } } },
    { text: "Auto + notify", options: { color: C.yellow50, bold: true, fill: { color: C.gray10 } } },
  ],
  [
    { text: "Critical", options: { color: C.red60, bold: true } },
    { text: "Major (Y.0.0)", options: { color: C.gray70 } },
    { text: "Destroys", options: { color: C.gray70 } },
    { text: "Block + escalate", options: { color: C.red60, bold: true } },
  ],
];

slide.addTable(riskRows, {
  x: 0.7, y: 2.65, w: 8.6,
  fontFace: "Arial", fontSize: 10,
  border: { pt: 0.5, color: C.gray20 },
  colW: [1.6, 2.2, 2.4, 2.4],
  autoPage: false,
  rowH: [0.38, 0.35, 0.35, 0.35],
});
```

Key features:
- `rowH` array gives per-row height control (header slightly taller than data rows)
- Risk level text (Low/Medium/Critical) uses matching accent colors (green60/yellow50/red60)
- Action column mirrors risk colors for visual scanning
- Alternating row fills applied at cell level via `fill` in options

---

## Comparison / Before-After Layout

Two side-by-side cards comparing previous and current state.

```javascript
const compW = 4.1, compH = 3.2;
const leftX = 0.7, rightX = 5.2, compY = 1.5;

// --- BEFORE card (red-tinted) ---
slide.addShape(pres.shapes.RECTANGLE, {
  x: leftX, y: compY, w: compW, h: compH,
  fill: { color: "FFF0F0" }, shadow: cardShadow(),
});

// Red top accent
const redBar = await renderGradientBar(["#A01520", "#DA1E28", "#FF4D55"], 400, 8, 0);
slide.addImage({ data: redBar, x: leftX, y: compY, w: compW, h: 0.08 });

slide.addText("BEFORE", {
  x: leftX + 0.25, y: compY + 0.2, w: 2.0, h: 0.25,
  fontSize: 9, fontFace: "Arial", color: C.red60,
  bold: true, charSpacing: 2, margin: 0,
});

slide.addText("Previous State Title", {
  x: leftX + 0.25, y: compY + 0.5, w: compW - 0.5, h: 0.35,
  fontSize: 16, fontFace: "Arial", color: C.gray100,
  bold: true, margin: 0,
});

// Before bullets
const beforeBullets = beforeItems.map((item, idx) => ({
  text: item,
  options: {
    bullet: { code: "2022" }, breakLine: idx < beforeItems.length - 1,
    fontSize: 11, color: C.gray70, paraSpaceAfter: 6,
  },
}));
slide.addText(beforeBullets, {
  x: leftX + 0.25, y: compY + 0.95, w: compW - 0.5, h: compH - 1.2,
  fontFace: "Arial", valign: "top", margin: 0,
});

// --- AFTER card (green-tinted) ---
slide.addShape(pres.shapes.RECTANGLE, {
  x: rightX, y: compY, w: compW, h: compH,
  fill: { color: "F0FFF4" }, shadow: cardShadow(),
});

const greenBar = await renderGradientBar(["#0E6027", "#198038", "#34D478"], 400, 8, 0);
slide.addImage({ data: greenBar, x: rightX, y: compY, w: compW, h: 0.08 });

slide.addText("AFTER", {
  x: rightX + 0.25, y: compY + 0.2, w: 2.0, h: 0.25,
  fontSize: 9, fontFace: "Arial", color: C.green60,
  bold: true, charSpacing: 2, margin: 0,
});

slide.addText("Improved State Title", {
  x: rightX + 0.25, y: compY + 0.5, w: compW - 0.5, h: 0.35,
  fontSize: 16, fontFace: "Arial", color: C.gray100,
  bold: true, margin: 0,
});

// After bullets (same pattern)
```

---

## Quote / Testimonial Layout

Large quotation with attribution and optional metric stats alongside.

```javascript
// Vertical gradient accent bar on left
const accentBar = await renderVerticalGradientBar(["#627EEF", "#8A3FFC", "#D946EF"], 8, 400);
slide.addImage({ data: accentBar, x: 0.7, y: 1.3, w: 0.08, h: 2.6 });

// Decorative quotation mark (SVG→PNG)
const quoteMark = await renderQuoteMark(["#8A3FFC", "#D946EF"], 120);
slide.addImage({ data: quoteMark, x: 1.0, y: 1.3, w: 0.625, h: 0.625 });

// Quote text — italic
slide.addText("This platform transformed how we deliver infrastructure. What took weeks now takes hours, with better governance and fewer incidents.", {
  x: 1.0, y: 1.95, w: 5.5, h: 1.2,
  fontSize: 17, fontFace: "Arial", color: C.gray100,
  italic: true, valign: "top", margin: 0,
});

// Attribution
slide.addText([
  { text: "— Sarah Chen, ", options: { bold: true, color: C.gray100 } },
  { text: "VP of Platform Engineering, Acme Corp", options: { color: C.gray70 } },
], {
  x: 1.0, y: 3.25, w: 5.5, h: 0.35,
  fontSize: 12, fontFace: "Arial", valign: "middle", margin: 0,
});

// Optional: metric stats on the right side
const statsX = 7.0, statsW = 2.6;
const stats = [
  { num: "73%", label: "FASTER DELIVERY" },
  { num: "4.9/5", label: "TEAM SATISFACTION" },
  { num: "Zero", label: "PRODUCTION INCIDENTS" },
];

for (let i = 0; i < stats.length; i++) {
  const sy = 1.5 + i * 1.1;
  slide.addText(stats[i].num, {
    x: statsX, y: sy, w: statsW, h: 0.5,
    fontSize: 28, fontFace: "Arial Black", color: C.purple60,
    bold: true, margin: 0,
  });
  slide.addText(stats[i].label, {
    x: statsX, y: sy + 0.5, w: statsW, h: 0.25,
    fontSize: 9, fontFace: "Arial", color: C.gray50,
    bold: true, charSpacing: 2, margin: 0,
  });
}
```

---

## KPI Dashboard Layout

Three metric panels with progress rings, labels, and sparklines.

```javascript
const panelW = 2.75, panelH = 3.0;
const panelGap = 0.45;
const panelStartX = 0.7, panelStartY = 1.5;

const kpis = [
  {
    title: "Deployment Success",
    value: 96, max: 100,
    colors: ["#198038", "#34D478"],
    sparkData: [88, 90, 92, 91, 94, 96],
    sparkColor: "#198038",
    label: "SUCCESS RATE",
    accentGrad: ["#0E6027", "#198038", "#34D478"],
  },
  {
    title: "Infrastructure Coverage",
    value: 78, max: 100,
    colors: ["#0F62FE", "#4589FF"],
    sparkData: [45, 52, 58, 65, 72, 78],
    sparkColor: "#0F62FE",
    label: "MODULES COVERED",
    accentGrad: ["#0043CE", "#0F62FE", "#4589FF"],
  },
  {
    title: "Policy Compliance",
    value: 92, max: 100,
    colors: ["#8A3FFC", "#D946EF"],
    sparkData: [70, 75, 80, 85, 89, 92],
    sparkColor: "#8A3FFC",
    label: "COMPLIANT",
    accentGrad: ["#627EEF", "#8A3FFC", "#D946EF"],
  },
];

for (let i = 0; i < kpis.length; i++) {
  const kpi = kpis[i];
  const px = panelStartX + i * (panelW + panelGap);

  // Card background
  slide.addShape(pres.shapes.RECTANGLE, {
    x: px, y: panelStartY, w: panelW, h: panelH,
    fill: { color: C.gray10 }, shadow: cardShadow(),
  });

  // Gradient top accent bar
  const topBar = await renderGradientBar(kpi.accentGrad, 400, 8, 0);
  slide.addImage({ data: topBar, x: px, y: panelStartY, w: panelW, h: 0.08 });

  // Panel title
  slide.addText(kpi.title, {
    x: px + 0.2, y: panelStartY + 0.2, w: panelW - 0.4, h: 0.3,
    fontSize: 14, fontFace: "Arial", color: C.gray100,
    bold: true, margin: 0,
  });

  // Progress ring (SVG→PNG)
  const ring = await renderProgressRing(kpi.value, kpi.max, kpi.colors, 200, 16);
  slide.addImage({
    data: ring,
    x: px + panelW/2 - 0.5, y: panelStartY + 0.65,
    w: 1.0, h: 1.0,
  });

  // Metric label
  slide.addText(kpi.label, {
    x: px + 0.2, y: panelStartY + 1.8, w: panelW - 0.4, h: 0.2,
    fontSize: 9, fontFace: "Arial", color: C.gray50,
    bold: true, charSpacing: 2, align: "center", margin: 0,
  });

  // Sparkline (SVG→PNG)
  const spark = await renderSparkline(kpi.sparkData, kpi.sparkColor, 200, 60);
  slide.addImage({
    data: spark,
    x: px + panelW/2 - 0.65, y: panelStartY + 2.2,
    w: 1.3, h: 0.39,
  });

  // Trend label
  slide.addText("6-MONTH TREND", {
    x: px + 0.2, y: panelStartY + 2.65, w: panelW - 0.4, h: 0.2,
    fontSize: 8, fontFace: "Arial", color: C.gray50,
    align: "center", charSpacing: 1.5, margin: 0,
  });
}
```

---

## Comparison Matrix Layout

Multi-column comparison grid with status icons per cell.

```javascript
import { FaCheckCircle, FaExclamationTriangle, FaTimesCircle } from "react-icons/fa";

const columns = ["Basic", "Standard", "Enterprise"];
const rows = ["SSO", "RBAC", "Audit Logs", "SLA", "Dedicated Support"];
const matrixData = [
  ["check", "check", "check"],
  ["warn", "check", "check"],
  ["none", "check", "check"],
  ["none", "warn", "check"],
  ["none", "none", "check"],
];

const colW = 2.0, rowH = 0.55;
const labelW = 2.0;
const matrixX = 0.7, matrixY = 1.5;

// Column headers with gradient accent bars
for (let c = 0; c < columns.length; c++) {
  const hx = matrixX + labelW + c * colW;

  const headerBar = await renderGradientBar(
    ["#0043CE", "#0F62FE", "#4589FF"], 400, 8, 0
  );
  slide.addImage({ data: headerBar, x: hx, y: matrixY, w: colW, h: 0.08 });

  slide.addShape(pres.shapes.RECTANGLE, {
    x: hx, y: matrixY, w: colW, h: rowH,
    fill: { color: C.gray10 },
  });

  slide.addText(columns[c], {
    x: hx, y: matrixY, w: colW, h: rowH,
    fontSize: 13, fontFace: "Arial", color: C.gray100,
    bold: true, align: "center", valign: "middle", margin: 0,
  });
}

// Pre-render icons
const checkIcon = await iconToBase64Png(FaCheckCircle, "#" + C.green60, 256);
const warnIcon = await iconToBase64Png(FaExclamationTriangle, "#" + C.yellow50, 256);
const noneIcon = await iconToBase64Png(FaTimesCircle, "#" + C.red60, 256);

const iconMap = { check: checkIcon, warn: warnIcon, none: noneIcon };

// Data rows
for (let r = 0; r < rows.length; r++) {
  const ry = matrixY + rowH + r * rowH;
  const rowBg = r % 2 === 0 ? C.white : C.gray10;

  // Row label
  slide.addShape(pres.shapes.RECTANGLE, {
    x: matrixX, y: ry, w: labelW, h: rowH,
    fill: { color: rowBg },
    line: { color: C.gray20, width: 0.5 },
  });
  slide.addText(rows[r], {
    x: matrixX + 0.2, y: ry, w: labelW - 0.4, h: rowH,
    fontSize: 11, fontFace: "Arial", color: C.gray100,
    bold: true, valign: "middle", margin: 0,
  });

  // Status icons per column
  for (let c = 0; c < columns.length; c++) {
    const cx = matrixX + labelW + c * colW;
    slide.addShape(pres.shapes.RECTANGLE, {
      x: cx, y: ry, w: colW, h: rowH,
      fill: { color: rowBg },
      line: { color: C.gray20, width: 0.5 },
    });
    slide.addImage({
      data: iconMap[matrixData[r][c]],
      x: cx + colW/2 - 0.14, y: ry + rowH/2 - 0.14,
      w: 0.28, h: 0.28,
    });
  }
}
```

---

## Process Flow with Human Gate

Horizontal process cards with numbered steps and a highlighted human approval gate.

```javascript
import { FaArrowRight, FaUserShield } from "react-icons/fa";

const steps = [
  { title: "Plan", desc: "Define modules", icon: FaCogs },
  { title: "Develop", desc: "Write HCL code", icon: FaCode },
  { title: "Review", desc: "Human approval", icon: FaUserShield, isGate: true },
  { title: "Test", desc: "Validate policy", icon: FaClipboardCheck },
  { title: "Deploy", desc: "Apply changes", icon: FaRocket },
];

const stepW = 1.6, stepH = 1.8;
const stepGap = 0.15;
const arrowW = 0.22;
const startX = 0.7, startY = 1.8;

for (let i = 0; i < steps.length; i++) {
  const step = steps[i];
  const sx = startX + i * (stepW + stepGap + arrowW);

  // Step number circle (OVAL)
  const numColor = step.isGate ? C.red60 : C.blue60;
  slide.addShape(pres.shapes.OVAL, {
    x: sx + stepW/2 - 0.18, y: startY - 0.4, w: 0.36, h: 0.36,
    fill: { color: numColor },
  });
  slide.addText(String(i + 1), {
    x: sx + stepW/2 - 0.18, y: startY - 0.4, w: 0.36, h: 0.36,
    fontSize: 14, fontFace: "Arial", color: C.white,
    bold: true, align: "center", valign: "middle", margin: 0,
  });

  // Card — human gate gets dashed border + red tint
  if (step.isGate) {
    slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x: sx, y: startY, w: stepW, h: stepH,
      rectRadius: 0.06,
      fill: { color: "FFF0F0" },
      line: { color: C.red60, width: 1.5, dashType: "dash" },
      shadow: cardShadow(),
    });

    // HUMAN GATE badge
    slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x: sx + stepW/2 - 0.55, y: startY + 0.1, w: 1.1, h: 0.24,
      fill: { color: C.red60 }, rectRadius: 0.04,
    });
    slide.addText("HUMAN GATE", {
      x: sx + stepW/2 - 0.55, y: startY + 0.1, w: 1.1, h: 0.24,
      fontSize: 8, fontFace: "Arial", color: C.white,
      bold: true, align: "center", valign: "middle", charSpacing: 1.5, margin: 0,
    });
  } else {
    slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x: sx, y: startY, w: stepW, h: stepH,
      rectRadius: 0.06,
      fill: { color: C.gray10 },
      shadow: cardShadow(),
    });
  }

  // Icon
  const iconColor = step.isGate ? "#" + C.red60 : "#" + C.blue60;
  const stepIcon = await iconToBase64Png(step.icon, iconColor, 256);
  slide.addImage({
    data: stepIcon,
    x: sx + stepW/2 - 0.2, y: startY + (step.isGate ? 0.5 : 0.25),
    w: 0.4, h: 0.4,
  });

  // Step title
  slide.addText(step.title, {
    x: sx + 0.15, y: startY + (step.isGate ? 1.0 : 0.75),
    w: stepW - 0.3, h: 0.3,
    fontSize: 13, fontFace: "Arial", color: C.gray100,
    bold: true, align: "center", margin: 0,
  });

  // Step description
  slide.addText(step.desc, {
    x: sx + 0.15, y: startY + (step.isGate ? 1.3 : 1.05),
    w: stepW - 0.3, h: 0.4,
    fontSize: 10, fontFace: "Arial", color: C.gray70,
    align: "center", valign: "top", margin: 0,
  });

  // Arrow connector (except after last step)
  if (i < steps.length - 1) {
    const arrowIcon = await iconToBase64Png(FaArrowRight, "#" + C.gray50, 256);
    slide.addImage({
      data: arrowIcon,
      x: sx + stepW + stepGap/2 - 0.01,
      y: startY + stepH/2 - 0.11,
      w: arrowW, h: arrowW,
    });
  }
}
```

---

## Pixel-to-Inch Conversion Helper

When translating pixel-based designs (1920×1080) to pptxgenjs inches, use this helper:

```javascript
const px = (v) => v / 192;  // 1920px = 10" → 192px per inch
```

This keeps coordinates proportionally accurate when porting from HTML mockups. Use for all positions and dimensions:

```javascript
slide.addText("SECTION", {
  x: px(80), y: px(48), w: 5, h: px(24),
  fontSize: 10, ...
});
```

---

## 4-Column Compounding Value Cards (Strategic Impact)

Four cards in a row, each showing a progression stage with gradient hero title, items, and outcome. Uses ROUNDED_RECTANGLE with per-card tinted backgrounds.

**Slide header** — use derived positions to prevent title/subtitle overlap. Choose titleH based on whether the title wraps:

```javascript
// Section label
slide.addText("STRATEGIC IMPACT", {
  x: px(80), y: px(40), w: 5, h: px(20),
  fontSize: 10, fontFace: "Arial", color: accentColor,
  bold: true, charSpacing: 3, margin: 0,
});
// Title — px(90) for single-line, px(170) for two-line wrapping titles
// At fontSize 22 "Arial Black", each line is ~0.37" — two lines need ≥0.74"
const titleY = px(64);
const titleH = px(170);  // use px(90) if title is short/single-line
slide.addText("How This Service Creates Compounding Value", {
  x: px(80), y: titleY, w: px(1760), h: titleH,
  fontSize: 22, fontFace: "Arial", color: C.gray100, bold: true, margin: 0,
});
// Subtitle — always derive from title position + px(16) gap
const subtitleY = titleY + titleH + px(16);
slide.addText("Supporting description text", {
  x: px(80), y: subtitleY, w: px(1760), h: px(30),
  fontSize: 11.5, fontFace: "Arial", color: C.gray70, margin: 0,
});
// Cards start below subtitle
const cardTop = subtitleY + px(60);
```

**Card layout:**

```javascript
const px = (v) => v / 192;
const cardW = px(396);
const cardH = px(540);
const accentH = px(8);
const cardXOffsets = [22, 462, 902, 1342];  // pixel x-offsets

const cards = [
  {
    num: "01", title: "Establish", subtitle: "Guardrails & Controls",
    items: ["RBAC and agent isolation", "Secrets management", "Policy enforcement", "Human-in-loop approvals"],
    outcome: "Zero unreviewed changes\nreach production",
    // Per-card color palette:
    ac1: "627EEF", ac2: "8A3FFC", ac3: "D946EF",  // gradient triplet
    numColor: "8A3FFC",       // step number
    outcomeColor: "6929C4",   // outcome text
    divColor: "C4B0FF",       // divider lines
    bgColor: "F2EEFF",        // card tinted background
    arrowColor: "8A3FFC",     // arrow connector
  },
  // ... more cards with unique color palettes
];

for (let i = 0; i < cards.length; i++) {
  const c = cards[i];
  const cx = px(80) + px(cardXOffsets[i]);
  const cy = px(250);

  // Card background — ROUNDED_RECTANGLE with tinted bg
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: cx, y: cy, w: cardW, h: cardH,
    rectRadius: 0.08, fill: { color: c.bgColor }, shadow: cardShadow(),
  });

  // Gradient accent bar (with borderRadius for rounded card tops)
  const barImg = await renderGradientBar(
    ["#" + c.ac1, "#" + c.ac2, "#" + c.ac3], 396, 8, 16
  );
  slide.addImage({ data: barImg, x: cx, y: cy, w: cardW, h: accentH });

  // Step number
  slide.addText(c.num, {
    x: cx + px(34), y: cy + px(36), w: px(60), h: px(22),
    fontSize: 9, fontFace: "Arial", color: c.numColor,
    bold: true, charSpacing: 2, margin: 0,
  });

  // Gradient hero title (SVG→PNG)
  const titleGrad = [
    { offset: 0, color: "#" + c.ac1 },
    { offset: 50, color: "#" + c.ac2 },
    { offset: 100, color: "#" + c.ac3 },
  ];
  const titleRW = c.title.length > 7 ? 900 : 700;
  const titleImg = await renderGradientTitle(c.title, titleGrad, titleRW, 120);
  const titleW = cardW - px(50);
  const titleH = titleW * (120 / titleRW);
  slide.addImage({ data: titleImg, x: cx + px(30), y: cy + px(78), w: titleW, h: titleH });

  // Subtitle
  slide.addText(c.subtitle, {
    x: cx + px(34), y: cy + px(158), w: cardW - px(68), h: px(28),
    fontSize: 10.5, fontFace: "Arial", color: C.gray70,
    bold: true, valign: "middle", margin: 0,
  });

  // Top divider line
  slide.addShape(pres.shapes.LINE, {
    x: cx + px(34), y: cy + px(198), w: cardW - px(68), h: 0,
    line: { color: c.divColor, width: 0.5 },
  });

  // Content items
  const itemYs = [240, 282, 324, 366];
  for (let j = 0; j < c.items.length; j++) {
    slide.addText(c.items[j], {
      x: cx + px(20), y: cy + px(itemYs[j]) - px(12),
      w: cardW - px(40), h: px(28),
      fontSize: 9, fontFace: "Arial", color: C.gray70,
      valign: "middle", margin: 0,
    });
  }

  // Bottom divider line
  slide.addShape(pres.shapes.LINE, {
    x: cx + px(34), y: cy + px(410), w: cardW - px(68), h: 0,
    line: { color: c.divColor, width: 0.5 },
  });

  // Outcome text
  slide.addText(c.outcome, {
    x: cx + px(20), y: cy + px(430), w: cardW - px(40), h: px(80),
    fontSize: 9, fontFace: "Arial", color: c.outcomeColor,
    bold: true, valign: "top", margin: 0,
  });

  // Arrow connector to next card
  if (i < cards.length - 1) {
    const arrowXOffsets = [418, 858, 1298];
    const arrowIcon = await iconToBase64Png(FaArrowRight, "#" + c.arrowColor, 256);
    slide.addImage({
      data: arrowIcon,
      x: px(80) + px(arrowXOffsets[i]) - 0.01,
      y: px(250) + px(270),
      w: 0.22, h: 0.22,
    });
  }
}
```

---

## REQUIRED Badge + Mandatory Card Highlighting

For prerequisite/checklist cards where one card needs special emphasis:

```javascript
const isMandatory = i === prereqs.length - 1;  // last card is required

// Card with conditional styling
slide.addShape(pres.shapes.RECTANGLE, {
  x: cx, y: cy, w: cardW, h: cardH,
  fill: { color: isMandatory ? "E8F7F7" : C.gray10 },  // tinted vs default
  line: isMandatory ? { color: accentColor, width: 1.5 } : undefined,
  shadow: cardShadow(),
});

// REQUIRED badge (only on mandatory card)
if (isMandatory) {
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: cx + cardW - 1.15, y: cy + 0.15, w: 0.95, h: 0.26,
    fill: { color: accentColor }, rectRadius: 0.05,
  });
  slide.addText("REQUIRED", {
    x: cx + cardW - 1.15, y: cy + 0.15, w: 0.95, h: 0.26,
    fontSize: 8, fontFace: "Arial", color: C.white,
    bold: true, align: "center", valign: "middle",
    charSpacing: 1.5, margin: 0,
  });
}

// Bullets with conditional emphasis
const bullets = items.map((item, idx) => ({
  text: item,
  options: {
    bullet: { code: "2022" },
    breakLine: idx < items.length - 1,
    fontSize: 10,
    color: isMandatory ? C.gray100 : C.gray70,  // bolder text on mandatory
    paraSpaceAfter: 5,
  },
}));
```

---

## Full Hybrid Proposal Structure

A production proposal deck uses the hybrid approach — HTML capture for title/closing, pptxgenjs for content:

```javascript
async function buildPresentation() {
  const pres = new pptxgen();
  pres.layout = "LAYOUT_16x9";

  // Slide 1: Title (HTML capture → full-bleed PNG)
  const s1 = pres.addSlide();
  s1.addImage({ path: "images/slide-title.png", x: 0, y: 0, w: 10, h: 5.625 });

  // Slides 2-N: Programmatic content slides
  const s2 = pres.addSlide();
  s2.background = { color: C.white };
  // ... challenge cards, pillars, timelines, etc.

  // Last Slide: Closing (HTML capture → full-bleed PNG)
  const sN = pres.addSlide();
  sN.addImage({ path: "images/slide-thankyou.png", x: 0, y: 0, w: 10, h: 5.625 });

  await pres.writeFile({ fileName: "proposal.pptx" });
}
```

The hybrid approach gives you premium branded title/closing slides (layered backgrounds, glows, brand fonts) while keeping content slides fully editable and programmatically precise.

---

## SVG Visual Strategy

SVG-rendered elements are the primary tool for creating visual variety and breaking up card-heavy layouts. Use them deliberately to create visual rhythm.

### Recommended Composition Patterns

| Pattern | Structure | Visual Effect |
|---------|-----------|---------------|
| **Flow → Cards** | SVG process flow at top, detail cards below | Narrative progression; audiences follow the flow then read details |
| **Donut → Grid** | SVG donut chart left, card grid right | Composition overview + drill-down; two reading zones |
| **Ring → Table** | Progress rings in KPI panels, data table below | Metrics at a glance + supporting data |
| **Quote → Stats** | SVG quote mark + vertical bar, progress ring stats | Emotional impact + quantitative proof |
| **Flow + Table** | SVG process flow above, risk matrix table below | Process context + decision framework |

### Frequency Rule

Every 2-3 slides should include at least one SVG visualization (process flow, donut, progress ring, sparkline). This prevents the deck from becoming a series of identical card layouts. Alternate between:
- **Full-width SVG** (process flow spanning 9.0" across the slide)
- **Inline SVG** (donut/ring embedded within a card or panel)
- **Decorative SVG** (quote marks, gradient bars as visual anchors)

### SVG vs. Native pptxgenjs Decision Guide

| Use Case | SVG Image | Native pptxgenjs |
|----------|-----------|-----------------|
| Process flows with gates | `renderProcessFlowSVG` — single image, compact | Individual shapes — editable in PowerPoint |
| Progress/completion | `renderProgressRing` — gradient arcs | No equivalent |
| Trend indicators | `renderSparkline` — compact inline chart | `addChart(LINE)` — full chart with axes |
| Composition breakdown | `renderDonutChart` — inline in cards | `addChart(DOUGHNUT)` — standalone chart |
| Decorative elements | `renderQuoteMark`, gradient bars | Shape-based — limited styling |
