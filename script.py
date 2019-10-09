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

def do_search():
    terms = token(input("Search query >> "))
    if terms == []:
        print("invalid query")
        sys.exit()  
    #搜索的结果答案
    
    if len(terms)==3:
        #A and B
        if terms[1]=="and":
            answer = merge2_and(terms[0],terms[2])   
            print(answer)
        #A or B       
        elif terms[1]=="or":
            answer = merge2_or(terms[0],terms[2])  
            print(answer)
        #A not B    
        elif terms[1]=="not":
            answer = merge2_not(terms[0],terms[2])
            print(answer)
        #输入的三个词格式不对    
        else:
            print("invalid query")
        
    elif len(terms)==5:
        #A and B and C
        if (terms[1]=="and") and (terms[3]=="and"):
            answer = merge3_and(terms[0],terms[2],terms[4])
            print(answer)
        #A or B or C
        elif (terms[1]=="or") and (terms[3]=="or"):
            answer = merge3_or(terms[0],terms[2],terms[4])
            print(answer)
        #(A and B) or C
        elif (terms[1]=="and") and (terms[3]=="or"):
            answer = merge3_and_or(terms[0],terms[2],terms[4])
            print(answer)
        #(A or B) and C
        elif (terms[1]=="or") and (terms[3]=="and"):
            answer = merge3_or_and(terms[0],terms[2],terms[4])
            print(answer)
        else:
            print("More format is not supported now!")
    #进行自然语言的排序查询，返回按相似度排序的最靠前的若干个结果
    else:
        leng = len(terms)
        answer = do_rankSearch(terms)
        print ("[Rank_Score: Tweetid]")
        for (tweetid,score) in answer:
            print (str(score/leng)+": "+tweetid)


def merge2_and(term1,term2):
    global postings
    answer = []  
    if (term1 not in postings) or (term2 not in postings):
        return answer
    else:
        i = len(postings[term1])
        j = len(postings[term2])
        x=0
        y=0
        # 教材上的and操作
        while x<i and y<j:
            if postings[term1][x]==postings[term2][y]:
                answer.append(postings[term1][x])
                x+=1
                y+=1
            elif postings[term1][x] < postings[term2][y]:
                x+=1
            else:
                y+=1            
        return answer

def merge2_or(term1,term2):
    answer=[]
    # 考虑两个都不在的情况
    if (term1 not in postings) and (term2 not in postings):
        answer = []   
    elif term2 not in postings:
        answer = postings[term1]
    elif term1 not in postings:
         answer = postings[term2]
    else:
        answer = postings[term1]
        for item in postings[term2]:
            if item not in answer:
                answer.append(item)
    return answer

def merge2_not(term1,term2):
    answer=[]
    if term1 not in postings:
        return answer      
    elif term2 not in postings:
        answer = postings[term1]
        return answer
        
    else:
        answer = postings[term1]
        ANS = []
        for ter in answer:
            if ter not in postings[term2]:
                ANS.append(ter)
        return ANS






