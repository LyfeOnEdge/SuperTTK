from PIL import Image, ImageDraw, ImageFont
import os

FONTPATH = os.path.abspath("../assets/fonts/Open_Sans/static/OpenSans/OpenSans-Bold.ttf")
OUTDIR = os.path.abspath("../assets/generated")
COLORS = ["black", "white"]
FONT_SIZES = [16,20,24,32,48,64]
CHARACTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%&~`+-.="
os.makedirs(OUTDIR,exist_ok=True)

def make_char_image(c, siz, fnt, clr):
	halfsiz = siz/2
	img = Image.new("RGBA",(siz,siz),(0,0,0,0))
	draw = ImageDraw.Draw(img)
	w, h = fnt.getsize(c)
	draw.text((halfsiz,halfsiz+(-siz/8 if c =="J" else 0)), c, fill=clr,font=fnt,anchor="mm")
	img.save(os.path.join(OUTDIR,f"{c}_{siz}_{clr}.png"))

for color in COLORS:
	for size in FONT_SIZES:
		font = ImageFont.truetype(FONTPATH, size)
		for char in CHARACTERS:
			make_char_image(char, size, font, color)