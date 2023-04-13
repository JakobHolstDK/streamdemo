import pygame
import datetime
import time
import random
import numpy
from PIL import Image, ImageDraw, ImageFont






def genimage(mytext, mysize):
  image = Image.new(mode="RGB", size=(800, 600), color=(0, 0, 0))
  draw = ImageDraw.Draw(image)
  font = ImageFont.truetype("arial.ttf", size=mysize)
  text = mytext
  text_box = draw.textbbox((0, 0), text, font=font)
  x = (image.width - text_box[2]) // 2
  y = (image.height - text_box[3]) // 2
  draw.text((x, y), text, font=font, fill=( 255, 0, 0))
  image.save("hello_pillow.png")
  

pygame.init()
genimage(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")), 60)
screen = pygame.display.set_mode((1900, 1200))

# Load the image
image = pygame.image.load("hello_pillow.png")
running = True
number=0
textsize=30
textmin=20
textmax=100
textsizedir=True

while running:
        sincount = int(numpy.sin(number) * 30)
        print(sincount)
        rotated_image = pygame.transform.rotate(image,sincount ) 
        screen.blit(rotated_image, (100, 100))
        pygame.display.flip()
        genimage(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")), textsize)
        add=random.randint(0,10)/10
        if (textsizedir):
             textsize = int(textsize + add)
             if (textsize > textmax):
                  textsizedir=False
        else:
             textsize = int(textsize - add)
             if (textsize < textmin):
                  textsizedir=True
        


        image = pygame.image.load("hello_pillow.png")
        number += 0.01

pygame.quit()
