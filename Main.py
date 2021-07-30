from datascience import *
import numpy as np
try:
    from googlesearch import search
except ImportError: 
    print("No module named 'google' found")
from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup
import re
import csv

import praw
from praw.models import MoreComments
    
class WebScrape():
    def __init__(self):
        self.cities = []
        self.dictionary = {}
    def scrapeCities(self):
            
        url = 'https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population'
        website_url = requests.get(url).text
        soup = BeautifulSoup(website_url, "lxml") 
         
        My_table = soup.find('table',{'class':'wikitable sortable'})
        new = My_table.findAll('tr')
            
        for i in range(1, len(new)):
            string = str(new[i])
            start = string.find("title=")+7
            end = string.find("\"", start, 900)
            altEnd = string.find(",", start, 900)
            if(end<altEnd):
                #print(string[start:end])
                self.cities.append(string[start:end])
            else:
                if (string[start:altEnd]=="Washington"):
                    self.cities.append("Washington DC")
                else:
                    self.cities.append(string[start:altEnd])    
                        
    def createCSV(self):
        
        for i in range(len(self.cities)):
            self.dictionary[self.cities[i]]=self.cities[i]
        
        datafile = open("Cities.csv", "w")
        
        writer = csv.writer(datafile)
        writer.writerow(['City Name Column', 'City Name']) #added
        for name, rating in self.dictionary.items():
            writer.writerow([name.lower(), rating])
        datafile.close()
        return self.dictionary
class City():
    def __init__(self, string):
        self.name = string;
        self.listedGuides = [];
        
    def addGuides(self):
        # to search
        query = self.name + " Travel Guide"

        for j in search(query, tld="co.in", num=5, stop=5, pause=2):
            self.listedGuides.append(j)
    
    def printAdvice(self):
        str1 = "Hey! Here are top 5 internet searches I found that could be helpful to you to plan a trip to " + self.name + ". \n\n"
        num = 1;
        for i in self.listedGuides:
            str1 += ("Link #" + str(num) + ": " + str(i) +"\n\n")
            num += 1
        otherName = self.name
        otherName = otherName.replace(' ', '+', 3)
        str1 += self.name +" on Google Maps: https://www.google.com/maps/place/"+ otherName + "\n\n"
        str1 += "Reminder, I'm just a bot. Have a safe and happy journey!"
        return str1
class Comment_Reader():
    def __init__(self, string):
        self.comment = string
        self.comment = self.comment.lower()
        self.city = ""
        self.num = -1;
    
    def readStr(self):
        for i in list1.column(0):
            self.num += 1
            if i in self.comment:
                self.city = i
                break
    
    def returnAdvice(self):
        
        if ("Reminder, I\'m just a bot. Have a safe and happy journey!" in self.comment):
            return ''
        elif(len(self.city) > 0):
            newCity = City(list1.column(1).item(self.num))
            newCity.addGuides()
            return newCity.printAdvice()
        else:
            #return "I do not have experience recommending travel guide for the cities you mentioned, if any."
            return ''
    
work = True
commentsChecked=[]

while(work):
    web = WebScrape()
    web.scrapeCities()
    web.createCSV()
    
    list1 = Table().read_table('Cities.csv')
    
    #city1 = City("Atlanta")
    #city1.addGuides()
    #print(city1.printAdvice())
    
    
    #newComment = Comment_Reader("I wish to go to Atlanta!")
    #newComment.readStr()
    #print(newComment.returnAdvice())
    
    #Enter your correct Reddit information into the variable below
    
    userAgent = 'AmericanTravelGuideBot'
    
    cID = 'pAModGt5lNHz5dy6esILSA'
    
    cSC= 'fYAZLaXpgdpZji38z1FOW93TKiPTRg'
    
    userN = 'TravelGuideBot'
    
    userP ='MasterChef'
    
    numFound = 0
    
    reddit = praw.Reddit(user_agent=userAgent, client_id=cID, client_secret=cSC, username=userN, password=userP)
    
    subreddit = reddit.subreddit('travel') #any subreddit you want to monitor
    
    
    keywords = {'travel ', 'visit ', 'go ', 'Travel', 'Visit', 'Go'} #makes a set of keywords to find in subreddits
    
    for submission in subreddit.hot(limit=100): #this views the top 10 posts in that subbreddit
    
        n_title = submission.title.lower() #makes the post title lowercase so we can compare our keywords with it.
        
        n_comments = submission.comments
        
        '''
        #for i in keywords: #goes through our keywords
        for top_level_comment in submission.comments:
                
            if isinstance(top_level_comment, MoreComments):
                continue
            
            #for i in keywords:
              
            newComment = Comment_Reader(top_level_comment.body)
            newComment.readStr()
            if (top_level_comment.body in commentsChecked) or ("Reminder, I'm just a bot. Have a safe and happy journey!" in top_level_comment.body):
                print()
            else:
            #print(newComment.returnAdvice())  
            #submission.reply(newComment.returnAdvice())
                if (len(newComment.returnAdvice())>0):
                    top_level_comment.reply(newComment.returnAdvice())
                commentsChecked.append(top_level_comment.body)
            #print(top_level_comment.body)
        '''
        flair = str(submission.link_flair_text)
        
        flair_final = flair.lower()
        
        if flair_final == 'itinerary' or flair_final == 'advice' or flair_final == 'question':
        
            #sub.add_comment('You posted with this flair! Congrats!')
                
            newComment = Comment_Reader(submission.title)
            newComment.readStr()
            #print(newComment.returnAdvice())
            if submission.title in commentsChecked:
                print()
            else:        
                if (len(newComment.returnAdvice())>0):
                    submission.reply(newComment.returnAdvice()) 
                commentsChecked.append(submission.title)
            
            newComment2 = Comment_Reader(submission.selftext)
            newComment2.readStr()
            #print(newComment2.returnAdvice())  
            if submission.selftext in commentsChecked:
                print()
            else:        
                if (len(newComment2.returnAdvice())>0):
                    submission.reply(newComment2.returnAdvice()) 
                commentsChecked.append(submission.selftext)
