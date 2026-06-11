from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[2]
PUBLIC = ROOT / "public"
OUT = ROOT / "store-assets"

CREAM = (254, 254, 254)
CREAM_WARM = (250, 249, 246)
CHARCOAL = (28, 28, 28)
MUTED = (95, 95, 93)
BORDER = (233, 233, 230)
GREEN = (34, 197, 94)

FONT_REGULAR = Path("/System/Library/Fonts/Supplemental/Arial.ttf")
FONT_BOLD = Path("/System/Library/Fonts/Supplemental/Arial Bold.ttf")


ASSETS = {
    "01-snap": {
        "title": "Snap a photo.\nKnow your calories.",
        "subhead": "Deglem turns a meal photo into calories and\nmacros in seconds.",
        "main": "macro",
        "side_a": "dashboard",
        "side_b": "progress",
        "pills": ["AI photo analysis", "No manual search"],
    },
    "02-macros": {
        "title": "Calories and\nmacros, instantly.",
        "subhead": "See protein, carbs, fat, and more\nbefore you log the meal.",
        "main": "macro",
        "side_a": "dashboard",
        "side_b": "profile",
        "pills": ["Macro breakdown", "Easy portion edits"],
    },
    "03-dashboard": {
        "title": "Track your day\nat a glance.",
        "subhead": "Daily calories, macro targets, and meal\nlogging stay in one simple view.",
        "main": "dashboard",
        "side_a": "macro",
        "side_b": "progress",
        "pills": ["Daily targets", "Fast meal logging"],
    },
    "04-progress": {
        "title": "Watch progress\nbuild over time.",
        "subhead": "Review weight trends, calories, and BMI\nas your habits improve.",
        "main": "progress",
        "side_a": "dashboard",
        "side_b": "profile",
        "pills": ["Progress charts", "Goal tracking"],
    },
    "05-profile": {
        "title": "Personal goals,\ncleanly managed.",
        "subhead": "Set targets, review profile details,\nand keep your plan focused.",
        "main": "profile",
        "side_a": "progress",
        "side_b": "dashboard",
        "pills": ["Personal targets", "Simple profile"],
    },
}


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT_BOLD if bold else FONT_REGULAR), size)


def add_shadow(base: Image.Image, layer: Image.Image, xy: tuple[int, int], blur: int, alpha: int) -> None:
    shadow = Image.new("RGBA", layer.size, (0, 0, 0, 0))
    mask = layer.getchannel("A").filter(ImageFilter.GaussianBlur(blur))
    shadow.putalpha(mask.point(lambda v: int(v * alpha / 255)))
    base.alpha_composite(shadow, xy)


def rounded_paste(base: Image.Image, img: Image.Image, box: tuple[int, int, int, int], radius: int) -> None:
    w = box[2] - box[0]
    h = box[3] - box[1]
    fitted = ImageOps.fit(img, (w, h), method=Image.Resampling.LANCZOS)
    mask = Image.new("L", (w, h), 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, w, h), radius=radius, fill=255)
    base.paste(fitted.convert("RGBA"), (box[0], box[1]), mask)


def make_phone(
    screenshot: Image.Image,
    size: tuple[int, int],
    radius: int,
    bezel: int,
    border_width: int,
    opacity: float = 1.0,
) -> Image.Image:
    w, h = size
    phone = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(phone)
    draw.rounded_rectangle((0, 0, w - 1, h - 1), radius=radius, fill=CHARCOAL)
    inner = (border_width, border_width, w - border_width, h - border_width)
    rounded_paste(phone, screenshot, inner, max(1, radius - bezel))
    if opacity < 1:
        phone.putalpha(phone.getchannel("A").point(lambda v: int(v * opacity)))
    return phone


def paste_rotated(base: Image.Image, layer: Image.Image, center: tuple[int, int], angle: float, shadow=True) -> None:
    rotated = layer.rotate(angle, expand=True, resample=Image.Resampling.BICUBIC)
    xy = (center[0] - rotated.width // 2, center[1] - rotated.height // 2)
    if shadow:
        add_shadow(base, rotated, xy, blur=34, alpha=52)
    base.alpha_composite(rotated, xy)


def make_background(size: tuple[int, int]) -> Image.Image:
    w, h = size
    base = Image.new("RGBA", size, CREAM + (255,))
    px = base.load()
    for y in range(h):
        t = y / max(1, h - 1)
        r = int(CREAM[0] * (1 - t) + CREAM_WARM[0] * t)
        g = int(CREAM[1] * (1 - t) + CREAM_WARM[1] * t)
        b = int(CREAM[2] * (1 - t) + CREAM_WARM[2] * t)
        for x in range(w):
            px[x, y] = (r, g, b, 255)

    glow = Image.new("RGBA", size, (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse((-w * 0.12, -h * 0.02, w * 0.38, h * 0.34), fill=GREEN + (24,))
    gd.ellipse((w * 0.62, h * 0.12, w * 1.16, h * 0.58), fill=CHARCOAL + (12,))
    base.alpha_composite(glow.filter(ImageFilter.GaussianBlur(max(18, w // 28))))

    dot = Image.new("RGBA", size, (0, 0, 0, 0))
    dd = ImageDraw.Draw(dot)
    step = 34 if w > 1100 else 28
    for y in range(0, int(h * 0.68), step):
        for x in range(0, w, step):
            dd.ellipse((x, y, x + 1, y + 1), fill=CHARCOAL + (22,))
    base.alpha_composite(dot)
    return base


def draw_brand(draw: ImageDraw.ImageDraw, base: Image.Image, xy: tuple[int, int], size: int, text_size: int) -> None:
    logo = Image.open(PUBLIC / "logo/deglem-glyph-dark.png").convert("RGBA").resize((size, size), Image.Resampling.LANCZOS)
    base.alpha_composite(logo, xy)
    draw.text((xy[0] + size + int(size * 0.34), xy[1] + int(size * 0.1)), "Deglem", font=font(text_size, True), fill=CHARCOAL)


def draw_multiline(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, fnt: ImageFont.FreeTypeFont, fill, spacing: int) -> None:
    x, y = xy
    for line in text.split("\n"):
        draw.text((x, y), line, font=fnt, fill=fill)
        bbox = draw.textbbox((x, y), line, font=fnt)
        y += bbox[3] - bbox[1] + spacing


def draw_pills(draw: ImageDraw.ImageDraw, xy: tuple[int, int], pills: list[str], text_size: int, pad_x: int, pad_y: int, gap: int) -> None:
    x, y = xy
    fnt = font(text_size, True)
    for item in pills:
        bbox = draw.textbbox((0, 0), item, font=fnt)
        w = bbox[2] - bbox[0] + pad_x * 2
        h = bbox[3] - bbox[1] + pad_y * 2
        draw.rounded_rectangle((x, y, x + w, y + h), radius=h // 2, fill=(254, 254, 254, 220), outline=BORDER, width=2)
        draw.text((x + pad_x, y + pad_y - 2), item, font=fnt, fill=MUTED)
        x += w + gap


def rounded_card(base: Image.Image, box: tuple[int, int, int, int], radius: int, fill=(254, 254, 254, 235), outline=BORDER, width=2) -> None:
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)
    shadow = Image.new("RGBA", base.size, (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle(box, radius=radius, fill=(0, 0, 0, 34))
    base.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(24)))
    base.alpha_composite(layer)


def draw_metric_card(base: Image.Image, box: tuple[int, int, int, int], label: str, value: str, unit: str, scale: float) -> None:
    rounded_card(base, box, int(24 * scale))
    draw = ImageDraw.Draw(base)
    x, y, _, _ = box
    draw.text((x + int(28 * scale), y + int(26 * scale)), label, font=font(int(25 * scale), True), fill=MUTED)
    draw.text((x + int(28 * scale), y + int(66 * scale)), value, font=font(int(54 * scale), True), fill=CHARCOAL)
    draw.text((x + int(28 * scale), y + int(128 * scale)), unit, font=font(int(24 * scale), True), fill=MUTED)


def draw_macro_panel(base: Image.Image, box: tuple[int, int, int, int], scale: float) -> None:
    rounded_card(base, box, int(36 * scale))
    draw = ImageDraw.Draw(base)
    x, y, _, _ = box
    draw.text((x + int(34 * scale), y + int(30 * scale)), "Meal breakdown", font=font(int(36 * scale), True), fill=CHARCOAL)
    metrics = [("Calories", "680", "kcal"), ("Protein", "26.5", "g"), ("Carbs", "78", "g"), ("Fat", "28.5", "g")]
    card_w = int(172 * scale)
    card_h = int(132 * scale)
    gap = int(18 * scale)
    top = y + int(96 * scale)
    for index, metric in enumerate(metrics):
        cx = x + int(34 * scale) + (index % 2) * (card_w + gap)
        cy = top + (index // 2) * (card_h + gap)
        draw_metric_card(base, (cx, cy, cx + card_w, cy + card_h), *metric, scale=scale)


def draw_calorie_ring(base: Image.Image, center: tuple[int, int], radius: int, width: int, scale: float) -> None:
    draw = ImageDraw.Draw(base)
    x, y = center
    bounds = (x - radius, y - radius, x + radius, y + radius)
    draw.arc(bounds, start=0, end=360, fill=BORDER, width=width)
    draw.arc(bounds, start=-86, end=206, fill=GREEN, width=width)
    draw.text((x - int(86 * scale), y - int(62 * scale)), "1490", font=font(int(72 * scale), True), fill=CHARCOAL)
    draw.text((x - int(118 * scale), y + int(20 * scale)), "/ 1850 kcal", font=font(int(32 * scale), True), fill=MUTED)


def draw_progress_chart(base: Image.Image, box: tuple[int, int, int, int], scale: float) -> None:
    rounded_card(base, box, int(34 * scale))
    draw = ImageDraw.Draw(base)
    x1, y1, x2, y2 = box
    draw.text((x1 + int(34 * scale), y1 + int(28 * scale)), "Calories this week", font=font(int(34 * scale), True), fill=CHARCOAL)
    chart = (x1 + int(58 * scale), y1 + int(118 * scale), x2 - int(44 * scale), y2 - int(58 * scale))
    for i in range(5):
        y = chart[1] + i * ((chart[3] - chart[1]) // 4)
        draw.line((chart[0], y, chart[2], y), fill=(215, 215, 210), width=max(1, int(2 * scale)))
    draw.line((chart[0], chart[3], chart[2], chart[3]), fill=CHARCOAL, width=max(2, int(3 * scale)))
    draw.line((chart[0], chart[1], chart[0], chart[3]), fill=CHARCOAL, width=max(2, int(3 * scale)))
    points = [
        (chart[0], chart[3] - int(78 * scale)),
        (chart[0] + int(86 * scale), chart[3] - int(146 * scale)),
        (chart[0] + int(176 * scale), chart[3] - int(132 * scale)),
        (chart[0] + int(268 * scale), chart[3] - int(142 * scale)),
        (chart[2], chart[3] - int(170 * scale)),
    ]
    area = points + [(chart[2], chart[3]), (chart[0], chart[3])]
    draw.polygon(area, fill=(19, 128, 116, 210))
    draw.line(points, fill=(19, 128, 116), width=max(3, int(5 * scale)))
    for px, py in points:
        draw.ellipse((px - int(7 * scale), py - int(7 * scale), px + int(7 * scale), py + int(7 * scale)), fill=(19, 128, 116))
    goal_y = chart[1] + int(76 * scale)
    draw.line((chart[0], goal_y, chart[2], goal_y), fill=(232, 124, 42), width=max(2, int(3 * scale)))
    draw.text((chart[0] + int(4 * scale), goal_y - int(34 * scale)), "1850 goal", font=font(int(20 * scale), True), fill=(232, 124, 42))


def draw_goal_panel(base: Image.Image, box: tuple[int, int, int, int], scale: float) -> None:
    rounded_card(base, box, int(32 * scale), fill=CHARCOAL + (244,), outline=CHARCOAL)
    draw = ImageDraw.Draw(base)
    x1, y1, x2, _ = box
    draw.text((x1 + int(34 * scale), y1 + int(32 * scale)), "Daily calorie goal", font=font(int(26 * scale), True), fill=(254, 254, 254))
    draw.text((x1 + int(34 * scale), y1 + int(78 * scale)), "1850 kcal", font=font(int(60 * scale), True), fill=(254, 254, 254))
    draw.text((x1 + int(34 * scale), y1 + int(154 * scale)), "72.5 kg -> 68.0 kg", font=font(int(25 * scale), True), fill=(210, 210, 205))
    draw.rounded_rectangle((x1 + int(34 * scale), y1 + int(210 * scale), x2 - int(34 * scale), y1 + int(232 * scale)), radius=int(11 * scale), fill=(254, 254, 254, 54))
    draw.rounded_rectangle((x1 + int(34 * scale), y1 + int(210 * scale), x1 + int(280 * scale), y1 + int(232 * scale)), radius=int(11 * scale), fill=GREEN)


def draw_header(draw: ImageDraw.ImageDraw, base: Image.Image, data: dict, scale: float) -> None:
    draw_brand(draw, base, (int(70 * scale), int(70 * scale)), int(52 * scale), int(42 * scale))
    draw_multiline(draw, (int(70 * scale), int(170 * scale)), data["title"], font(int(82 * scale), True), CHARCOAL, int(5 * scale))
    draw_multiline(draw, (int(70 * scale), int(374 * scale)), data["subhead"], font(int(31 * scale)), MUTED, int(6 * scale))
    draw_pills(draw, (int(70 * scale), int(510 * scale)), data["pills"], int(23 * scale), int(15 * scale), int(11 * scale), int(14 * scale))


def compose_tall(kind: str, name: str, data: dict, screenshots: dict[str, Image.Image]) -> Image.Image:
    is_app = kind == "app-store"
    size = (1290, 2796) if is_app else (1080, 1920)
    canvas = make_background(size)
    draw = ImageDraw.Draw(canvas)
    scale = size[0] / 1080

    if is_app:
        scale = 1.2
        draw_header(draw, canvas, data, scale)
        phone_large = make_phone(screenshots[data["main"]], (int(610 * scale), int(1326 * scale)), int(62 * scale), int(13 * scale), int(13 * scale))
        phone_medium = make_phone(screenshots[data["main"]], (int(500 * scale), int(1087 * scale)), int(52 * scale), int(11 * scale), int(11 * scale))
        if name == "01-snap":
            meal = ImageOps.fit(screenshots["macro"], (int(720 * scale), int(560 * scale)), method=Image.Resampling.LANCZOS, centering=(0.5, 0.18))
            rounded_paste(canvas, meal, (int(92 * scale), int(690 * scale), int(812 * scale), int(1250 * scale)), int(38 * scale))
            draw_macro_panel(canvas, (int(124 * scale), int(1120 * scale), int(512 * scale), int(1476 * scale)), scale)
            paste_rotated(canvas, phone_large, (int(665 * scale), int(1740 * scale)), 4)
        elif name == "02-macros":
            paste_rotated(canvas, phone_medium, (int(288 * scale), int(1548 * scale)), -5)
            draw_macro_panel(canvas, (int(610 * scale), int(828 * scale), int(1036 * scale), int(1270 * scale)), scale)
            draw_metric_card(canvas, (int(660 * scale), int(1345 * scale), int(1010 * scale), int(1510 * scale)), "Health rating", "5/10", "editable estimate", scale)
            draw.text((int(620 * scale), int(1642 * scale)), "Adjust portions\nbefore logging.", font=font(int(56 * scale), True), fill=CHARCOAL)
        elif name == "03-dashboard":
            paste_rotated(canvas, phone_medium, (int(300 * scale), int(1570 * scale)), 0)
            draw_calorie_ring(canvas, (int(780 * scale), int(1055 * scale)), int(190 * scale), int(22 * scale), scale)
            draw_metric_card(canvas, (int(650 * scale), int(1370 * scale), int(985 * scale), int(1535 * scale)), "Protein", "150/185", "g", scale)
            draw_metric_card(canvas, (int(650 * scale), int(1570 * scale), int(985 * scale), int(1735 * scale)), "Carbs", "58/62", "g", scale)
        elif name == "04-progress":
            draw_progress_chart(canvas, (int(86 * scale), int(770 * scale), int(988 * scale), int(1260 * scale)), scale)
            paste_rotated(canvas, phone_medium, (int(790 * scale), int(1690 * scale)), 5)
            draw_multiline(
                draw,
                (int(92 * scale), int(1392 * scale)),
                "See the trend,\nnot just\nthe day.",
                font(int(58 * scale), True),
                CHARCOAL,
                int(8 * scale),
            )
        else:
            paste_rotated(canvas, phone_medium, (int(790 * scale), int(1600 * scale)), 6)
            draw_goal_panel(canvas, (int(92 * scale), int(790 * scale), int(580 * scale), int(1085 * scale)), scale)
            draw_metric_card(canvas, (int(92 * scale), int(1160 * scale), int(420 * scale), int(1330 * scale)), "Current", "72.5", "kg", scale)
            draw_metric_card(canvas, (int(92 * scale), int(1370 * scale), int(420 * scale), int(1540 * scale)), "Goal", "68.0", "kg", scale)
    else:
        draw_header(draw, canvas, data, scale)
        phone_large = make_phone(screenshots[data["main"]], (584, 1270), 62, 13, 13)
        phone_medium = make_phone(screenshots[data["main"]], (440, 956), 48, 10, 11)
        if name == "01-snap":
            meal = ImageOps.fit(screenshots["macro"], (660, 390), method=Image.Resampling.LANCZOS, centering=(0.5, 0.18))
            rounded_paste(canvas, meal, (70, 610, 730, 1000), 34)
            draw_macro_panel(canvas, (92, 910, 450, 1250), scale)
            paste_rotated(canvas, phone_large, (650, 1326), 4)
        elif name == "02-macros":
            paste_rotated(canvas, phone_medium, (270, 1245), -5)
            draw_macro_panel(canvas, (574, 700, 1012, 1118), scale)
            draw_metric_card(canvas, (620, 1185, 980, 1345), "Health rating", "5/10", "editable estimate", scale)
            draw.text((585, 1468), "Adjust portions\nbefore logging.", font=font(54, True), fill=CHARCOAL)
        elif name == "03-dashboard":
            paste_rotated(canvas, phone_medium, (265, 1260), 0)
            draw_calorie_ring(canvas, (766, 890), 176, 20, scale)
            draw_metric_card(canvas, (635, 1180, 965, 1338), "Protein", "150/185", "g", scale)
            draw_metric_card(canvas, (635, 1370, 965, 1528), "Carbs", "58/62", "g", scale)
        elif name == "04-progress":
            draw_progress_chart(canvas, (70, 640, 1010, 1078), scale)
            paste_rotated(canvas, phone_medium, (790, 1430), 5)
            draw_multiline(
                draw,
                (76, 1210),
                "See the trend,\nnot just\nthe day.",
                font(54, True),
                CHARCOAL,
                8,
            )
        else:
            paste_rotated(canvas, phone_medium, (760, 1300), 6)
            draw_goal_panel(canvas, (70, 660, 560, 930), scale)
            draw_metric_card(canvas, (80, 1040, 400, 1200), "Current", "72.5", "kg", scale)
            draw_metric_card(canvas, (80, 1240, 400, 1400), "Goal", "68.0", "kg", scale)
    return canvas.convert("RGB")


def compose_feature(screenshots: dict[str, Image.Image]) -> Image.Image:
    size = (1024, 500)
    canvas = make_background(size)
    draw = ImageDraw.Draw(canvas)
    draw_brand(draw, canvas, (70, 52), 44, 36)
    draw_multiline(draw, (70, 134), "Calories from\none photo", font(62, True), CHARCOAL, 4)
    draw_multiline(draw, (72, 292), "Snap a meal. Get calories and macros in\nseconds.", font(25), MUTED, 4)
    side = make_phone(screenshots["dashboard"], (174, 378), 36, 7, 7, 0.78)
    main = make_phone(screenshots["macro"], (218, 474), 40, 7, 7)
    paste_rotated(canvas, side, (660, 266), -7)
    paste_rotated(canvas, main, (790, 265), 5)
    return canvas.convert("RGB")


def main() -> None:
    screenshots = {
        "dashboard": Image.open(PUBLIC / "screenshots/dashboard.png").convert("RGBA"),
        "macro": Image.open(PUBLIC / "screenshots/macro.png").convert("RGBA"),
        "progress": Image.open(PUBLIC / "screenshots/progress.png").convert("RGBA"),
        "profile": Image.open(PUBLIC / "screenshots/profile.png").convert("RGBA"),
    }

    (OUT / "app-store").mkdir(parents=True, exist_ok=True)
    (OUT / "google-play").mkdir(parents=True, exist_ok=True)

    for name, data in ASSETS.items():
        compose_tall("app-store", name, data, screenshots).save(OUT / "app-store" / f"{name}.png", optimize=True)
        compose_tall("google-play", name, data, screenshots).save(OUT / "google-play" / f"{name}.png", optimize=True)
    compose_feature(screenshots).save(OUT / "google-play" / "feature-graphic.png", optimize=True)


if __name__ == "__main__":
    main()
