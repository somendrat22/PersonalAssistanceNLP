# building a chatbot with deep nlp

# Importing the libraries
import numpy as np
import tensorflow as tf
import re 
# It will be used to clean the library. 
import time 
# this library will be used to train the code
import json
# Importing the dataset 

lines =  open('utterances.jsonl')
conversations = open('conversations.json')

with open('utterances.jsonl', 'r') as json_file:
    json_list = list(json_file)


id2line = {}

for jsonStr in json_list:
    jsonObj = json.loads(jsonStr)
    id2line[jsonObj["id"]] = jsonObj["text"]

