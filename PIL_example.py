from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
def make_vertical_label(label):
     font = ImageFont.load("courB08.pil")
     fontMask = Image.new("RGBA", (20,49), (10,144,216))
     draw = ImageDraw.Draw(fontMask)
     sizex, sizey = draw.textsize(label,font=font)
     fontMask = fontMask.resize((sizex,sizey))
     draw=ImageDraw.Draw(fontMask)
     bimsize=(sizex, sizey)
     width , height = bimsize ; xoff = yoff = 0
     draw.text((xoff,yoff), label, fill=(255,255,255),
                font=font)
     fontMask = fontMask.rotate(90)
     fontMask.save('output.png','PNG')

make_vertical_label("Python")
