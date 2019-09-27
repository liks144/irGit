#!/usr/bin/env python

import re
import sys
from textblob import Word
from textblob import TextBlob
from collections import defaultdict

userProp = ["username","text","tweetid"]
postings = defaultdict(dict)

def get_postings():
    
    global postings
    f = open(r"/Users/liks/iGit/irGit/data/demo.txt")  
    lines = f.readlines()#读取全部内容

    for line in lines:
       line = tokenize_tweet(line)
       tweetid = line[0]
       line.pop(0)
       unique_terms = set(line)
       for te in unique_terms:#建立倒排索引
           if te in postings.keys():                    
               postings[te].append(tweetid)
           else:
               postings[te] = [tweetid]
    # print(postings)

def tokenize_tweet(string):
    
    string=string.lower()
    a = string.index("username")
    b = string.index("clusterno")
    c = string.rindex("tweetid")-1
    d = string.rindex("errorcode")
    e = string.index("text")
    f = string.index("timestr")-3
    #提取用户名、tweet内容和tweetid三部分主要信息
    string = string[c:d]+string[a:b]+string[e:f]
    # print(string)
    terms=TextBlob(string).words.singularize()
    # print(terms)

    result=[]
    for word in terms:
        expected_str = Word(word)
        expected_str = expected_str.lemmatize("v")
        if expected_str not in userProp:
            result.append(expected_str)
    return result

def token(query):
    query = query.lower()
    terms=TextBlob(query).words.singularize()

    result=[]
    for word in terms:#query和term做同样的处理
        expected_str = Word(word)
        expected_str = expected_str.lemmatize("v")     
        result.append(expected_str)
    return result
















