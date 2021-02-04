# coding: utf-8
# -*- coding: utf-8 -*-
# pyright: reportMissingImports=false, reportUnusedVariable=false, reportUntypedBaseClass=error,reportUndefinedVariable=false

import pandas as pd
import numpy as np
from sklearn.metrics import *
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
#from sklearn.neural_network.multilayer_perceptron import MLPClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression

from . import *
import pickle
import os, sys, re, time
import numpy as np
#STEP 1-ALLOW DJANGO TO RUN FROM COMMAND LINE AND NOT BROWSER
project_path="/home/lewis/Documents/FakeNewsProject/fakenewsgui"
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
"fakenewsgui.settings"),
sys.path.append(project_path)
os.chdir(project_path)

from django.core.wsgi import get_wsgi_application
application=get_wsgi_application()
from django.contrib.gis.views import feed
from myapp.scrapper import *
from myapp.util import *


from myapp.models import *

#LOADING UTIL FILE


# coding: utf-8
# -*- coding: utf-8 -*-
#to return our dictionary of canonical words

#from fakenewsgui.myapp.models import *
#from fakenewsgui.myapp import *

from . import *
import numpy as np
#from .models import *

def loadCanonDict():
    canonDict = DictEntry.objects.all()
    dictSize = canonDict.count() + 1
    cDict = {}
    for cw in canonDict:
        cDict[cw.canonWord] = cw.pk
    
    return cDict

#create dictionary table with all our words

#buildExampleRow: Take in some text, spit out a row vector ready for stacking or analysis
#In: body text in canonical-word form and the canonical dictionary we're using
#Out: a numpy array with 1s and 0s set up properly.
#Process an article into a row for one example. This is a task we’ll need to repeat again if we test any new example,
#so again we’ll create a utility function for it:

def buildExampleRow(body_text, cDict):
    dictSize = len(cDict.keys())

    example_vector = np.zeros(dictSize+2)
    cwords = body_text.split()


#example_vector=one_ex_vector
#if word is in article==1,else its 0
    for word in cwords:
        if(word in cDict.keys()):
            example_vector[cDict[word]-1] = 1
        else:
            pass
            #print("This word doesn't exist in the dict:" + word)

    return (example_vector)

#processExamples: Using examples from the DB, process them into a training set
#in: The examples as a Django queryset, the canonical dictionary
#out: A tuple with Y_vector and Examples_matrix

#function to load up our examples from the database.
def processExamples(qs_Examples, cDict):
    Y_vector = np.zeros(qs_Examples.count(), dtype=np.int8)
    Y_vec_count = 0
    examplesMatrix = None
    
    for ex in qs_Examples:
        Y_vector[Y_vec_count] = int(ex.quality_class)
        Y_vec_count = Y_vec_count + 1
        
        if(examplesMatrix is None):
            examplesMatrix = buildExampleRow(ex.body_text, cDict)
        else:
            examplesMatrix = np.vstack([examplesMatrix, buildExampleRow(ex.body_text, cDict)])
        #print('.', end='', flush=True)
        #print("." )
        pass

    return( (Y_vector, examplesMatrix))





#Method:
# 1. Load the models from disk
print("Loading model...")
log_model = pickle.load(open('/home/lewis/Documents/FakeNewsProject/fakenewsgui/myapp/log_model.sav', 'rb'))
svc_model = pickle.load(open('/home/lewis/Documents/FakeNewsProject/fakenewsgui/myapp/svc_model.sav', 'rb'))
mlp_model = pickle.load(open('/home/lewis/Documents/FakeNewsProject/fakenewsgui/myapp/MLPC_model.sav', 'rb'))
mnb_model=  pickle.load(open('/home/lewis/Documents/FakeNewsProject/fakenewsgui/myapp/multinomial_model.sav','rb'))
gnb_model = pickle.load(open('/home/lewis/Documents/FakeNewsProject/fakenewsgui/myapp/gaussian_model.sav', 'rb'))
bernoulli_model = pickle.load(open('/home/lewis/Documents/FakeNewsProject/fakenewsgui/myapp/bernoulli_model.sav', 'rb'))
print("Model loaded successful.")


# 2. Use SoupStrainer to get the URL and process the article-turn it into an example

print("Starting the  dictionaries of words")
cDict = loadCanonDict()
soup = SoupStrainer()
soup.init()

# 3. Get user input to get a URL
#turn article into input for the model
url = input("Enter a link to analyze: ")

print("Analyzing your link: " + url)
if(soup.loadAddress(url)):
    siteArticle = buildExampleRow(soup.extractText, cDict)
else:
    print("This is a wrong URL or You are offline")
    exit(0)

siteArticle = siteArticle.reshape(1, -1)

# 5. Send the X row to the model to produce a prediction

log_prediction = log_model.predict(siteArticle)
log_probabilities = log_model.predict_proba(siteArticle)

svc_prediction = svc_model.predict(siteArticle)
svc_probabilities = svc_model.predict_proba(siteArticle)

mlp_prediction = mlp_model.predict(siteArticle)
mlp_probabilities = mlp_model.predict_proba(siteArticle)

gnb_prediction = gnb_model.predict(siteArticle)
gnb_probabilities = gnb_model.predict_proba(siteArticle)

mnb_prediction = mnb_model.predict(siteArticle)
mnb_probabilities = mnb_model.predict_proba(siteArticle)

bernoulli_prediction = bernoulli_model.predict(siteArticle)
bernoulli_probabilities = bernoulli_model.predict_proba(siteArticle)

# 6. Display the processed text and the results


print("*** SVC ")
print("Prediction on this article is: ")
print(svc_prediction)
print("Probabilities:")
print(svc_probabilities)
print("\n")


print("*** Logistic ")
print("Prediction on this article is: ")
print(log_prediction)

print("Probabilities:")
print(log_probabilities)
print("\n")


print("*** MLP ")
print("Prediction on this article is: ")
print(mlp_prediction)
print("Probabilities:")
print(mlp_probabilities)
print("\n")



print("*** MultinomialNB")
print("Prediction on this article is: ")
print(mnb_prediction)
print("Probabilities:")
print(mnb_probabilities)
print("\n")



print("*** BernoulliNB")
print("Prediction on this article is: ")
print(bernoulli_prediction)
print("Probabilities:")
print(bernoulli_probabilities)
print("\n")


print("*** GNB")
print("Prediction on this article is: ")
print(gnb_prediction)

print("Probabilities:")
print(gnb_probabilities)

print("**********************************************")

count=0
countlog=0
countsvc=0
countbern=0
countmlp=0
countmnb=0
countgnb=0

if( log_prediction==[4] or log_prediction == [2]):
    countlog+=1

if( svc_prediction==[4] or svc_prediction == [2]):
    countsvc+=1

if( mlp_prediction==[4] or mlp_prediction == [2]):
    countmlp+=1

if( bernoulli_prediction==[4] or bernoulli_prediction == [2]):
    countbern+=1


if( mnb_prediction==[4] or mnb_prediction == [2]):
    countmnb+=1

if( gnb_prediction==[4] or gnb_prediction == [2]):
    countgnb+=1


counttot=countlog+countmlp+countsvc+countgnb+countmnb+countbern
if (counttot >= 3):
    print("THIS IS REAL NEWS ")
    print("The count is:", counttot)
else:
    print("The count is:", counttot)
    print("THIS IS FAKE NEWS")
                  
       
print("**********************************************")
        