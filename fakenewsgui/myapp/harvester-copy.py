# coding: utf-8
# -*- coding: utf-8 -*-

#load dataset into db
#load a page from url
#parse page and store using beautiful soup


import os,sys,re,time
import pandas as pd
from bs4 import SoupStrainer,BeautifulSoup
#from fakenewsgui import *
from .strainer import *
from . import *



#STEP 1-ALLOW DJANGO TO RUN FROM COMMAND LINE AND NOT BROWSER
project_path="/home/lewis/Documents/FakeNewsProject/fakenewsgui"
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
"fakenewsgui.settings"),
sys.path.append(project_path)
os.chdir(project_path)
from django.core.wsgi import get_wsgi_application
application=get_wsgi_application()
from django.contrib.gis.views import feed

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
             ae=ArticleExample(models.Model)
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
                
                
                
                
        
            


