from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
HERE = Path(__file__).parent
BLUE = (2, 98, 169, 255)
S = 4                       # supersampling
W, H, R = 130 * S, 106 * S, 9 * S
FONT = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"

def base():
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(im).rounded_rectangle((0, 0, W - 1, H - 1), R, fill=BLUE)
    return im

def odf():
    im = base(); d = ImageDraw.Draw(im)
    x0, y0, x1, y1 = 18 * S, 22 * S, 112 * S, 66 * S        # patch panel
    d.rounded_rectangle((x0, y0, x1, y1), 3 * S, fill="white")
    for row in range(2):
        for col in range(6):
            cx = x0 + (9 + col * 15) * S; cy = y0 + (10 + row * 22) * S
            d.rectangle((cx, cy, cx + 9 * S, cy + 9 * S), fill=BLUE)
    f = ImageFont.truetype(FONT, 22 * S)
    d.text((W / 2, 86 * S), "ODF", font=f, fill="white", anchor="mm")
    return im

def router_5g():
    im = Image.open(HERE / "icons" / "core_router.png").convert("RGBA").resize((W, H), Image.LANCZOS)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((80 * S, 4 * S, 126 * S, 32 * S), 5 * S, fill="white", outline=BLUE, width=2 * S)
    d.text((103 * S, 18 * S), "5G", font=ImageFont.truetype(FONT, 20 * S), fill=BLUE, anchor="mm")
    return im

for name, fn in [("custom_odf", odf), ("custom_router_5g", router_5g)]:
    fn().resize((W // 2, H // 2), Image.LANCZOS).save(HERE / "icons" / f"{name}.png")
    print("saved", name)
