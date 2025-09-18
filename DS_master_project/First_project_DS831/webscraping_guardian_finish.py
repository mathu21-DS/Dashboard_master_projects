"""
@author: Margrethe, Esben, Benjamin & Yousef
"""

#Importing packages
import requests
from urllib.request import urlopen
import json

  
# Function scrapes the Guardian API for a specific search term and saves
# The articles in a folder with the name of the search term. 
# Function parameters explained: topic is the search query, pages is for each pages to get the 200 articles apiurl, API_Key is your personal Guardian API key

def scrapeit(topic, pages, API_Key):
    # 1) Crawling with theguardian api
    #all articles in one txt.file or cvs file. It can only come to 200 articles for each page.
    id = 1
    #add in the data there is retrieved
    data1 = []
    
    # 2) Extract Articles information
    #For loop for each topic
    for i in range(pages):
        url ="https://content.guardianapis.com/search?q="+str(topic)+"&page-size=200&page="+str(1+i)+"&api-key="+str(API_Key)
        
        # Create the binary string html containing the HTML source
        response = requests.get(url)
        
        #it get the content inside the guardian API website
        response = response.content
        
        #loads() is used to convert the JSON String document into the Python dictionary.
        response = json.loads(response)
        
        article = 200 #It has to match the page size from the URL
        for value in range(article):
            #It go into the dictionary and move from key response, key results and then into a list where each apiurl is
            #each apiurl is found by the value there chance from 1 to 200 because of the for loop 
            content = response['response']['results'][value]['apiUrl']
            #the apiurl is added into the url1 together with the API_key
            url1 = content+"?api-key="+str(API_Key)+"&show-blocks=all&show-tags=keyword&show-fields=bodyText"

            # Create the binary string html containing the HTML source
            with urlopen(url1) as response1:
                source = response1.read()
                data = json.loads(source) #now it have become a python object as a dictionary instead of a json file
    
                datajson = data['response']['content']
            
                #get all the tags in the article
                try:
                    for a in range(0,20):#We decide to get a maximum of 20 tags
                                        #we try and except to ensure that it do not crash/show error when collecting the tags
                        #Not nessersary
                        #tag = []
                        #it added all the tag together into a list by for looping each index with a
                        tag = [datajson['tags'][a]['webTitle'] for a in range(len(datajson['tags']))]
                except:
                  pass
            
            #get the timeline
            timeline = (datajson['webPublicationDate'])
            
            #get the the headline
            title = (datajson['webTitle'])
            
            #get the content inside the article
            text = (datajson['fields']['bodyText'])
            
            #show each article number order
            article_id = 'article'+str(id)
            
            #add 1 to the IDs number everytime it finish downloading an article
            id += 1
            #replace character in the string with ''
            #article_text= text.replace(';','')
            # finds the timestamp of the article and deletes the Z and T so it is easier to code later on
            articletimeline= timeline.replace("Z", "").replace("T", " ")
            # finds the articlenames, and deletes all signs you are not allowed to name your folder
            #articlename = title.replace("?", "").replace("/", " ").replace(":"," ").replace("*"," ").replace("<"," ").replace("|"," ").replace("‘","").replace("’","").replace(";","").replace(",","").replace(".","").replace("%","")
            
            #"""#1
#-------------------------------------------
            #append the article number, title, timeline, tags in a list and article text
            
            #for the text file
            #data1.append([article_id, articlename, articletimeline, tag, article_text])
            
            #for the cvs file
            data1.append([article_id, title, articletimeline, tag, text])
            
            #3 Export structured article data to a csv file
            import pandas as pd
            
            #add in each list from data1
            #also make a csv.file containing the information in data1
            df = pd.DataFrame(data1,
                columns = ['ID', 'name' , 'Timeline', 'Tags', 'Text'])
            #index=False is to remove index nr for each row
            df.to_csv('Articles1_'+str(topic)+'.csv', index=False, encoding='utf-8')
                        
            #shows how many articles it has scraped
            print(id)
            #"""#1
            
            """#2
#----------------------------------------------------------
import time
import os
            #3 Export structured article data to a txt file
            #second way to save each article ID', 'Title' , 'Timeline', 'Tags', 'Text in a txt.file. The same way as in Benjamins code
            #it do not make its own map to ad the articles in.
            #open the folder called article where it saves the article name and prepared to write into the txt file
            #open the folder where you wish to save your files
            try:
                    
                articlefile = open("article/"+str(articlename)+'.txt', 'w', encoding = "utf-8")
                # The timer is a safeguard for crashing the computer
                time.sleep(0.1)
           
            #each variable with write write into a txt file and chance a line down because of \n
            
            #Here can there be decided which content there could be saved in a txt file
            #Right now it only saves the articles text information
            
            #articlefile.write(article_id + '\n')
            #articlefile.write(title + '\n')
            #articlefile.write(articletimeline + '\n')
            #do a for loop and ad in each tag from the article
            #for article in tag:
            #    articlefile.write(article + '\n')
             
                articlefile.write(article_text)
            except OSError:
                pass
            #close the file so it will not run over the maximum allowed file descriptions on your system and your applications may give an error
            articlefile.close()          
            #First way to store the article data
            
            #shows how many articles it has scraped
            print(id)
            """#2

# This is how we call our function to extract data. Note that every page number adds 200 articles. 
scrapeit("Denmark", 5, "1e5a2054-9937-45fd-b8f2-db552832febd")