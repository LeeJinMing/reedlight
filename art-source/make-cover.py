"""Compose a promotional cover from the project's own artwork, separate from preview evidence."""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import random
ROOT=Path(__file__).resolve().parent
OUT=ROOT/"submission"
OUT.mkdir(exist_ok=True)
font=Path("C:/Windows/Fonts/georgia.ttf")
font_i=Path("C:/Windows/Fonts/georgiai.ttf")
def typeface(path,px):return ImageFont.truetype(str(path),px)
random.seed(34)
im=Image.new("RGB",(1200,800),"#102f3a")
draw=ImageDraw.Draw(im)
# Offset ink contours and guide lines echo the registration of layered paper prints.
for x in range(42,1180,14):
    draw.line((x,49,x,54 if x%28 else 58), fill="#4b7372",width=1)
for _ in range(32000):
    x=random.randrange(1200);y=random.randrange(800);v=random.randrange(2,10)
    draw.point((x,y),fill=(16+v,47+v,58+v))
for k,c in [(0,"#28525a"),(11,"#3a6567"),(22,"#71938a")]:
    draw.arc((506+k//2,43+k,1250-k,723-k),196,350,fill=c,width=2)
for x in [58,1139]:
    for y in [88,740]:
        draw.line((x-8,y,x+8,y),fill="#90aea2",width=2)
        draw.line((x,y-8,x,y+8),fill="#90aea2",width=2)
flat=Image.open(ROOT/"plates/registered-print.png").convert("RGBA")
cut=flat.crop(flat.getbbox())
cut.thumbnail((744,570),Image.Resampling.LANCZOS)
im.paste(cut,(448,117),cut)
draw=ImageDraw.Draw(im)
draw.text((73,198),"Reedlight",font=typeface(font,106),fill="#ffedb7",stroke_width=0)
draw.line((83,352,402,352),fill="#d5ac68",width=2)
draw.text((81,381),"A parallax print",font=typeface(font_i,42),fill="#8ce1ce")
draw.text((81,681),"The kingfisher study",font=typeface(font_i,29),fill="#e1cc9e")
im.save(OUT/"Reedlight-cover.jpg",quality=94,subsampling=0)
# Compare the unregistered view and the registered view using pinhole projection.
def sample_view(x):
    result=Image.new("RGBA",(900,600),"#193641")
    for z,name in [(130,"far-perch"),(101,"middle-wing"),(76,"near-mask")]:
        shift=round(((16-x)*(101/z-1))*18)
        layer=Image.open(ROOT/("plates/"+name+".png")).convert("RGBA")
        result.alpha_composite(layer,(shift,0))
    return result.convert("RGB")
proof=Image.new("RGB",(900,300));proof.paste(sample_view(0).resize((450,300)),(0,0));proof.paste(sample_view(16).resize((450,300)),(450,0))
proof.save(ROOT/"plate-registration-study.jpg",quality=94)

