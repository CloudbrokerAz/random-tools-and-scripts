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

Create IBM-branded PowerPoint presentations using python-pptx, following the IBM Design Language and Carbon Design System standards. Presentations use the official IBM POTX template as a base and can leverage all 49 slide layouts.

## How It Works

The skill uses three components:

1. **POTX Template** -- `resources/templates/IBM_presentation_brand_covers_v_2_1_Plex_embed.potx` (base template with IBM Plex Sans embedded)
2. **Builder Script** -- `scripts/build_presentation.py` (programmatic PPTX generation via python-pptx)
3. **Brand Assets** -- `resources/` directory (images, icons, logos, pictograms) -- see `resources/MANIFEST.md` for the full catalog

## Workflow

1. Understand the presentation topic, audience, and length
2. Plan the slide structure (10-20 slides for a standard presentation)
3. Select appropriate layouts for each slide from the 49 available (see reference below)
4. Build a JSON slide specification
5. Run `scripts/build_presentation.py` to generate the PPTX

## Slide Layout Reference

All 49 layouts from the IBM template. Consult this when choosing layouts for each slide.

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

## IBM Design Language Reference

### Color Palette (Carbon Design System)

**Primary:**
- IBM Blue 60: `#0F62FE` (primary brand blue)

**Theme Accents:**
- Purple 50: `#A56EFF`
- Cyan 80: `#003A6D`
- Teal 50: `#009D9A`
- Magenta 70: `#9F1853`
- Red 50: `#FA4D56`

**Backgrounds:**
- White: `#FFFFFF`
- Cyan 10: `#E5F6FF`
- Cyan 20: `#BAE6FF`
- Gray 10: `#F4F4F4`

**Text:**
- Black: `#000000`
- Gray 100: `#161616`
- Gray 90: `#262626`

**Full Gray Scale:** Gray 10 (`#F4F4F4`) through Gray 100 (`#161616`)
**Full Blue Scale:** Blue 10 (`#EDF5FF`) through Blue 100 (`#001141`)

### Typography

All text uses **IBM Plex Sans** (embedded in the template).

| Use | Weight | Size |
|-----|--------|------|
| Display / Hero | Extra Light | 84-168pt |
| Section titles | Light | 86pt |
| Standard titles | Light | ~50pt |
| Body text | Light | 28pt |
| Labels / captions | Regular | 14-16pt |

Rules: always left-aligned, sentence case, no justified text.

### Grid System

| Property | Value |
|----------|-------|
| Content inset from edges | 0.63" |
| Narrow column width | ~5.4" |
| Wide column width | ~12.08" |
| Column positions (left edges) | 0.63", 7.29", 13.96", 20.63" |
| Divider line weight | 1.0pt solid |
| Footer position | 14.02" from top |
| Slide number position | Bottom-right at 25.75" |

## HashiCorp Product Color Mapping

When building slides about HashiCorp products, use the IBM palette equivalents:

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

All HashiCorp products are now part of IBM. Use IBM brand colors rather than original HashiCorp product colors.

## Recommended Presentation Structure

A well-structured IBM presentation follows this pattern:

1. **Cover slide** (layout 0-5) -- title, subtitle, date, author
2. **Agenda / Contents** (layout 6) -- overview of sections
3. **Section dividers** (layout 7) -- between major sections
4. **Content slides** (layouts 9-34) -- main content, use layouts matching the content type
5. **Data / metrics slides** (layouts 11-14) -- statistics, KPIs, benchmarks
6. **Media slides** (layouts 35-39) -- screenshots, architecture diagrams, demos
7. **Contact / team slide** (layout 40) -- if applicable
8. **Legal / disclaimer** (layout 43-44) -- if needed
9. **End slide** (layout 47) -- always close with the IBM logo slide

**Layout selection guidance:**
- Comparing 2-4 items? Use box layouts (26-34)
- Showing a process or feature list? Use text column layouts (15-25)
- Presenting a key stat or quote? Use callout layouts (9-10) or data layouts (11-14)
- Showing a screenshot or diagram? Use media layouts (35-39)
- Need a table or chart? Use layouts 41-42

## Available Resources

See `resources/MANIFEST.md` for the complete asset catalog. Key assets:

- **25 cover background images** (1920x1080) for imagery cover layouts
- **6 Carbon-style SVG pictograms** with PNG fallbacks for column and box layouts
- **5 Carbon Design System icons** (SVG + PNG) for inline use
- **IBM 8-bar logo** in multiple formats (PNG, SVG)
- **18 EMF pictogram vectors** for infographic-style slides
- **Brand photography** in various aspect ratios

## Script Reference

The builder script at `scripts/build_presentation.py` accepts a JSON specification:

```json
{
  "title": "Presentation Title",
  "output_file": "output.pptx",
  "slides": [
    {
      "layout": 0,
      "title": "Title Text",
      "body": ["Body text 1", "Body text 2"],
      "image": "path/to/image.png",
      "notes": "Speaker notes"
    }
  ]
}
```

### Slide Object Fields

| Field | Type | Description |
|-------|------|-------------|
| `layout` | int | Layout index (0-48) from the reference above |
| `title` | string | Slide title text |
| `body` | string[] | Body text areas, mapped to placeholders in order |
| `image` | string | Path to image file (relative to skill root) |
| `notes` | string | Speaker notes for the slide |

### Running the Builder

```bash
# From the skill directory
python scripts/build_presentation.py spec.json

# Or pipe JSON directly
echo '{"title": "Demo", "output_file": "demo.pptx", "slides": [...]}' | python scripts/build_presentation.py -
```

The script loads the POTX template, iterates through the slide specs, applies content to the matching layout placeholders, inserts images, and writes the final PPTX.

## Rules

1. **Always use the IBM POTX template** -- never create presentations from scratch.
2. **Use IBM brand colors only** -- never use original HashiCorp brand colors in IBM-context slides.
3. **Left-align all text** -- no centered or justified text per IBM Design Language.
4. **Sentence case for all headings** -- not Title Case or ALL CAPS.
5. **IBM Plex Sans only** -- the template embeds it; do not substitute other fonts.
6. **End every deck with layout 47** -- the IBM logo end slide.
7. **Consult the layout reference** before selecting layouts -- choose the layout that best matches the content type rather than forcing content into a generic layout.
8. **Check `resources/MANIFEST.md`** for available assets before referencing images or icons.
