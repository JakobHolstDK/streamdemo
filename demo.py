#!/usr/bin/env python
from PIL import Image
import os
# Load the image
import pygame
import datetime
import time
import random
import numpy
from PIL import Image, ImageDraw, ImageFont
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QApplication
import sys
import redis

redis_client = redis.Redis(host='localhost', port=6379, db=0)



def showimage(imagename):
    app = QApplication(sys.argv)
    label = QLabel()
    pixmap = QPixmap(imagename)
    label.setPixmap(pixmap)
    label.show()
    sys.exit(app.exec_())

def randomplace(x, place, percentx):
  if (place == "right"):
    rangex = int(x - (x / 100 * percentx))
    myx = random.randrange(rangex, x)

  if (place == "left"):
    rangex = int(x / 100 * percentx)
    myx = random.randrange(0, rangex)
  return myx

def randangle():
    randomangle = int(random.randrange(90))
    return randomangle


def genpostit(mytext, myangle, mysize, filename):
    bgimage = Image.open("postit.jpg")
    draw = ImageDraw.Draw(bgimage)
    font = ImageFont.truetype("arial.ttf", size=mysize)
    text = mytext
    text_box = draw.textbbox((0, 0), text, font=font)
    x = (bgimage.width - text_box[2]) // 2
    y = (bgimage.height - text_box[3]) // 2
    draw.text((x, y), text, font=font, fill=(5, 44, 2))
    bgimage = bgimage.resize((100, 100))
    bgimage.save(filename)


def genmasterimage(imagename, x, y):
    bgimage = Image.open("images/wedding.png")
    speechfilename = redis_client.get("speechfile")
    print(speechfilename.decode())
    #speechfilename = speechfilename.decode()
    oldpaper = Image.open(speechfilename)
    redis_client.keys
    Image.Image.paste(bgimage, oldpaper, (800, 200))
    for key in redis_client.scan_iter("statement:*"):
      print(key.decode())
      postitid = key.decode()
      myplacement = redis_client.hget(postitid, 'placement')
      myplacement = myplacement.decode()
      myfilename = redis_client.hget(postitid, 'filename')
      myfilename = myfilename.decode()
      mystatement = redis_client.hget(postitid, 'statement')
      mystatement = mystatement.decode()
      myx = redis_client.hget(postitid, 'x')
      myx = int(myx.decode())
      myy = redis_client.hget(postitid, 'y')
      myy = int(myy.decode())
      myimage = Image.open(myfilename)
      myimage_copy = myimage.copy().convert('RGBA')
      for x in range(myimage_copy.width):
       for y in range(myimage_copy.height):
        r, g, b, a = myimage_copy.getpixel((x, y))
        if (r, g, b) == (255, 255, 255):
            myimage_copy.putpixel((x, y), (r, g, b, 0))
      if bgimage.mode != 'RGBA':
        bgimage = bgimage.convert('RGBA')
      bgimage.alpha_composite(myimage_copy, dest=(myx, myy))
    bgimage.save(imagename)

genmasterimage("masterimage.png", 2560, 1440)
showimage("masterimage.png")
time.sleep(4)
