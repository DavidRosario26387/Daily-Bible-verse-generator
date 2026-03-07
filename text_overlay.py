from io import BytesIO
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FONT_PATH = os.path.join(BASE_DIR, "fonts", "EBGaramond-VariableFont_wght.ttf")


def wrap_text_pixel(draw, text, font, max_width):

    words = text.split()
    lines = []
    current = ""

    for word in words:

        test = current + " " + word if current else word
        w = draw.textlength(test, font=font)

        if w <= max_width:
            current = test
        else:
            lines.append(current)
            current = word

    if current:
        lines.append(current)

    return "\n".join(lines)


def region_complexity(image, box):

    crop = image.crop(box).convert("L")
    arr = np.array(crop)

    return arr.std()


def find_best_region(image):

    width, height = image.size

    regions = {
        "top": (0, 0, width, int(height * 0.35)),
        "center": (0, int(height * 0.3), width, int(height * 0.7)),
        "bottom": (0, int(height * 0.65), width, height)
    }

    scores = {}

    for name, box in regions.items():
        scores[name] = region_complexity(image, box)

    return min(scores, key=scores.get)


def region_brightness(image, box):

    crop = image.crop(box).convert("L")
    arr = np.array(crop)

    return arr.mean()


def generate_verse_image(image_bytes, verse, reference) -> bytes:

    img = Image.open(BytesIO(image_bytes)).convert("RGB")

    width, height = img.size
    draw = ImageDraw.Draw(img)

    position = find_best_region(img)

    padding_x = int(width * 0.08)
    max_width = width - padding_x * 2

    font_size = int(height * 0.055)
    ref_size = int(font_size * 0.55)

    while True:

        verse_font = ImageFont.truetype(FONT_PATH, font_size)
        ref_font = ImageFont.truetype(FONT_PATH, ref_size)

        wrapped = wrap_text_pixel(draw, verse, verse_font, max_width)

        bbox = draw.multiline_textbbox(
            (0, 0),
            wrapped,
            font=verse_font,
            spacing=10
        )

        verse_w = bbox[2] - bbox[0]
        verse_h = bbox[3] - bbox[1]

        if verse_h < height * 0.35:
            break

        font_size -= 2
        ref_size = int(font_size * 0.55)

    if position == "top":
        verse_y = int(height * 0.12)

    elif position == "center":
        verse_y = (height - verse_h) / 2

    else:
        verse_y = height - verse_h - int(height * 0.12)

    verse_x = (width - verse_w) / 2

    ref_text = f"— {reference}"

    ref_x = width - padding_x
    ref_y = verse_y + verse_h + int(font_size * 0.9)

    brightness = region_brightness(
        img,
        (
            int(verse_x),
            int(verse_y),
            int(verse_x + verse_w),
            int(verse_y + verse_h)
        )
    )

    if brightness > 140:
        text_color = (40, 40, 40)
        stroke_color = (255, 255, 255)
    else:
        text_color = (245, 245, 245)
        stroke_color = (30, 30, 30)

    stroke_width = max(2, int(font_size * 0.06))

    draw.multiline_text(
        (verse_x, verse_y),
        wrapped,
        font=verse_font,
        fill=text_color,
        stroke_width=stroke_width,
        stroke_fill=stroke_color,
        spacing=10,
        align="center"
    )

    ref_color = tuple(int(c * 0.85) for c in text_color)

    draw.text(
        (ref_x, ref_y),
        ref_text,
        font=ref_font,
        fill=ref_color,
        anchor="ra"
    )

    buffer = BytesIO()
    img.save(buffer, format="JPEG", quality=95)

    return buffer.getvalue()