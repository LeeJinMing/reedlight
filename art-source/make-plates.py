"""Original paired paper-cut artwork. Coordinates are in a 600 x 400 print space."""
from pathlib import Path
import io
import json
import math
import struct

from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT=Path(__file__).resolve().parent
OUT=ROOT/"plates"
OUT.mkdir(exist_ok=True)
W,H,S=600,400,3
INK="#173d49"
CREAM="#ffedb7"
GOLD="#f5b346"
TEAL="#168c8e"
AQUA="#6ce4d0"
CORAL="#f67e48"
def poly(draw,xy,fill):
    draw.polygon([(int(x*S),int(y*S)) for x,y in xy],fill=fill)
def ellipse(draw,box,fill):
    draw.ellipse([int(v*S) for v in box],fill=fill)
def line(draw,xy,fill,width):
    draw.line([(int(x*S),int(y*S)) for x,y in xy],fill=fill,width=int(width*S),joint="curve")
def plate():
    im=Image.new("RGBA",(W*S,H*S));return im,ImageDraw.Draw(im)

far,f=plate()
# The back slice contains moving water, the legs, the outer tail and the near reed.
for x,y,r in [(116,288,19),(159,309,35),(337,308,41),(433,275,16),(249,340,26)]:
    line(f,[(x-r,y),(x+r,y)],AQUA,2)
poly(f,[(189,270),(215,258),(321,264),(379,252),(448,251),(414,260),(340,274),(265,281)],GOLD)
poly(f,[(219,266),(270,264),(321,266),(298,270)],CREAM)
poly(f,[(262,217),(232,253),(144,278),(185,250),(212,227)],TEAL)
poly(f,[(234,240),(211,255),(166,270),(199,248)],AQUA)
for a in [0,13]:
    poly(f,[(288+a,233),(292+a,234),(290+a,259),(303+a,259),(287+a,264),(278+a,264),(285+a,258)],CORAL)
for x,y in [(82,278),(493,277)]:
    line(f,[(x+8,y+21),(x,y-4),(x-6,y-40)],GOLD,2)
    poly(f,[(x-6,y-34),(x-14,y-51),(x-17,y-71),(x-11,y-66),(x-5,y-46)],GOLD)

mid,m=plate()
# The belly point meets the back-layer tail and front-layer breast.
poly(m,[(213,232),(235,199),(271,175),(309,152),(341,139),(359,150),(352,181),(334,201),(319,233),(297,249),(271,252),(240,246)],CORAL)
poly(m,[(221,232),(267,192),(302,174),(287,205),(248,231)],TEAL)
poly(m,[(237,221),(254,191),(308,156),(331,148),(312,169),(282,190)],AQUA)
poly(m,[(249,242),(275,218),(307,181),(328,174),(313,212),(298,235),(272,248)],"#db6039")
poly(m,[(294,243),(318,208),(332,184),(342,179),(331,203),(317,228)],CREAM)
# Raised far wing, cut into long, folded feather shapes.
poly(m,[(262,190),(237,169),(202,102),(193,68),(219,97),(226,59),(248,91),(251,65),(270,104),(281,146),(287,170)],TEAL)
poly(m,[(258,173),(218,101),(240,126),(260,153)],AQUA)
poly(m,[(258,153),(234,83),(251,118),(267,145)],GOLD)
poly(m,[(272,148),(258,88),(272,115),(279,138)],AQUA)

near,n=plate()
# Distinct bill, white throat and single high-contrast eye complete the silhouette.
poly(n,[(302,165),(318,143),(342,127),(360,120),(386,121),(400,134),(407,146),(396,158),(373,164),(358,181),(336,185),(343,160)],TEAL)
poly(n,[(331,141),(352,125),(382,124),(394,131),(379,131),(349,139)],AQUA)
poly(n,[(344,154),(359,143),(384,140),(399,143),(386,150),(367,153),(354,163)],INK)
poly(n,[(353,177),(363,158),(384,153),(371,163),(361,180),(347,192)],CREAM)
poly(n,[(398,141),(466,143),(409,152),(396,151)],INK)
poly(n,[(401,151),(451,145),(408,156)],GOLD)
ellipse(n,(384,136,393,145),CREAM);ellipse(n,(387,138,392,143),INK)
for x,y in [(342,139),(349,135),(357,133),(366,130)]:
    line(n,[(x,y),(x+4,y-1)],CREAM,2)
# Two near-wing quills cross one gap; their registration is visible from a distance.
poly(n,[(217,231),(257,194),(297,167),(312,165),(291,183),(254,206)],"#235d77")
poly(n,[(218,238),(251,214),(279,195),(288,191),(269,211),(249,224)],AQUA)

flat=Image.new("RGBA",(900,600))
for painted in (far, mid, near):
    flat.alpha_composite(painted.resize(flat.size, Image.Resampling.LANCZOS))
flat.save(OUT/"registered-print.png",optimize=True)

# Cut across the painted subjects, so no sheet contains an intact head or wing.
# Assign each final pixel to exactly one depth, including its antialiased alpha.
owners = Image.new("L", flat.size)
cuts = ImageDraw.Draw(owners)
edge = -400
widths = (54, 37, 72, 45, 61, 42, 55)
band = 0
while edge < flat.width + flat.height:
    next_edge = edge + widths[band % len(widths)]
    cuts.polygon([(edge,0), (next_edge,0), (next_edge-224,600), (edge-224,600)], fill=band % 3)
    edge = next_edge
    band += 1
plates = []
for index, name in enumerate(("far-perch", "middle-wing", "near-mask")):
    mask = owners.point([255 if value == index else 0 for value in range(256)])
    sheet = Image.new("RGBA", flat.size)
    sheet.paste(flat, mask=mask)
    sheet.save(OUT / (name + ".png"), optimize=True)
    plates.append(sheet)

def make_glb():
    # Each plane subtends the same rectangle from the design eye. glTF units are metres.
    depths=[1.30,1.01,.76];eye_x=.16;reference_z=1.01
    pieces=[];views=[];access=[];nodes=[];meshes=[];images=[];materials=[]
    def view(data,target=None):
        missing=(-sum(map(len,pieces)))%4
        if missing:pieces.append(b"\0"*missing)
        pos=sum(map(len,pieces));pieces.append(data);v={"buffer":0,"byteOffset":pos,"byteLength":len(data)}
        if target:v["target"]=target
        views.append(v);return len(views)-1
    def make_acc(rows,fmt,typ,comp,target,extrema=False):
        raw=b"".join(struct.pack("<"+fmt,*row) for row in rows)
        a={"bufferView":view(raw,target),"componentType":comp,"count":len(rows),"type":typ}
        if extrema:a.update(min=list(map(min,zip(*rows))),max=list(map(max,zip(*rows))))
        access.append(a);return len(access)-1
    uv=make_acc([(0,1),(1,1),(1,0),(0,0)],"2f","VEC2",5126,34962)
    inds=make_acc([(0,),(1,),(2,),(0,),(2,),(3,)],"H","SCALAR",5123,34963)
    for i,(im,z,name) in enumerate(zip(plates,depths,["Far perch","Middle wing","Near mask"])):
        k=z/reference_z;hw=.25*k;hh=k/6
        loc=[eye_x*(1-k)+.08*k,-.10*k,-z]
        positions=[(-hw,-hh,0),(hw,-hh,0),(hw,hh,0),(-hw,hh,0)]
        pos=make_acc(positions,"3f","VEC3",5126,34962,True)
        stream=io.BytesIO();im.save(stream,"PNG",optimize=True)
        images.append({"bufferView":view(stream.getvalue()),"mimeType":"image/png"})
        materials.append({"name":name,"pbrMetallicRoughness":{"baseColorTexture":{"index":i},"metallicFactor":0,"roughnessFactor":1},
                          "extensions":{"KHR_materials_unlit":{}},"doubleSided":True,"alphaMode":"BLEND"})
        meshes.append({"name":name,"primitives":[{"attributes":{"POSITION":pos,"TEXCOORD_0":uv},"indices":inds,"material":i}]})
        nodes.append({"name":name,"mesh":i,"translation":loc})
    binary=b"".join(pieces)
    doc={"asset":{"version":"2.0","generator":"Parallax Press plate generator"},"scene":0,"scenes":[{"nodes":[0,1,2]}],
         "extensionsUsed":["KHR_materials_unlit"],"nodes":nodes,"meshes":meshes,"materials":materials,"images":images,
         "samplers":[{"magFilter":9729,"minFilter":9729,"wrapS":33071,"wrapT":33071}],
         "textures":[{"source":i,"sampler":0} for i in range(3)],"accessors":access,"bufferViews":views,"buffers":[{"byteLength":len(binary)}]}
    payload=json.dumps(doc,separators=(",",":")).encode();payload+=b" "*((-len(payload))%4);binary+=b"\0"*((-len(binary))%4)
    body=struct.pack("<I4s",len(payload),b"JSON")+payload+struct.pack("<I4s",len(binary),b"BIN\0")+binary
    (OUT/"kingfisher-press.glb").write_bytes(struct.pack("<4sII",b"glTF",2,len(body)+12)+body)
make_glb()

