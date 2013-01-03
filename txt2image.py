# -*- coding: utf-8 -*-

import os
import Image, ImageFont, ImageDraw

def txt2image(data):
    text = data
    im = Image.new("RGB", (1024, 768), (255, 255, 255))
    dr = ImageDraw.Draw(im)
    font = ImageFont.truetype(os.path.join("fonts", "msyh.ttf"), 14)

    dr.text((10, 50), text, font=font, fill="#000000")

    im.show()
    im.save("t.png")
