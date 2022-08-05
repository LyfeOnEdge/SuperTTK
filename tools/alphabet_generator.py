from PIL import Image, ImageDraw, ImageFont
import os

COLORS = ["black", "white"]
FONT_SIZES = [16,20,24,32,48,64]
##CHARACTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%&~`+-.="
CHARACTERS = string.printable
OUTDIR = os.path.abspath("./generated")

os.makedirs(OUTDIR,exist_ok=True)

path = os.path.abspath("../assets/fonts/Open_Sans/static/OpenSans/OpenSans-Bold.ttf")

def make_char_image(c, siz, fnt, clr):
	W, H = siz, siz
	img = Image.new("RGBA",(W,H),(0,0,0,0))
	draw = ImageDraw.Draw(img)
	w, h = fnt.getsize(c)
	if c == "J": #This one char... #Moving J up an 8th fixes it.
		draw.text((W/2,H/2-siz/8), c, fill=clr,font=fnt,anchor="mm")
	else:
		draw.text((W/2,H/2), c, fill=clr,font=fnt,anchor="mm")
	img.save(os.path.join(OUTDIR,f"{c}_{siz}_{clr}.png"))

for color in COLORS:
	for size in FONT_SIZES:
		font = ImageFont.truetype(path, size)
		for char in CHARACTERS:
			make_char_image(char, size, font, color)
