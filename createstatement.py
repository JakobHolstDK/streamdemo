#!/usr/bin/env python

import requests
import json
import openai
import redis
import os
import textwrap

angle = 0
width = 100
myenv ={ "tmp": "./tmp", "images": "./images" }
myscreen = { "x": 2560, "y": 1440, "right": 30, "left": 30 , "up": 90, "down": 90 , "fontsize": 20 }

redis_client = redis.Redis(host='localhost', port=6379, db=0)







openai.api_key = os.getenv("OPENAI_API_KEY")


def createcontext():
  try:
      ai_assistant = redis_client.get("ai_assistant")
      ai_assistant = ai_assistant.decode()
  except:
      ai_assistant="The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly."
      redis_client.set("ai_assistant", ai_assistant)

  try:
      ai_situation = redis_client.get("ai_situation")
      ai_situation = ai_situation.decode()
  except:
      ai_situation="\nHuman: The situation is at a wedding in Ireland. A woman name Victoria, 30 years from England and a man named Peter, who is From Ireland but have lived in England most of his life, he is 32 years old . They have 2 children a boy, Vera 5 years old and a  boy Winston 3 years old\n "
  context = ai_assistant + "\n" + ai_situation + "\n"
  context = context + "\nHuman: Please make up 20 random events from theit past. Said by one of the atendee to the wedding about them or just one of them? Name the person with a random name and relation to them, just make something funny up\nAI:"
  return context



def createstatement( prompt ):
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
context =  createcontext()
statement = createstatement(context)
print(statement)