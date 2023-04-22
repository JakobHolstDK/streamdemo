#!/usr/bin/env python
from PIL import Image
import datetime
import time
import random
from PIL import Image, ImageDraw, ImageFont
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QApplication
import sys
import redis
import uuid
import textwrap
import math


width = 15
angle = -12


redis_client = redis.Redis(host='localhost', port=6379, db=0)
# List of possible statements
myenv ={ "tmp": "./tmp", "images": "./images" }
myscreen = { "x": 2560, "y": 1440, "right": 20, "left": 20 , "up": 90, "down": 90 , "fontsize": 60 }

placements = [
    "right",
    "left"
]
person = {}
person['left'] = [
    "she",
    "Mary"
    ]

person['right'] = [
    "he",
    "Peter"
    ]


statements = [
    "is an amazing dancer.",
    "has a great sense of humor.",
    "is a talented musician.",
    "is an excellent cook.",
    "has traveled to many countries.",
    "is a natural leader.",
    "is a great listener.",
    "has a contagious smile.",
    "is always up for an adventure.",
    "has a heart of gold.",
    "is a skilled writer.",
    "is an exceptional athlete.",
    "has a brilliant mind.",
    "is a compassionate friend.",
    "has a unique perspective.",
    "is a gifted public speaker.",
    "has overcome great challenges.",
    "is a loyal companion.",
    "is a visionary thinker.",
    "is an inspiring role model.",
    "has some massive knockers.",
    "has huge mental problems"
]

def generatestatment():
    myplace = random.choice(placements)
    mypronome = random.choice(person[myplace])
    mystatement = random.choice(statements)
    print(mypronome + " " + mystatement)
    mypayload = { "place": myplace, "statement": mypronome + ' ' + mystatement } 
    return mypayload

    
#    print(pronome + ' ' + statement)

def createpostit():
    unique_id = str(uuid.uuid4())
    epoch_time = time.time()
    epoch_time_ns = int(epoch_time * 1e9)
    postitid = str(epoch_time_ns).zfill(19)
    unique_filename = myenv['tmp'] + '/' + 'postit_' + unique_id + '.png'
    mystatement = generatestatment()
    myrx = randomplace(mystatement['place'])
    myry = randomplace('up')
    bgimage = Image.open(myenv['images'] + "/postit.png")
    text_image = Image.new("RGBA", (bgimage.width, bgimage.height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(text_image)
    font = ImageFont.truetype("arial.ttf", size=myscreen["fontsize"])
    text = mystatement['statement']
    wrapped_text = textwrap.wrap(text, width)
    textplace=-100
    for text in wrapped_text:
      text_box = draw.textbbox((0, 0), text, font=font)
      x = (bgimage.width - text_box[2]) // 2
      y = (bgimage.height - text_box[3]) // 2
      y = y + textplace
      draw.text((x, y), text, font=font, fill=(5, 44, 2))
      textplace += 60
    rotated_text_image = text_image.rotate(angle, expand=True)
    myimage_copy = rotated_text_image.copy().convert('RGBA')
    for x in range(myimage_copy.width):
      for y in range(myimage_copy.height):
        r, g, b, a = myimage_copy.getpixel((x, y))
        if (r, g, b) == (255, 255, 255):
          myimage_copy.putpixel((x, y), (r, g, b, 0))
    if bgimage.mode != 'RGBA':
      bgimage = bgimage.convert('RGBA')
    bgimage.alpha_composite(myimage_copy, dest=(-50, -100))
    bgimage = bgimage.resize((200, 200))
    bgimage.save(unique_filename)
    redis_client.hset("statement:" + postitid, 'placement', mystatement["place"])
    redis_client.hset("statement:" + postitid, 'filename', unique_filename)
    redis_client.hset("statement:" + postitid, 'statement', text)
    redis_client.hset("statement:" + postitid, 'x', myrx)
    redis_client.hset("statement:" + postitid, 'y', myry)


def randomplace(place):
    if (place == "right"):
        rangex = int(myscreen["x"] - (myscreen["x"] / 100 * myscreen["right"]))
        myx = random.randrange(rangex, myscreen["x"])

    if (place == "down"):
        rangex = int(myscreen["y"] - (myscreen["y"] / 100 * myscreen["down"]))
        myx = random.randrange(rangex, myscreen["y"])

    if (place == "left"):
        rangex = int(myscreen["x"] / 100 * myscreen["left"])
        myx = random.randrange(0, rangex)

    if (place == "up"):
        rangex = int(myscreen["y"] / 100 * myscreen["up"])
        myx = random.randrange(100, rangex) + 100
    return myx


def randangle():
    randomangle = int(random.randrange(90))
    return randomangle
iterations = 10
while iterations > 0:
  createpostit()
  iterations = iterations - 1


