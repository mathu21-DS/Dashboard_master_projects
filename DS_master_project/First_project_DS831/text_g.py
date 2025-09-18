# -*- coding: utf-8 -*-
"""
Created on Tue Dec 21 22:08:42 2021

@author: Margrethe, Esben, Benjamin & Yousef
"""
import pandas as pd

#get the csv file
text1 = pd.read_csv('Articles_Denmark.csv')
text2=pd.read_csv('Articles_Denmark.csv',usecols=[1,3])

text3=pd.read_csv('Articles_Denmark.csv',usecols=[1])


#add in each articles title into a list
article_title=[]
for title in text1['name']:
    article_title.append(title) #is a list

#makes a list of each tags which is part of each article
Tags_list =[]
for i in range(len(text1['ID'])): 
    x = text1["Tags"][i].replace(" '", "").replace("'", "").replace(' "', '').replace('"', '') # the chances############
    list_article = x.strip('][').split(',')                                     ##It makes each row with the list tags into a a list with sub list of the aritcles tags
    Tags_list.append(list_article) #make list og the tags list in csv           ##make list of the tags list in csv file

#make a dictionary with the titles as keys and tags as values    
zip_iterator = zip(article_title, Tags_list)
a_dictionary = dict(zip_iterator)


tag_once = []
for I in article_title:
    for J in range(len(a_dictionary.get(I))):                                    #function get() the I get the key from the article name
                                                                                 #with the key using the J get each tag inside the list of tags
                                                                                 #append out each value from each articles name
        try:
            tag_once.append(a_dictionary[I][J])
        except:
            pass

#where there removes dublication of tag
uniqueList = []

for letter in tag_once:                                                         #take each tag in the list
    if letter not in uniqueList:                                                #It screened the list of the tag and only add a new tag if it not in the new list uniqueList
        uniqueList.append(letter)                                                #only add a new tag if it not in the new list uniqueList

tags_articles = [] #Dictionary of key matching the paticular article
for I in article_title:
    for J in range(len(a_dictionary.get(I))): #run the lengt of how many tag the perticular article have
        a_list = []
        for tag in uniqueList: #Contain a unique list of tags
            a_dict = {}
            if tag == a_dictionary[I][J]: #if tag in uniqueList is in a_dictionary[I][J] then it get added to the dictionary
                a_dict[tag] = I             #Then it added to the dictionary once and then into the list as a dictionary
                a_list.append(a_dict.copy())                                     #dict.copy() append the a_list of the copy of the dict object of key name and value tags
            else:
                pass
        tags_articles += a_list                                                  #each for loop of the a_list is the dict object is added into the list tags_articles
        
#With all the key(tag) repreating in the list become all the values added together to one key
key_values = {}

for d in tags_articles:
    for k,v in d.items():                                                       #The item() in the for loop go through each pair of key:value
                                                                                #the k get the key and the v get the value in each dictionary in the list
        if k in key_values.keys():                                              #if tag match the key in key.values.keys() then it append all the article name to that key
            key_values[k].append(v)                                             #then it append all the article name to that key
        else:    
            key_values[k]=[v]                                                   #if it do not match in if then nothing happends
