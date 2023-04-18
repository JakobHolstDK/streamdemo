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

redis_client = redis.Redis(host='localhost', port=6379, db=0)
# List of possible statements
myenv ={ "tmp": "./tmp", "images": "./images" }
myscreen = { "x": 1900, "y": 1020, "right": 30, "left": 30 , "up": 90, "down": 90 , "fontsize": 40 }

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
    unique_filename = myenv['tmp'] + '/' + 'postit_' + unique_id + '.jpg'
    mystatement = generatestatment()
    myrx = randomplace(mystatement['place'])
    myry = randomplace('up')
    bgimage = Image.open(myenv['images'] + "/postit.jpg")
    draw = ImageDraw.Draw(bgimage)
    font = ImageFont.truetype("arial.ttf", size=myscreen["fontsize"])
    text = mystatement['statement']
    text_box = draw.textbbox((0, 0), text, font=font)
    x = (bgimage.width - text_box[2]) // 2
    y = (bgimage.height - text_box[3]) // 2
    draw.text((x, y), text, font=font, fill=(5, 44, 2))
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


