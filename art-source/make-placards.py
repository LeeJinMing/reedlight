"""Draw readable world-space cue textures for the optical exhibit."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

root = Path(__file__).resolve().parent
out = root / "placards"
out.mkdir(exist_ok=True)
fonts = Path("C:/Windows/Fonts")
heading = ImageFont.truetype(str(fonts / "georgia.ttf"), 51)
labels = {
    "invitation": "Aim at Start for 1 second",
    "look": "Look toward the paper",
    "right": "Shift right slowly",
    "left": "Shift left slowly",
    "higher": "Move a little higher",
    "lower": "Move a little lower",
    "closer": "Move a little closer",
    "back": "Move back a little",
    "hold": "Hold this position",
    "ready": "Aligned. Pull your print",
    "printed": "Your kingfisher print",
    "return-left": "Move left to start again",
    "return-right": "Move right to start again",
    "return-back": "Step back to start again",
    "return-closer": "Step closer to start again",
    "return-higher": "Rise to the starting height",
    "return-lower": "Lower to the starting height",
}

for state, label in labels.items():
    image = Image.new("RGBA", (1024, 256))
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((8, 8, 1015, 247), 29, fill="#103540", outline="#9ac8bd", width=4)
    accent = "#ffc36c" if state in ("ready", "printed") else "#76e4d1"
    for x, dy in ((54, 0), (86, -9), (118, 0)):
        draw.polygon([(x, 91+dy), (x+22, 80+dy), (x+5, 160+dy), (x-16, 172+dy)], fill=accent)
    draw.text((164, 31), "Reedlight", font=heading, fill="#ffedb7", stroke_width=0)
    size = 75
    while True:
        body = ImageFont.truetype(str(fonts / "segoeuib.ttf"), size)
        if draw.textlength(label, font=body) <= 826:
            break
        size -= 1
    draw.text((164, 117), label, font=body, fill="#f4fff9")
    image.save(out / f"cue-{state}.png", optimize=True)
