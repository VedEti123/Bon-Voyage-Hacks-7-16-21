from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup
import re
import csv

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
                    #print(string[start:altEnd])
                    self.cities.append(string[start:altEnd])        
        
    def createCSV(self):

        for i in range(len(self.cities)):
            self.dictionary[self.cities[i]]=self.cities[i]
           
        datafile = open("Cities.csv", "w")

        writer = csv.writer(datafile)
        for name, rating in self.dictionary.items():
            writer.writerow([name, rating])
        datafile.close()
        return self.dictionary
    
web = WebScrape()
web.scrapeCities()
web.createCSV()
