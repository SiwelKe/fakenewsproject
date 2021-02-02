# coding: utf-8
# -*- coding: utf-8 -*-

#load dataset into db
#load a page from url
#parse page and store using beautiful soup


import os,sys,re,time
import pandas as pd
from bs4 import SoupStrainer,BeautifulSoup
#from fakenewsgui import *
#from .strainer import *
#from fakenewsgui.myapp import *



#STEP 1-ALLOW DJANGO TO RUN FROM COMMAND LINE AND NOT BROWSER
project_path="/home/lewis/Documents/FakeNewsProject/fakenewsgui"
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
"fakenewsgui.settings"),
sys.path.append(project_path)
os.chdir(project_path)
from django.core.wsgi import get_wsgi_application
application=get_wsgi_application()
from django.contrib.gis.views import feed



from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib3, re, string, json, html
from urllib3.exceptions import HTTPError
from io import StringIO
from nltk.stem import PorterStemmer
import os,sys

#STEP 1-ALLOW DJANGO TO RUN FROM COMMAND LINE AND NOT BROWSER
project_path="/home/lewis/Documents/FakeNewsProject/fakenewsgui"
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
"fakenewsgui.settings"),
sys.path.append(project_path)
os.chdir(project_path)

from django.core.wsgi import get_wsgi_application
application=get_wsgi_application()
from django.contrib.gis.views import feed
from . import *
from myapp.models import *
#from fakenewsgui.myapp.models import *
#from fakenewsgui.myapp.models import ArticleExample






ps= PorterStemmer()

#class to clean the dataset 
#remove common terms
#loading up the web page and grabbing the resulting HTML file.
# extract the visible text, strip it of punctuation, ensure it is a real word, then stem it.
#BeautifulSoup for parsing the HTML
#urllib3 for loading the web pages
#PorterStemmer to do the word stemming.


class SoupStrainer():
    englishDictionary={}
    haveHeadline=False
    recHeadline=''
    locToGet=''
    pageData=None
    errMsg=None
    soup=None
    msgOutput=True
    #initialize dictionary/english words as json

    def init(self):
        with open("/home/lewis/Documents/FakeNewsProject/fakenewsgui/words_dictionary.json") as json_file:
            self.englishDictionary=json.load(json_file)

    #filter out tags that are not visible from webpage
    def tag_filter(self,element):
        if element.parent.name in ['style','script','head',
         'title', 'meta', '[document]']:
         return  False
         if isinstance(element,Comment):
             return False
        return True

    #fucntion to get the headlines
    def find_headline(self, soup):
        reOgTitle = re.compile('og:title', re.IGNORECASE)
        reTwTitle = re.compile('twitter:title', re.IGNORECASE)
        haveHeadline = False
    
    #confirming that address in file is a url
    def loadAddress(self,address):
        self.locToGet = address
        self.haveHeadline = False

        htmatch = re.compile('.*http.*')
        user_agent = {'user-agent': 'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0'}
        ps = PorterStemmer()

        if(htmatch.match(self.locToGet) is None):
            self.locToGet = "http://" + self.locToGet
        

        #load the url
        #get the html file
        if(len(self.locToGet) > 5):
            if(self.msgOutput):
                print("Ready to load page data for: " + self.locToGet + " which was derived from " + address)

            try:
                urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
                http = urllib3.PoolManager(2, headers=user_agent)
                r = http.request('GET', self.locToGet)
                self.pageData = r.data
                if(self.msgOutput):
                    print("Page data loaded OK")
                    #print(self.pageData)
            except:
                self.errMsg = 'Error on HTTP request'
                if(self.msgOutput):
                    print("Problem loading the page")
                return False


            #get the text from html file and clean by removing punctuations
            #using beautiful soup to get page data ie the text and headline
            self.extractText = ''
            self.recHeadline = self.locToGet
            self.soup = BeautifulSoup(self.pageData, 'html.parser')
            self.find_headline(self.soup)

            scraped_texts = self.soup.findAll(text=True)

            #pass the text data through out tag filter func
            visible_text = filter(self.tag_filter, scraped_texts)
            allVisText = u"".join(t.strip() for t in visible_text)


            for word in allVisText.split():
                canonWord = word.lower()
                canonWord = canonWord.translate(str.maketrans('', '', string.punctuation))
                canonWord = canonWord.strip(string.punctuation)

                #if word is in the dictionary json file,stem it
                if(canonWord in self.englishDictionary):
                    canonWord = ps.stem(canonWord)
                    self.extractText = self.extractText + canonWord + " "
                    #self.extractText = canonWord + '',
              #=else:
                    #print("Excluded word: " + canonWord)

            return True





#scrapping using beautiful soup
ss=SoupStrainer()
print("Starting the dictionary...")
ss.init()

#scrapping function
#politifact provides a csv of urls

def harvest_Politifact_data():
    print("Ready to harvest Politifact data.")
    input("Enter to continue, Ctl+C to cancel")
    print("Reading URLs file")

#convert the file into a dataframe called df_csv
#csv file as URLS and Scores

df_csv=pd.read_csv("/home/lewis/Documents/newsbot/politifact_data.csv"
,error_bad_lines=False,quotechar='"', thousands=',',low_memory=False)


#Parser

for index, row in df_csv.iterrows():
    #each url is found in the news_url column in csv
      print("Attempting URL: " + row['news_url'])

      if(ss.loadAddress(row['news_url'])):
         print("Loaded OK")

         #clean out more using 500 characters
         if (len(ss.extractText)>500):

             #save the results of parser into a body_text
             #ae=ArticleExample(models.Model)
             ae = ArticleExample()
             ae.body_text=ss.extractText
             ae.origin_url = row['news_url']
             ae.origin_source = 'politifact data'
             ae.bias_score = 0 # Politifact data doesn't have this
             ae.bias_class = 5 # 5 is 'no data'
             ae.quality_score = row['score']
             ae.quality_class = row['class']
             ae.save()
             print("Data is Saved, Loading…")
             time.sleep(1)
         else:
            print("**** This URL produced insufficient data.")
      else:
        print("**** Error on that URL ^^^^^")
                
                
                
                
        
            


