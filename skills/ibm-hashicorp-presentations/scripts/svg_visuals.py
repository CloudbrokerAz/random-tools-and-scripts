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
    font_size = int(spec.get("font_size", 144))

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

    label_font = _get_font(size=42 * scale)
    value_font = _get_font(size=36 * scale, bold=True)

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

    label_font = _get_font(size=42 * scale, bold=True)
    sub_font = _get_font(size=33 * scale)

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
    value_font = _get_font(size=120 * scale, bold=True)
    vw, vh = _text_bbox(draw, value_text, value_font)

    # Label text (smaller, gray)
    label_font = _get_font(size=48 * scale)
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


def _render_donut_chart(spec: dict) -> bytes:
    """Render a multi-segment donut chart with legend.

    Spec fields:
        segments: list of {"label": str, "value": float, "color": str}
        size: int - image diameter (default 400)
        hole_size: float - inner hole ratio 0-1 (default 0.5)
        center_label: str - optional text in the center
        show_legend: bool - draw legend below chart (default True)
    """
    segments = spec.get("segments", [])
    if not segments:
        return None

    base_size = int(spec.get("size", 400))
    hole_size = float(spec.get("hole_size", 0.5))
    center_label = spec.get("center_label")
    show_legend = spec.get("show_legend", True)

    scale = 2
    chart_size = base_size * scale

    # Calculate legend space
    legend_item_h = 24 * scale
    legend_padding = 16 * scale
    legend_h = (len(segments) * legend_item_h + legend_padding) if show_legend else 0

    total_w = chart_size
    total_h = chart_size + legend_h

    img = Image.new("RGBA", (total_w, total_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Compute total value and angles
    total_value = sum(float(s.get("value", 0)) for s in segments)
    if total_value <= 0:
        return None

    margin = 4 * scale
    bbox = [margin, margin, chart_size - margin, chart_size - margin]

    # Draw pie segments
    start_angle = -90.0
    for seg in segments:
        val = float(seg.get("value", 0))
        color = _parse_hex_color(seg.get("color", "#0F62FE"))
        sweep = (val / total_value) * 360.0
        if sweep > 0:
            end_angle = start_angle + sweep
            draw.pieslice(bbox, start_angle, end_angle, fill=color + (255,))
            start_angle = end_angle

    # Draw center hole (white circle)
    hole_radius = int((chart_size / 2 - margin) * hole_size)
    cx, cy = chart_size // 2, chart_size // 2
    draw.ellipse(
        [cx - hole_radius, cy - hole_radius, cx + hole_radius, cy + hole_radius],
        fill=(255, 255, 255, 255),
    )

    # Center label
    if center_label:
        font = _get_font(size=60 * scale, bold=True)
        tw, th = _text_bbox(draw, center_label, font)
        draw.text(
            (cx - tw // 2, cy - th // 2),
            center_label,
            fill=(50, 50, 50, 255),
            font=font,
        )

    # Legend
    if show_legend:
        legend_font = _get_font(size=36 * scale)
        swatch_size = 12 * scale
        lx = 16 * scale
        ly = chart_size + legend_padding // 2
        for seg in segments:
            color = _parse_hex_color(seg.get("color", "#0F62FE"))
            label = str(seg.get("label", ""))
            val = seg.get("value", 0)
            legend_text = f"{label} ({val})"
            # Color swatch
            draw.rectangle(
                [lx, ly + 2 * scale, lx + swatch_size, ly + 2 * scale + swatch_size],
                fill=color + (255,),
            )
            # Label text
            draw.text(
                (lx + swatch_size + 8 * scale, ly),
                legend_text,
                fill=(80, 80, 80, 255),
                font=legend_font,
            )
            ly += legend_item_h

    return _to_png_bytes(img)


def _render_sparkline(spec: dict) -> bytes:
    """Render an inline trend line with gradient fill area.

    Spec fields:
        values: list of float - data points
        color: str - line color (default "#0F62FE")
        fill_opacity: float - opacity of area fill below line (default 0.2)
        size: tuple - (width, height) in pixels (default (400, 120))
        show_endpoints: bool - dots on first/last points (default True)
        line_width: int - line thickness (default 3)
    """
    values = spec.get("values", [])
    if not values or len(values) < 2:
        return None

    color = _parse_hex_color(spec.get("color", "#0F62FE"))
    fill_opacity = float(spec.get("fill_opacity", 0.2))
    raw_size = spec.get("size", (400, 120))
    if isinstance(raw_size, list):
        raw_size = tuple(raw_size)
    show_endpoints = spec.get("show_endpoints", True)
    line_width = int(spec.get("line_width", 3))

    scale = 2
    w, h = int(raw_size[0]) * scale, int(raw_size[1]) * scale
    lw = line_width * scale

    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Padding
    pad_x = 8 * scale
    pad_y = 8 * scale
    plot_w = w - 2 * pad_x
    plot_h = h - 2 * pad_y

    min_val = min(values)
    max_val = max(values)
    val_range = max_val - min_val if max_val != min_val else 1.0

    # Compute point coordinates
    n = len(values)
    points = []
    for i, v in enumerate(values):
        px = pad_x + int((i / (n - 1)) * plot_w)
        py = pad_y + int((1.0 - (v - min_val) / val_range) * plot_h)
        points.append((px, py))

    # Fill area below line (semi-transparent)
    fill_alpha = max(0, min(255, int(fill_opacity * 255)))
    fill_color = color + (fill_alpha,)
    # Build polygon: line points + bottom-right + bottom-left
    fill_points = list(points) + [(points[-1][0], h), (points[0][0], h)]
    # Draw filled polygon on a separate layer and composite
    fill_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    fill_draw = ImageDraw.Draw(fill_layer)
    fill_draw.polygon(fill_points, fill=fill_color)
    img = Image.alpha_composite(img, fill_layer)
    draw = ImageDraw.Draw(img)

    # Draw line segments
    draw.line(points, fill=color + (255,), width=lw, joint="curve")

    # Endpoint dots
    if show_endpoints:
        dot_r = lw * 2
        for pt in [points[0], points[-1]]:
            draw.ellipse(
                [pt[0] - dot_r, pt[1] - dot_r, pt[0] + dot_r, pt[1] + dot_r],
                fill=color + (255,),
            )

    return _to_png_bytes(img)


def _render_gradient_bar(spec: dict) -> bytes:
    """Render a high-quality horizontal or vertical gradient bar.

    Faster alternative to accent_gradient using column/row fills instead of
    pixel-by-pixel putpixel.

    Spec fields:
        colors: list of hex strings (2-3 gradient stops)
        size: tuple - (width, height) in pixels (default (800, 16))
        orientation: str - "horizontal" or "vertical" (default "horizontal")
        corner_radius: int - rounded corners (default 0)
    """
    colors_hex = spec.get("colors", ["#0F62FE", "#BE95FF"])
    raw_size = spec.get("size", (800, 16))
    if isinstance(raw_size, list):
        raw_size = tuple(raw_size)
    orientation = spec.get("orientation", "horizontal")
    corner_radius = int(spec.get("corner_radius", 0))

    colors = [_parse_hex_color(c) for c in colors_hex]
    if len(colors) < 2:
        colors.append(colors[0])

    scale = 2
    w, h = int(raw_size[0]) * scale, int(raw_size[1]) * scale
    cr = corner_radius * scale

    # Build gradient image using line draws (much faster than putpixel)
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    length = w if orientation == "horizontal" else h
    num_segments = len(colors) - 1

    for px in range(length):
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
        fill = (r, g, b, 255)

        if orientation == "horizontal":
            draw.line([(px, 0), (px, h - 1)], fill=fill)
        else:
            draw.line([(0, px), (w - 1, px)], fill=fill)

    # Apply rounded corner mask if requested
    if cr > 0:
        mask = Image.new("L", (w, h), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.rounded_rectangle([0, 0, w - 1, h - 1], radius=cr, fill=255)
        img.putalpha(mask)

    return _to_png_bytes(img)


def _render_quote_mark(spec: dict) -> bytes:
    """Render a decorative large quotation mark for quote slides.

    Spec fields:
        color: str - hex color (default "#0F62FE")
        size: int - image size in pixels (default 200)
        style: str - "open" or "close" (default "open")
    """
    color = _parse_hex_color(spec.get("color", "#0F62FE"))
    base_size = int(spec.get("size", 200))
    style = spec.get("style", "open")

    scale = 2
    size = base_size * scale

    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Try to render using a large font glyph first
    glyph = "\u201C" if style == "open" else "\u201D"  # smart quotes
    font = _get_font(size=int(size * 0.85), bold=True)
    tw, th = _text_bbox(draw, glyph, font)

    # If the font rendered something meaningful, use it
    if tw > size * 0.05 and th > size * 0.05:
        tx = (size - tw) // 2
        ty = (size - th) // 2
        draw.text((tx, ty), glyph, fill=color + (255,), font=font)
    else:
        # Fallback: draw two filled circles with tails
        dot_r = size // 6
        gap = size // 4
        cx1 = size // 2 - gap // 2
        cx2 = size // 2 + gap // 2
        cy = size // 2 - dot_r // 2

        for cx in [cx1, cx2]:
            # Circle
            draw.ellipse(
                [cx - dot_r, cy - dot_r, cx + dot_r, cy + dot_r],
                fill=color + (255,),
            )
            # Tail (comma shape)
            if style == "open":
                tail_pts = [
                    (cx - dot_r, cy),
                    (cx - dot_r - dot_r // 2, cy + dot_r * 2),
                    (cx, cy + dot_r // 2),
                ]
            else:
                tail_pts = [
                    (cx + dot_r, cy),
                    (cx + dot_r + dot_r // 2, cy + dot_r * 2),
                    (cx, cy + dot_r // 2),
                ]
            draw.polygon(tail_pts, fill=color + (255,))

    return _to_png_bytes(img)


def _render_comparison_bars(spec: dict) -> bytes:
    """Render side-by-side before/after comparison bars.

    Spec fields:
        items: list of {"label": str, "before": float, "after": float,
               "before_color": str, "after_color": str}
        max_value: float - scale maximum (optional, auto from data)
        size: tuple - (width, height) in pixels (default (800, 400))
        before_label: str - legend label for before bars (default "Before")
        after_label: str - legend label for after bars (default "After")
    """
    items = spec.get("items", [])
    if not items:
        return None

    raw_size = spec.get("size", (800, 400))
    if isinstance(raw_size, list):
        raw_size = tuple(raw_size)
    before_label = spec.get("before_label", "Before")
    after_label = spec.get("after_label", "After")

    # Determine max value
    all_vals = []
    for item in items:
        all_vals.append(float(item.get("before", 0)))
        all_vals.append(float(item.get("after", 0)))
    max_value = float(spec.get("max_value", 0)) or (max(all_vals) if all_vals else 1)

    scale = 2
    w, h = int(raw_size[0]) * scale, int(raw_size[1]) * scale

    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    label_font = _get_font(size=39 * scale)
    value_font = _get_font(size=33 * scale, bold=True)
    legend_font = _get_font(size=36 * scale)

    # Legend at top
    legend_y = 8 * scale
    swatch = 12 * scale
    # "Before" swatch
    default_before_color = _parse_hex_color(items[0].get("before_color", "#8D8D8D"))
    default_after_color = _parse_hex_color(items[0].get("after_color", "#0F62FE"))
    draw.rectangle(
        [16 * scale, legend_y, 16 * scale + swatch, legend_y + swatch],
        fill=default_before_color + (255,),
    )
    draw.text(
        (16 * scale + swatch + 6 * scale, legend_y - 1 * scale),
        before_label,
        fill=(80, 80, 80, 255),
        font=legend_font,
    )
    bl_w, _ = _text_bbox(draw, before_label, legend_font)
    ax = 16 * scale + swatch + 6 * scale + bl_w + 20 * scale
    draw.rectangle(
        [ax, legend_y, ax + swatch, legend_y + swatch],
        fill=default_after_color + (255,),
    )
    draw.text(
        (ax + swatch + 6 * scale, legend_y - 1 * scale),
        after_label,
        fill=(80, 80, 80, 255),
        font=legend_font,
    )

    # Bar area
    top_margin = 36 * scale
    bottom_margin = 8 * scale
    bar_area_h = h - top_margin - bottom_margin

    n = len(items)
    row_h = bar_area_h // n if n > 0 else bar_area_h
    bar_h = max(row_h // 3, 6 * scale)
    bar_gap = 4 * scale

    # Determine label width
    label_widths = []
    for item in items:
        tw, _ = _text_bbox(draw, str(item.get("label", "")), label_font)
        label_widths.append(tw)
    label_area = max(label_widths) + 16 * scale if label_widths else 100 * scale
    bar_start_x = label_area + 10 * scale
    bar_max_w = w - bar_start_x - 60 * scale

    y = top_margin
    for item in items:
        lbl = str(item.get("label", ""))
        before_val = float(item.get("before", 0))
        after_val = float(item.get("after", 0))
        before_color = _parse_hex_color(item.get("before_color", "#8D8D8D"))
        after_color = _parse_hex_color(item.get("after_color", "#0F62FE"))

        # Label centered vertically in row
        _, lh = _text_bbox(draw, lbl, label_font)
        ly = y + (row_h - lh) // 2
        draw.text((10 * scale, ly), lbl, fill=(50, 50, 50, 255), font=label_font)

        # Before bar (top)
        b_bar_y = y + (row_h // 2) - bar_h - bar_gap // 2
        b_bar_w = int((before_val / max_value) * bar_max_w) if max_value > 0 else 0
        b_bar_w = max(b_bar_w, 2)
        draw.rounded_rectangle(
            [bar_start_x, b_bar_y, bar_start_x + b_bar_w, b_bar_y + bar_h],
            radius=bar_h // 4,
            fill=before_color + (255,),
        )
        # Value text
        bv_str = str(item.get("before", ""))
        draw.text(
            (bar_start_x + b_bar_w + 6 * scale, b_bar_y),
            bv_str,
            fill=(120, 120, 120, 255),
            font=value_font,
        )

        # After bar (bottom)
        a_bar_y = y + (row_h // 2) + bar_gap // 2
        a_bar_w = int((after_val / max_value) * bar_max_w) if max_value > 0 else 0
        a_bar_w = max(a_bar_w, 2)
        draw.rounded_rectangle(
            [bar_start_x, a_bar_y, bar_start_x + a_bar_w, a_bar_y + bar_h],
            radius=bar_h // 4,
            fill=after_color + (255,),
        )
        av_str = str(item.get("after", ""))
        draw.text(
            (bar_start_x + a_bar_w + 6 * scale, a_bar_y),
            av_str,
            fill=(80, 80, 80, 255),
            font=value_font,
        )

        y += row_h

    return _to_png_bytes(img)


def _render_stat_card(spec: dict) -> bytes:
    """Render an enhanced metric card with accent bar, trend indicator.

    Spec fields:
        value: str - the big number (e.g., "99.9%")
        label: str - description text
        color: str - accent color
        trend: str - optional "up", "down", or "flat"
        trend_value: str - optional trend text (e.g., "+12%")
        size: tuple - (width, height) in pixels (default (400, 300))
    """
    value_text = str(spec.get("value", ""))
    label_text = str(spec.get("label", ""))
    accent = _parse_hex_color(spec.get("color", "#0F62FE"))
    trend = spec.get("trend")
    trend_value = spec.get("trend_value")
    raw_size = spec.get("size", (400, 300))
    if isinstance(raw_size, list):
        raw_size = tuple(raw_size)

    scale = 2
    w, h = int(raw_size[0]) * scale, int(raw_size[1]) * scale

    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Card background with subtle border
    bg_color = (255, 255, 255, 255)
    border_color = (220, 220, 220, 255)
    radius = 12 * scale
    draw.rounded_rectangle(
        [0, 0, w - 1, h - 1],
        radius=radius,
        fill=bg_color,
        outline=border_color,
        width=2 * scale,
    )

    # Top accent bar (4px logical height)
    accent_h = 4 * scale
    draw.rounded_rectangle(
        [0, 0, w - 1, accent_h + radius],
        radius=radius,
        fill=accent + (255,),
    )
    # Fill the lower portion of the accent area to make a flat bottom edge
    draw.rectangle(
        [0, accent_h, w - 1, accent_h + radius],
        fill=bg_color,
    )
    # Redraw the accent bar precisely at top with rounded top corners only
    draw.rectangle(
        [radius, 0, w - 1 - radius, accent_h],
        fill=accent + (255,),
    )
    # Top-left and top-right arcs for rounded corners
    draw.pieslice(
        [0, 0, radius * 2, radius * 2],
        180, 270,
        fill=accent + (255,),
    )
    draw.pieslice(
        [w - 1 - radius * 2, 0, w - 1, radius * 2],
        270, 360,
        fill=accent + (255,),
    )
    # Fill remaining area between arcs and bar
    draw.rectangle([0, accent_h, w - 1, accent_h], fill=accent + (255,))

    # Value text (large, bold, accent color)
    value_font = _get_font(size=108 * scale, bold=True)
    vw, vh = _text_bbox(draw, value_text, value_font)

    # Label text
    label_font = _get_font(size=42 * scale)
    lw, lh = _text_bbox(draw, label_text, label_font)

    # Trend section
    trend_font = _get_font(size=39 * scale, bold=True)
    trend_h = 0
    trend_full_text = ""
    if trend and trend_value:
        arrow = ""
        if trend == "up":
            arrow = "\u25B2 "  # up triangle
        elif trend == "down":
            arrow = "\u25BC "  # down triangle
        elif trend == "flat":
            arrow = "\u25B6 "  # right triangle
        trend_full_text = arrow + trend_value
        _, trend_h = _text_bbox(draw, trend_full_text, trend_font)

    # Layout vertically centered
    spacing = 10 * scale
    content_start = accent_h + 16 * scale
    content_area = h - content_start - 16 * scale
    total_content_h = vh + spacing + lh + (spacing + trend_h if trend_h else 0)
    start_y = content_start + (content_area - total_content_h) // 2

    # Draw value
    vx = (w - vw) // 2
    draw.text((vx, start_y), value_text, fill=accent + (255,), font=value_font)

    # Draw label
    lx = (w - lw) // 2
    draw.text(
        (lx, start_y + vh + spacing),
        label_text,
        fill=(100, 100, 100, 255),
        font=label_font,
    )

    # Draw trend
    if trend_full_text:
        ttw, _ = _text_bbox(draw, trend_full_text, trend_font)
        tx = (w - ttw) // 2
        ty = start_y + vh + spacing + lh + spacing
        if trend == "up":
            trend_color = (36, 161, 72, 255)  # green
        elif trend == "down":
            trend_color = (218, 30, 40, 255)  # red
        else:
            trend_color = (120, 120, 120, 255)  # gray
        draw.text((tx, ty), trend_full_text, fill=trend_color, font=trend_font)

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
        "donut_chart": _render_donut_chart,
        "sparkline": _render_sparkline,
        "gradient_bar": _render_gradient_bar,
        "quote_mark": _render_quote_mark,
        "comparison_bars": _render_comparison_bars,
        "stat_card": _render_stat_card,
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
