"""
@dr.gifuto 用アイキャッチ画像ジェネレーター（1080x1080）

使い方:
    from generate_eyecatch import make_image
    make_image(title="1行目\n2行目\n3行目", out_path="post-031.jpg")

タイトルは「\n」で改行位置を指定できる。横幅に収まらない行は自動で文字サイズを下げる。
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1080
FONT_BOLD = "/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc"
FONT_MED = "/usr/share/fonts/opentype/noto/NotoSansCJK-Medium.ttc"

# 配色（深い紺〜青緑のグラデーション + 水色のアクセント）
BG_TOP = (14, 52, 74)
BG_BOTTOM = (8, 26, 42)
ACCENT = (110, 214, 230)
TEXT = (255, 255, 255)
SUB = (190, 214, 224)

MARGIN = 90
MAX_TITLE_SIZE = 92
MIN_TITLE_SIZE = 56


def _fit_size(draw, lines, max_width):
    size = MAX_TITLE_SIZE
    while size > MIN_TITLE_SIZE:
        font = ImageFont.truetype(FONT_BOLD, size)
        if all(draw.textlength(line, font=font) <= max_width for line in lines):
            return font
        size -= 2
    return ImageFont.truetype(FONT_BOLD, MIN_TITLE_SIZE)


def make_image(
    title: str,
    out_path: str,
    kicker: str = "医師が書く 放射線医療コラム",
    footer: str = "@dr.gifuto｜医師＠岐阜",
):
    img = Image.new("RGB", (W, H), BG_TOP)
    draw = ImageDraw.Draw(img)

    for y in range(H):
        t = y / H
        c = tuple(int(BG_TOP[i] + (BG_BOTTOM[i] - BG_TOP[i]) * t) for i in range(3))
        draw.line([(0, y), (W, y)], fill=c)

    # 右上の薄い円（装飾）
    deco = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ddraw = ImageDraw.Draw(deco)
    ddraw.ellipse([(W - 360, -220), (W + 220, 360)], outline=(110, 214, 230, 50), width=3)
    ddraw.ellipse([(W - 300, -160), (W + 160, 300)], outline=(110, 214, 230, 30), width=2)
    img = Image.alpha_composite(img.convert("RGBA"), deco).convert("RGB")
    draw = ImageDraw.Draw(img)

    draw.rectangle([(MARGIN, 150), (MARGIN + 80, 158)], fill=ACCENT)
    kicker_font = ImageFont.truetype(FONT_MED, 36)
    draw.text((MARGIN, 182), kicker, font=kicker_font, fill=ACCENT)

    lines = [l for l in title.split("\n") if l.strip()]
    title_font = _fit_size(draw, lines, W - MARGIN * 2)
    line_h = int(title_font.size * 1.42)
    block_h = line_h * len(lines)
    top_area, bottom_area = 270, H - 200
    y = top_area + max(0, (bottom_area - top_area - block_h) // 2) - 20
    for line in lines:
        draw.text((MARGIN, y), line, font=title_font, fill=TEXT)
        y += line_h

    draw.line([(MARGIN, H - 170), (W - MARGIN, H - 170)], fill=(60, 96, 118), width=2)
    footer_font = ImageFont.truetype(FONT_MED, 34)
    draw.text((MARGIN, H - 140), footer, font=footer_font, fill=SUB)

    img.save(out_path, "JPEG", quality=92)
    return out_path


if __name__ == "__main__":
    make_image(title="放射線治療と\n陽子線治療の\n違いは？", out_path="sample.jpg")
    print("done")
