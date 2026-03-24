---
name: deck-reviewer
description: >
  Review PowerPoint (PPTX) slide decks for visual quality, accessibility, and clarity.
  Runs automated checks for overlapping shapes, alignment issues, WCAG color-contrast
  compliance, slide-type variety, line clarity, and visual clutter — then provides
  actionable human-readable recommendations. Use this skill whenever the user wants to
  review, audit, critique, or QA a slide deck, presentation, or PPTX file. Also trigger
  when users say things like "check my slides", "review this deck", "is this presentation
  accessible", "audit my PowerPoint", "find issues in my slides", "make sure my deck
  looks clean", or ask about contrast, alignment, overlap, or visual quality of slides.
  Even if the user just says "look over this pptx" or "anything wrong with these slides",
  use this skill.
---

# Deck Reviewer

Review PPTX presentations for visual quality, accessibility compliance, and audience digestibility.

## What this skill catches

| Category | What it finds | Why it matters |
|---|---|---|
| **Overlapping shapes** | Boxes, text frames, or images that collide | Overlaps confuse the viewer about what belongs together and create visual noise |
| **Alignment near-misses** | Objects that are *almost* aligned or *almost* centered | Near-misses look sloppier than being clearly offset — the eye detects "almost right" as wrong |
| **WCAG contrast** | Text/background color pairs that fail AA or AAA | Low contrast makes text unreadable for ~8% of people with color vision deficiency, and everyone in a bright room |
| **Slide variety** | Decks dominated by one slide type | Monotonous layouts lose audience attention; rhythm changes re-engage the room |
| **Line clarity** | Very thin lines or low-contrast connectors | Lines that vanish on a projector defeat their purpose |
| **Visual density** | Slides with too many shapes or excessive coverage | Cluttered slides overwhelm — the audience reads instead of listening |

## How to use this skill

### Step 1: Run the automated analysis

Execute the review script against the target PPTX file:

```bash
python /path/to/skills/deck-reviewer/scripts/review_deck.py <file.pptx>
```

For machine-readable output (useful for further processing):

```bash
python /path/to/skills/deck-reviewer/scripts/review_deck.py <file.pptx> --json
```

Use the virtual environment at `/workspace/.venv` if python-pptx is installed there:

```bash
/workspace/.venv/bin/python /workspace/.claude/skills/deck-reviewer/scripts/review_deck.py <file.pptx>
```

### Step 2: Interpret the automated results

The script produces a per-slide breakdown with severity levels:

- **ERROR** — Must fix. WCAG AA contrast failures are the most common. These are accessibility violations.
- **WARNING** — Should fix. Overlaps, thin lines, low variety, and clutter. These degrade the viewing experience.
- **INFO** — Consider fixing. Near-miss alignments, AAA-only contrast gaps. Polish items.

### Step 3: Perform qualitative review

The script catches measurable issues, but some visual problems require judgment. After reading the automated report, review the deck holistically for these things the script cannot catch:

**Layout and flow:**
- Does the eye know where to look first on each slide? (visual hierarchy)
- Are related items grouped and unrelated items separated? (proximity principle)
- Is there enough whitespace / breathing room?
- Do slide transitions feel logical — does the story flow?

**Typography:**
- Is the font size large enough for the back of the room? (minimum 24pt for body, 30pt+ for headings)
- Are there too many font sizes or styles competing on one slide?
- Is text left-aligned for body content? (centered body text is harder to scan)

**Color:**
- Beyond contrast ratios: is color used consistently? (same meaning = same color throughout)
- Is information conveyed by color alone without a secondary indicator? (WCAG 1.4.1)
- Are there more than 3-4 colors in active use? (too many = visual noise)

**Images and graphics:**
- Are images high-resolution enough for the slide dimensions?
- Do decorative elements distract from the content?
- Are icons/graphics consistent in style (don't mix flat icons with 3D renders)?

**Content density per slide:**
- The "billboard test": could someone grasp the slide's point in 3 seconds?
- If a slide has more than 6 bullet points, it probably needs to be split

### Step 4: Deliver the review

Structure the review as:

1. **Overall assessment** — one paragraph: is this deck in good shape, needs polish, or has structural problems?
2. **Critical issues** (errors) — list each with slide number, what's wrong, and how to fix it
3. **Recommended improvements** (warnings) — grouped by category
4. **Polish suggestions** (info) — optional, for decks that are already solid
5. **Slide variety assessment** — what types are present, what's missing, specific suggestions for which slides to convert

When recommending fixes, be specific: "Slide 4: change the subtitle from #999999 to #767676 to meet AA contrast on white" is actionable. "Fix contrast" is not.

## Reference

For detailed WCAG contrast thresholds, alignment best practices, and slide variety guidelines, see `references/review-criteria.md`.
