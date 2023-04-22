#!/usr/bin/env python

import openai
import redis
import os
from PIL import Image
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
import textwrap
import math
import uuid

angle = 0
width = 100
myenv ={ "tmp": "./tmp", "images": "./images" }
myscreen = { "x": 2560, "y": 1440, "right": 30, "left": 30 , "up": 90, "down": 90 , "fontsize": 20 }

redis_client = redis.Redis(host='localhost', port=6379, db=0)







openai.api_key = os.getenv("OPENAI_API_KEY")


#openai.ChatCompletion.create(
#  model="gpt-3.5-turbo",
#  messages=[
#        {"role": "system", "content": "You are a helpful assistant."},
#        {"role": "user", "content": "Who won the world series in 2020?"},
#        {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
#        {"role": "user", "content": "Where was it played?"}
#    ]
#)

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def createcontext():
  try:
      ai_assistant = redis_client.get("ai_assistant")
      ai_assistant = ai_assistantant.decode()
  except:
      ai_assistant="The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly."
      redis_client.set("ai_assistant", ai_assistant)

  try:
      ai_situation = redis_client.get("ai_situation")
      ai_situation = ai_situation.decode()
  except:
      ai_situation="\nHuman: The situation is at a wedding in iceland. A woman name Mary, 30 years from Denmark and a man named Peter,  who is From Iceland but have lived in Denmark most of his life, he is 32 years old . They have 2 children a boy, Freya 5 years old and a  boy Asger 3 years old\n Friend and family have the following to say:\n"
      redis_client.set("ai_assistant", ai_assistant)
  context = ai_assistant + "\n" + ai_situation + "\n"


  keys =  redis_client.keys("statement:*")
  for key in keys:
    key = key.decode()
    context = context 
    statement = redis_client.hget(key, "statement")
    statement = statement.decode()
    context = context + statement + "\n"
  context = context + "\nHuman: Please create a long speech with at least 2000 words to them at their wedding base on all these statements? \nAI:"
  return context



def createspeech( prompt ):
  response = openai.Completion.create(
    model="text-davinci-003",
    prompt=prompt,
    temperature=0.9,
    max_tokens=1500,
    top_p=1,
    frequency_penalty=0.0,
    presence_penalty=0.6,
    stop=[" Human:", " AI:"]
)
  return(response['choices'][0]['text'])


def savespeech(text, myfilename):
  print(text)
  print("---------------------------------------------------------")
  bgimage = Image.open(myenv['images'] + "/old-paper.png")
  text_image = Image.new("RGBA", (bgimage.width, bgimage.height), (0, 0, 0, 0))
  draw = ImageDraw.Draw(text_image)
  font = ImageFont.truetype("arial.ttf", size=myscreen["fontsize"])
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
  bgimage.save(myfilename)

context =  createcontext()
print(context)
speech = createspeech(context)
print(speech)

unique_id = str(uuid.uuid4())
unique_filename = myenv['tmp'] + '/' + 'speech_' + unique_id + '.png'
savespeech(speech, unique_filename)

redis_client.set("speech", speech)
redis_client.set("speechfile", unique_filename)


