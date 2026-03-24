# Visual Review Criteria Reference

## Table of Contents
1. [WCAG Color Contrast](#wcag-color-contrast)
2. [Alignment and Centering](#alignment-and-centering)
3. [Overlap Rules](#overlap-rules)
4. [Slide Variety Guidelines](#slide-variety-guidelines)
5. [Line and Connector Clarity](#line-and-connector-clarity)
6. [Visual Density](#visual-density)

---

## WCAG Color Contrast

Based on WCAG 2.1 Success Criteria 1.4.3 (AA) and 1.4.6 (AAA).

### Contrast ratio formula

```
ratio = (L1 + 0.05) / (L2 + 0.05)
```

Where L1 is the relative luminance of the lighter color and L2 of the darker.

### Thresholds

| Text size | WCAG AA (minimum) | WCAG AAA (enhanced) |
|---|---|---|
| Normal text (<18pt, or <14pt bold) | 4.5:1 | 7:1 |
| Large text (>=18pt, or >=14pt bold) | 3:1 | 4.5:1 |

### Common pitfalls in presentations

- **Light gray text on white**: #999999 on #FFFFFF = 2.85:1 (FAIL AA). Use #767676 or darker.
- **White text on light photos**: text over images needs a scrim/overlay or text shadow.
- **Brand colors as text**: many brand palettes weren't designed for text contrast. Verify every combination.
- **Chart labels**: small text on colored chart segments often fails. Use external labels or increase size.

### Non-text contrast (WCAG 1.4.11)

UI components and graphical objects need 3:1 contrast against adjacent colors. In presentations this applies to:
- Icons that convey meaning
- Chart lines and data points
- Borders that define regions
- Interactive elements in embedded content

---

## Alignment and Centering

### The near-miss problem

A shape that is 0.05" off-center looks worse than one that is clearly offset by 0.5". The brain detects "almost right" as an error, but reads deliberate asymmetry as intentional. The script flags shapes within 0.15" of alignment as near-misses.

### Alignment best practices

- **Title text**: should be exactly centered or exactly left-aligned to a consistent margin
- **Body text**: left-align to a consistent left margin across all slides
- **Cards / columns**: if using a multi-column layout, columns should have equal width and equal gutters
- **Grouped objects**: items in a visual group (e.g., 3 icons with labels) should share a common baseline and equal horizontal spacing
- **Vertical rhythm**: maintain consistent spacing between stacked elements (e.g., all bullets have the same gap)

### Slide margins

Standard safe zones:
- **4:3 slides (10" x 7.5")**: 0.5" margins on all sides
- **16:9 slides (13.33" x 7.5")**: 0.75" left/right, 0.5" top/bottom
- **IBM large format (26.67" x 15")**: proportionally larger margins, typically 1-1.5"

Shapes that extend into or beyond the margin may get clipped when projected.

---

## Overlap Rules

### Intentional vs. accidental overlap

Not all overlap is bad. The script filters out common intentional patterns:
- **Text over image**: a text box on top of a background image is standard design
- **Decorative shapes**: accent bars or gradient overlays behind content

Flagged overlaps are shape-on-shape collisions where both shapes carry content (text, data, icons) and the overlap creates ambiguity about which shape "owns" the overlapping region.

### When overlap is a problem

- Two text boxes partially covering each other — the reader can't tell which to read first
- A shape border cutting through another shape's content
- Chart elements overlapping labels
- Icons overlapping text they aren't associated with

### How to fix overlaps

1. **Resize**: make one shape smaller so they don't collide
2. **Reposition**: move shapes apart, respecting the alignment grid
3. **Layer intentionally**: if overlap is desired, ensure one shape is fully behind the other (send to back) and the front shape has enough contrast/opacity to be clearly distinct
4. **Group**: if shapes belong together, group them into a single object

---

## Slide Variety Guidelines

### Why variety matters

Audiences process slides in ~3 seconds before deciding whether to read further. If every slide looks the same, attention drops after the 3rd or 4th slide in a row. Varying slide types forces the brain to re-engage with each transition.

### Recommended mix for a 15-slide deck

| Type | Suggested count | Purpose |
|---|---|---|
| Title / section divider | 2-3 | Signal structure and transitions |
| Statement / quote | 1-2 | Pause for emphasis, punctuate key points |
| Text + visual | 4-6 | Core content with supporting imagery |
| Chart / data | 2-3 | Evidence and quantitative proof |
| Image-focus | 1-2 | Emotional impact, break from text |
| Diagram / process | 1-2 | Show relationships and flows |

### Rules of thumb

- No more than 3 slides of the same type in a row
- At least 3 distinct slide types in any deck over 5 slides
- The most common type should not exceed 60% of the deck
- Every 4-5 slides, change the visual rhythm (e.g., go from text-heavy to image-focus)

---

## Line and Connector Clarity

### Minimum line weight

- **0.75pt**: minimum for on-screen viewing
- **1pt**: minimum for projected presentations (recommended default)
- **1.5pt+**: use for emphasis lines, key connectors, and borders

Lines below 0.5pt are nearly invisible on most projectors and many screens.

### Line contrast

Lines and connectors need sufficient contrast against their background:
- Minimum 3:1 ratio against the slide background
- Dashed and dotted lines need even higher contrast because the gaps reduce perceived weight

### Connector best practices

- Use consistent line styles throughout the deck (don't mix solid and dashed randomly)
- Arrow heads should be large enough to see at projection distance
- Avoid diagonal lines where horizontal/vertical would work — diagonals look messy at small scales
- Connector lines should terminate at shape edges, not float in whitespace

---

## Visual Density

### Shape count thresholds

| Shapes on slide | Assessment |
|---|---|
| 1-8 | Clean — typical well-designed slide |
| 9-15 | Moderate — check that grouping and spacing are clear |
| 16+ | Dense — likely needs simplification or splitting into multiple slides |

### Coverage thresholds

| Coverage (% of slide area) | Assessment |
|---|---|
| < 60% | Good whitespace |
| 60-80% | Moderate — acceptable if well-organized |
| 80-90% | Dense — consider removing decorative elements |
| > 90% | Cramped — the slide needs breathing room |

### Text density

- Maximum ~40 words per slide for presentations (not handouts)
- No more than 6 bullet points per slide
- If you need more content, split across slides or move to speaker notes
