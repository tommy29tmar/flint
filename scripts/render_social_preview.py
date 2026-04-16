"""Render a simple social preview image for the SIGIL repository.

Run with:
    uv run --with pillow python scripts/render_social_preview.py
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "social-preview.png"
WIDTH = 1280
HEIGHT = 640


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = []
    if bold:
        candidates.extend(
            [
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf",
            ]
        )
    else:
        candidates.extend(
            [
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                "/usr/share/fonts/TTF/DejaVuSans.ttf",
            ]
        )
    for path in candidates:
        try:
            return ImageFont.truetype(path, size=size)
        except OSError:
            continue
    return ImageFont.load_default()


def lerp(a: int, b: int, t: float) -> int:
    return int(a + (b - a) * t)


def build_background() -> Image.Image:
    image = Image.new("RGB", (WIDTH, HEIGHT), "#0d1117")
    px = image.load()
    top = (12, 18, 28)
    bottom = (22, 37, 46)
    for y in range(HEIGHT):
        t = y / (HEIGHT - 1)
        row = (lerp(top[0], bottom[0], t), lerp(top[1], bottom[1], t), lerp(top[2], bottom[2], t))
        for x in range(WIDTH):
            px[x, y] = row
    return image


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    image = build_background()
    draw = ImageDraw.Draw(image)

    coral = "#ff6b57"
    sand = "#ffe9cf"
    teal = "#6be3d8"
    slate = "#8ba0ad"
    line = "#223445"

    draw.rounded_rectangle((54, 54, WIDTH - 54, HEIGHT - 54), radius=36, outline=line, width=3)
    draw.rounded_rectangle((88, 104, 280, 156), radius=20, fill=coral)

    title_font = load_font(70, bold=True)
    subtitle_font = load_font(38, bold=False)
    small_font = load_font(28, bold=False)
    label_font = load_font(24, bold=True)

    draw.text((114, 111), "SIGIL", font=label_font, fill="#10161d")
    draw.text((88, 180), "Compiled", font=title_font, fill=sand)
    draw.text((88, 266), "reasoning", font=title_font, fill=sand)
    draw.text((88, 352), "contracts", font=title_font, fill=sand)
    draw.text((88, 438), "for LLM workflows", font=title_font, fill=sand)
    draw.text((91, 516), "Compress the work, not just the words.", font=subtitle_font, fill=teal)
    draw.text((92, 570), "OpenAI  •  Anthropic  •  Gemini", font=small_font, fill=slate)

    x0 = 860
    y0 = 146
    w = 260
    h = 56
    gap = 24
    colors = [coral, teal, sand]
    labels = ["task", "transport", "context"]
    values = ["compiled", "routed", "cached"]
    for i, (color, label, value) in enumerate(zip(colors, labels, values)):
        top = y0 + i * (h + gap)
        draw.rounded_rectangle((x0, top, x0 + w, top + h), radius=18, outline=color, width=3)
        draw.text((x0 + 18, top + 10), f"{label}  ->  {value}", font=small_font, fill=color)

    small_font = load_font(24, bold=False)
    draw.line((860, 414, 1120, 414), fill=line, width=3)
    draw.text((860, 446), "symbolic IR  •  routed transport", font=small_font, fill=slate)
    draw.text((860, 482), "compiled context  •  audit path", font=small_font, fill=slate)

    image.save(OUT, format="PNG", optimize=True)
    print(OUT)


if __name__ == "__main__":
    main()
