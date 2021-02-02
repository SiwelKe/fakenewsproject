# coding: utf-8
# -*- coding: utf-8 -*-

#TO SAVE THE MODELS

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

import pickle
import os, sys, re, time
#STEP 1-ALLOW DJANGO TO RUN FROM COMMAND LINE AND NOT BROWSER
project_path="/home/lewis/Documents/FakeNewsProject/fakenewsgui"
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
"fakenewsgui.settings"),
sys.path.append(project_path)
os.chdir(project_path)

from django.core.wsgi import get_wsgi_application
application=get_wsgi_application()
from django.contrib.gis.views import feed
#from fakenewsgui.myapp.models import *
#from fakenewsgui.myapp.util import *
from . import *
from myapp.models import *

#LOADING UTIL FILE
# coding: utf-8
# -*- coding: utf-8 -*-
#to return our dictionary of canonical words

#from fakenewsgui.myapp.models import *
#from fakenewsgui.myapp import *
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
            print("This word doesn't exist in the dict:" + word)

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
        print(".")

    return( (Y_vector, examplesMatrix))









print("Setting up..")
cDict = loadCanonDict()
qs_Examples = ArticleExample.objects.filter(quality_class__lt = 5)
print("Processing examples")

(Y_vector, examplesMatrix) = processExamples(qs_Examples, cDict)
X_train, X_test, y_train, y_test = train_test_split(examplesMatrix, Y_vector, test_size=0.2)

#a dictionary with our models
chosen_models = {}
chosen_models['/home/lewis/Documents/FakeNewsProject/fakenewsgui/myapp/MLPC_model.sav'] = MLPClassifier(hidden_layer_sizes=(128,64,32,16,8), max_iter=2500)
chosen_models['/home/lewis/Documents/FakeNewsProject/fakenewsgui/myapp/svc_model.sav'] = SVC(gamma='scale', probability = True)
chosen_models['/home/lewis/Documents/FakeNewsProject/fakenewsgui/myapp/log_model.sav'] = LogisticRegression()
#chosen_models['fakenewsgui/myapp/GaussianNB_model.sav'] = GaussianNB()
chosen_models['/home/lewis/Documents/FakeNewsProject/fakenewsgui/myapp/gaussian_model.sav'] = GaussianNB()


#cycle through the chosen models, train them, and decide if we want to keep them
for fname, model in chosen_models.items():
    print("Working on " + fname)
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    print("Classification report: ")
    print(classification_report(predictions, y_test))
    print("***************")

    dosave = input("Save " + fname + "? ")
    if(dosave == 'y' or dosave == 'Y'):
        print("Saving...")
        pickle.dump(model, open(fname, 'wb'))
        print("Saved!")
    else:
        print("Not saved!")