#!/usr/bin/env python

import openai
import redis
import os

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
context =  createcontext()
speech = createspeech(context)
redis_client.set("speech", speech)
