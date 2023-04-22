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

lines =  open('movie_lines.txt', encoding= 'utf-8', errors = 'ignore').read().split('\n')
conversations = open('movie_conversations.txt', encoding = 'utf-8', errors = 'ignore').read().split('\n')




# creating a map which will map line with its ids
id2line = {}

for line in lines:
    _line = line.split(' +++$+++ ')
    if len(_line) == 5:
        id2line[_line[0]] = _line[4]


# creating a list of all the conversations
conversations_ids = []

for conversation in  conversations[:-1]:
    _conversation = conversation.split(' +++$+++ ')[-1][1:-1].replace("'", "").replace(" ", "")
    conversations_ids.append(_conversation.split(','))


# getting seprately the questions & the answers
questions = []
answers = []

for conversation in conversations_ids:
    for i in range(len(conversation) - 1):
        questions.append(id2line[conversation[i]])
        answers.append(id2line[conversation[i + 1]])

# for i  in range(0, 10):
#     print("Question" + "- "  + questions[i])
#     print("Answer" + " - " + answers[i])

# Prepration of questions and answers are done... Starting cleaning process

def cleanText(text):
    #This function will put all the text in the lower case 
    text = text.lower()
    # To remove punctuations we are going to use Re Libraray
    text = re.sub(r"i'm", "i am", text)
    text = re.sub(r"he's", "he is", text)
    text = re.sub(r"she's", "she is", text)
    text = re.sub(r"that's", "that is", text)
    text = re.sub(r"what's", "what is", text)
    text = re.sub(r"where's", "where is", text)
    text = re.sub(r"\'ll", "will", text)
    text = re.sub(r"\'ve", "have", text)
    text = re.sub(r"\'d", "would", text)
    text = re.sub(r"\'re", "are", text)
    text = re.sub(r"i'm", "i am", text)
    text = re.sub(r"won't", "will not", text)
    text = re.sub(r"can't", "cannot ", text)
    text = re.sub(r"[-()\"#/@;:<>{}+=~|.?,]", "", text)
    return text

# cleaning the questions 

cleanedQuestions = []

for q in questions:
    cleanedQuestions.append(cleanText(q))

# Cleaning the answers 

cleanedAnswers = []

for a in answers:
    cleanedAnswers.append(cleanText(a))


# for i  in range(0, 10):
#     print("Question" + "- "  + questions[i])
#     print("Question" + "- "  + cleanedQuestions[i])
#     print("Answers" + "- "  + answers[i])
#     print("Answer" + " - " + cleanedAnswers[i])


word2count = {}

for question in cleanedQuestions:
    for word in question.split():
        if word not in word2count:
            word2count[word]  = 1
        else:
            word2count[word] += 1

for answer in cleanedAnswers:
    for word in answer.split():
        if word not in word2count:
            word2count[word]  = 1
        else:
            word2count[word] += 1


# Tokenization and filtering non frequent words
# We are going to create 2 dictionaries. First that is going to mark each word to unique integer

threshold = 20
questionsword2int = {}
answersword2int = {}
wordNumber = 0

for word, count in word2count.items():
    if(count >= threshold):
        questionsword2int[word] = wordNumber
        wordNumber += 1

wordNumber = 0
for word, count in word2count.items():
    if(count >= threshold):
        answersword2int[word] = wordNumber
        wordNumber += 1

# Adding the last tokens to these two dictionaries
# These last tokens are useful in encode and decode the sec to se model

tokens = ['<PAD>', '<EOS>', '<OUT>', '<SOS>']

# for token in tokens:

    