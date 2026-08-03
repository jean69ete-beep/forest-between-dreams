"""
make_stone.py — Inscribe Michelle's poem onto the Monet Glade stone

Run from the forest-between-dreams folder:
    pip install Pillow
    python make_stone.py

Output: images/Monet_Stone_poem.png
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os, sys

# ── Paths ────────────────────────────────────────────────────────────────────
STONE_IN  = os.path.join("images", "Monet_Stone.png")
STONE_OUT = os.path.join("images", "Monet_Stone_poem.png")

# ── The poem ─────────────────────────────────────────────────────────────────
POEM = [
    "In the stillness of the glade,",
    "where light and shadow dance,",
    "and the forest whispers secrets low.",
    "",
    "In the quiet hours, when dawn's pale fire",
    "creeps over the hills,",
    "and the forest awakens,",
    "its heartbeat echoing through the trees.",
    "",
    "In the stillness, I find my own pulse,",
    "my own rhythm, my own symphony —",
    "and in this harmony, I am home.",
    "",
    "Where love resides, where hearts entwine,",
    "where the forest whispers secrets of the divine.",
]

SIGNATURE = "— Michelle  ·  August 1, 2026"

# ── Font selection (tries several Windows/Linux options) ─────────────────────
def find_font(size):
    candidates = [
        # Windows — elegant serifs
        r"C:\Windows\Fonts\palai.ttf",       # Palatino Linotype Italic
        r"C:\Windows\Fonts\pali.ttf",         # Palatino Linotype
        r"C:\Windows\Fonts\garabd.ttf",       # Garamond Bold (italic fallback)
        r"C:\Windows\Fonts\georgia.ttf",      # Georgia
        r"C:\Windows\Fonts\cambria.ttc",      # Cambria
        r"C:\Windows\Fonts\times.ttf",        # Times New Roman
        # Linux
        "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            print(f"  Using font: {path}")
            return ImageFont.truetype(path, size)
    print("  No preferred font found — using default bitmap font")
    return ImageFont.load_default()

# ── Main ─────────────────────────────────────────────────────────────────────
def main():
    if not os.path.exists(STONE_IN):
        print(f"ERROR: {STONE_IN} not found.")
        print("Please save Monet_Stone.png into the images/ folder first.")
        sys.exit(1)

    print(f"Loading {STONE_IN} …")
    img = Image.open(STONE_IN).convert("RGBA")
    W, H = img.size
    print(f"  Size: {W} × {H}")

    # ── Overlay: subtle dark veil over center-left of stone ──────────────────
    veil = Image.new("RGBA", img.size, (0, 0, 0, 0))
    vd   = ImageDraw.Draw(veil)

    # Soft rectangular dark area where text will sit
    tx, ty = int(W * 0.04), int(H * 0.28)   # top-left of text zone
    tw, th = int(W * 0.62), int(H * 0.68)   # width, height of text zone

    # Gradient veil using successive rectangles
    for i in range(80):
        alpha = int(90 * (1 - abs(i / 80 - 0.5) * 1.2))
        alpha = max(0, min(120, alpha))
        rect = [tx + i * 2, ty, tx + tw - i * 2, ty + th]
        vd.rectangle(rect, fill=(0, 0, 0, alpha))

    img = Image.alpha_composite(img, veil)
    draw = ImageDraw.Draw(img)

    # ── Fonts ────────────────────────────────────────────────────────────────
    poem_size = max(22, int(H * 0.030))   # scales with image height
    sig_size  = max(16, int(H * 0.022))
    poem_font = find_font(poem_size)
    sig_font  = find_font(sig_size)

    # ── Colors ───────────────────────────────────────────────────────────────
    # Pale carved-stone color — moonmist/frost
    TEXT_COLOR   = (232, 240, 245, 210)   # frost, slightly transparent
    SHADOW_COLOR = (10,  20,  10,  130)   # deep shadow for depth
    SIG_COLOR    = (212, 192, 144, 185)   # moon-gold for signature

    # ── Layout: measure and position lines ───────────────────────────────────
    line_h = int(poem_size * 1.65)
    all_lines = POEM + ["", SIGNATURE]

    # Total text block height
    block_h = len(all_lines) * line_h
    # Start Y: vertically centred in text zone
    start_y = ty + (th - block_h) // 2

    for i, line in enumerate(all_lines):
        if not line:
            continue
        y = start_y + i * line_h
        is_sig = (line == SIGNATURE)
        font   = sig_font if is_sig else poem_font
        color  = SIG_COLOR if is_sig else TEXT_COLOR

        # Draw shadow (1px offset for carved depth)
        draw.text((tx + 22 + 1, y + 1), line, font=font, fill=SHADOW_COLOR)
        draw.text((tx + 22 - 1, y - 1), line, font=font, fill=SHADOW_COLOR)
        # Draw text
        draw.text((tx + 22, y), line, font=font, fill=color)

    # ── Save ─────────────────────────────────────────────────────────────────
    out = img.convert("RGB")
    out.save(STONE_OUT, "PNG", optimize=True)
    print(f"\nSaved → {STONE_OUT}")
    print("Now place Monet_Stone_poem.png in your images/ folder")
    print("and update monet.html to reference it.")

if __name__ == "__main__":
    main()
