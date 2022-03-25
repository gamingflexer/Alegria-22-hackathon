
import nltk

#nltk.download('punkt')
import json
import re
import os
import pandas as pd
import nltk
import string
import tika
from tika import parser
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nameparser.parser import HumanName
from nltk import *
#nltk.download('stopwords')
#nltk.download('punkt')
#nltk.download('averaged_perceptron_tagger')
#nltk.download('maxent_ne_chunker')
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk.tokenize import sent_tokenize, word_tokenize
#nltk.download('words')
#nltk.download('wordnet')
#nltk.download('omw-1.4')
from date_extractor import extract_dates
import pyap
extracted_dates = {}
person_list = []
person_names=person_list

words_stop = ["page 1 of 1","Resume", "page 1 of 2","page 1 of 3", "page 1 of 4",
                "page 2 of 2","page 3 of 3","page 4 of 4","page 2 of 3",
                "page 2 of 4","page 3 of 4","resume"]

#def url(text):
 #   url = re.search("(?P<url>https?://[^\s]+)", text).group("url")
  #  return(url)

url1 =[]

def url(text5):
    try:
     url= re.search("(?P<url>https?://[^\s]+)", text5).group("url")


    except:
        url=None
    return url
def url_func(text2):
    tex=text2
    val1 = "so"
    while(val1!=""):
      val1=url(tex)
      if(val1==None):
          break

      else:

        url1.append(val1)
        for i in url1:
            tex=tex.replace(i,"")


    return url1

#url_func(text1)


def email(text):
    emails = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", text)
    return(emails)

def get_phone_numbers(string):
    r = re.compile(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})')
    phone_numbers = r.findall(string)
    return [re.sub(r'\D', '', num) for num in phone_numbers]


# dates grabber
def data_grabber(text):
    dates = extract_dates(text)
    return dates




person_list = []
person_names=person_list
def get_human_names(text):
    tokens = nltk.tokenize.word_tokenize(text)
    pos = nltk.pos_tag(tokens)
    sentt = nltk.ne_chunk(pos, binary = False)

    person = []
    name = ""
    for subtree in sentt.subtrees(filter=lambda t: t.label() == 'PERSON'):
        for leaf in subtree.leaves():
            person.append(leaf[0])
        if len(person) > 1: #avoid grabbing lone surnames
            for part in person:
                name += part + ' '
            if name[:-1] not in person_list:
                person_list.append(name[:-1])
            name = ''
        person = []
def human_name(text):
    names = get_human_names(text)
    for person in person_list:
        person_split = person.split(" ")
        for name in person_split:
            if wordnet.synsets(name):
                if (name in person):
                    person_names.remove(person)
                    break

    person_names

def address_grabber(text):
    regexp = "[0-9]{1,3} .+, .+, [A-Z]{2} [0-9]{5}"
    address = re.findall(regexp, text)
    #addresses = pyap.parse(text, country='INDIA')
    return address

#find pincode
def pincode_grabber(text):
    pincode =  r"[^\d][^a-zA-Z\d](\d{6})[^a-zA-Z\d]"
    pattern = re.compile(pincode)
    result = pattern.findall(text)
    if len(result)==0:
        return ' '
    return result[0]

def dob_grabber(text, ents):
        dob = 'Not found'
        lines = [line.strip() for line in text.split('\n')]
        dob_pattern = r'((\d)?(\d)(th)?.((jan)|(feb)|(mar)|(apr)|(may)|(jun)|(jul)|(aug)|(sep)|(oct)|(nov)|(dec)|(january)|(february)|(march)|(april)|(may)|(june)|(july)|(august)|(september)|(october)|(november)|(december)|(\d{2})).(\d{4}))'
        required = ''
        matches = ['dob', 'date of birth', 'birth date']
        flag = 0
        count = 0
        for lin in lines:

            if any(x in lin.lower().strip() for x in matches):
                required = lin.lower() + '\n'
                flag = 1
            if flag == 1:
                if len(lin.split()) < 1: continue
                required += lin.lower() + '\n'
                count += 1
            if count > 4:
                break
        required = ' '.join(req for req in required.split())

        match = re.findall(dob_pattern, required)
        try:
            return match[0][0]
        except:
            return ''


def pre_process1_rsw1(text):
    text = "".join(text.split('\n'))  # remove whitespaces
    text = text.lower()

    # using re
    text = re.sub('http\S+\s*', ' ', text)
    text = re.sub('RT|cc', ' ', text)
    text = re.sub('#\S+', ' ', text)
    #text = re.sub('@\S+', ' ', text)

    # for i in range (len(emails)): #removes emails
    #   text = text.replace(emails[i],"")

    text = re.sub(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})', '', text)  # removes phone numbers
    text = re.sub(r'[^\x00-\x7f]', ' ', text)
    text = re.sub('\s+', ' ', text)
    text = re.sub("\n", " ", text)

    # remove uncessary stop words
    for i in range(len(words_stop)):  # removes emails
        text = text.replace(words_stop[i], "")

    return ''.join(text)

def pre_process2_rsw(text):
    stop_words= set(stopwords.words("english"))
    word_tokens=word_tokenize(text)
    new_text= [word for word in word_tokens if word not in stop_words]
    return new_text


# remove puncutations
def pre_process3_rpm(text):
    translator = str.maketrans(",", string.punctuation)
    return text.translate(translator)


# remove hex code
def remove_hexcode_rhc(text):
    text = re.sub(r'[^\x00-\x7f]', r'', text)
    return text

url1.clear()




