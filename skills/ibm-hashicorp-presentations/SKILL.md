---
name: ibm-hashicorp-presentations
description: >
  Creates professional IBM-branded PowerPoint (PPTX) presentations for HashiCorp technology content.
  Use this skill whenever the user wants to build a slide deck, presentation, or PowerPoint about
  Terraform, Vault, Consul, Nomad, Packer, Waypoint, Boundary, Vagrant, or any IBM infrastructure
  and cloud automation topic. Also trigger for general IBM-branded presentations, PPTX generation,
  slide deck creation, or when the user mentions making slides, building a deck, creating a
  presentation, or generating PowerPoint files. This skill handles the full pipeline: planning
  slide structure, selecting from 49 IBM template layouts, populating content, and producing a
  finished .pptx file using python-pptx and the official IBM brand template. Covers infrastructure
  as code, secrets management, service mesh, workload orchestration, image building, access
  management, application deployment, development environments, hybrid cloud, and multi-cloud
  automation topics.
---

# IBM/HashiCorp Presentation Builder

Create IBM-branded PowerPoint presentations using python-pptx, the official IBM POTX template, and a visual enhancement layer that adds accent bars, data visualizations, icon overlays, and callout shapes. Three components drive every deck: the POTX template (brand layouts and embedded IBM Plex Sans), the builder script (`scripts/build_presentation.py`), and the brand asset library in `resources/` (see `resources/MANIFEST.md`).

## Workflow

1. Understand the presentation topic, audience, and target length
2. Plan slide structure with visual variety -- alternate layouts, backgrounds, and enhancement types
3. Build a JSON slide specification with visual enhancements on every content slide
4. Run `scripts/build_presentation.py` to generate the PPTX

## Visual Design Principles

These rules are mandatory. Every generated deck must follow them.

- **Every content slide must have at least one visual element beyond text** -- an accent bar, icon overlay, callout shape, data visualization, or background color change. Plain white slides with only text are never acceptable.
- **Alternate backgrounds** every 3-4 slides: white -> cyan_10 (`#E5F6FF`) -> white -> gray_10 (`#F4F4F4`). This creates visual rhythm and prevents monotony.
- **Use accent bars** on data slides (above each metric), box layouts (top of each card), and section dividers. Accent bars are the single highest-impact visual element available.
- **Include a data visualization** (progress ring, horizontal bars, process flow) every 2-3 slides where the content includes quantitative data.
- **Place pictograms/icons** on feature and comparison slides using the `overlays` field. See `resources/MANIFEST.md` for available PNG assets.
- **Never exceed 5 bullets** per column. Keep bullet text under 60 characters.
- **Use the callouts field** for bottom-of-slide takeaway bars with tinted backgrounds.
- **Minimum font size: 9pt** -- anything smaller is unreadable when projected.

## Typography Rules

| Element | Font | Max ~chars | Notes |
|---------|------|-----------|-------|
| Title | IBM Plex Sans Light | ~50 | Wraps to 2 lines beyond this |
| Body/bullets | IBM Plex Sans Light | ~80 per line | 60 in narrow columns |
| Data value | IBM Plex Sans | ~10 | Large display numbers |
| Labels | IBM Plex Sans | ~30 | Uppercase, letter-spaced |
| Minimum font | -- | -- | 9pt absolute minimum |

All text: left-aligned, sentence case, IBM Plex Sans only.

## Slide Layout Reference

All 49 layouts from the IBM template. Slide dimensions are **26.67" x 15.00"** (non-standard large format). Content area starts at ~0.63" from edges.

### Cover Layouts (0-5)

| # | Name | Description |
|---|------|-------------|
| 0 | Cover, imagery | Full-bleed background image, title, 2 body text areas, IBM logo bottom-right |
| 1 | Cover, cyan | Cyan (#E5F6FF) background fill, title, 2 body areas, IBM logo |
| 2 | Cover, plain | White background, large title only, IBM logo |
| 3 | Cover, plain, label | Like #2 plus a label text area at bottom |
| 4 | Cover, imagery, half | Right-half image, left-side title, IBM logo bottom-left |
| 5 | Cover, imagery, half, label | Like #4 plus label text at top-left |

### Navigation / Structure (6-8)

| # | Name | Description |
|---|------|-------------|
| 6 | Contents | Title upper-left, 2 body columns on right |
| 7 | Section divider | Large title upper-left |
| 8 | Large text | Very large title area (hero text / quotes) |

### Callout (9-10)

| # | Name | Description |
|---|------|-------------|
| 9 | Callout, headline | Title left, large body right |
| 10 | Callout, stand-alone | Single large body area |

### Data (11-14)

| # | Name | Description |
|---|------|-------------|
| 11 | Data, 2 callouts, vertical | 2 body + 2 large number areas, vertical divider |
| 12 | Data, 3 callouts, vertical | Title + 3 columns with number headers |
| 13 | Data, 2 callouts, horizontal | 2 rows with numbers left, body right |
| 14 | Data, 3 callouts, horizontal | Title + 3 rows with numbers + body |

### Text Column (15-25)

| # | Name | Description |
|---|------|-------------|
| 15 | Text, 4 columns | Title + 4 equal body columns |
| 16 | Text, 4 columns, short dividers | Same + 3 vertical divider lines |
| 17 | Text, 4 columns, dividers, headlines | Same + headline per column |
| 18 | Text, 4 columns, dividers, pictograms | Same + 1.33" pictogram image slots |
| 19 | Text, 1 wide column, divider | Title + narrow left + wide right column |
| 20 | Text, 2 wide columns | Title + 2 wide body columns |
| 21 | Text, 2 columns, large title | Large title + 2 narrow right columns |
| 22 | Text, 2 columns, small title | Small title + 2 narrow right columns |
| 23 | Text, 2 columns, dividers, large title | Same + column headers + dividers |
| 24 | Text, 2 columns, dividers, small title | Same + column headers + dividers |
| 25 | Text, 2 columns, dividers, pictograms | Title + descriptive left + 2 right columns with pictograms |

### Box / Grid (26-34)

| # | Name | Description |
|---|------|-------------|
| 26 | Boxes, 4 stacked wide, pictograms | 2x2 grid with pictograms + body |
| 27 | Boxes, 4 stacked, small title | Small title + 2x2 grid |
| 28 | Boxes, 4 stacked, large title | Large title + 2x2 grid |
| 29 | Boxes, 4 horizontal, small title | Small title + 4 columns bottom |
| 30 | Boxes, 4 horizontal, large title | Large title + 4 columns bottom |
| 31 | Boxes, 6 stacked | Title + 3x2 grid |
| 32 | Boxes, 6 stacked, icons | Title + 3x2 grid with 0.44" icon slots |
| 33 | Boxes, 6 stacked, alternate, large title | Large title + 2 top + 4 bottom boxes |
| 34 | Boxes, 6 stacked, alternate, small title | Small title + same arrangement |

### Media (35-39)

| # | Name | Description |
|---|------|-------------|
| 35 | Video or imagery, half, inset | Title + 2 left text columns + right image (inset) |
| 36 | Video or imagery, 3/4, bleed | Title + left text + 3/4 image bleeding to edge |
| 37 | Video or imagery, 3/4, inset | Title + left text + 3/4 image with margins |
| 38 | Video or imagery, bleed | Full-bleed image |
| 39 | Video or imagery, inset | Full image with margins |

### Special (40-48)

| # | Name | Description |
|---|------|-------------|
| 40 | Contacts, profiles, contributors | Title + 6 profile slots (2x3 grid), each with photo + text |
| 41 | Table | Title + table placeholder |
| 42 | Chart | Title + source text + chart area |
| 43 | Legal disclaimer, one column | Title + body + 1 legal text column |
| 44 | Legal disclaimer, two columns | Title + body + 2 legal text columns |
| 45 | Blank slide | Title + footer + slide number only |
| 46 | Blank slide, no footer | Title + slide number only |
| 47 | End slide | IBM logo only (centered) |
| 48 | DEFAULT | Empty layout |

## Layout Selection Guide

Choose layouts based on content type, then add visual enhancements:

- **Key statistic or quote**: Callout (9-10) or Data (11-14) with accent bars above each number
- **Feature comparison (2-4 items)**: Box layouts (26-34) with icon overlays in each cell
- **Process or feature list**: Text column layouts (15-25) with pictograms via overlays
- **Architecture diagram**: Media layouts (35-39) with an image
- **Contact/team info**: Layout 40 with profile images
- **Section transition**: Layout 7 with a background color change
- **Opening impact**: Layout 8 (Large text) for hero quotes with a vertical accent bar
- **Table or chart**: Layouts 41-42
- **Legal/disclaimer**: Layouts 43-44

## IBM Color Palette

**Primary:** IBM Blue 60: `#0F62FE`

**Theme Accents:**
- Purple 50: `#A56EFF` | Cyan 80: `#003A6D` | Teal 50: `#009D9A`
- Magenta 70: `#9F1853` | Red 50: `#FA4D56`

**Backgrounds:**
- White: `#FFFFFF` | Cyan 10: `#E5F6FF` | Cyan 20: `#BAE6FF` | Gray 10: `#F4F4F4`

**Text:**
- Black: `#000000` | Gray 100: `#161616` | Gray 90: `#262626`

**Full scales:** Gray 10 (`#F4F4F4`) through Gray 100 (`#161616`); Blue 10 (`#EDF5FF`) through Blue 100 (`#001141`)

### HashiCorp Product Color Mapping

All HashiCorp products are now part of IBM. Use IBM brand colors, not original HashiCorp colors.

| Product | Domain | IBM Color |
|---------|--------|-----------|
| Terraform | Infrastructure as Code | Purple 50 `#A56EFF` |
| Vault | Secrets Management | Yellow 30 `#F1C21B` |
| Consul | Service Mesh | Magenta 50 `#EE5396` |
| Nomad | Workload Orchestration | Green 50 `#24A148` |
| Packer | Image Building | Cyan 50 `#1192E8` |
| Boundary | Access Management | Red 50 `#FA4D56` |
| Waypoint | Application Deployment | Teal 50 `#009D9A` |
| Vagrant | Development Environments | Blue 60 `#0F62FE` |

## JSON Slide Specification Reference

```json
{
  "title": "Presentation Title",
  "output_file": "output.pptx",
  "slides": [
    {
      "layout": 0,
      "title": "Slide Title",
      "body": ["Bullet 1", "Bullet 2"],
      "image": "path/to/image.png",
      "notes": "Speaker notes",

      "background": "cyan_10",
      "accent_color": "#0F62FE",
      "accent_bars": [
        {"x": 0.63, "y": 1.2, "width": 24.0, "height": 0.1, "color": "#0F62FE"}
      ],
      "overlays": [
        {"image": "resources/icons/pptx_image70.png", "x": 1.0, "y": 2.0, "width": 1.33, "height": 1.33}
      ],
      "dividers": [
        {"x": 13.33, "y": 3.0, "length": 9.0, "orientation": "vertical"}
      ],
      "callouts": [
        {"x": 0.63, "y": 12.5, "width": 24.0, "height": 1.2, "fill": "#EDF5FF", "border": "#0F62FE", "text": "Key takeaway text here"}
      ],
      "visuals": [
        {"type": "progress_ring", "value": 85, "max": 100, "color": "#0F62FE", "x": 5.0, "y": 4.0, "width": 4.0, "height": 4.0}
      ]
    }
  ]
}
```

### Slide Object Fields

| Field | Type | Description |
|-------|------|-------------|
| `layout` | int | Layout index 0-48 |
| `title` | string | Slide title |
| `body` | string or string[] | Body text (string[] creates bullet list) |
| `body_right` | string[] | Right column text (for 2-column layouts) |
| `subtitle` | string | Subtitle or label text |
| `image` | string | Path to image (for picture placeholders) |
| `icons` | string[] | Paths to icons (for pictogram placeholders) |
| `data_points` | object[] | Data with value/label (for data layouts) |
| `profiles` | object[] | Contact info with name/role/image |
| `table_data` | object | Table with headers/rows arrays |
| `columns` | string[] | Column content (for 4-column layouts) |
| `column_headings` | string[] | Column headers |
| `boxes` | string[] | Box content (for grid layouts) |
| `box_headings` | string[] | Box headers |
| `notes` | string | Speaker notes |
| **`background`** | string | Slide background: "white", "cyan_10", "gray_10", or hex |
| **`accent_color`** | string | Hex color for accent elements |
| **`accent_bars`** | object[] | Colored rectangles: {x, y, width, height, color} |
| **`overlays`** | object[] | Freeform images: {image, x, y, width, height} |
| **`dividers`** | object[] | Lines: {x, y, length, orientation, color} |
| **`callouts`** | object[] | Highlight shapes: {x, y, width, height, fill, border, text} |
| **`visuals`** | object[] | Data viz: {type, ...params, x, y, width, height} |

All position values (x, y, width, height, length) are in **inches** on the 26.67" x 15.00" slide canvas.

## Visual Data Types Reference

| Type | Params | Use Case |
|------|--------|----------|
| `progress_ring` | value, max, color, label | KPI gauges, completion percentages |
| `horizontal_bars` | data[{label, value, color}] | Side-by-side comparisons |
| `accent_gradient` | colors[] | Decorative color strips |
| `process_flow` | steps[{label, sublabel, color}] | Step-by-step workflows |
| `metric_card` | value, label, color | Standalone KPI display |
| `icon_badge` | number, color | Numbered step indicators |

## Visual Recipe Patterns

Use these recipes as starting points. Combine and adapt them to the content.

### KPI Dashboard
- Layout 45 (blank) with background `"gray_10"`
- 3 `progress_ring` visuals positioned across the slide
- Accent bar at top in blue (`#0F62FE`)
- Each ring gets a `metric_card` below it
- Callout bar at bottom with takeaway text

### Comparison Grid
- Layout 27 or 28 (4 stacked boxes)
- Accent bars at top of each box area
- Icon overlays (pictograms from `resources/icons/`) in each box
- Background `"white"`

### Process Flow
- Layout 45 (blank) with `process_flow` visual spanning the width
- Numbered step details below as callout shapes
- Accent gradient bar at top

### Feature Showcase
- Layout 18 (4 columns with pictograms)
- Icon overlays for each feature
- Accent bars above each column
- Callout bar at bottom

### Quote / Impact Slide
- Layout 8 (large text) with background `"cyan_10"`
- Thick vertical accent bar at left edge
- Large title text IS the quote

### Data Highlight
- Layout 12 (3 callouts vertical)
- Accent bar above each data value
- Background `"white"`
- Callout bar at bottom with source citation

## Available Resources

See `resources/MANIFEST.md` for the full catalog. Most useful assets:

- **25 cover background images** (1920x1080) -- `resources/images/potx_image*.png`
- **6 SVG pictograms with PNG fallbacks** -- `resources/icons/pptx_image7[0-1].png` through `pptx_image81.svg`
- **5 Carbon icons** (SVG + 64x64 PNG) -- `resources/icons/pptx_image89.png` through `pptx_image98.svg`
- **IBM logo** -- `resources/images/potx_image2.png` (1584x632)
- **Brand photography** in portrait, landscape, square, and panoramic sizes

## Recommended Presentation Structure

1. **Cover slide** (layout 0-5) -- title, subtitle, date, author
2. **Agenda / Contents** (layout 6) -- overview of sections
3. **Section dividers** (layout 7) -- between major sections, with background color change
4. **Content slides** (layouts 9-34) -- main content with visual enhancements
5. **Data / metrics slides** (layouts 11-14) -- statistics, KPIs, with accent bars and visuals
6. **Media slides** (layouts 35-39) -- screenshots, architecture diagrams
7. **Contact / team slide** (layout 40) -- if applicable
8. **Legal / disclaimer** (layout 43-44) -- if needed
9. **End slide** (layout 47) -- always close with the IBM logo slide

## Rules

1. Always use the IBM POTX template -- never create presentations from scratch
2. Use IBM brand colors only -- never use original HashiCorp brand colors
3. Left-align all text, sentence case -- no centered, justified, or title-cased text
4. IBM Plex Sans only -- the template embeds it
5. End every deck with layout 47
6. Every content slide must have at least one visual enhancement beyond text
7. Alternate slide backgrounds for visual rhythm (white -> cyan_10 -> white -> gray_10)
8. Keep text within character limits -- overflow is never acceptable
9. Consult `resources/MANIFEST.md` before referencing images or icons
