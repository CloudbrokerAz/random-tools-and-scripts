"""Render data visualizations as PNG bytes using Pillow.

This module is used by build_presentation.py to generate data visualization
images that get placed on slides. Each visualization is specified as a dict
with a "type" key and type-specific parameters.
"""

import io
import math
from PIL import Image, ImageDraw, ImageFont


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def _parse_hex_color(hex_str: str) -> tuple:
    """Convert '#RRGGBB' or 'RRGGBB' to (R, G, B) tuple."""
    if not hex_str:
        return (0, 0, 0)
    h = hex_str.lstrip("#")
    if len(h) == 3:
        h = h[0] * 2 + h[1] * 2 + h[2] * 2
    if len(h) != 6:
        return (0, 0, 0)
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def _get_font(size=24, bold=False):
    """Get a Pillow font. Try IBM Plex Sans, fall back to default."""
    font_names = []
    if bold:
        font_names += [
            "IBMPlexSans-Bold.ttf",
            "IBM-Plex-Sans-Bold.ttf",
            "IBMPlexSans-SemiBold.ttf",
        ]
    font_names += [
        "IBMPlexSans-Regular.ttf",
        "IBM-Plex-Sans-Regular.ttf",
        "IBMPlexSans-Medium.ttf",
        "IBMPlexSans.ttf",
    ]
    # Common system font paths (macOS / Linux)
    search_dirs = [
        "/Library/Fonts",
        "/System/Library/Fonts",
        "/System/Library/Fonts/Supplemental",
        "/usr/share/fonts/truetype",
        "/usr/share/fonts",
    ]
    for directory in search_dirs:
        for name in font_names:
            try:
                return ImageFont.truetype(f"{directory}/{name}", size)
            except (OSError, IOError):
                continue
    # Fallback: try just the font name (relies on fontconfig or system path)
    for name in font_names:
        try:
            return ImageFont.truetype(name, size)
        except (OSError, IOError):
            continue
    # Last resort: Pillow built-in bitmap font (ignores size, but never fails)
    return ImageFont.load_default()


def _to_png_bytes(image: Image.Image) -> bytes:
    """Encode a PIL Image to PNG bytes."""
    buf = io.BytesIO()
    image.save(buf, format="PNG")
    return buf.getvalue()


def _text_bbox(draw: ImageDraw.ImageDraw, text: str, font):
    """Return (width, height) of rendered text, compatible across Pillow versions."""
    try:
        bbox = draw.textbbox((0, 0), text, font=font)
        return bbox[2] - bbox[0], bbox[3] - bbox[1]
    except AttributeError:
        return draw.textsize(text, font=font)


# ---------------------------------------------------------------------------
# Renderers
# ---------------------------------------------------------------------------

def _render_progress_ring(spec: dict) -> bytes:
    """Render a circular progress ring (KPI gauge).

    Spec fields:
        value: float - current value
        max: float - maximum value (default 100)
        color: str - hex color for the progress arc (e.g., "#0F62FE")
        track_color: str - hex color for the background track (default "#E0E0E0")
        size: int - image size in pixels (default 400)
        thickness: int - arc thickness in pixels (default 40)
        label: str - optional center text (if omitted, shows percentage)
        font_size: int - center text font size (default 48)
    """
    value = float(spec.get("value", 0))
    max_val = float(spec.get("max", 100))
    color = _parse_hex_color(spec.get("color", "#0F62FE"))
    track_color = _parse_hex_color(spec.get("track_color", "#E0E0E0"))
    base_size = int(spec.get("size", 400))
    thickness = int(spec.get("thickness", 40))
    label = spec.get("label")
    font_size = int(spec.get("font_size", 48))

    # 2x for high-res
    scale = 2
    size = base_size * scale
    thick = thickness * scale
    fs = font_size * scale

    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    margin = thick // 2 + 4
    bbox = [margin, margin, size - margin, size - margin]

    # Background track (full circle)
    draw.arc(bbox, 0, 360, fill=track_color + (255,), width=thick)

    # Progress arc (starting from top, i.e., -90 degrees)
    pct = min(value / max_val, 1.0) if max_val > 0 else 0
    sweep = pct * 360
    if sweep > 0:
        start_angle = -90
        end_angle = start_angle + sweep
        draw.arc(bbox, start_angle, end_angle, fill=color + (255,), width=thick)

    # Center text
    if label is None:
        label = f"{int(round(pct * 100))}%"
    font = _get_font(size=fs, bold=True)
    tw, th = _text_bbox(draw, label, font)
    tx = (size - tw) // 2
    ty = (size - th) // 2
    draw.text((tx, ty), label, fill=color + (255,), font=font)

    return _to_png_bytes(img)


def _render_horizontal_bars(spec: dict) -> bytes:
    """Render a horizontal bar chart.

    Spec fields:
        data: list of {"label": str, "value": float, "color": str}
        max_value: float - scale maximum (default: auto from data)
        size: tuple - (width, height) in pixels (default (800, 400))
        bar_height: int - height of each bar (default 40)
        gap: int - gap between bars (default 20)
        show_values: bool - show value text on bars (default True)
    """
    data = spec.get("data", [])
    if not data:
        return None

    raw_size = spec.get("size", (800, 400))
    if isinstance(raw_size, list):
        raw_size = tuple(raw_size)
    bar_height = int(spec.get("bar_height", 40))
    gap = int(spec.get("gap", 20))
    show_values = spec.get("show_values", True)

    values = [float(d.get("value", 0)) for d in data]
    max_value = float(spec.get("max_value", 0)) or max(values) if values else 1

    # 2x for high-res
    scale = 2
    w, h = int(raw_size[0]) * scale, int(raw_size[1]) * scale
    bh = bar_height * scale
    g = gap * scale

    # Auto-size height if too small
    needed_h = len(data) * (bh + g) + g
    if h < needed_h:
        h = needed_h

    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    label_font = _get_font(size=14 * scale)
    value_font = _get_font(size=12 * scale, bold=True)

    # Determine label area width
    label_widths = []
    for d in data:
        tw, _ = _text_bbox(draw, str(d.get("label", "")), label_font)
        label_widths.append(tw)
    label_area = max(label_widths) + 20 * scale if label_widths else 100 * scale
    bar_area_start = label_area + 10 * scale
    bar_area_width = w - bar_area_start - 20 * scale

    y = g
    for d in data:
        lbl = str(d.get("label", ""))
        val = float(d.get("value", 0))
        color = _parse_hex_color(d.get("color", "#0F62FE"))

        # Label
        _, lh = _text_bbox(draw, lbl, label_font)
        ly = y + (bh - lh) // 2
        draw.text((10 * scale, ly), lbl, fill=(50, 50, 50, 255), font=label_font)

        # Bar
        bar_w = int((val / max_value) * bar_area_width) if max_value > 0 else 0
        bar_w = max(bar_w, 2)
        draw.rounded_rectangle(
            [bar_area_start, y, bar_area_start + bar_w, y + bh],
            radius=bh // 4,
            fill=color + (255,),
        )

        # Value text
        if show_values:
            val_str = str(d.get("value", ""))
            vw, vh = _text_bbox(draw, val_str, value_font)
            vx = bar_area_start + bar_w + 8 * scale
            vy = y + (bh - vh) // 2
            draw.text((vx, vy), val_str, fill=(80, 80, 80, 255), font=value_font)

        y += bh + g

    return _to_png_bytes(img)


def _render_accent_gradient(spec: dict) -> bytes:
    """Render a horizontal (or vertical) gradient bar.

    Spec fields:
        colors: list of hex color strings (2-3 stops)
        size: tuple - (width, height) in pixels (default (800, 16))
        orientation: str - "horizontal" or "vertical" (default "horizontal")
    """
    colors_hex = spec.get("colors", ["#0F62FE", "#BE95FF"])
    raw_size = spec.get("size", (800, 16))
    if isinstance(raw_size, list):
        raw_size = tuple(raw_size)
    orientation = spec.get("orientation", "horizontal")

    colors = [_parse_hex_color(c) for c in colors_hex]
    if len(colors) < 2:
        colors.append(colors[0])

    scale = 2
    w, h = int(raw_size[0]) * scale, int(raw_size[1]) * scale

    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))

    if orientation == "vertical":
        length = h
    else:
        length = w

    # Build gradient segments
    num_segments = len(colors) - 1
    for px in range(length):
        # Determine which segment we are in
        t_global = px / max(length - 1, 1)
        seg_idx = min(int(t_global * num_segments), num_segments - 1)
        seg_start = seg_idx / num_segments
        seg_end = (seg_idx + 1) / num_segments
        t_local = (t_global - seg_start) / (seg_end - seg_start) if seg_end > seg_start else 0

        c1 = colors[seg_idx]
        c2 = colors[seg_idx + 1]
        r = int(c1[0] + (c2[0] - c1[0]) * t_local)
        g = int(c1[1] + (c2[1] - c1[1]) * t_local)
        b = int(c1[2] + (c2[2] - c1[2]) * t_local)

        if orientation == "vertical":
            for x in range(w):
                img.putpixel((x, px), (r, g, b, 255))
        else:
            for y in range(h):
                img.putpixel((px, y), (r, g, b, 255))

    return _to_png_bytes(img)


def _render_process_flow(spec: dict) -> bytes:
    """Render a horizontal process flow diagram with step boxes and arrows.

    Spec fields:
        steps: list of {"label": str, "sublabel": str (optional), "color": str}
        size: tuple - (width, height) in pixels (default (1600, 160))
        arrow_color: str - hex color for arrows (default "#8D8D8D")
    """
    steps = spec.get("steps", [])
    if not steps:
        return None

    raw_size = spec.get("size", (1600, 160))
    if isinstance(raw_size, list):
        raw_size = tuple(raw_size)
    arrow_color = _parse_hex_color(spec.get("arrow_color", "#8D8D8D"))

    scale = 2
    w, h = int(raw_size[0]) * scale, int(raw_size[1]) * scale

    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    n = len(steps)
    arrow_w = 30 * scale
    padding = 16 * scale
    total_arrow_space = arrow_w * max(n - 1, 0)
    box_w = (w - total_arrow_space - padding * 2) // n if n > 0 else w
    box_h = h - padding * 2
    radius = 12 * scale

    label_font = _get_font(size=14 * scale, bold=True)
    sub_font = _get_font(size=11 * scale)

    x = padding
    box_positions = []
    for i, step in enumerate(steps):
        color = _parse_hex_color(step.get("color", "#0F62FE"))

        # Rounded rectangle box
        x1, y1 = x, padding
        x2, y2 = x + box_w, padding + box_h
        draw.rounded_rectangle([x1, y1, x2, y2], radius=radius, fill=color + (255,))
        box_positions.append((x1, y1, x2, y2))

        # Label text (centered)
        lbl = str(step.get("label", ""))
        tw, th = _text_bbox(draw, lbl, label_font)
        cx = x1 + (box_w - tw) // 2
        sublabel = step.get("sublabel")
        if sublabel:
            stw, sth = _text_bbox(draw, sublabel, sub_font)
            total_text_h = th + 6 * scale + sth
            cy = y1 + (box_h - total_text_h) // 2
            draw.text((cx, cy), lbl, fill=(255, 255, 255, 255), font=label_font)
            sx = x1 + (box_w - stw) // 2
            draw.text((sx, cy + th + 6 * scale), sublabel, fill=(230, 230, 230, 255), font=sub_font)
        else:
            cy = y1 + (box_h - th) // 2
            draw.text((cx, cy), lbl, fill=(255, 255, 255, 255), font=label_font)

        # Arrow to next box
        if i < n - 1:
            ax1 = x2 + 4 * scale
            ax2 = x2 + arrow_w - 4 * scale
            ay = padding + box_h // 2
            # Arrow shaft
            shaft_h = 3 * scale
            draw.rectangle(
                [ax1, ay - shaft_h // 2, ax2 - 8 * scale, ay + shaft_h // 2],
                fill=arrow_color + (255,),
            )
            # Arrow head
            head_size = 8 * scale
            draw.polygon(
                [
                    (ax2, ay),
                    (ax2 - head_size, ay - head_size),
                    (ax2 - head_size, ay + head_size),
                ],
                fill=arrow_color + (255,),
            )

        x += box_w + arrow_w

    return _to_png_bytes(img)


def _render_metric_card(spec: dict) -> bytes:
    """Render a standalone metric/KPI card with large number and label.

    Spec fields:
        value: str - the metric value (e.g., "85%", "$4.2M")
        label: str - description text below the value
        color: str - accent color for the value text
        size: tuple - (width, height) in pixels (default (400, 300))
    """
    value_text = str(spec.get("value", ""))
    label_text = str(spec.get("label", ""))
    accent = _parse_hex_color(spec.get("color", "#0F62FE"))
    raw_size = spec.get("size", (400, 300))
    if isinstance(raw_size, list):
        raw_size = tuple(raw_size)

    scale = 2
    w, h = int(raw_size[0]) * scale, int(raw_size[1]) * scale

    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Light background with subtle border
    bg_color = (250, 250, 250, 255)
    border_color = (220, 220, 220, 255)
    radius = 16 * scale
    draw.rounded_rectangle([0, 0, w - 1, h - 1], radius=radius, fill=bg_color, outline=border_color, width=2 * scale)

    # Value text (large, bold, accent color)
    value_font = _get_font(size=40 * scale, bold=True)
    vw, vh = _text_bbox(draw, value_text, value_font)

    # Label text (smaller, gray)
    label_font = _get_font(size=16 * scale)
    lw, lh = _text_bbox(draw, label_text, label_font)

    spacing = 12 * scale
    total_h = vh + spacing + lh
    start_y = (h - total_h) // 2

    vx = (w - vw) // 2
    draw.text((vx, start_y), value_text, fill=accent + (255,), font=value_font)

    lx = (w - lw) // 2
    draw.text((lx, start_y + vh + spacing), label_text, fill=(120, 120, 120, 255), font=label_font)

    return _to_png_bytes(img)


def _render_icon_badge(spec: dict) -> bytes:
    """Render a numbered circle badge.

    Spec fields:
        number: int or str - the number/text to show
        color: str - background color
        size: int - diameter in pixels (default 80)
        text_color: str - text color (default "#FFFFFF")
    """
    number = str(spec.get("number", ""))
    color = _parse_hex_color(spec.get("color", "#0F62FE"))
    base_size = int(spec.get("size", 80))
    text_color = _parse_hex_color(spec.get("text_color", "#FFFFFF"))

    scale = 2
    size = base_size * scale

    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Filled circle
    draw.ellipse([0, 0, size - 1, size - 1], fill=color + (255,))

    # Centered text
    font = _get_font(size=int(size * 0.45), bold=True)
    tw, th = _text_bbox(draw, number, font)
    tx = (size - tw) // 2
    ty = (size - th) // 2
    draw.text((tx, ty), number, fill=text_color + (255,), font=font)

    return _to_png_bytes(img)


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def render_visual(spec: dict) -> bytes:
    """Render a visualization to PNG bytes based on the spec dict.

    Args:
        spec: Dict with 'type' key and type-specific params.
              Positioning fields (x, y, width, height) are ignored here -
              they're handled by the caller.

    Returns:
        PNG image bytes, or None if rendering fails.
    """
    vis_type = spec.get("type", "")
    renderers = {
        "progress_ring": _render_progress_ring,
        "horizontal_bars": _render_horizontal_bars,
        "accent_gradient": _render_accent_gradient,
        "process_flow": _render_process_flow,
        "metric_card": _render_metric_card,
        "icon_badge": _render_icon_badge,
    }
    renderer = renderers.get(vis_type)
    if renderer is None:
        return None
    try:
        return renderer(spec)
    except Exception as e:
        import sys
        print(f"  WARNING: render_visual({vis_type}) failed: {e}", file=sys.stderr)
        return None
