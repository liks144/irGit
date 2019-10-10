#!/usr/bin/env python

import re
import sys
import string
from textblob import Word
from textblob import TextBlob
from collections import defaultdict

userProp = ["username","text","tweetid"]
postings = defaultdict(dict)

def rtv(PRE,TERM,opt):
    global postings
    answer = []
    if opt == 1:
        # 1 做 and
        if (TERM not in postings) or PRE==[] :
            return answer#直接是个空集
        else:
            i = len(PRE)
            j = len(postings[TERM])
            x = 0
            y = 0
            while x<i and y<j:
                if PRE[x]==postings[TERM][y]:
                #postings中每一项的key是词
                    answer.append(postings[TERM][y])
                    x+=1
                    y+=1
                elif PRE[x] < postings[TERM][y]:
                    x+=1
                else:
                    y+=1
            return answer
    elif opt == 2:
        # 2 做 or
        if (TERM not in postings) and PRE==[]:
            return answer
        elif TERM not in postings:
            return PRE
        elif PRE == []:
            return postings[TERM]
        else:
            i = len(PRE)
            j = len(postings[TERM])
            x=0
            y=0
            
            PRE.append('99999999999999999')
            postings[TERM].append('99999999999999999')

            while x<i or y<j:
                if PRE[x]==postings[TERM][y]:
                    answer.append(PRE[x])
                    x+=1
                    y+=1
                elif PRE[x] < postings[TERM][y]:
                    answer.append(PRE[x])
                    x+=1
                else:
                    answer.append(postings[TERM][y])
                    y+=1
            postings[TERM].pop()
        return answer

    elif opt == 3:
        # 3 做 not
        if (TERM not in postings) and PRE==[]:
            return answer
        elif TERM not in postings:
            return PRE
        elif PRE == []:
            return answer
        else:
            i = len(PRE)
            j = len(postings[TERM])
            x=0
            y=0
            postings[TERM].append('99999999999999999')
            while x<i:
                if PRE[x]==postings[TERM][y]:
                    # answer.append(postings[TERM][x])
                    x+=1
                    y+=1
                elif PRE[x] < postings[TERM][y]:
                    answer.append(PRE[x])
                    x+=1
                else:
                    # answer.append(postings[TERM][y])
                    y+=1
            postings[TERM].pop()  
        return answer

def retrive(wordlist):
    # wordlist = str.split()
    jump = False
    endbit = False
    firstbit = True
    preset = []
    # cnt = 1
    for i,word in enumerate(wordlist):
        # print("我是第%s次进枚举" % cnt)
        # cnt += 1
        if jump==True:
            jump = False
            # flag用于跳过下次循环
            pass
        if i+1 != len(wordlist):#直到倒数第二个
            # print(i)
            # print(len(wordlist))
            if word == "and":
                preset = rtv(preset,wordlist[i+1],1)
                endbit = False
                jump = True
            elif word == "or":
                preset = rtv(preset,wordlist[i+1],2)
                endbit = False
                jump = True
            elif word == "not":
                preset = rtv(preset,wordlist[i+1],3)
                endbit = False
                jump = True
            else:
                # print("第一个是%s" % word)
                if firstbit == True:
                    preset = rtv(preset,word,2)
                    firstbit = False
                else:
                    preset = rtv(preset,word,1)
                endbit = True
        elif endbit == True:
            preset = rtv(preset,word,1)
    return preset

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

def token(query):#做normalize
    query = query.lower()
    terms=TextBlob(query).words.singularize()

    result=[]
    for word in terms:#query和term做同样的处理
        expected_str = Word(word)
        expected_str = expected_str.lemmatize("v")     
        result.append(expected_str)
    return result

def GeneratePosting():

    global postings
    f = open(r"data/tweets.txt")  
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
    for value in postings.values():
        value.sort()
    # print(postings)

def Search():
    terms = token(input("Search query >> "))
    if terms == []:
        sys.exit()
    # print(terms)
    print(retrive(terms))


def main():
    GeneratePosting()
    while True:
        Search()


if __name__ == "__main__":
    main()    