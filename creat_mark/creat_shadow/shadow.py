from PIL import Image, ImageFont,ImageDraw
import os

x, y = 50, 50

fname1 = "./IMG_9359.JPG"
im = Image.open(fname1)
pointsize = 30
fillcolor = "white"
shadowcolor = "black"

word = "hi there"

font = "../38.ttf"
draw = ImageDraw.Draw(im)
font = ImageFont.truetype(font, pointsize)

draw.text((x - 1, y), word, font=font, fill=shadowcolor)
draw.text((x + 1, y), word, font=font, fill=shadowcolor)
draw.text((x, y - 1), word, font=font, fill=shadowcolor)
draw.text((x, y + 1), word, font=font, fill=shadowcolor)

draw.text((x - 1, y - 1), word, font=font, fill=shadowcolor)
draw.text((x + 1, y - 1), word, font=font, fill=shadowcolor)
draw.text((x - 1, y + 1), word, font=font, fill=shadowcolor)
draw.text((x + 1, y + 1), word, font=font, fill=shadowcolor)

draw.text((x, y), word, font=font, fill=fillcolor)

fname2 = "with_shadow.jpg"
im.save(fname2)

os.startfile(fname2)
