# HashiCorp CY26 Kit — Asset Catalog

All assets live in `assets/media/` relative to the skill directory. Use `path.resolve(__dirname, 'assets/media/filename')` or construct absolute paths from the skill directory.

## Quick Lookup by Product

A table mapping product name to icon filename(s) for fast reference:

| Product | Raw Icon | Bordered Icon | Filled Icon | Logo (standalone) | Logo (HashiCorp) | Logo (HCP) | Logo (Enterprise) | Logo (Community) |
|---------|----------|---------------|-------------|-------------------|-------------------|------------|-------------------|-----------------|
| Terraform | image64.png | image70.png, image71.svg | image74.png, image75.svg | image42.png | image12.png | image34.png | image51.png | image58.png |
| Vault | image67.png | image82.png | image80.png | image39.png | image16.png | image31.png | image50.png | image55.png |
| Consul | image61.png | image76.png | image79.png | image40.png | image19.png | image28.png | image48.png | image54.png |
| Nomad | image62.png | — | image73.png | image38.png | image15.png | — | image52.png | image56.png |
| Boundary | image60.png | image77.png | image78.png | image41.png | image18.png | image33.png | image47.png | image53.png |
| Packer | image63.png | image69.png | — | image45.png | image13.png | image29.png | — | image57.png |
| Vagrant | image66.png | image81.png | — | image44.png | image43.png | image30.png | — | image59.png |
| Waypoint | image68.png | image72.png | — | image46.png | image14.png | image32.png | — | — |

Additional HCP products:
- HCP Vault Radar: image17.png
- HCP Vault Dedicated: image49.png

## Product Color Map

| Product | Primary Color | Hex |
|---------|--------------|-----|
| Terraform | Purple | `#7B42BC` |
| Vault | Yellow | `#FFD814` |
| Consul | Pink | `#E03875` |
| Nomad | Green | `#06D092` |
| Boundary | Red | `#F24C53` |
| Packer | Blue | `#1DAEFF` |
| Vagrant | Blue | `#1868F2` |
| Waypoint | Teal | `#14C6CB` |

## Backgrounds & Gradients

Full-slide backgrounds and gradient layers used for title/divider slides and decorative overlays.

| Filename | Size | Description |
|----------|------|-------------|
| hc-gradient-base.png | 60KB | Full-slide gradient base — subtle rainbow gradient across top edge, white body. Same as image6.png. Primary light-mode background layer. |
| hc-glow-left.png | 380KB | Soft pastel glow blob for bottom-left corner overlay |
| hc-glow-right.png | 1.1MB | Soft pastel glow blob for top-right corner overlay |
| hc-arc-lines.png | 162KB | Concentric arc lines overlay — very faint gray. Same as image4.png |
| hc-alternate-bg.png | 672KB | White-to-light-purple vertical gradient. Same as image7.png |
| image1.png | 1.8MB | Dark background with gradient arc sweep (purple/pink/gold) bottom-left |
| image2.png | 5.0MB | Dark background with gradient arc sweep (purple/pink/gold) top-right |
| image5.png | 946KB | Soft pastel glow blob (pink top, purple bottom) — decorative overlay |
| image8.png | 2.1MB | Gradient arc sweep section (purple-to-gold, bottom portion only) |
| image11.png | 742KB | Full-slide gradient: white-to-light-purple/blue at bottom edge |
| image20.png | 2.1MB | Dark background with gradient arc sweep bottom-left (variant of image1) |
| image25.png | 4.3MB | Wide gradient glow strip across top edge (purple-pink-gold on black) |
| image26.png | 913KB | Rounded rectangle card frame with soft blue/purple outer glow shadow |

**Background layering order** (light mode slides):
1. `hc-gradient-base.png` — gradient-edge base
2. `hc-arc-lines.png` — arc lines overlay
3. `hc-glow-left.png` or `hc-glow-right.png` — soft glow blob

**Brand gradient stops**: `#6C81FF` (blue) → `#C08DFF` (purple) → `#FF8791` (pink) → `#F9B571` (gold)
- Dark variant: used in image1, image2, image8, image20, image25, image85, image86.svg
- Light variant: `#CDD4FF` → `#E5D0FF` → `#FFC2C7` → `#FCDEC4` — used in image87, image88.svg

## Logos & Branding

| Filename | Size | Description |
|----------|------|-------------|
| hashicorp-logo.svg | 542B | HashiCorp hexagon "H" mark (black). Same as image22.svg |
| image21.png | 11KB | HashiCorp hexagon "H" mark (black, PNG, 518×548) |
| image83.png | 11KB | HashiCorp hexagon "H" mark (black, centered with whitespace) |
| image84.png | 3KB | HashiCorp "H" icon in black rounded border (300×300) |
| image35.png | 109KB | "HashiCorp, an IBM Company" — horizontal lockup |
| image36.png | 60KB | "HashiCorp, an IBM Company" — stacked/vertical lockup |
| image37.png | 11KB | "HashiCorp Cloud Platform" — horizontal text logo with HCP icon |
| Hashicorp_Logos-CompactStrap_OnLight.png | 122KB | Compact strap logo on light background |
| Hashicorp_Logos-CompactStrap_OnDark.png | 120KB | Compact strap logo on dark background |
| Hashicorp_Logos-CompactStrap_OnLight.svg | 16KB | Compact strap logo SVG (light variant) |
| Hashicorp_Logos-CompactStrap_OnDark.svg | 16KB | Compact strap logo SVG (dark variant) |
| HashiCorp Full product strap_.svg | 122KB | Full product strap with all product logos in horizontal bar |

## Product Icons

### Raw Icons (no background, transparent)

| Filename | Product | Size | Notes |
|----------|---------|------|-------|
| image60.png | Boundary | 10KB | Red, 242×433 |
| image61.png | Consul | 15KB | Pink, 333×433 |
| image62.png | Nomad | 11KB | Green hexagon, 301×433 |
| image63.png | Packer | 9KB | Blue, 211×433 |
| image64.png | Terraform | 2KB | Purple, 100×114 (small) |
| image65.svg | Terraform | 501B | Purple SVG, 50×57 viewBox |
| image66.png | Vagrant | 2KB | Blue, 146×217 (small) |
| image67.png | Vault | 11KB | Yellow triangle, 320×433 |
| image68.png | Waypoint | 13KB | Teal, 385×433 |

### Bordered Icons (icon in rounded-corner border)

| Filename | Product | Size | Notes |
|----------|---------|------|-------|
| image69.png | Packer | 15KB | Blue border, 793×792 |
| image70.png | Terraform | 2KB | Purple border, 132×132 (small) |
| image71.svg | Terraform | 2.7KB | Purple border SVG, 66×66 viewBox |
| image72.png | Waypoint | 15KB | Teal border, 793×793 |
| image76.png | Consul | 5KB | Pink border, 265×265 |
| image77.png | Boundary | 3KB | Red border, 265×265 |
| image81.png | Vagrant | 3KB | Blue border, 265×265 |
| image82.png | Vault | 3KB | Yellow border, 265×265 |

### Filled Background Icons (solid color rounded square)

| Filename | Product | Size | Notes |
|----------|---------|------|-------|
| image73.png | Nomad | 8KB | Green filled, 577×577 |
| image74.png | Terraform | 2KB | Purple filled, 128×128 (small) |
| image75.svg | Terraform | 1.2KB | Purple filled SVG, 64×64 viewBox |
| image78.png | Boundary | 3KB | Red filled, 257×257 |
| image79.png | Consul | 5KB | Pink filled, 257×256 |
| image80.png | Vault | 3KB | Yellow filled, 257×257 |

## Product Logos with Text

All product logos are 433px tall, varying widths. Four naming tiers exist:

### Tier 1: "HashiCorp ProductName"
image12 (Terraform), image13 (Packer), image14 (Waypoint), image15 (Nomad), image16 (Vault), image18 (Boundary), image19 (Consul)

### Tier 2: "ProductName" (standalone)
image38 (Nomad), image39 (Vault), image40 (Consul), image41 (Boundary), image42 (Terraform), image43 (HashiCorp Vagrant), image44 (Vagrant), image45 (Packer), image46 (Waypoint)

### Tier 3: "HCP ProductName"
image17 (HCP Vault Radar), image28 (HCP Consul), image29 (HCP Packer), image30 (HCP Vagrant), image31 (HCP Vault), image32 (HCP Waypoint), image33 (HCP Boundary), image34 (HCP Terraform)

### Tier 4: Enterprise & Community Editions
Enterprise: image47 (Boundary), image48 (Consul), image49 (HCP Vault Dedicated), image50 (Vault), image51 (Terraform), image52 (Nomad)
Community: image53 (Boundary), image54 (Consul), image55 (Vault), image56 (Nomad), image57 (Packer), image58 (Terraform), image59 (Vagrant)

## SVG Graphics

| Filename | Size | Description |
|----------|------|-------------|
| image22.svg | 542B | HashiCorp "H" logo mark (black, 258×274 viewBox) |
| image65.svg | 501B | Terraform icon glyph (purple #7B42BC, 50×57) |
| image71.svg | 2.7KB | Terraform icon in rounded border (purple, 66×66) |
| image75.svg | 1.2KB | Terraform filled icon (purple, 64×64) |
| image86.svg | 21KB | Timeline/roadmap gradient bar with data points — DARK variant (2035×247). Shows adoption curve with 0%/45%/75%/100% markers. |
| image88.svg | 19KB | Timeline/roadmap gradient bar with data points — LIGHT variant (2035×247). Same layout as image86 with lighter palette. |

## Decorative / Design Reference

| Filename | Size | Description |
|----------|------|-------------|
| image85.png | 224KB | Gradient color reference bar — dark variant with percentage labels |
| image87.png | 179KB | Gradient color reference bar — light variant with percentage labels |
| image23.png | 8KB | Image placeholder icon (gray circle with photo icon) |
| image27.png | 620KB | Canva logo (partner/tool logo, 2048×1152) |
| thumbnail.jpeg | 4KB | PPTX thumbnail |

## EMF Files (Windows Enhanced Metafile)

| Filename | Size | Description |
|----------|------|-------------|
| image3.emf | 211KB | Vector graphic used by slide layouts |
| image9.emf | 15.7MB | Large complex vector illustration/diagram |
| image10.emf | 412KB | Vector graphic element for slide layouts |

Note: EMF files are Windows-specific vector formats. They can be embedded in PPTX via pptxgenjs `addImage({ path: ... })` but are not renderable in web contexts. Prefer PNG/SVG equivalents where available.
