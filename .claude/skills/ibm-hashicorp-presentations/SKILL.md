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

Create IBM-branded PowerPoint presentations using python-pptx, the official IBM POTX template, and a visual enhancement layer that adds accent bars, data visualizations, icon overlays, callout shapes, cards, text boxes, and programmatic shape placement. Three components drive every deck: the POTX template (brand layouts and embedded IBM Plex Sans), the builder script (`scripts/build_presentation.py`), and the brand asset library in `resources/` (see `resources/MANIFEST.md`). Cards and text boxes enable fully composed slides with precise positioning, shadows, and rich text -- use them to build polished, magazine-quality layouts on blank slides.

## Workflow

1. Understand the presentation topic, audience, and target length
2. Plan slide structure with visual variety -- alternate layouts, backgrounds, and enhancement types
3. Build a JSON slide specification with visual enhancements on every content slide
4. Run `scripts/build_presentation.py` to generate the PPTX

## Visual Design Principles

These rules are mandatory. Every generated deck must follow them.

- **Every content slide must have at least one visual element beyond text** -- an accent bar, icon overlay, callout shape, card, text box, data visualization, or background color change. Plain white slides with only text are never acceptable.
- **Alternate backgrounds** every 3-4 slides: white -> cyan_10 (`#E5F6FF`) -> white -> gray_10 (`#F4F4F4`). This creates visual rhythm and prevents monotony.
- **Use cards for grouped content** -- when presenting 2-4 related items (features, products, comparisons), use the `cards` field to create polished card layouts with accent bars, shadows, and structured text. Cards are the most impactful visual pattern. Prefer cards over basic box layouts for any grouping of related concepts.
- **Apply shadows to cards and callouts** -- set `"shadow": true` on all cards and prominent callout shapes. Shadows add depth and visual hierarchy. On white-background slides, shadows are essential for separating cards from the background.
- **Use rich text in callouts** -- combine bold and regular text in callout bars using the `rich_text` field for visual emphasis. Use rich_text for key insights, source citations, and summary takeaways.
- **Place text boxes for custom layouts** -- when template placeholders don't provide enough flexibility, use `text_boxes` to place section labels, large metrics, or annotations precisely. On layout 45 (blank), always use text_boxes for titles and subtitles.
- **Include sparklines and donut charts** for data-rich slides -- sparklines show trends inline beneath stat cards, donut charts show composition breakdowns alongside detail cards.
- **Use accent bars** on data slides (above each metric), box layouts (top of each card), and section dividers. Accent bars are the single highest-impact visual element available.
- **Include a data visualization** (progress ring, horizontal bars, process flow, donut chart, sparkline) every 2-3 slides where the content includes quantitative data.
- **Place pictograms/icons** on feature and comparison slides using the `overlays` field. See `resources/MANIFEST.md` for available PNG assets.
- **Never exceed 5 bullets** per column. Keep bullet text under 60 characters.
- **Use the callouts field** for bottom-of-slide takeaway bars with tinted backgrounds.
- **Minimum font size: 9pt** -- anything smaller is unreadable when projected.
- **Never repeat the same visual pattern on consecutive slides** -- if slide N uses a 3-card layout, slide N+1 must use a different pattern (e.g., process flow + callout, donut chart + detail cards, comparison bars, KPI dashboard with progress rings). Monotony is the biggest visual problem.
- **Use at least 4 different visualization types per deck** -- choose from: progress_ring, horizontal_bars, donut_chart, sparkline, gradient_bar, quote_mark, comparison_bars, stat_card, process_flow. A 10-slide deck should have at least 4 distinct visual types. A 6-slide deck should have at least 3.
- **Mix card counts per slide** -- avoid using 3 or 4 cards on every slide. Vary between: 1 large card + visualization, 2 side-by-side cards, 3 column cards, or no cards at all (pure visualization slides). Some slides should be visualization-dominant with no cards.
- **Include at least one visualization-only slide** -- dedicate one slide to a full-width horizontal_bars, comparison_bars, or donut_chart visual without any cards. Data should breathe.
- **progress_ring and horizontal_bars are underused** -- actively use progress_ring for completion/maturity metrics and horizontal_bars for rankings or comparisons. These two types add significant visual variety.
- **Prevent text box overlap** -- when using layout 45 (blank) with text_boxes, do NOT set a `title` field in the slide spec (this prevents the template's "Click to add title" from appearing on top of your text_boxes). Use text_boxes for ALL text placement on blank slides.
- **Maintain padding between all elements** -- ensure at least 0.3" gap between cards, text boxes, visuals, and callouts. No two elements should share the same x,y position or overlap vertically. Plan positions as: title area (y=0.5-2.0), content area (y=2.5-11.5), callout area (y=12.0-13.5).
- **Use consistent vertical zones** on blank slides:
  - Zone 1 (y=0.3-0.6): Section label (small uppercase text, 18pt, accent color)
  - Zone 2 (y=0.7-2.0): Slide title (bold 44pt) + subtitle (22pt, gray)
  - Zone 3 (y=2.5-11.5): Main content area (cards, visuals, tables)
  - Zone 4 (y=12.0-13.8): Bottom callout bar

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
- **Feature comparison (2-4 items)**: Layout 45 (blank) with cards for each feature -- use accent colors to distinguish items
- **Process or feature list**: Text column layouts (15-25) with pictograms via overlays, or layout 45 with process_flow visual + detail cards
- **Architecture diagram**: Media layouts (35-39) with an image
- **Contact/team info**: Layout 40 with profile images
- **Section transition**: Layout 7 with a background color change and gradient_bar visual
- **Opening impact**: Layout 8 (Large text) for hero quotes with a vertical accent bar and quote_mark visual
- **Table or chart**: Layouts 41-42
- **Legal/disclaimer**: Layouts 43-44
- **KPI dashboard**: Layout 45 with stat_card visuals, sparklines, and progress_ring visuals
- **Composition data**: Layout 45 with donut_chart on left and detail cards on right
- **Before/after comparison**: Layout 45 with two large side-by-side cards in contrasting colors

## IBM Color Palette

**Primary:** IBM Blue 60: `#0F62FE`

**Theme Accents:**
- Purple 50: `#A56EFF` | Cyan 80: `#003A6D` | Teal 50: `#009D9A`
- Magenta 70: `#9F1853` | Red 50: `#FA4D56`

**Backgrounds:**
- White: `#FFFFFF` | Cyan 10: `#E5F6FF` | Cyan 20: `#BAE6FF` | Gray 10: `#F4F4F4`

**Dark Backgrounds (for dramatic hero and section slides):**
- Gray 100: `#161616` | Blue 90: `#001D6C` | Purple 90: `#1C0F30` | Teal 90: `#004144`

**Tinted Card Backgrounds (for visual variety in cards):**
- Blue tint: `#EDF5FF` | Purple tint: `#F5F0FF` | Teal tint: `#E0F7F6` | Green tint: `#DEFBE6`
- Red tint: `#FFF0F0` | Magenta tint: `#FFF0F7` | Yellow tint: `#FFF8E1`

**Text:**
- Black: `#000000` | Gray 100: `#161616` | Gray 90: `#262626`

**Gradient Color Pairs (for gradient_bar visuals and accent variety):**
- Blue gradient: `["#0043CE", "#0F62FE", "#4589FF"]`
- Purple gradient: `["#6929C4", "#8A3FFC", "#BE95FF"]`
- Teal gradient: `["#005D5D", "#009D9A", "#08BDBA"]`
- Green gradient: `["#0E6027", "#198038", "#42BE65"]`
- Magenta gradient: `["#740937", "#D02670", "#FF7EB6"]`

Use gradient_bar visuals with these color triplets on section dividers and accent elements for richer color depth.

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
        {
          "x": 0.63, "y": 12.5, "width": 25.4, "height": 1.5,
          "fill": "#EDF5FF", "border": "#0F62FE",
          "shadow": true,
          "rich_text": [
            {"text": "Key insight: ", "bold": true, "color": "#161616"},
            {"text": "Organizations using IaC reduce provisioning time by 85%.", "bold": false, "color": "#525252"}
          ]
        }
      ],
      "cards": [
        {
          "x": 0.63, "y": 2.5, "width": 8.0, "height": 5.0,
          "fill": "#FFFFFF", "accent_color": "#0F62FE",
          "title": "Card Title",
          "body": ["Bullet one", "Bullet two", "Bullet three"],
          "icon": "resources/icons/pptx_image70.png",
          "shadow": true, "corner_radius": 0.15
        }
      ],
      "text_boxes": [
        {
          "x": 0.63, "y": 0.5, "width": 20.0, "height": 1.5,
          "text": "Slide Title Text",
          "font_size": 22, "bold": true, "color": "#161616",
          "font": "IBM Plex Sans Light", "align": "left", "valign": "top"
        }
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
| `table` | object | Programmatic table: {x, y, width, height, headers, rows, col_widths} |
| `columns` | string[] | Column content (for 4-column layouts) |
| `column_headings` | string[] | Column headers |
| `boxes` | string[] | Box content (for grid layouts) |
| `box_headings` | string[] | Box headers |
| `notes` | string | Speaker notes |
| **`background`** | string | Slide background: "white", "cyan_10", "gray_10", or hex |
| **`accent_color`** | string | Hex color for accent elements |
| **`accent_bars`** | object[] | Colored rectangles: {x, y, width, height, color} |
| **`overlays`** | object[] | Freeform images: {image, x, y, width, height} |
| **`scrim`** | object | Semi-transparent dark overlay for text contrast: {x, y, width, height, color, opacity}. Place AFTER overlays, BEFORE text. Mandatory on all image-backed slides. |
| **`dividers`** | object[] | Lines: {x, y, length, orientation, color} |
| **`callouts`** | object[] | Highlight shapes: {x, y, width, height, fill, border, text, shadow, rich_text, font_size, valign, text_color, corner_radius} |
| **`cards`** | object[] | Card elements: {x, y, width, height, fill, accent_color, title, body, icon, shadow, border_color, corner_radius} |
| **`text_boxes`** | object[] | Freeform text: {x, y, width, height, text, font_size, bold, color, font, align, valign, rich_text} |
| **`visuals`** | object[] | Data viz: {type, ...params, x, y, width, height} |

Each visual object supports an optional `render_mode` field: `"native"` (default, editable shapes/charts) or `"png"` (legacy bitmap image).

All position values (x, y, width, height, length) are in **inches** on the 26.67" x 15.00" slide canvas.

**Note on tables:** For tables on blank slides, use the `table` field (not `table_data`) to create a programmatically positioned table with exact coordinates. The `table` field takes: `{x, y, width, height, headers, rows, col_widths}`.

## Card Specification Reference

Cards are the primary building block for visually polished slides. Use layout 45 (blank) and compose slides entirely from cards, text boxes, and visuals.

### Card Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| x | float | required | Left position in inches |
| y | float | required | Top position in inches |
| width | float | required | Card width in inches |
| height | float | required | Card height in inches |
| fill | string | "#F4F4F4" | Background color (hex) |
| accent_color | string | "#0F62FE" | Top accent bar color |
| title | string | none | Bold title text |
| body | string/string[] | none | Body text or bullet list |
| icon | string | none | Path to icon image |
| shadow | bool | false | Apply drop shadow |
| border_color | string | none | Border color (hex) |
| corner_radius | float | 0.15 | Corner radius in inches |

### Card Layout Rules

- **Minimum card width**: 5.0" (ensures readable text)
- **Accent bar height**: 0.15" (automatic, placed at top of card)
- **Title area**: starts 0.3" below top, 0.3" left padding, Bold 28pt IBM Plex Sans
- **Body area**: starts 0.3" below title, 0.3" left padding, Regular 22pt IBM Plex Sans
- **Shadow**: always enable on white-background slides for depth
- **Spacing between cards**: minimum 0.5" gap
- **Maximum cards per slide**: 4 across (narrower cards become hard to read)
- **Card height**: match all cards on a row to the same height for visual alignment

## Text Box Specification Reference

Text boxes enable precise text placement for slide titles, section labels, metrics, and annotations when template placeholders are insufficient.

### Text Box Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| x | float | required | Left position in inches |
| y | float | required | Top position in inches |
| width | float | required | Box width in inches |
| height | float | required | Box height in inches |
| text | string | none | Plain text content |
| rich_text | object[] | none | [{text, bold, color}] segments |
| font_size | int | 22 | Font size in points |
| bold | bool | false | Bold text |
| color | string | "#161616" | Text color (hex) |
| font | string | "IBM Plex Sans" | Font face |
| align | string | "left" | Horizontal: left, center, right |
| valign | string | "top" | Vertical: top, middle, bottom |

### Common Text Box Patterns

- **Slide title**: x=0.63, y=0.5, w=20.0, h=1.5, font_size=48, bold=true, font="IBM Plex Sans Light"
- **Subtitle**: x=0.63, y=1.5, w=20.0, h=1.0, font_size=26, color="#525252"
- **Section label**: x=0.63, y=0.3, w=10.0, h=0.5, font_size=20, bold=true, color="#0F62FE" (uppercase text)
- **Large metric**: x=centered, y=centered, font_size=72, bold=true, color=accent
- **Attribution**: x=3.5, y=8.0, w=15.0, h=1.0, font_size=22, color="#525252"

## Enhanced Callout Reference

Callouts now support rich text, shadows, custom font sizes, vertical alignment, text colors, and adjustable corners. Use callouts for bottom-of-slide insight bars, highlighted takeaways, and source citations.

### Callout Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| x | float | required | Left position in inches |
| y | float | required | Top position in inches |
| width | float | required | Callout width in inches |
| height | float | required | Callout height in inches |
| fill | string | required | Background color (hex) |
| border | string | none | Border color (hex) |
| text | string | none | Plain text content |
| rich_text | object[] | none | [{text, bold, color}] segments for mixed formatting |
| shadow | bool | false | Apply drop shadow |
| font_size | int | 22 | Font size in points |
| valign | string | "middle" | Vertical alignment: top, middle, bottom |
| text_color | string | "#161616" | Text color (hex, used with plain text) |
| corner_radius | float | 0.1 | Corner radius in inches |

### Enhanced Callout Example

```json
"callouts": [{
  "x": 0.63, "y": 12.5, "width": 25.4, "height": 1.5,
  "fill": "#EDF5FF", "border": "#0F62FE",
  "shadow": true,
  "rich_text": [
    {"text": "Key insight: ", "bold": true, "color": "#161616"},
    {"text": "Organizations using IaC reduce provisioning time by 85%.", "bold": false, "color": "#525252"}
  ]
}]
```

## Visual Data Types Reference

| Type | Params | Use Case |
|------|--------|----------|
| `progress_ring` | value, max, color, label | KPI gauges, completion percentages |
| `horizontal_bars` | data[{label, value, color}] | Side-by-side comparisons |
| `accent_gradient` | colors[] | Decorative color strips |
| `process_flow` | steps[{label, sublabel, color}] | Step-by-step workflows |
| `metric_card` | value, label, color | Standalone KPI display |
| `icon_badge` | number, color | Numbered step indicators |
| `donut_chart` | segments[{label, value, color}], hole_size, center_label, show_legend | Composition breakdowns |
| `sparkline` | values[], color, fill_opacity, show_endpoints, line_width | Inline trend indicators |
| `gradient_bar` | colors[], orientation, corner_radius | Premium accent bars |
| `quote_mark` | color, style("open"/"close") | Decorative quote marks |
| `comparison_bars` | items[{label, before, after, before_color, after_color}], before_label, after_label | Before/after comparisons |
| `stat_card` | value, label, color, trend, trend_value | Enhanced KPI cards |

All visualization types except `gradient_bar` and `accent_gradient` are rendered as **native PowerPoint shapes and charts** by default. This means text in charts, labels, and values is fully editable in PowerPoint after creation. Set `"render_mode": "png"` on any visual to force legacy bitmap rendering.

## Visual Recipe Patterns

Use these recipes as direct templates. Copy the JSON structure, adjust content, and adapt colors to your topic. All recipes use precise positioning coordinates for the 26.67" x 15.00" slide canvas.

### Visual Variety Rule

Every deck must demonstrate a MINIMUM of 20 distinct visual techniques across all slides. Visual techniques include:
- Different card counts (2-card, 3-card, 4-card layouts count as separate techniques)
- Different visualization types (donut_chart, horizontal_bars, progress_ring, etc.)
- Background images vs solid colors
- Dark slides (gray_100) vs light slides
- Tables with styled headers
- Pictogram overlays on cards
- Numbered step lists
- Architecture diagrams
- Process flows
- Quote slides with quote marks
- Large metric hero numbers
- Comparison bars
- Rich text callouts with shadows
- Icon feature grids
- Full-width visualizations (no cards)

Plan the visual technique for each slide BEFORE writing the JSON spec. Ensure maximum variety — no two consecutive slides should use the same primary technique.

Example variety plan for a 30-slide deck:
1. Cover with background image (layout 4) + pictogram overlay
2. Agenda / Contents (layout 6) with accent bar
3. Recipe 7: Four-Column Pillar Cards with pictogram icons
4. Recipe 22: Full-Width Bar Chart (visualization-only)
5. Recipe 16: Large Metric Hero (dark background, 200pt number)
6. Recipe 9: Section Divider with gradient_bar
7. Recipe 21: Architecture Diagram (layered native shapes)
8. Recipe 3: Process Flow + 3 Detail Cards
9. Recipe 29: Centered Donut + Legend Cards
10. Recipe 18: Feature Comparison Matrix (styled table)
11. Recipe 26: Two-Row Stat Banner (6 metrics, no cards)
12. Recipe 9: Section Divider with gradient_bar
13. Recipe 23: Progress Ring Dashboard (4 rings, no cards)
14. Recipe 28: Split Image + Stats (customer success)
15. Recipe 19: Pros/Cons Split (green/red cards)
16. Recipe 5: Quote / Impact Slide with quote_mark
17. Recipe 27: Timeline Roadmap with milestone markers
18. Recipe 17: Numbered Step List with icon_badges
19. Recipe 30: Full-Width Process Flow (5 steps, no cards)
20. Recipe 9: Section Divider with gradient_bar
21. Recipe 31: Two-Column Bullets with Icons
22. Recipe 33: Metric Comparison Strip (5 narrow cards)
23. Recipe 32: Gradient Hero Text (dark slide, big statement)
24. Recipe 34: Stacked Callout Bars (key takeaways)
25. Recipe 35: Photo Grid with Captions
26. Recipe 2: KPI Dashboard with Stat Cards + sparklines
27. Recipe 8: Metrics Highlight with Sparklines
28. Recipe 12: Data Table with Callout
29. Recipe 24: Half-Image Feature Slide
30. Recipe 4: Comparison / Before-After
31. End slide (layout 47)

This sequence uses 25 distinct recipes, 10+ visualization types, background images, dark slides, tables, pictograms, photo grids, and timeline roadmaps — exceeding the 20-technique minimum.

### Recipe 1: Three-Card Feature Layout

Three side-by-side cards for features, products, or capabilities. The most common and impactful slide pattern.

```json
{
  "layout": 45,
  "title": "",
  "background": "gray_10",
  "text_boxes": [
    {"x": 0.63, "y": 0.5, "width": 20.0, "height": 1.5, "text": "Unified infrastructure automation", "font_size": 22, "bold": true, "color": "#161616", "font": "IBM Plex Sans Light"},
    {"x": 0.63, "y": 1.5, "width": 20.0, "height": 1.0, "text": "Three pillars of modern cloud operations", "font_size": 13, "color": "#525252"}
  ],
  "cards": [
    {
      "x": 0.63, "y": 2.5, "width": 8.0, "height": 5.0,
      "fill": "#FFFFFF", "accent_color": "#A56EFF",
      "title": "Provision",
      "body": ["Infrastructure as Code with Terraform", "Multi-cloud resource provisioning", "State management and drift detection", "Module registry for reuse"],
      "icon": "resources/icons/pptx_image70.png",
      "shadow": true, "corner_radius": 0.15
    },
    {
      "x": 9.23, "y": 2.5, "width": 8.0, "height": 5.0,
      "fill": "#FFFFFF", "accent_color": "#F1C21B",
      "title": "Secure",
      "body": ["Secrets management with Vault", "Dynamic credential generation", "Encryption as a service", "Identity-based access control"],
      "icon": "resources/icons/pptx_image71.png",
      "shadow": true, "corner_radius": 0.15
    },
    {
      "x": 17.83, "y": 2.5, "width": 8.0, "height": 5.0,
      "fill": "#FFFFFF", "accent_color": "#EE5396",
      "title": "Connect",
      "body": ["Service mesh with Consul", "Service discovery and health checks", "Secure service-to-service communication", "Traffic management and observability"],
      "icon": "resources/icons/pptx_image72.png",
      "shadow": true, "corner_radius": 0.15
    }
  ],
  "callouts": [{
    "x": 0.63, "y": 8.5, "width": 25.4, "height": 1.5,
    "fill": "#EDF5FF", "border": "#0F62FE", "shadow": true,
    "rich_text": [
      {"text": "IBM advantage: ", "bold": true, "color": "#161616"},
      {"text": "Integrated platform with unified management, enterprise support, and compliance built in.", "bold": false, "color": "#525252"}
    ]
  }],
  "notes": "Emphasize that all three capabilities work together as an integrated platform under IBM."
}
```

### Recipe 2: KPI Dashboard with Stat Cards

Three stat cards with progress rings and a summary callout. Use for metrics, outcomes, and performance data.

```json
{
  "layout": 45,
  "title": "",
  "background": "white",
  "text_boxes": [
    {"x": 0.63, "y": 0.5, "width": 20.0, "height": 1.5, "text": "Platform adoption metrics", "font_size": 22, "bold": true, "color": "#161616", "font": "IBM Plex Sans Light"},
    {"x": 0.63, "y": 1.5, "width": 20.0, "height": 1.0, "text": "Q4 2025 enterprise customer results", "font_size": 13, "color": "#525252"}
  ],
  "visuals": [
    {"type": "stat_card", "value": "85%", "label": "Faster provisioning", "color": "#0F62FE", "trend": "up", "trend_value": "+12%", "x": 0.63, "y": 2.5, "width": 8.0, "height": 3.5},
    {"type": "stat_card", "value": "3.2x", "label": "Developer productivity", "color": "#A56EFF", "trend": "up", "trend_value": "+0.8x", "x": 9.23, "y": 2.5, "width": 8.0, "height": 3.5},
    {"type": "stat_card", "value": "60%", "label": "Cost reduction", "color": "#009D9A", "trend": "up", "trend_value": "+15%", "x": 17.83, "y": 2.5, "width": 8.0, "height": 3.5},
    {"type": "progress_ring", "value": 85, "max": 100, "color": "#0F62FE", "label": "Provisioning", "x": 2.0, "y": 7.0, "width": 4.5, "height": 4.5},
    {"type": "progress_ring", "value": 78, "max": 100, "color": "#A56EFF", "label": "Productivity", "x": 11.0, "y": 7.0, "width": 4.5, "height": 4.5},
    {"type": "progress_ring", "value": 60, "max": 100, "color": "#009D9A", "label": "Cost savings", "x": 20.0, "y": 7.0, "width": 4.5, "height": 4.5}
  ],
  "callouts": [{
    "x": 0.63, "y": 12.5, "width": 25.4, "height": 1.5,
    "fill": "#EDF5FF", "border": "#0F62FE", "shadow": true,
    "rich_text": [
      {"text": "Source: ", "bold": true, "color": "#161616"},
      {"text": "IBM internal customer benchmarks, Q4 2025. Based on 200+ enterprise deployments.", "bold": false, "color": "#525252"}
    ]
  }],
  "notes": "Highlight that these are real customer outcomes, not theoretical projections."
}
```

### Recipe 3: Process Flow with Detail Cards

Horizontal process flow at top, detail cards below for each step. Use for workflows, implementation phases, and methodologies.

```json
{
  "layout": 45,
  "title": "",
  "background": "white",
  "text_boxes": [
    {"x": 0.63, "y": 0.5, "width": 20.0, "height": 1.5, "text": "Implementation methodology", "font_size": 22, "bold": true, "color": "#161616", "font": "IBM Plex Sans Light"},
    {"x": 0.63, "y": 1.5, "width": 20.0, "height": 1.0, "text": "Four-phase approach to production readiness", "font_size": 13, "color": "#525252"}
  ],
  "visuals": [
    {
      "type": "process_flow", "x": 0.63, "y": 2.0, "width": 25.4, "height": 2.5,
      "steps": [
        {"label": "Assess", "sublabel": "Week 1-2", "color": "#0F62FE"},
        {"label": "Design", "sublabel": "Week 3-4", "color": "#A56EFF"},
        {"label": "Implement", "sublabel": "Week 5-8", "color": "#009D9A"},
        {"label": "Operate", "sublabel": "Ongoing", "color": "#24A148"}
      ]
    }
  ],
  "cards": [
    {
      "x": 0.63, "y": 5.5, "width": 6.0, "height": 6.5,
      "fill": "#FFFFFF", "accent_color": "#0F62FE",
      "title": "Assess",
      "body": ["Audit existing infrastructure", "Identify automation candidates", "Map security requirements", "Define success metrics"],
      "shadow": true
    },
    {
      "x": 7.23, "y": 5.5, "width": 6.0, "height": 6.5,
      "fill": "#FFFFFF", "accent_color": "#A56EFF",
      "title": "Design",
      "body": ["Architecture blueprints", "Module structure planning", "Policy as code framework", "Integration patterns"],
      "shadow": true
    },
    {
      "x": 13.83, "y": 5.5, "width": 6.0, "height": 6.5,
      "fill": "#FFFFFF", "accent_color": "#009D9A",
      "title": "Implement",
      "body": ["Terraform workspace setup", "Vault cluster deployment", "CI/CD pipeline integration", "Testing and validation"],
      "shadow": true
    },
    {
      "x": 20.43, "y": 5.5, "width": 6.0, "height": 6.5,
      "fill": "#FFFFFF", "accent_color": "#24A148",
      "title": "Operate",
      "body": ["Monitoring and alerting", "Drift detection enforcement", "Secret rotation automation", "Continuous compliance"],
      "shadow": true
    }
  ],
  "notes": "Walk through each phase, emphasizing that IBM provides support at every stage."
}
```

### Recipe 4: Comparison / Before-After

Two large side-by-side cards in contrasting colors. Use for before/after, old vs. new, problem vs. solution.

```json
{
  "layout": 45,
  "title": "",
  "background": "gray_10",
  "text_boxes": [
    {"x": 0.63, "y": 0.5, "width": 20.0, "height": 1.5, "text": "The transformation impact", "font_size": 22, "bold": true, "color": "#161616", "font": "IBM Plex Sans Light"},
    {"x": 0.63, "y": 1.5, "width": 20.0, "height": 1.0, "text": "Manual operations vs. automated infrastructure", "font_size": 13, "color": "#525252"}
  ],
  "cards": [
    {
      "x": 0.63, "y": 2.5, "width": 12.5, "height": 9.5,
      "fill": "#FFF0F0", "accent_color": "#DA1E28",
      "title": "Before: Manual operations",
      "body": ["Weeks-long provisioning cycles", "Configuration drift across environments", "Shared credentials in spreadsheets", "Tribal knowledge for deployments", "Compliance audits take months"],
      "shadow": true, "corner_radius": 0.15
    },
    {
      "x": 13.73, "y": 2.5, "width": 12.5, "height": 9.5,
      "fill": "#F0FFF4", "accent_color": "#198038",
      "title": "After: Automated with IBM",
      "body": ["Minutes-to-provision with Terraform", "Consistent state across all environments", "Dynamic secrets with Vault", "Codified, repeatable deployments", "Continuous compliance verification"],
      "shadow": true, "corner_radius": 0.15
    }
  ],
  "visuals": [
    {
      "type": "comparison_bars", "x": 0.63, "y": 12.5, "width": 25.4, "height": 1.5,
      "items": [
        {"label": "Provisioning time", "before": 100, "after": 15, "before_color": "#DA1E28", "after_color": "#198038"},
        {"label": "Security incidents", "before": 100, "after": 25, "before_color": "#DA1E28", "after_color": "#198038"}
      ],
      "before_label": "Before", "after_label": "After"
    }
  ],
  "notes": "Use this slide to make the business case. The contrast between red and green makes the improvement immediately visceral."
}
```

### Recipe 5: Quote / Impact Slide

Large quote with decorative quote mark and attribution. Use for customer testimonials, executive quotes, and vision statements.

```json
{
  "layout": 8,
  "title": "",
  "background": "cyan_10",
  "accent_bars": [
    {"x": 0.4, "y": 0.42, "width": 0.18, "height": 14.0, "color": "#0F62FE"}
  ],
  "visuals": [
    {"type": "quote_mark", "color": "#0F62FE", "style": "open", "x": 0.63, "y": 2.0, "width": 2.5, "height": 2.5}
  ],
  "text_boxes": [
    {
      "x": 3.5, "y": 2.5, "width": 20.0, "height": 5.0,
      "text": "Terraform and Vault together eliminated 90% of our manual infrastructure work. The IBM integration made enterprise adoption seamless.",
      "font_size": 28, "color": "#161616", "font": "IBM Plex Sans Light"
    },
    {
      "x": 3.5, "y": 8.0, "width": 15.0, "height": 1.0,
      "text": "-- Sarah Chen, VP of Platform Engineering, Fortune 500 Financial Services",
      "font_size": 11, "color": "#525252"
    }
  ],
  "notes": "Pause after showing this slide. Let the quote speak for itself."
}
```

### Recipe 6: Donut Chart with Detail Cards

Donut chart on the left showing composition, detail cards on the right explaining segments. Use for market share, resource allocation, cost breakdown.

```json
{
  "layout": 45,
  "title": "",
  "background": "white",
  "text_boxes": [
    {"x": 0.63, "y": 0.5, "width": 20.0, "height": 1.5, "text": "Infrastructure automation adoption", "font_size": 22, "bold": true, "color": "#161616", "font": "IBM Plex Sans Light"},
    {"x": 0.63, "y": 1.5, "width": 20.0, "height": 1.0, "text": "Enterprise workload distribution by automation platform", "font_size": 13, "color": "#525252"}
  ],
  "visuals": [
    {
      "type": "donut_chart", "x": 0.63, "y": 2.5, "width": 8.0, "height": 8.0,
      "segments": [
        {"label": "Terraform", "value": 45, "color": "#A56EFF"},
        {"label": "Vault", "value": 25, "color": "#F1C21B"},
        {"label": "Consul", "value": 15, "color": "#EE5396"},
        {"label": "Other", "value": 15, "color": "#C6C6C6"}
      ],
      "hole_size": 0.6, "center_label": "100%", "show_legend": true
    }
  ],
  "cards": [
    {
      "x": 10.0, "y": 2.5, "width": 16.0, "height": 2.0,
      "fill": "#FFFFFF", "accent_color": "#A56EFF",
      "title": "Terraform (45%)",
      "body": "Primary IaC platform for multi-cloud provisioning",
      "shadow": true
    },
    {
      "x": 10.0, "y": 5.0, "width": 16.0, "height": 2.0,
      "fill": "#FFFFFF", "accent_color": "#F1C21B",
      "title": "Vault (25%)",
      "body": "Secrets management and encryption services",
      "shadow": true
    },
    {
      "x": 10.0, "y": 7.5, "width": 16.0, "height": 2.0,
      "fill": "#FFFFFF", "accent_color": "#EE5396",
      "title": "Consul (15%)",
      "body": "Service mesh and service discovery",
      "shadow": true
    },
    {
      "x": 10.0, "y": 10.0, "width": 16.0, "height": 2.0,
      "fill": "#FFFFFF", "accent_color": "#C6C6C6",
      "title": "Other (15%)",
      "body": "Custom scripts, legacy tools, and manual processes",
      "shadow": true
    }
  ],
  "notes": "Highlight that Terraform + Vault together represent 70% of infrastructure automation workloads."
}
```

### Recipe 7: Four-Column Pillar Cards

Four tall cards for pillars, principles, or product features. Use for value propositions, product suites, and capability overviews.

```json
{
  "layout": 45,
  "title": "",
  "background": "gray_10",
  "text_boxes": [
    {"x": 0.63, "y": 0.5, "width": 20.0, "height": 1.5, "text": "The IBM infrastructure platform", "font_size": 22, "bold": true, "color": "#161616", "font": "IBM Plex Sans Light"},
    {"x": 0.63, "y": 1.5, "width": 20.0, "height": 1.0, "text": "Four integrated capabilities for modern infrastructure", "font_size": 13, "color": "#525252"}
  ],
  "cards": [
    {
      "x": 0.63, "y": 2.5, "width": 6.0, "height": 10.0,
      "fill": "#FFFFFF", "accent_color": "#A56EFF",
      "title": "Provision",
      "body": ["Multi-cloud IaC", "Module registry", "State management", "Plan and apply workflows", "Policy enforcement"],
      "icon": "resources/icons/pptx_image70.png",
      "shadow": true
    },
    {
      "x": 7.23, "y": 2.5, "width": 6.0, "height": 10.0,
      "fill": "#FFFFFF", "accent_color": "#F1C21B",
      "title": "Secure",
      "body": ["Dynamic secrets", "Encryption as a service", "PKI management", "Database credentials", "Cloud IAM integration"],
      "icon": "resources/icons/pptx_image71.png",
      "shadow": true
    },
    {
      "x": 13.83, "y": 2.5, "width": 6.0, "height": 10.0,
      "fill": "#FFFFFF", "accent_color": "#EE5396",
      "title": "Connect",
      "body": ["Service discovery", "Health checking", "Traffic management", "mTLS encryption", "Multi-datacenter mesh"],
      "icon": "resources/icons/pptx_image72.png",
      "shadow": true
    },
    {
      "x": 20.43, "y": 2.5, "width": 6.0, "height": 10.0,
      "fill": "#FFFFFF", "accent_color": "#24A148",
      "title": "Run",
      "body": ["Workload orchestration", "Batch scheduling", "Multi-region deploy", "Auto-scaling", "Rolling updates"],
      "icon": "resources/icons/pptx_image73.png",
      "shadow": true
    }
  ],
  "notes": "Each pillar maps to a HashiCorp product. Use accent colors from the product color mapping."
}
```

### Recipe 8: Metrics Highlight with Sparklines

Three metric areas with sparklines showing trends below each stat card. Use for time-series data, growth metrics, and performance tracking.

```json
{
  "layout": 45,
  "title": "",
  "background": "white",
  "text_boxes": [
    {"x": 0.63, "y": 0.5, "width": 20.0, "height": 1.5, "text": "Growth trajectory", "font_size": 22, "bold": true, "color": "#161616", "font": "IBM Plex Sans Light"},
    {"x": 0.63, "y": 1.5, "width": 20.0, "height": 1.0, "text": "12-month platform adoption trends", "font_size": 13, "color": "#525252"}
  ],
  "visuals": [
    {"type": "stat_card", "value": "2,847", "label": "Active workspaces", "color": "#0F62FE", "trend": "up", "trend_value": "+34%", "x": 0.63, "y": 2.5, "width": 8.0, "height": 3.0},
    {"type": "stat_card", "value": "156K", "label": "Secrets managed", "color": "#A56EFF", "trend": "up", "trend_value": "+52%", "x": 9.23, "y": 2.5, "width": 8.0, "height": 3.0},
    {"type": "stat_card", "value": "99.97%", "label": "Platform uptime", "color": "#009D9A", "trend": "stable", "trend_value": "+0.02%", "x": 17.83, "y": 2.5, "width": 8.0, "height": 3.0},
    {"type": "sparkline", "values": [120, 180, 250, 310, 520, 780, 1100, 1400, 1800, 2100, 2500, 2847], "color": "#0F62FE", "fill_opacity": 0.1, "show_endpoints": true, "line_width": 2, "x": 0.63, "y": 6.0, "width": 8.0, "height": 3.0},
    {"type": "sparkline", "values": [15, 22, 35, 48, 62, 78, 95, 110, 125, 138, 148, 156], "color": "#A56EFF", "fill_opacity": 0.1, "show_endpoints": true, "line_width": 2, "x": 9.23, "y": 6.0, "width": 8.0, "height": 3.0},
    {"type": "sparkline", "values": [99.9, 99.92, 99.95, 99.93, 99.96, 99.95, 99.97, 99.96, 99.97, 99.98, 99.97, 99.97], "color": "#009D9A", "fill_opacity": 0.1, "show_endpoints": true, "line_width": 2, "x": 17.83, "y": 6.0, "width": 8.0, "height": 3.0}
  ],
  "callouts": [{
    "x": 0.63, "y": 12.5, "width": 25.4, "height": 1.5,
    "fill": "#EDF5FF", "border": "#0F62FE", "shadow": true,
    "rich_text": [
      {"text": "Trend: ", "bold": true, "color": "#161616"},
      {"text": "Workspace growth accelerating quarter-over-quarter with 34% increase in active Terraform workspaces.", "bold": false, "color": "#525252"}
    ]
  }],
  "notes": "The sparklines tell the growth story visually. Point out the acceleration curve in workspaces."
}
```

### Recipe 9: Section Divider (Enhanced)

Section transition slide with accent bar and gradient decoration. Use between major sections of the deck.

```json
{
  "layout": 7,
  "title": "Security and compliance",
  "background": "cyan_10",
  "accent_bars": [
    {"x": 0.63, "y": 7.0, "width": 25.4, "height": 0.15, "color": "#0F62FE"}
  ],
  "visuals": [
    {"type": "gradient_bar", "colors": ["#0F62FE", "#A56EFF", "#009D9A"], "orientation": "horizontal", "corner_radius": 0.0, "x": 0.63, "y": 7.3, "width": 25.4, "height": 0.08}
  ],
  "text_boxes": [
    {"x": 0.63, "y": 8.0, "width": 15.0, "height": 1.0, "text": "How IBM protects your infrastructure at every layer", "font_size": 13, "color": "#525252"}
  ],
  "notes": "Transition slide. Pause briefly before advancing."
}
```

### Recipe 10: Architecture / Product Grid

2x3 grid of product cards with icons and descriptions. Use for product portfolios, solution components, and technology stacks.

```json
{
  "layout": 45,
  "title": "",
  "background": "white",
  "text_boxes": [
    {"x": 0.63, "y": 0.5, "width": 20.0, "height": 1.5, "text": "IBM infrastructure automation portfolio", "font_size": 22, "bold": true, "color": "#161616", "font": "IBM Plex Sans Light"},
    {"x": 0.63, "y": 1.5, "width": 20.0, "height": 1.0, "text": "Comprehensive tooling for every infrastructure need", "font_size": 13, "color": "#525252"}
  ],
  "cards": [
    {
      "x": 0.63, "y": 2.5, "width": 8.0, "height": 4.5,
      "fill": "#FFFFFF", "accent_color": "#A56EFF",
      "title": "Terraform",
      "body": ["Infrastructure as Code", "Multi-cloud provisioning", "State management"],
      "icon": "resources/icons/pptx_image70.png",
      "shadow": true
    },
    {
      "x": 9.23, "y": 2.5, "width": 8.0, "height": 4.5,
      "fill": "#FFFFFF", "accent_color": "#F1C21B",
      "title": "Vault",
      "body": ["Secrets management", "Dynamic credentials", "Encryption services"],
      "icon": "resources/icons/pptx_image71.png",
      "shadow": true
    },
    {
      "x": 17.83, "y": 2.5, "width": 8.0, "height": 4.5,
      "fill": "#FFFFFF", "accent_color": "#EE5396",
      "title": "Consul",
      "body": ["Service mesh", "Service discovery", "Traffic management"],
      "icon": "resources/icons/pptx_image72.png",
      "shadow": true
    },
    {
      "x": 0.63, "y": 7.5, "width": 8.0, "height": 4.5,
      "fill": "#FFFFFF", "accent_color": "#24A148",
      "title": "Nomad",
      "body": ["Workload orchestration", "Batch scheduling", "Multi-region deployment"],
      "icon": "resources/icons/pptx_image73.png",
      "shadow": true
    },
    {
      "x": 9.23, "y": 7.5, "width": 8.0, "height": 4.5,
      "fill": "#FFFFFF", "accent_color": "#1192E8",
      "title": "Packer",
      "body": ["Image building", "Multi-platform support", "Pipeline integration"],
      "icon": "resources/icons/pptx_image74.png",
      "shadow": true
    },
    {
      "x": 17.83, "y": 7.5, "width": 8.0, "height": 4.5,
      "fill": "#FFFFFF", "accent_color": "#FA4D56",
      "title": "Boundary",
      "body": ["Access management", "Identity-based access", "Session management"],
      "icon": "resources/icons/pptx_image75.png",
      "shadow": true
    }
  ],
  "notes": "Each product maps to its IBM brand color. Emphasize the breadth of the portfolio."
}
```

### Recipe 11: Timeline / Phases

Horizontal process flow with numbered phase cards below. Use for roadmaps, project timelines, and migration plans.

```json
{
  "layout": 45,
  "title": "",
  "background": "white",
  "text_boxes": [
    {"x": 0.63, "y": 0.5, "width": 20.0, "height": 1.5, "text": "Migration roadmap", "font_size": 22, "bold": true, "color": "#161616", "font": "IBM Plex Sans Light"},
    {"x": 0.63, "y": 1.5, "width": 20.0, "height": 1.0, "text": "12-month journey to fully automated infrastructure", "font_size": 13, "color": "#525252"}
  ],
  "visuals": [
    {
      "type": "process_flow", "x": 0.63, "y": 2.0, "width": 25.4, "height": 2.0,
      "steps": [
        {"label": "Phase 1", "sublabel": "Months 1-3", "color": "#0F62FE"},
        {"label": "Phase 2", "sublabel": "Months 4-6", "color": "#A56EFF"},
        {"label": "Phase 3", "sublabel": "Months 7-9", "color": "#009D9A"},
        {"label": "Phase 4", "sublabel": "Months 10-12", "color": "#24A148"}
      ]
    },
    {"type": "icon_badge", "number": 1, "color": "#0F62FE", "x": 2.63, "y": 4.5, "width": 1.0, "height": 1.0},
    {"type": "icon_badge", "number": 2, "color": "#A56EFF", "x": 9.23, "y": 4.5, "width": 1.0, "height": 1.0},
    {"type": "icon_badge", "number": 3, "color": "#009D9A", "x": 15.83, "y": 4.5, "width": 1.0, "height": 1.0},
    {"type": "icon_badge", "number": 4, "color": "#24A148", "x": 22.43, "y": 4.5, "width": 1.0, "height": 1.0}
  ],
  "cards": [
    {
      "x": 0.63, "y": 5.5, "width": 6.0, "height": 6.5,
      "fill": "#FFFFFF", "accent_color": "#0F62FE",
      "title": "Foundation",
      "body": ["Deploy Terraform Enterprise", "Initial workspace structure", "Core module library", "Team onboarding"],
      "shadow": true
    },
    {
      "x": 7.23, "y": 5.5, "width": 6.0, "height": 6.5,
      "fill": "#FFFFFF", "accent_color": "#A56EFF",
      "title": "Expansion",
      "body": ["Multi-cloud adoption", "Vault integration", "Policy as code", "CI/CD pipelines"],
      "shadow": true
    },
    {
      "x": 13.83, "y": 5.5, "width": 6.0, "height": 6.5,
      "fill": "#FFFFFF", "accent_color": "#009D9A",
      "title": "Optimization",
      "body": ["Service mesh rollout", "Cost optimization", "Advanced modules", "Self-service portal"],
      "shadow": true
    },
    {
      "x": 20.43, "y": 5.5, "width": 6.0, "height": 6.5,
      "fill": "#FFFFFF", "accent_color": "#24A148",
      "title": "Maturity",
      "body": ["Full automation", "Compliance as code", "Multi-region active", "Center of excellence"],
      "shadow": true
    }
  ],
  "notes": "This is a typical 12-month journey. Adjust phases based on the customer's starting point and complexity."
}
```

### Recipe 12: Data Table with Callout

Table layout with accent decoration and insight callout. Use for feature comparisons, pricing tiers, and detailed specifications.

```json
{
  "layout": 41,
  "title": "Feature comparison by tier",
  "background": "white",
  "accent_bars": [
    {"x": 0.63, "y": 2.8, "width": 25.4, "height": 0.1, "color": "#0F62FE"}
  ],
  "table_data": {
    "headers": ["Capability", "Standard", "Plus", "Premium"],
    "rows": [
      ["Terraform workspaces", "5", "50", "Unlimited"],
      ["Vault secrets engines", "3", "10", "Unlimited"],
      ["Policy sets", "1", "5", "Unlimited"],
      ["Audit logging", "30 days", "90 days", "1 year"],
      ["Support SLA", "Business hours", "24x5", "24x7"],
      ["SSO/SAML", "No", "Yes", "Yes"]
    ]
  },
  "text_boxes": [
    {"x": 0.63, "y": 0.3, "width": 10.0, "height": 0.5, "text": "PRICING AND PACKAGING", "font_size": 10, "bold": true, "color": "#0F62FE"}
  ],
  "callouts": [{
    "x": 0.63, "y": 12.5, "width": 25.4, "height": 1.5,
    "fill": "#F4F4F4", "border": "#525252", "shadow": true,
    "rich_text": [
      {"text": "Recommendation: ", "bold": true, "color": "#161616"},
      {"text": "Plus tier provides the best value for mid-size enterprises with 10-50 teams.", "bold": false, "color": "#525252"}
    ]
  }],
  "notes": "Be prepared to discuss custom enterprise pricing beyond the Premium tier."
}
```

### Recipe 13: Two-Box Comparison

Two equal cards side by side for "Option A vs Option B" decisions. Uses neutral accent colors (not red/green like Before/After) for balanced comparisons where neither option is inherently better.

```json
{
  "layout": 45,
  "title": "",
  "background": "gray_10",
  "text_boxes": [
    {"x": 0.63, "y": 0.5, "width": 20.0, "height": 1.5, "text": "Deployment model comparison", "font_size": 48, "bold": true, "color": "#161616", "font": "IBM Plex Sans Light"},
    {"x": 0.63, "y": 1.7, "width": 20.0, "height": 1.0, "text": "Choose the model that fits your operational requirements", "font_size": 22, "color": "#525252"}
  ],
  "cards": [
    {
      "x": 0.63, "y": 2.5, "width": 12.2, "height": 9.5,
      "fill": "#FFFFFF", "accent_color": "#0F62FE",
      "title": "Self-managed deployment",
      "body": ["Full control over infrastructure", "Custom network topology", "On-premises or private cloud", "Team manages upgrades and patches", "Best for regulated industries"],
      "shadow": true, "corner_radius": 0.15
    },
    {
      "x": 13.73, "y": 2.5, "width": 12.2, "height": 9.5,
      "fill": "#FFFFFF", "accent_color": "#A56EFF",
      "title": "IBM-managed SaaS",
      "body": ["Zero infrastructure overhead", "Automatic updates and scaling", "Built-in HA and DR", "99.99% uptime SLA", "Best for fast-moving teams"],
      "shadow": true, "corner_radius": 0.15
    }
  ],
  "dividers": [
    {"x": 13.18, "y": 3.0, "length": 8.5, "orientation": "vertical", "color": "#C6C6C6"}
  ],
  "callouts": [{
    "x": 0.63, "y": 12.5, "width": 25.4, "height": 1.5,
    "fill": "#EDF5FF", "border": "#0F62FE", "shadow": true,
    "rich_text": [
      {"text": "Recommendation: ", "bold": true, "color": "#161616"},
      {"text": "Start with IBM-managed SaaS for fastest time-to-value, migrate to self-managed only if regulatory requirements demand it.", "bold": false, "color": "#525252"}
    ]
  }],
  "notes": "This is a balanced comparison -- neither option is wrong. Guide the audience based on their specific constraints."
}
```

### Recipe 14: Three-Pillar Layout

Three tall vertical columns with heading and bullets. Wider than 4-column layouts (each 8.0" wide) for more readable content per column.

```json
{
  "layout": 45,
  "title": "",
  "background": "white",
  "text_boxes": [
    {"x": 0.63, "y": 0.5, "width": 20.0, "height": 1.5, "text": "Zero trust security framework", "font_size": 48, "bold": true, "color": "#161616", "font": "IBM Plex Sans Light"},
    {"x": 0.63, "y": 1.7, "width": 20.0, "height": 1.0, "text": "Three pillars of modern infrastructure security", "font_size": 22, "color": "#525252"}
  ],
  "cards": [
    {
      "x": 0.63, "y": 2.5, "width": 8.0, "height": 10.0,
      "fill": "#FFFFFF", "accent_color": "#0F62FE",
      "title": "Identity",
      "body": ["Machine identity with SPIFFE", "Workload attestation", "Certificate-based auth", "Dynamic credentials", "Short-lived tokens"],
      "shadow": true, "corner_radius": 0.15
    },
    {
      "x": 9.23, "y": 2.5, "width": 8.0, "height": 10.0,
      "fill": "#FFFFFF", "accent_color": "#F1C21B",
      "title": "Encryption",
      "body": ["Transit secrets engine", "Auto-unseal with KMS", "Key rotation policies", "Data masking", "Tokenization"],
      "shadow": true, "corner_radius": 0.15
    },
    {
      "x": 17.83, "y": 2.5, "width": 8.0, "height": 10.0,
      "fill": "#FFFFFF", "accent_color": "#009D9A",
      "title": "Access Control",
      "body": ["Policy as code with Sentinel", "Namespace isolation", "RBAC with OIDC", "Session recording", "Just-in-time access"],
      "shadow": true, "corner_radius": 0.15
    }
  ],
  "notes": "Each pillar maps to Vault capabilities. Emphasize that all three work together as a unified security layer."
}
```

### Recipe 15: Four-Quadrant Grid

2x2 grid with labeled quadrants and different tinted backgrounds per quadrant. Use for matrices, 2x2 frameworks, and categorized overviews.

```json
{
  "layout": 45,
  "title": "",
  "background": "white",
  "text_boxes": [
    {"x": 0.63, "y": 0.5, "width": 20.0, "height": 1.5, "text": "Automation maturity model", "font_size": 48, "bold": true, "color": "#161616", "font": "IBM Plex Sans Light"},
    {"x": 0.63, "y": 1.7, "width": 20.0, "height": 1.0, "text": "Assess your organization across two dimensions", "font_size": 22, "color": "#525252"},
    {"x": 0.2, "y": 5.5, "width": 0.4, "height": 5.0, "text": "Automation scope", "font_size": 18, "bold": true, "color": "#525252", "align": "center", "valign": "middle"},
    {"x": 9.0, "y": 13.8, "width": 10.0, "height": 0.5, "text": "Process maturity", "font_size": 18, "bold": true, "color": "#525252", "align": "center"}
  ],
  "cards": [
    {
      "x": 0.63, "y": 2.5, "width": 12.5, "height": 5.2,
      "fill": "#EDF5FF", "accent_color": "#0F62FE",
      "title": "Reactive automation",
      "body": ["Ad-hoc scripts and runbooks", "Manual trigger, automated execution", "Limited scope, high tribal knowledge"],
      "shadow": true, "corner_radius": 0.15
    },
    {
      "x": 13.73, "y": 2.5, "width": 12.5, "height": 5.2,
      "fill": "#F6F2FF", "accent_color": "#A56EFF",
      "title": "Proactive automation",
      "body": ["Infrastructure as Code everywhere", "Policy-driven guardrails", "Self-service with governance"],
      "shadow": true, "corner_radius": 0.15
    },
    {
      "x": 0.63, "y": 8.2, "width": 12.5, "height": 5.2,
      "fill": "#F4F4F4", "accent_color": "#525252",
      "title": "Manual operations",
      "body": ["Ticket-driven provisioning", "Shared credentials in vaults", "Snowflake environments"],
      "shadow": true, "corner_radius": 0.15
    },
    {
      "x": 13.73, "y": 8.2, "width": 12.5, "height": 5.2,
      "fill": "#DEFBE6", "accent_color": "#198038",
      "title": "Autonomous platform",
      "body": ["Event-driven scaling", "Self-healing infrastructure", "Continuous compliance verification"],
      "shadow": true, "corner_radius": 0.15
    }
  ],
  "notes": "Guide the audience to place themselves on the grid. Most enterprises start in the bottom-left quadrant."
}
```

### Recipe 16: Large Metric Hero

A dramatic full-slide metric display with supporting context, accent decoration, and visual impact. This is a visualization-only slide with NO cards.

```json
{
  "layout": 45,
  "background": "gray_100",
  "text_boxes": [
    {"x": 0.63, "y": 0.5, "width": 10.0, "height": 0.6, "text": "THE IMPACT", "font_size": 18, "bold": true, "color": "#0F62FE", "font": "IBM Plex Sans"},
    {"x": 0.63, "y": 1.2, "width": 20.0, "height": 1.5, "text": "Infrastructure provisioning time", "font_size": 36, "color": "#FFFFFF", "font": "IBM Plex Sans Light"},
    {"x": 3.0, "y": 4.0, "width": 20.67, "height": 5.0, "text": "85%", "font_size": 200, "bold": true, "color": "#0F62FE", "align": "center"},
    {"x": 3.0, "y": 8.5, "width": 20.67, "height": 1.5, "text": "reduction", "font_size": 44, "color": "#FFFFFF", "align": "center", "font": "IBM Plex Sans Light"},
    {"x": 3.0, "y": 10.5, "width": 20.67, "height": 1.0, "text": "Based on 200+ enterprise deployments across financial services, healthcare, and technology sectors", "font_size": 16, "color": "#8D8D8D", "align": "center"}
  ],
  "accent_bars": [
    {"x": 0.63, "y": 3.5, "width": 25.4, "height": 0.08, "color": "#0F62FE"},
    {"x": 0.63, "y": 10.0, "width": 25.4, "height": 0.08, "color": "#0F62FE"}
  ],
  "visuals": [
    {"type": "progress_ring", "value": 85, "max": 100, "color": "#0F62FE", "x": 20.0, "y": 1.0, "width": 3.5, "height": 3.5}
  ]
}
```

Key design elements: dark background (gray_100) for dramatic contrast, massive 200pt metric, section label + context title above, supporting text below, accent bars as horizontal rules, progress ring in the corner for visual reinforcement.

### Recipe 17: Numbered Step List

Vertical numbered steps (1-2-3-4) flowing down the page. Use for sequential instructions, onboarding flows, and getting-started guides.

```json
{
  "layout": 45,
  "title": "",
  "background": "white",
  "text_boxes": [
    {"x": 0.63, "y": 0.5, "width": 20.0, "height": 1.5, "text": "Getting started in four steps", "font_size": 48, "bold": true, "color": "#161616", "font": "IBM Plex Sans Light"},
    {"x": 0.63, "y": 1.7, "width": 20.0, "height": 1.0, "text": "From zero to production-ready in under a week", "font_size": 22, "color": "#525252"},
    {"x": 3.0, "y": 3.0, "width": 18.0, "height": 1.0, "text": "Create your organization", "font_size": 24, "bold": true, "color": "#161616"},
    {"x": 3.0, "y": 3.7, "width": 18.0, "height": 1.0, "text": "Sign up on IBM Cloud, create a Terraform Cloud org, and connect your identity provider for SSO.", "font_size": 18, "color": "#525252"},
    {"x": 3.0, "y": 5.5, "width": 18.0, "height": 1.0, "text": "Configure your first workspace", "font_size": 24, "bold": true, "color": "#161616"},
    {"x": 3.0, "y": 6.2, "width": 18.0, "height": 1.0, "text": "Link a VCS repository, set variables, and configure run triggers for your initial infrastructure.", "font_size": 18, "color": "#525252"},
    {"x": 3.0, "y": 8.0, "width": 18.0, "height": 1.0, "text": "Apply governance policies", "font_size": 24, "bold": true, "color": "#161616"},
    {"x": 3.0, "y": 8.7, "width": 18.0, "height": 1.0, "text": "Enable Sentinel policies for cost controls, security baselines, and naming conventions.", "font_size": 18, "color": "#525252"},
    {"x": 3.0, "y": 10.5, "width": 18.0, "height": 1.0, "text": "Scale to your teams", "font_size": 24, "bold": true, "color": "#161616"},
    {"x": 3.0, "y": 11.2, "width": 18.0, "height": 1.0, "text": "Create team workspaces, publish reusable modules, and onboard developers with self-service workflows.", "font_size": 18, "color": "#525252"}
  ],
  "visuals": [
    {"type": "icon_badge", "number": 1, "color": "#0F62FE", "x": 1.0, "y": 3.0, "width": 1.5, "height": 1.5},
    {"type": "icon_badge", "number": 2, "color": "#A56EFF", "x": 1.0, "y": 5.5, "width": 1.5, "height": 1.5},
    {"type": "icon_badge", "number": 3, "color": "#009D9A", "x": 1.0, "y": 8.0, "width": 1.5, "height": 1.5},
    {"type": "icon_badge", "number": 4, "color": "#24A148", "x": 1.0, "y": 10.5, "width": 1.5, "height": 1.5}
  ],
  "dividers": [
    {"x": 1.75, "y": 4.6, "length": 0.8, "orientation": "vertical", "color": "#C6C6C6"},
    {"x": 1.75, "y": 7.1, "length": 0.8, "orientation": "vertical", "color": "#C6C6C6"},
    {"x": 1.75, "y": 9.6, "length": 0.8, "orientation": "vertical", "color": "#C6C6C6"}
  ],
  "notes": "Walk through each step live if possible. Emphasize that step 1 takes under 10 minutes."
}
```

### Recipe 18: Feature Comparison Matrix

Table with checkmark/X columns showing capabilities across options. Use for vendor comparisons, tier features, and technology evaluations.

```json
{
  "layout": 41,
  "title": "Platform capability comparison",
  "background": "white",
  "accent_bars": [
    {"x": 0.63, "y": 2.8, "width": 25.4, "height": 0.1, "color": "#0F62FE"}
  ],
  "text_boxes": [
    {"x": 0.63, "y": 0.3, "width": 10.0, "height": 0.5, "text": "COMPETITIVE ANALYSIS", "font_size": 10, "bold": true, "color": "#0F62FE"}
  ],
  "table_data": {
    "headers": ["Capability", "IBM + HashiCorp", "Vendor B", "Vendor C", "Open Source DIY"],
    "rows": [
      ["Multi-cloud IaC", "✓", "✓", "✗", "✓"],
      ["Dynamic secrets", "✓", "✗", "✗", "✗"],
      ["Service mesh", "✓", "✗", "✓", "✓"],
      ["Policy as code", "✓", "✓", "✗", "✗"],
      ["Enterprise support", "✓", "✓", "✓", "✗"],
      ["Unified platform", "✓", "✗", "✗", "✗"],
      ["FedRAMP authorized", "✓", "✗", "✓", "✗"],
      ["Self-hosted option", "✓", "✓", "✗", "✓"]
    ]
  },
  "callouts": [{
    "x": 0.63, "y": 12.5, "width": 25.4, "height": 1.5,
    "fill": "#EDF5FF", "border": "#0F62FE", "shadow": true,
    "rich_text": [
      {"text": "Key differentiator: ", "bold": true, "color": "#161616"},
      {"text": "IBM + HashiCorp is the only platform offering unified IaC, secrets, and service mesh with enterprise support and FedRAMP authorization.", "bold": false, "color": "#525252"}
    ]
  }],
  "notes": "Avoid naming specific competitors in public presentations. Use 'Vendor B' and 'Vendor C' placeholders and fill in verbally."
}
```

### Recipe 19: Pros/Cons Split

Two columns with green advantages on left and red considerations on right. Use for balanced evaluations, trade-off discussions, and decision support.

```json
{
  "layout": 45,
  "title": "",
  "background": "gray_10",
  "text_boxes": [
    {"x": 0.63, "y": 0.5, "width": 20.0, "height": 1.5, "text": "Multi-cloud strategy trade-offs", "font_size": 48, "bold": true, "color": "#161616", "font": "IBM Plex Sans Light"},
    {"x": 0.63, "y": 1.7, "width": 20.0, "height": 1.0, "text": "Key factors for your multi-cloud decision", "font_size": 22, "color": "#525252"}
  ],
  "cards": [
    {
      "x": 0.63, "y": 2.5, "width": 12.2, "height": 9.5,
      "fill": "#F0FFF4", "accent_color": "#198038",
      "title": "Advantages",
      "body": ["✓ Avoid vendor lock-in and negotiate better pricing", "✓ Best-of-breed services from each cloud provider", "✓ Geographic redundancy and disaster recovery", "✓ Regulatory compliance across jurisdictions", "✓ Leverage team expertise across platforms"],
      "shadow": true, "corner_radius": 0.15
    },
    {
      "x": 13.73, "y": 2.5, "width": 12.2, "height": 9.5,
      "fill": "#FFF0F0", "accent_color": "#DA1E28",
      "title": "Considerations",
      "body": ["✗ Increased operational complexity", "✗ Higher tooling and training costs", "✗ Network latency between providers", "✗ Inconsistent security policies", "✗ Requires mature platform engineering team"],
      "shadow": true, "corner_radius": 0.15
    }
  ],
  "callouts": [{
    "x": 0.63, "y": 12.5, "width": 25.4, "height": 1.5,
    "fill": "#EDF5FF", "border": "#0F62FE", "shadow": true,
    "rich_text": [
      {"text": "IBM perspective: ", "bold": true, "color": "#161616"},
      {"text": "Terraform and Consul eliminate the top three considerations by providing a unified control plane across all cloud providers.", "bold": false, "color": "#525252"}
    ]
  }],
  "notes": "Be honest about trade-offs -- it builds trust. Then show how IBM addresses each consideration."
}
```

### Recipe 20: Icon Feature Grid

2x3 grid of icon badges with labels and descriptions. Use for feature overviews, capability catalogs, and product highlights where each item deserves equal visual weight.

```json
{
  "layout": 45,
  "title": "",
  "background": "cyan_10",
  "text_boxes": [
    {"x": 0.63, "y": 0.5, "width": 20.0, "height": 1.5, "text": "Platform capabilities at a glance", "font_size": 48, "bold": true, "color": "#161616", "font": "IBM Plex Sans Light"},
    {"x": 0.63, "y": 1.7, "width": 20.0, "height": 1.0, "text": "Six core capabilities that power modern infrastructure", "font_size": 22, "color": "#525252"},
    {"x": 3.0, "y": 3.0, "width": 5.5, "height": 0.8, "text": "Provisioning", "font_size": 24, "bold": true, "color": "#161616"},
    {"x": 3.0, "y": 3.7, "width": 5.5, "height": 1.5, "text": "Declarative IaC with plan, apply, and destroy lifecycle management", "font_size": 18, "color": "#525252"},
    {"x": 11.6, "y": 3.0, "width": 5.5, "height": 0.8, "text": "Secrets", "font_size": 24, "bold": true, "color": "#161616"},
    {"x": 11.6, "y": 3.7, "width": 5.5, "height": 1.5, "text": "Dynamic secret generation with automatic rotation and revocation", "font_size": 18, "color": "#525252"},
    {"x": 20.2, "y": 3.0, "width": 5.5, "height": 0.8, "text": "Networking", "font_size": 24, "bold": true, "color": "#161616"},
    {"x": 20.2, "y": 3.7, "width": 5.5, "height": 1.5, "text": "Service mesh with automatic mTLS and traffic management", "font_size": 18, "color": "#525252"},
    {"x": 3.0, "y": 8.0, "width": 5.5, "height": 0.8, "text": "Orchestration", "font_size": 24, "bold": true, "color": "#161616"},
    {"x": 3.0, "y": 8.7, "width": 5.5, "height": 1.5, "text": "Workload scheduling across regions with bin-packing and affinity", "font_size": 18, "color": "#525252"},
    {"x": 11.6, "y": 8.0, "width": 5.5, "height": 0.8, "text": "Imaging", "font_size": 24, "bold": true, "color": "#161616"},
    {"x": 11.6, "y": 8.7, "width": 5.5, "height": 1.5, "text": "Automated machine image builds for every cloud and hypervisor", "font_size": 18, "color": "#525252"},
    {"x": 20.2, "y": 8.0, "width": 5.5, "height": 0.8, "text": "Access", "font_size": 24, "bold": true, "color": "#161616"},
    {"x": 20.2, "y": 8.7, "width": 5.5, "height": 1.5, "text": "Identity-based access to hosts and services with session recording", "font_size": 18, "color": "#525252"}
  ],
  "visuals": [
    {"type": "icon_badge", "number": 1, "color": "#A56EFF", "x": 0.63, "y": 3.0, "width": 2.0, "height": 2.0},
    {"type": "icon_badge", "number": 2, "color": "#F1C21B", "x": 9.23, "y": 3.0, "width": 2.0, "height": 2.0},
    {"type": "icon_badge", "number": 3, "color": "#EE5396", "x": 17.83, "y": 3.0, "width": 2.0, "height": 2.0},
    {"type": "icon_badge", "number": 4, "color": "#24A148", "x": 0.63, "y": 8.0, "width": 2.0, "height": 2.0},
    {"type": "icon_badge", "number": 5, "color": "#1192E8", "x": 9.23, "y": 8.0, "width": 2.0, "height": 2.0},
    {"type": "icon_badge", "number": 6, "color": "#FA4D56", "x": 17.83, "y": 8.0, "width": 2.0, "height": 2.0}
  ],
  "notes": "Each capability maps to a HashiCorp product. Use this as an overview before diving into individual product slides."
}
```

### Recipe 21: Architecture Diagram

A layered architecture visualization using native shapes. Each layer is a horizontal band with labeled components. Use this instead of a placeholder for architecture slides.

```json
{
  "layout": 45,
  "background": "white",
  "text_boxes": [
    {"x": 0.63, "y": 0.3, "width": 10.0, "height": 0.5, "text": "REFERENCE ARCHITECTURE", "font_size": 18, "bold": true, "color": "#0F62FE"},
    {"x": 0.63, "y": 0.8, "width": 20.0, "height": 1.2, "text": "HashiCorp stack on IBM Cloud", "font_size": 44, "bold": true, "color": "#161616", "font": "IBM Plex Sans Light"}
  ],
  "visuals": [
    {
      "type": "architecture_diagram",
      "x": 0.63, "y": 2.5, "width": 25.4, "height": 11.0,
      "layers": [
        {"label": "Applications", "color": "#0F62FE", "items": ["Web Apps", "APIs", "Batch Jobs", "Microservices"]},
        {"label": "Orchestration", "color": "#24A148", "items": ["Nomad Scheduler", "Task Drivers", "Allocations"]},
        {"label": "Networking", "color": "#EE5396", "items": ["Consul Connect", "Service Mesh", "Health Checks", "DNS"]},
        {"label": "Security", "color": "#F1C21B", "items": ["Vault Secrets", "PKI Certs", "Transit Encrypt", "Auth Methods"]},
        {"label": "Infrastructure", "color": "#A56EFF", "items": ["Terraform IaC", "IBM VPC", "IBM IKS", "IBM Cloud DBs"]}
      ],
      "connectors": true
    }
  ]
}
```

Each layer renders as a full-width band with a colored accent bar on the left, layer label, and component boxes arranged horizontally. Vertical connectors link layers to show the dependency flow. All text is editable.

### Recipe 22: Full-Width Bar Chart

A visualization-dominant slide showing a horizontal_bars chart spanning most of the slide width. Use for rankings, survey results, or adoption data.

```json
{
  "layout": 45,
  "background": "white",
  "text_boxes": [
    {"x": 0.63, "y": 0.3, "width": 10.0, "height": 0.5, "text": "ADOPTION METRICS", "font_size": 18, "bold": true, "color": "#0F62FE"},
    {"x": 0.63, "y": 0.8, "width": 20.0, "height": 1.2, "text": "HashiCorp product adoption across enterprise", "font_size": 44, "bold": true, "color": "#161616", "font": "IBM Plex Sans Light"}
  ],
  "visuals": [
    {
      "type": "horizontal_bars",
      "x": 0.63, "y": 2.5, "width": 25.4, "height": 9.0,
      "data": [
        {"label": "Terraform", "value": 89, "color": "#A56EFF"},
        {"label": "Vault", "value": 72, "color": "#F1C21B"},
        {"label": "Consul", "value": 58, "color": "#EE5396"},
        {"label": "Packer", "value": 45, "color": "#1192E8"},
        {"label": "Nomad", "value": 34, "color": "#24A148"},
        {"label": "Boundary", "value": 22, "color": "#FA4D56"}
      ],
      "max_value": 100
    }
  ],
  "callouts": [
    {"x": 0.63, "y": 12.0, "width": 25.4, "height": 1.5, "fill": "#EDF5FF", "border": "#0F62FE", "shadow": true, "rich_text": [
      {"text": "Source: ", "bold": true, "color": "#161616"},
      {"text": "HashiCorp 2025 State of Cloud Strategy Survey, n=3,500 respondents", "color": "#525252"}
    ]}
  ]
}
```

### Recipe 23: Progress Ring Dashboard

Three or four progress rings with labels showing maturity or completion across dimensions. Visualization-dominant slide.

```json
{
  "layout": 45,
  "background": "gray_10",
  "text_boxes": [
    {"x": 0.63, "y": 0.3, "width": 10.0, "height": 0.5, "text": "MATURITY ASSESSMENT", "font_size": 18, "bold": true, "color": "#0F62FE"},
    {"x": 0.63, "y": 0.8, "width": 20.0, "height": 1.2, "text": "Cloud infrastructure automation readiness", "font_size": 44, "bold": true, "color": "#161616", "font": "IBM Plex Sans Light"},
    {"x": 1.0, "y": 8.8, "width": 5.5, "height": 0.8, "text": "Provisioning", "font_size": 22, "bold": true, "color": "#161616", "align": "center"},
    {"x": 7.5, "y": 8.8, "width": 5.5, "height": 0.8, "text": "Security", "font_size": 22, "bold": true, "color": "#161616", "align": "center"},
    {"x": 14.0, "y": 8.8, "width": 5.5, "height": 0.8, "text": "Networking", "font_size": 22, "bold": true, "color": "#161616", "align": "center"},
    {"x": 20.5, "y": 8.8, "width": 5.5, "height": 0.8, "text": "Orchestration", "font_size": 22, "bold": true, "color": "#161616", "align": "center"},
    {"x": 1.0, "y": 9.5, "width": 5.5, "height": 1.0, "text": "Terraform adoption at scale", "font_size": 16, "color": "#525252", "align": "center"},
    {"x": 7.5, "y": 9.5, "width": 5.5, "height": 1.0, "text": "Vault secrets management", "font_size": 16, "color": "#525252", "align": "center"},
    {"x": 14.0, "y": 9.5, "width": 5.5, "height": 1.0, "text": "Consul service mesh", "font_size": 16, "color": "#525252", "align": "center"},
    {"x": 20.5, "y": 9.5, "width": 5.5, "height": 1.0, "text": "Nomad workload scheduler", "font_size": 16, "color": "#525252", "align": "center"}
  ],
  "visuals": [
    {"type": "progress_ring", "value": 85, "max": 100, "color": "#0F62FE", "x": 1.0, "y": 3.0, "width": 5.5, "height": 5.5},
    {"type": "progress_ring", "value": 62, "max": 100, "color": "#A56EFF", "x": 7.5, "y": 3.0, "width": 5.5, "height": 5.5},
    {"type": "progress_ring", "value": 45, "max": 100, "color": "#009D9A", "x": 14.0, "y": 3.0, "width": 5.5, "height": 5.5},
    {"type": "progress_ring", "value": 28, "max": 100, "color": "#24A148", "x": 20.5, "y": 3.0, "width": 5.5, "height": 5.5}
  ]
}
```

### Recipe 24: Half-Image Feature Slide

A content slide with brand photography on one side and feature text on the other. Uses the `overlays` field for the image.

```json
{
  "layout": 45,
  "background": "white",
  "overlays": [
    {"image": "resources/images/pptx_image22.png", "x": 0.0, "y": 0.0, "width": 13.33, "height": 15.0}
  ],
  "text_boxes": [
    {"x": 14.0, "y": 0.5, "width": 12.0, "height": 0.6, "text": "ENTERPRISE READY", "font_size": 18, "bold": true, "color": "#0F62FE"},
    {"x": 14.0, "y": 1.2, "width": 12.0, "height": 1.5, "text": "Built for scale", "font_size": 44, "bold": true, "color": "#161616", "font": "IBM Plex Sans Light"}
  ],
  "cards": [
    {"x": 14.0, "y": 3.0, "width": 12.0, "height": 3.5, "fill": "#F4F4F4", "accent_color": "#0F62FE", "title": "Multi-cloud support", "body": ["AWS, Azure, GCP, and IBM Cloud", "Single workflow across all providers", "Consistent governance everywhere"], "shadow": true},
    {"x": 14.0, "y": 7.0, "width": 12.0, "height": 3.5, "fill": "#F4F4F4", "accent_color": "#A56EFF", "title": "Enterprise controls", "body": ["Policy as code with Sentinel", "SSO and RBAC integration", "Audit logging and compliance"], "shadow": true}
  ]
}
```

### Recipe 25: Pictogram Feature Grid

A 2×3 grid using actual IBM Carbon pictograms from the resources directory. Each cell has a pictogram icon, a bold label, and description text.

```json
{
  "layout": 45,
  "background": "gray_10",
  "text_boxes": [
    {"x": 0.63, "y": 0.3, "width": 10.0, "height": 0.5, "text": "CAPABILITIES", "font_size": 18, "bold": true, "color": "#0F62FE"},
    {"x": 0.63, "y": 0.8, "width": 20.0, "height": 1.2, "text": "Enterprise platform features", "font_size": 44, "bold": true, "color": "#161616", "font": "IBM Plex Sans Light"},
    {"x": 2.5, "y": 4.0, "width": 6.0, "height": 0.6, "text": "Team collaboration", "font_size": 22, "bold": true, "color": "#161616"},
    {"x": 2.5, "y": 4.6, "width": 6.0, "height": 1.0, "text": "Workspaces, RBAC, and shared state for team productivity", "font_size": 16, "color": "#525252"},
    {"x": 10.8, "y": 4.0, "width": 6.0, "height": 0.6, "text": "Workflow automation", "font_size": 22, "bold": true, "color": "#161616"},
    {"x": 10.8, "y": 4.6, "width": 6.0, "height": 1.0, "text": "CI/CD integration, auto-apply, and drift detection", "font_size": 16, "color": "#525252"},
    {"x": 19.1, "y": 4.0, "width": 6.0, "height": 0.6, "text": "Network security", "font_size": 22, "bold": true, "color": "#161616"},
    {"x": 19.1, "y": 4.6, "width": 6.0, "height": 1.0, "text": "Service mesh, mTLS, and zero-trust networking", "font_size": 16, "color": "#525252"},
    {"x": 2.5, "y": 8.5, "width": 6.0, "height": 0.6, "text": "Cost management", "font_size": 22, "bold": true, "color": "#161616"},
    {"x": 2.5, "y": 9.1, "width": 6.0, "height": 1.0, "text": "Resource tagging, budget alerts, and optimization insights", "font_size": 16, "color": "#525252"},
    {"x": 10.8, "y": 8.5, "width": 6.0, "height": 0.6, "text": "Leadership visibility", "font_size": 22, "bold": true, "color": "#161616"},
    {"x": 10.8, "y": 9.1, "width": 6.0, "height": 1.0, "text": "Executive dashboards, compliance reporting, risk scoring", "font_size": 16, "color": "#525252"},
    {"x": 19.1, "y": 8.5, "width": 6.0, "height": 0.6, "text": "Analytics insights", "font_size": 22, "bold": true, "color": "#161616"},
    {"x": 19.1, "y": 9.1, "width": 6.0, "height": 1.0, "text": "Usage trends, deployment metrics, and capacity planning", "font_size": 16, "color": "#525252"}
  ],
  "overlays": [
    {"image": "resources/icons/pptx_image78.png", "x": 1.0, "y": 2.8, "width": 1.33, "height": 1.33},
    {"image": "resources/icons/pptx_image72.png", "x": 9.3, "y": 2.8, "width": 1.33, "height": 1.33},
    {"image": "resources/icons/pptx_image74.png", "x": 17.6, "y": 2.8, "width": 1.33, "height": 1.33},
    {"image": "resources/icons/pptx_image76.png", "x": 1.0, "y": 7.3, "width": 1.33, "height": 1.33},
    {"image": "resources/icons/pptx_image70.png", "x": 9.3, "y": 7.3, "width": 1.33, "height": 1.33},
    {"image": "resources/icons/pptx_image80.png", "x": 17.6, "y": 7.3, "width": 1.33, "height": 1.33}
  ]
}
```

### Recipe 26: Two-Row Stat Banner

Two horizontal stat rows spanning the slide width. Each row has 3 metrics side by side. No cards -- just accent bars, big numbers, and labels. Use for executive summary dashboards and high-level KPI overviews.

```json
{
  "layout": 45,
  "title": "",
  "background": "white",
  "text_boxes": [
    {"x": 0.63, "y": 0.3, "width": 10.0, "height": 0.5, "text": "EXECUTIVE DASHBOARD", "font_size": 18, "bold": true, "color": "#0F62FE"},
    {"x": 0.63, "y": 0.8, "width": 20.0, "height": 1.2, "text": "Key performance indicators", "font_size": 44, "bold": true, "color": "#161616", "font": "IBM Plex Sans Light"},
    {"x": 0.63, "y": 3.2, "width": 8.0, "height": 1.5, "text": "85%", "font_size": 72, "bold": true, "color": "#0F62FE", "align": "center"},
    {"x": 0.63, "y": 4.7, "width": 8.0, "height": 0.8, "text": "Faster provisioning", "font_size": 20, "color": "#525252", "align": "center"},
    {"x": 9.33, "y": 3.2, "width": 8.0, "height": 1.5, "text": "3.2x", "font_size": 72, "bold": true, "color": "#A56EFF", "align": "center"},
    {"x": 9.33, "y": 4.7, "width": 8.0, "height": 0.8, "text": "Developer productivity", "font_size": 20, "color": "#525252", "align": "center"},
    {"x": 18.03, "y": 3.2, "width": 8.0, "height": 1.5, "text": "$4.2M", "font_size": 72, "bold": true, "color": "#009D9A", "align": "center"},
    {"x": 18.03, "y": 4.7, "width": 8.0, "height": 0.8, "text": "Annual savings", "font_size": 20, "color": "#525252", "align": "center"},
    {"x": 0.63, "y": 8.2, "width": 8.0, "height": 1.5, "text": "99.9%", "font_size": 72, "bold": true, "color": "#24A148", "align": "center"},
    {"x": 0.63, "y": 9.7, "width": 8.0, "height": 0.8, "text": "Platform uptime", "font_size": 20, "color": "#525252", "align": "center"},
    {"x": 9.33, "y": 8.2, "width": 8.0, "height": 1.5, "text": "12K", "font_size": 72, "bold": true, "color": "#EE5396", "align": "center"},
    {"x": 9.33, "y": 9.7, "width": 8.0, "height": 0.8, "text": "Secrets rotated daily", "font_size": 20, "color": "#525252", "align": "center"},
    {"x": 18.03, "y": 8.2, "width": 8.0, "height": 1.5, "text": "200+", "font_size": 72, "bold": true, "color": "#F1C21B", "align": "center"},
    {"x": 18.03, "y": 9.7, "width": 8.0, "height": 0.8, "text": "Enterprise customers", "font_size": 20, "color": "#525252", "align": "center"}
  ],
  "accent_bars": [
    {"x": 0.63, "y": 2.8, "width": 8.0, "height": 0.12, "color": "#0F62FE"},
    {"x": 9.33, "y": 2.8, "width": 8.0, "height": 0.12, "color": "#A56EFF"},
    {"x": 18.03, "y": 2.8, "width": 8.0, "height": 0.12, "color": "#009D9A"},
    {"x": 0.63, "y": 7.8, "width": 8.0, "height": 0.12, "color": "#24A148"},
    {"x": 9.33, "y": 7.8, "width": 8.0, "height": 0.12, "color": "#EE5396"},
    {"x": 18.03, "y": 7.8, "width": 8.0, "height": 0.12, "color": "#F1C21B"}
  ],
  "dividers": [
    {"x": 8.98, "y": 2.8, "length": 8.5, "orientation": "vertical", "color": "#E0E0E0"},
    {"x": 17.68, "y": 2.8, "length": 8.5, "orientation": "vertical", "color": "#E0E0E0"}
  ],
  "callouts": [{
    "x": 0.63, "y": 12.5, "width": 25.4, "height": 1.5,
    "fill": "#EDF5FF", "border": "#0F62FE", "shadow": true,
    "rich_text": [
      {"text": "Source: ", "bold": true, "color": "#161616"},
      {"text": "IBM internal benchmarks across 200+ enterprise deployments, FY2025.", "bold": false, "color": "#525252"}
    ]
  }],
  "notes": "Let the numbers speak for themselves. Pause on this slide to let the audience absorb the metrics."
}
```

### Recipe 27: Timeline Roadmap

Horizontal timeline with 4-5 milestone markers (circles on a line) with labels above and descriptions below. Use icon_badge for milestones connected by a horizontal divider line. Use for product roadmaps, project milestones, and release planning.

```json
{
  "layout": 45,
  "title": "",
  "background": "gray_10",
  "text_boxes": [
    {"x": 0.63, "y": 0.3, "width": 10.0, "height": 0.5, "text": "PRODUCT ROADMAP", "font_size": 18, "bold": true, "color": "#0F62FE"},
    {"x": 0.63, "y": 0.8, "width": 20.0, "height": 1.2, "text": "2026 infrastructure platform milestones", "font_size": 44, "bold": true, "color": "#161616", "font": "IBM Plex Sans Light"},
    {"x": 1.0, "y": 3.5, "width": 4.5, "height": 0.7, "text": "Q1 2026", "font_size": 22, "bold": true, "color": "#0F62FE", "align": "center"},
    {"x": 6.5, "y": 3.5, "width": 4.5, "height": 0.7, "text": "Q2 2026", "font_size": 22, "bold": true, "color": "#A56EFF", "align": "center"},
    {"x": 12.0, "y": 3.5, "width": 4.5, "height": 0.7, "text": "Q3 2026", "font_size": 22, "bold": true, "color": "#009D9A", "align": "center"},
    {"x": 17.5, "y": 3.5, "width": 4.5, "height": 0.7, "text": "Q4 2026", "font_size": 22, "bold": true, "color": "#24A148", "align": "center"},
    {"x": 23.0, "y": 3.5, "width": 3.5, "height": 0.7, "text": "2027", "font_size": 22, "bold": true, "color": "#EE5396", "align": "center"},
    {"x": 1.0, "y": 7.0, "width": 4.5, "height": 0.6, "text": "Foundation", "font_size": 20, "bold": true, "color": "#161616", "align": "center"},
    {"x": 1.0, "y": 7.6, "width": 4.5, "height": 1.5, "text": "Terraform Cloud migration complete. Core module library published.", "font_size": 16, "color": "#525252", "align": "center"},
    {"x": 6.5, "y": 7.0, "width": 4.5, "height": 0.6, "text": "Security layer", "font_size": 20, "bold": true, "color": "#161616", "align": "center"},
    {"x": 6.5, "y": 7.6, "width": 4.5, "height": 1.5, "text": "Vault integration live. Dynamic secrets for all workloads.", "font_size": 16, "color": "#525252", "align": "center"},
    {"x": 12.0, "y": 7.0, "width": 4.5, "height": 0.6, "text": "Service mesh", "font_size": 20, "bold": true, "color": "#161616", "align": "center"},
    {"x": 12.0, "y": 7.6, "width": 4.5, "height": 1.5, "text": "Consul Connect deployed. Zero-trust networking enabled.", "font_size": 16, "color": "#525252", "align": "center"},
    {"x": 17.5, "y": 7.0, "width": 4.5, "height": 0.6, "text": "Full automation", "font_size": 20, "bold": true, "color": "#161616", "align": "center"},
    {"x": 17.5, "y": 7.6, "width": 4.5, "height": 1.5, "text": "Self-service portal live. Policy as code enforced.", "font_size": 16, "color": "#525252", "align": "center"},
    {"x": 23.0, "y": 7.0, "width": 3.5, "height": 0.6, "text": "AI-driven ops", "font_size": 20, "bold": true, "color": "#161616", "align": "center"},
    {"x": 23.0, "y": 7.6, "width": 3.5, "height": 1.5, "text": "Predictive scaling and auto-remediation.", "font_size": 16, "color": "#525252", "align": "center"}
  ],
  "visuals": [
    {"type": "icon_badge", "number": 1, "color": "#0F62FE", "x": 2.5, "y": 4.5, "width": 1.5, "height": 1.5},
    {"type": "icon_badge", "number": 2, "color": "#A56EFF", "x": 8.0, "y": 4.5, "width": 1.5, "height": 1.5},
    {"type": "icon_badge", "number": 3, "color": "#009D9A", "x": 13.5, "y": 4.5, "width": 1.5, "height": 1.5},
    {"type": "icon_badge", "number": 4, "color": "#24A148", "x": 19.0, "y": 4.5, "width": 1.5, "height": 1.5},
    {"type": "icon_badge", "number": 5, "color": "#EE5396", "x": 24.0, "y": 4.5, "width": 1.5, "height": 1.5}
  ],
  "dividers": [
    {"x": 1.0, "y": 5.25, "length": 25.0, "orientation": "horizontal", "color": "#C6C6C6"}
  ],
  "accent_bars": [
    {"x": 0.63, "y": 6.5, "width": 25.4, "height": 0.08, "color": "#0F62FE"}
  ],
  "notes": "Walk through each milestone. Emphasize that each quarter builds on the previous -- this is a cumulative journey."
}
```

### Recipe 28: Split Image + Stats

Left half: brand photography overlay. Right half: 3 stacked stat_card visuals with trend arrows. Good for customer success slides and case study highlights.

```json
{
  "layout": 45,
  "title": "",
  "background": "white",
  "overlays": [
    {"image": "resources/images/pptx_image22.png", "x": 0.0, "y": 0.0, "width": 13.33, "height": 15.0}
  ],
  "text_boxes": [
    {"x": 14.0, "y": 0.3, "width": 12.0, "height": 0.5, "text": "CUSTOMER SUCCESS", "font_size": 18, "bold": true, "color": "#0F62FE"},
    {"x": 14.0, "y": 0.8, "width": 12.0, "height": 1.2, "text": "Global bank transformation", "font_size": 44, "bold": true, "color": "#161616", "font": "IBM Plex Sans Light"}
  ],
  "visuals": [
    {"type": "stat_card", "value": "92%", "label": "Faster deployments", "color": "#0F62FE", "trend": "up", "trend_value": "+47%", "x": 14.0, "y": 2.5, "width": 12.0, "height": 3.0},
    {"type": "stat_card", "value": "$8.5M", "label": "Annual cost savings", "color": "#24A148", "trend": "up", "trend_value": "+$2.1M", "x": 14.0, "y": 6.0, "width": 12.0, "height": 3.0},
    {"type": "stat_card", "value": "Zero", "label": "Credential breaches since adoption", "color": "#009D9A", "trend": "stable", "trend_value": "18 months", "x": 14.0, "y": 9.5, "width": 12.0, "height": 3.0}
  ],
  "callouts": [{
    "x": 14.0, "y": 13.0, "width": 12.0, "height": 1.2,
    "fill": "#EDF5FF", "border": "#0F62FE", "shadow": true,
    "rich_text": [
      {"text": "Industry: ", "bold": true, "color": "#161616"},
      {"text": "Financial services | 50,000+ employees | Multi-cloud", "bold": false, "color": "#525252"}
    ]
  }],
  "notes": "This is a real customer story. Use specific numbers to build credibility. The photo adds a human element."
}
```

### Recipe 29: Centered Donut + Legend Cards

Large centered donut_chart (8"x8") with 3-4 small legend cards arranged around it explaining each segment. Use for budget allocation, resource distribution, and portfolio breakdowns.

```json
{
  "layout": 45,
  "title": "",
  "background": "cyan_10",
  "text_boxes": [
    {"x": 0.63, "y": 0.3, "width": 10.0, "height": 0.5, "text": "BUDGET ALLOCATION", "font_size": 18, "bold": true, "color": "#0F62FE"},
    {"x": 0.63, "y": 0.8, "width": 20.0, "height": 1.2, "text": "Infrastructure automation investment", "font_size": 44, "bold": true, "color": "#161616", "font": "IBM Plex Sans Light"}
  ],
  "visuals": [
    {
      "type": "donut_chart", "x": 9.33, "y": 3.0, "width": 8.0, "height": 8.0,
      "segments": [
        {"label": "Platform licenses", "value": 40, "color": "#0F62FE"},
        {"label": "Professional services", "value": 25, "color": "#A56EFF"},
        {"label": "Training", "value": 20, "color": "#009D9A"},
        {"label": "Support", "value": 15, "color": "#F1C21B"}
      ],
      "hole_size": 0.55, "center_label": "$2.4M", "show_legend": false
    }
  ],
  "cards": [
    {
      "x": 0.63, "y": 3.0, "width": 8.0, "height": 2.5,
      "fill": "#FFFFFF", "accent_color": "#0F62FE",
      "title": "Platform licenses (40%)",
      "body": "Terraform Cloud, Vault Enterprise, and Consul licenses",
      "shadow": true, "corner_radius": 0.15
    },
    {
      "x": 0.63, "y": 6.0, "width": 8.0, "height": 2.5,
      "fill": "#FFFFFF", "accent_color": "#A56EFF",
      "title": "Professional services (25%)",
      "body": "IBM consulting for architecture design and migration support",
      "shadow": true, "corner_radius": 0.15
    },
    {
      "x": 18.03, "y": 3.0, "width": 8.0, "height": 2.5,
      "fill": "#FFFFFF", "accent_color": "#009D9A",
      "title": "Training (20%)",
      "body": "Team enablement, certification programs, and workshops",
      "shadow": true, "corner_radius": 0.15
    },
    {
      "x": 18.03, "y": 6.0, "width": 8.0, "height": 2.5,
      "fill": "#FFFFFF", "accent_color": "#F1C21B",
      "title": "Support (15%)",
      "body": "24x7 enterprise support with dedicated technical account manager",
      "shadow": true, "corner_radius": 0.15
    }
  ],
  "callouts": [{
    "x": 0.63, "y": 12.5, "width": 25.4, "height": 1.5,
    "fill": "#EDF5FF", "border": "#0F62FE", "shadow": true,
    "rich_text": [
      {"text": "ROI insight: ", "bold": true, "color": "#161616"},
      {"text": "Typical payback period of 9-12 months based on operational efficiency gains and reduced incident costs.", "bold": false, "color": "#525252"}
    ]
  }],
  "notes": "The donut chart shows the investment breakdown. Emphasize that training and services accelerate time-to-value."
}
```

### Recipe 30: Full-Width Process Flow

Process flow spanning the entire slide width at 25.4" with 5-6 steps. No cards below -- the flow IS the content. Thick arrows, large labels. Use for end-to-end workflows, CI/CD pipelines, and operational processes.

```json
{
  "layout": 45,
  "title": "",
  "background": "white",
  "text_boxes": [
    {"x": 0.63, "y": 0.3, "width": 10.0, "height": 0.5, "text": "CI/CD PIPELINE", "font_size": 18, "bold": true, "color": "#0F62FE"},
    {"x": 0.63, "y": 0.8, "width": 20.0, "height": 1.2, "text": "End-to-end infrastructure delivery", "font_size": 44, "bold": true, "color": "#161616", "font": "IBM Plex Sans Light"},
    {"x": 0.63, "y": 7.5, "width": 4.0, "height": 0.6, "text": "Code commit", "font_size": 18, "bold": true, "color": "#161616", "align": "center"},
    {"x": 0.63, "y": 8.1, "width": 4.0, "height": 1.5, "text": "Developer pushes IaC changes to version control with PR review", "font_size": 14, "color": "#525252", "align": "center"},
    {"x": 5.33, "y": 7.5, "width": 4.0, "height": 0.6, "text": "Plan", "font_size": 18, "bold": true, "color": "#161616", "align": "center"},
    {"x": 5.33, "y": 8.1, "width": 4.0, "height": 1.5, "text": "Terraform generates execution plan showing proposed changes", "font_size": 14, "color": "#525252", "align": "center"},
    {"x": 10.03, "y": 7.5, "width": 4.0, "height": 0.6, "text": "Policy check", "font_size": 18, "bold": true, "color": "#161616", "align": "center"},
    {"x": 10.03, "y": 8.1, "width": 4.0, "height": 1.5, "text": "Sentinel policies validate compliance, cost, and security rules", "font_size": 14, "color": "#525252", "align": "center"},
    {"x": 14.73, "y": 7.5, "width": 4.0, "height": 0.6, "text": "Approve", "font_size": 18, "bold": true, "color": "#161616", "align": "center"},
    {"x": 14.73, "y": 8.1, "width": 4.0, "height": 1.5, "text": "Team lead reviews and approves the plan for production apply", "font_size": 14, "color": "#525252", "align": "center"},
    {"x": 19.43, "y": 7.5, "width": 4.0, "height": 0.6, "text": "Apply", "font_size": 18, "bold": true, "color": "#161616", "align": "center"},
    {"x": 19.43, "y": 8.1, "width": 4.0, "height": 1.5, "text": "Terraform provisions resources and updates state file", "font_size": 14, "color": "#525252", "align": "center"},
    {"x": 22.63, "y": 7.5, "width": 4.0, "height": 0.6, "text": "Monitor", "font_size": 18, "bold": true, "color": "#161616", "align": "center"},
    {"x": 22.63, "y": 8.1, "width": 4.0, "height": 1.5, "text": "Drift detection alerts on unauthorized changes", "font_size": 14, "color": "#525252", "align": "center"}
  ],
  "visuals": [
    {
      "type": "process_flow", "x": 0.63, "y": 2.5, "width": 25.4, "height": 4.5,
      "steps": [
        {"label": "Code", "sublabel": "VCS Push", "color": "#0F62FE"},
        {"label": "Plan", "sublabel": "Terraform", "color": "#A56EFF"},
        {"label": "Policy", "sublabel": "Sentinel", "color": "#F1C21B"},
        {"label": "Approve", "sublabel": "Review", "color": "#009D9A"},
        {"label": "Apply", "sublabel": "Provision", "color": "#24A148"},
        {"label": "Monitor", "sublabel": "Drift detect", "color": "#EE5396"}
      ]
    }
  ],
  "callouts": [{
    "x": 0.63, "y": 12.5, "width": 25.4, "height": 1.5,
    "fill": "#F4F4F4", "border": "#525252", "shadow": true,
    "rich_text": [
      {"text": "Automation benefit: ", "bold": true, "color": "#161616"},
      {"text": "Steps 2-6 are fully automated. Human intervention only required at the approval gate.", "bold": false, "color": "#525252"}
    ]
  }],
  "notes": "Walk through the pipeline left-to-right. Emphasize that the entire flow from commit to monitoring is automated except for the approval step."
}
```

### Recipe 31: Two-Column Bullets with Icons

Two card columns (12" each) where each card has a pictogram icon overlay at the top, a heading, and bullet points. Similar to Recipe 13 but with icons prominent. Use for detailed feature descriptions, platform capabilities, and solution components.

```json
{
  "layout": 45,
  "title": "",
  "background": "gray_10",
  "text_boxes": [
    {"x": 0.63, "y": 0.3, "width": 10.0, "height": 0.5, "text": "PLATFORM OVERVIEW", "font_size": 18, "bold": true, "color": "#0F62FE"},
    {"x": 0.63, "y": 0.8, "width": 20.0, "height": 1.2, "text": "Core platform capabilities", "font_size": 44, "bold": true, "color": "#161616", "font": "IBM Plex Sans Light"}
  ],
  "cards": [
    {
      "x": 0.63, "y": 2.5, "width": 12.2, "height": 5.0,
      "fill": "#FFFFFF", "accent_color": "#A56EFF",
      "title": "Infrastructure as Code",
      "body": ["Declarative configuration language", "Multi-cloud provider support", "Plan and preview before applying", "Module registry for reusable components"],
      "icon": "resources/icons/pptx_image70.png",
      "shadow": true, "corner_radius": 0.15
    },
    {
      "x": 13.73, "y": 2.5, "width": 12.2, "height": 5.0,
      "fill": "#FFFFFF", "accent_color": "#F1C21B",
      "title": "Secrets management",
      "body": ["Dynamic credential generation", "Automatic secret rotation", "Encryption as a service", "Identity-based access policies"],
      "icon": "resources/icons/pptx_image72.png",
      "shadow": true, "corner_radius": 0.15
    },
    {
      "x": 0.63, "y": 8.0, "width": 12.2, "height": 5.0,
      "fill": "#FFFFFF", "accent_color": "#EE5396",
      "title": "Service networking",
      "body": ["Service discovery and health checks", "Automatic mTLS encryption", "Traffic splitting and routing", "Multi-datacenter federation"],
      "icon": "resources/icons/pptx_image74.png",
      "shadow": true, "corner_radius": 0.15
    },
    {
      "x": 13.73, "y": 8.0, "width": 12.2, "height": 5.0,
      "fill": "#FFFFFF", "accent_color": "#24A148",
      "title": "Workload orchestration",
      "body": ["Container and VM scheduling", "Batch job processing", "Multi-region deployments", "Rolling updates with canary support"],
      "icon": "resources/icons/pptx_image78.png",
      "shadow": true, "corner_radius": 0.15
    }
  ],
  "notes": "Each card represents a major platform pillar. Use the icons to create visual anchors for each capability area."
}
```

### Recipe 32: Gradient Hero Text

Dark background (gray_100) slide with a single powerful statement in large 60pt text spanning the width. Thin accent bars above and below. Optional subtitle. No visuals -- text IS the visual. Use for key messages, vision statements, and transition moments.

```json
{
  "layout": 45,
  "title": "",
  "background": "#161616",
  "text_boxes": [
    {"x": 0.63, "y": 0.3, "width": 10.0, "height": 0.5, "text": "OUR VISION", "font_size": 18, "bold": true, "color": "#0F62FE"},
    {"x": 2.0, "y": 4.0, "width": 22.67, "height": 5.0, "text": "Every enterprise deserves infrastructure that is secure by default, automated by design, and scalable without limits.", "font_size": 60, "color": "#FFFFFF", "font": "IBM Plex Sans Light"},
    {"x": 2.0, "y": 9.5, "width": 22.67, "height": 1.5, "text": "The IBM infrastructure platform makes this possible today.", "font_size": 26, "color": "#8D8D8D", "font": "IBM Plex Sans Light"}
  ],
  "accent_bars": [
    {"x": 2.0, "y": 3.5, "width": 22.67, "height": 0.1, "color": "#0F62FE"},
    {"x": 2.0, "y": 11.5, "width": 22.67, "height": 0.1, "color": "#0F62FE"}
  ],
  "visuals": [
    {"type": "gradient_bar", "colors": ["#0F62FE", "#A56EFF", "#009D9A"], "orientation": "horizontal", "corner_radius": 0.0, "x": 2.0, "y": 11.7, "width": 22.67, "height": 0.06}
  ],
  "notes": "Let the statement land. Pause for 3-5 seconds before advancing. The dark background and large text create a cinematic moment."
}
```

### Recipe 33: Metric Comparison Strip

4 or 5 narrow vertical cards side by side (each ~4.5" wide), each showing one metric with an accent-colored top bar, big number, label, and a sparkline below. Good for dashboards, performance tracking, and multi-metric comparisons.

```json
{
  "layout": 45,
  "title": "",
  "background": "white",
  "text_boxes": [
    {"x": 0.63, "y": 0.3, "width": 10.0, "height": 0.5, "text": "PERFORMANCE DASHBOARD", "font_size": 18, "bold": true, "color": "#0F62FE"},
    {"x": 0.63, "y": 0.8, "width": 20.0, "height": 1.2, "text": "Platform health metrics", "font_size": 44, "bold": true, "color": "#161616", "font": "IBM Plex Sans Light"}
  ],
  "cards": [
    {
      "x": 0.63, "y": 2.5, "width": 4.8, "height": 4.5,
      "fill": "#F4F4F4", "accent_color": "#0F62FE",
      "title": "Uptime",
      "body": "99.99%",
      "shadow": true, "corner_radius": 0.15
    },
    {
      "x": 5.93, "y": 2.5, "width": 4.8, "height": 4.5,
      "fill": "#F4F4F4", "accent_color": "#A56EFF",
      "title": "Deployments",
      "body": "1,247",
      "shadow": true, "corner_radius": 0.15
    },
    {
      "x": 11.23, "y": 2.5, "width": 4.8, "height": 4.5,
      "fill": "#F4F4F4", "accent_color": "#009D9A",
      "title": "Mean time to recovery",
      "body": "4.2 min",
      "shadow": true, "corner_radius": 0.15
    },
    {
      "x": 16.53, "y": 2.5, "width": 4.8, "height": 4.5,
      "fill": "#F4F4F4", "accent_color": "#24A148",
      "title": "Cost per deploy",
      "body": "$0.42",
      "shadow": true, "corner_radius": 0.15
    },
    {
      "x": 21.83, "y": 2.5, "width": 4.8, "height": 4.5,
      "fill": "#F4F4F4", "accent_color": "#EE5396",
      "title": "Policy pass rate",
      "body": "98.7%",
      "shadow": true, "corner_radius": 0.15
    }
  ],
  "visuals": [
    {"type": "sparkline", "values": [99.95, 99.97, 99.98, 99.99, 99.99, 99.98, 99.99, 99.99, 100, 99.99, 99.99, 99.99], "color": "#0F62FE", "fill_opacity": 0.15, "show_endpoints": true, "line_width": 2, "x": 0.63, "y": 7.5, "width": 4.8, "height": 3.0},
    {"type": "sparkline", "values": [820, 890, 950, 980, 1020, 1080, 1100, 1150, 1190, 1210, 1230, 1247], "color": "#A56EFF", "fill_opacity": 0.15, "show_endpoints": true, "line_width": 2, "x": 5.93, "y": 7.5, "width": 4.8, "height": 3.0},
    {"type": "sparkline", "values": [12, 10, 8.5, 7.2, 6.1, 5.5, 5.0, 4.8, 4.5, 4.3, 4.2, 4.2], "color": "#009D9A", "fill_opacity": 0.15, "show_endpoints": true, "line_width": 2, "x": 11.23, "y": 7.5, "width": 4.8, "height": 3.0},
    {"type": "sparkline", "values": [1.2, 1.0, 0.85, 0.72, 0.65, 0.58, 0.52, 0.48, 0.45, 0.43, 0.42, 0.42], "color": "#24A148", "fill_opacity": 0.15, "show_endpoints": true, "line_width": 2, "x": 16.53, "y": 7.5, "width": 4.8, "height": 3.0},
    {"type": "sparkline", "values": [92, 93.5, 94.8, 95.5, 96.2, 96.8, 97.1, 97.5, 97.9, 98.2, 98.5, 98.7], "color": "#EE5396", "fill_opacity": 0.15, "show_endpoints": true, "line_width": 2, "x": 21.83, "y": 7.5, "width": 4.8, "height": 3.0}
  ],
  "callouts": [{
    "x": 0.63, "y": 12.5, "width": 25.4, "height": 1.5,
    "fill": "#F4F4F4", "border": "#525252", "shadow": true,
    "rich_text": [
      {"text": "Trend: ", "bold": true, "color": "#161616"},
      {"text": "All five metrics improving month-over-month. Cost per deployment down 65% since platform adoption.", "bold": false, "color": "#525252"}
    ]
  }],
  "notes": "Each column tells a story through the card metric and the sparkline trend below. Point out the improving trajectory across all five dimensions."
}
```

### Recipe 34: Stacked Callout Bars

3-4 full-width callout shapes stacked vertically, each with different tint colors and rich text. Good for key takeaways, agenda items with emphasis, and executive summary points.

```json
{
  "layout": 45,
  "title": "",
  "background": "white",
  "text_boxes": [
    {"x": 0.63, "y": 0.3, "width": 10.0, "height": 0.5, "text": "KEY TAKEAWAYS", "font_size": 18, "bold": true, "color": "#0F62FE"},
    {"x": 0.63, "y": 0.8, "width": 20.0, "height": 1.2, "text": "What you should remember", "font_size": 44, "bold": true, "color": "#161616", "font": "IBM Plex Sans Light"}
  ],
  "callouts": [
    {
      "x": 0.63, "y": 2.5, "width": 25.4, "height": 2.5,
      "fill": "#EDF5FF", "border": "#0F62FE", "shadow": true,
      "font_size": 24, "corner_radius": 0.15,
      "rich_text": [
        {"text": "1. Infrastructure as Code is foundational. ", "bold": true, "color": "#0F62FE"},
        {"text": "Terraform enables consistent, repeatable infrastructure across all cloud providers with a single workflow. Start here.", "bold": false, "color": "#161616"}
      ]
    },
    {
      "x": 0.63, "y": 5.5, "width": 25.4, "height": 2.5,
      "fill": "#F6F2FF", "border": "#A56EFF", "shadow": true,
      "font_size": 24, "corner_radius": 0.15,
      "rich_text": [
        {"text": "2. Secrets management eliminates breaches. ", "bold": true, "color": "#A56EFF"},
        {"text": "Vault replaces static credentials with dynamic, short-lived secrets that are automatically rotated and audited.", "bold": false, "color": "#161616"}
      ]
    },
    {
      "x": 0.63, "y": 8.5, "width": 25.4, "height": 2.5,
      "fill": "#DEFBE6", "border": "#198038", "shadow": true,
      "font_size": 24, "corner_radius": 0.15,
      "rich_text": [
        {"text": "3. Zero trust networking is achievable. ", "bold": true, "color": "#198038"},
        {"text": "Consul Connect provides service mesh with automatic mTLS, removing the need for manual certificate management.", "bold": false, "color": "#161616"}
      ]
    },
    {
      "x": 0.63, "y": 11.5, "width": 25.4, "height": 2.5,
      "fill": "#FFF8E1", "border": "#F1C21B", "shadow": true,
      "font_size": 24, "corner_radius": 0.15,
      "rich_text": [
        {"text": "4. IBM makes it enterprise-ready. ", "bold": true, "color": "#8A6D3B"},
        {"text": "Integrated support, compliance certifications, and professional services accelerate time-to-value.", "bold": false, "color": "#161616"}
      ]
    }
  ],
  "notes": "This is a summary slide. Each callout bar reinforces a key message from the presentation. Use at the end before the closing slide."
}
```

### Recipe 35: Photo Grid with Captions

2x2 grid using brand photography overlays (from resources/images/) with text captions below each photo. Good for team introductions, case studies, and multi-location overviews.

```json
{
  "layout": 45,
  "title": "",
  "background": "gray_10",
  "text_boxes": [
    {"x": 0.63, "y": 0.3, "width": 10.0, "height": 0.5, "text": "OUR TEAM", "font_size": 18, "bold": true, "color": "#0F62FE"},
    {"x": 0.63, "y": 0.8, "width": 20.0, "height": 1.2, "text": "Global infrastructure platform team", "font_size": 44, "bold": true, "color": "#161616", "font": "IBM Plex Sans Light"},
    {"x": 0.63, "y": 8.5, "width": 12.2, "height": 0.7, "text": "Platform engineering", "font_size": 22, "bold": true, "color": "#161616"},
    {"x": 0.63, "y": 9.2, "width": 12.2, "height": 1.0, "text": "Terraform and infrastructure automation specialists based in Austin, TX", "font_size": 16, "color": "#525252"},
    {"x": 13.73, "y": 8.5, "width": 12.2, "height": 0.7, "text": "Security engineering", "font_size": 22, "bold": true, "color": "#161616"},
    {"x": 13.73, "y": 9.2, "width": 12.2, "height": 1.0, "text": "Vault and secrets management experts based in San Francisco, CA", "font_size": 16, "color": "#525252"},
    {"x": 0.63, "y": 13.5, "width": 12.2, "height": 0.7, "text": "Networking team", "font_size": 22, "bold": true, "color": "#161616"},
    {"x": 0.63, "y": 14.2, "width": 12.2, "height": 1.0, "text": "Consul and service mesh architects based in London, UK", "font_size": 16, "color": "#525252"},
    {"x": 13.73, "y": 13.5, "width": 12.2, "height": 0.7, "text": "Solutions architecture", "font_size": 22, "bold": true, "color": "#161616"},
    {"x": 13.73, "y": 14.2, "width": 12.2, "height": 1.0, "text": "Customer-facing solution designers based in New York, NY", "font_size": 16, "color": "#525252"}
  ],
  "overlays": [
    {"image": "resources/images/pptx_image5.png", "x": 0.63, "y": 2.5, "width": 12.2, "height": 5.5},
    {"image": "resources/images/pptx_image22.png", "x": 13.73, "y": 2.5, "width": 12.2, "height": 5.5},
    {"image": "resources/images/pptx_image11.jpg", "x": 0.63, "y": 10.5, "width": 12.2, "height": 2.7},
    {"image": "resources/images/potx_image16.png", "x": 13.73, "y": 10.5, "width": 12.2, "height": 2.7}
  ],
  "accent_bars": [
    {"x": 0.63, "y": 2.3, "width": 12.2, "height": 0.1, "color": "#0F62FE"},
    {"x": 13.73, "y": 2.3, "width": 12.2, "height": 0.1, "color": "#A56EFF"},
    {"x": 0.63, "y": 10.3, "width": 12.2, "height": 0.1, "color": "#009D9A"},
    {"x": 13.73, "y": 10.3, "width": 12.2, "height": 0.1, "color": "#EE5396"}
  ],
  "notes": "Replace placeholder images with actual team photos. Update names, locations, and descriptions to match your team."
}
```

## Available Resources

See `resources/MANIFEST.md` for the full catalog. Most useful assets:

- **25 cover background images** (1920x1080) -- `resources/images/potx_image*.png`
- **6 SVG pictograms with PNG fallbacks** -- `resources/icons/pptx_image7[0-1].png` through `pptx_image81.svg`
- **5 Carbon icons** (SVG + 64x64 PNG) -- `resources/icons/pptx_image89.png` through `pptx_image98.svg`
- **IBM logo** -- `resources/images/potx_image2.png` (1584x632)
- **Brand photography** in portrait, landscape, square, and panoramic sizes

## Brand Asset Usage Rules

Every deck must incorporate brand assets from `resources/` — do not generate decks with only programmatic shapes.

### Cover Slides
Use **layout 0** (Cover, imagery — full-bleed background) for visually impactful covers. Set the `image` field to one of these 1920x1080 backgrounds:
- `resources/images/potx_image16.png` — Technology/abstract (recommended for tech topics)
- `resources/images/potx_image14.png` — Abstract/geometric
- `resources/images/potx_image18.png` — Urban/architecture
- `resources/images/potx_image20.png` — Minimal/clean
- `resources/images/potx_image3.png` — Dark minimal background

**IMPORTANT: Do NOT put pictogram icon overlays on cover slides.** Cover slides should be clean — just the background image, title, and subtitle.

### Section Dividers and Heading Slides — MUST use background images
Section dividers (layout 7), agenda slides (layout 6), and topic heading slides are the MOST visible slides in a deck. They MUST use full-bleed background images — never plain white or solid-color backgrounds. Use layout 45 (blank) with a full-bleed background image overlay instead of layout 7 if needed.

**How to create a visually rich section divider on layout 45:**
1. Add a full-bleed background image via `overlays`: `{"image": "resources/images/potx_imageNN.png", "x": 0, "y": 0, "width": 26.67, "height": 15.0}`
2. **ALWAYS add a dark scrim** for text contrast using the `scrim` field: `{"x": 0, "y": 0, "width": 26.67, "height": 15.0, "color": "#000000", "opacity": 60}` — this creates a semi-transparent dark overlay between the image and text so white text is always readable regardless of image brightness
3. Add the section title as a large text_box with white text (font_size 60, bold)
4. Add a subtitle text_box below (font_size 28, white or light gray)
5. Add a gradient_bar or accent_bar for brand color

**Complete section divider example:**
```json
{
  "layout": 45,
  "overlays": [{"image": "resources/images/potx_image8.png", "x": 0, "y": 0, "width": 26.67, "height": 15.0}],
  "scrim": {"x": 0, "y": 0, "width": 26.67, "height": 15.0, "color": "#000000", "opacity": 60},
  "text_boxes": [
    {"x": 0.63, "y": 5.0, "width": 20.0, "height": 3.0, "text": "Section Title", "font_size": 60, "bold": true, "color": "#FFFFFF"},
    {"x": 0.63, "y": 8.5, "width": 20.0, "height": 1.5, "text": "Subtitle text here", "font_size": 28, "color": "#E0E0E0"}
  ],
  "visuals": [{"type": "gradient_bar", "colors": ["#0043CE", "#0F62FE", "#4589FF"], "x": 0.63, "y": 4.5, "width": 10.0, "height": 0.15}]
}
```

The `scrim` field creates a semi-transparent overlay. Use `opacity: 60` (60% opaque) for most images. For very bright images, increase to `opacity: 70`. The scrim is placed AFTER the image overlay but BEFORE text boxes, ensuring text contrast.

**Background image catalog for section dividers and headings** — use DIFFERENT images throughout the deck, never repeat:

| Image | Style | Best for |
|-------|-------|----------|
| `resources/images/potx_image4.png` | Nature/landscape | Overview, introduction |
| `resources/images/potx_image6.png` | Nature/landscape | Benefits, value |
| `resources/images/potx_image8.png` | Abstract/technology | Technical sections |
| `resources/images/potx_image9.png` | Abstract/architecture | Architecture, design |
| `resources/images/potx_image10.png` | Urban/architecture | Enterprise, scale |
| `resources/images/potx_image11.png` | Landscape | Strategy, vision |
| `resources/images/potx_image12.png` | People/workplace | Team, collaboration |
| `resources/images/potx_image13.png` | Nature | Growth, transformation |
| `resources/images/potx_image15.png` | Abstract | Innovation |
| `resources/images/potx_image17.png` | Abstract | Technology deep dive |
| `resources/images/potx_image19.png` | Urban | Implementation, roadmap |
| `resources/images/potx_image21.png` | Abstract/technology | Security, compliance |
| `resources/images/potx_image22.jpeg` | Landscape | Customer success |
| `resources/images/potx_image23.jpeg` | People/urban | Case studies |
| `resources/images/potx_image24.jpeg` | Nature/aerial | Big picture, strategy |
| `resources/images/potx_image25.jpeg` | Abstract/pattern | Data, analytics |
| `resources/images/potx_image26.jpeg` | Urban/architecture | Infrastructure |
| `resources/images/potx_image27.jpeg` | Abstract | Next steps, call to action |

**Asset usage minimum for section dividers:** In a 30-slide deck with 5-6 sections, each section divider MUST use a different background image. The agenda slide should also use a background image.

### Pictograms on Content Slides ONLY
Use pictogram overlays on feature, comparison, and capability slides — **never on cover, section divider, quote, or end slides**. These PNG pictograms are Carbon Design System style (150-180px):
- `resources/icons/pptx_image70.png` — Project management / team planning
- `resources/icons/pptx_image72.png` — Automation / workflow
- `resources/icons/pptx_image74.png` — Network / connectivity
- `resources/icons/pptx_image76.png` — Finance / currency
- `resources/icons/pptx_image78.png` — Leadership / team
- `resources/icons/pptx_image80.png` — Analytics / charts

Place these via the `overlays` field or as card `icon` values. Size them at 1.5" × 1.5" on the slide. Only use pictograms where they add meaning — match the icon to the content (e.g., network icon on a networking slide, analytics icon on a metrics slide).

### Small Carbon Icons
For smaller icon needs (badges, lists):
- `resources/icons/pptx_image89.png` — Verified / checkmark (64x64)
- `resources/icons/pptx_image91.png` — Network nodes (64x64)
- `resources/icons/pptx_image93.png` — Document (64x64)
- `resources/icons/pptx_image95.png` — Cycle / loop (64x64)
- `resources/icons/pptx_image97.png` — Growth / sprout (64x64)

### Brand Photography
For media slides (layouts 35-39) or half-image covers (layout 4), use:
- `resources/images/pptx_image5.png` — People/workplace (portrait)
- `resources/images/pptx_image11.jpg` — Landscape (wide)
- `resources/images/pptx_image22.png` — Wide format

### IBM Logo
- `resources/images/potx_image2.png` — IBM 8-bar wordmark (1584x632)

### Asset Usage Minimum
- Every deck must use at least **8 background images** (1 cover + 5-6 section dividers + 1-2 content slides)
- Every section divider and heading slide MUST have a full-bleed background image — no plain backgrounds
- Every deck must use at least 3 pictogram overlays on content slides
- Feature/capability slides should always have an icon per feature card
- Use DIFFERENT images throughout — never repeat the same background image in a deck

## Recommended Presentation Structure

Comprehensive decks should be 25-30 slides to provide sufficient depth and visual variety. Shorter decks (10-15 slides) are acceptable for focused topics but must still meet the visual variety minimum.

1. **Cover slide** (layout 0-5) -- title, subtitle, date, author
2. **Agenda / Contents** (layout 6) -- overview of sections
3. **Section dividers** (layout 45 with full-bleed background image overlay) -- between major sections, use a different brand photograph for each section divider with white text overlay and gradient_bar accent
4. **Content slides** (layouts 9-34 or layout 45 with cards) -- main content with visual enhancements
5. **Data / metrics slides** (layout 45 with stat_cards and sparklines, or layouts 11-14) -- statistics, KPIs
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
10. Use cards with shadows on every slide that groups 2+ related items
11. Use text_boxes for titles and subtitles on layout 45 (blank) slides -- the template placeholder is insufficient
12. Use rich_text in callouts for key insights -- never use plain text for important takeaways
