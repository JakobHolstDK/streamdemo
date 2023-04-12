from PIL import Image, ImageDraw, ImageFont
import torch

from PIL import Image, ImageDraw, ImageFont

image = Image.new(mode="RGB", size=(400, 400), color=(255, 255, 255))
draw = ImageDraw.Draw(image)
font = ImageFont.truetype("arial.ttf", size=40)
text = "Keep KALM!"
text_box = draw.textbbox((0, 0), text, font=font)
x = (image.width - text_box[2]) // 2
y = (image.height - text_box[3]) // 2
draw.text((x, y), text, font=font, fill=(0, 0, 0))
image.save("hello_pillow.png")
