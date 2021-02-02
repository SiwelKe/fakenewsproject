from django.shortcuts import render
import pandas as pd
import numpy as np
import pickle,os,sys,re,time



#STEP 1-ALLOW DJANGO TO RUN FROM COMMAND LINE AND NOT BROWSER
project_path="/home/lewis/Documents/FakeNewsProject/fakenewsgui"
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
"fakenewsgui.settings"),
sys.path.append(project_path)
os.chdir(project_path)

from django.core.wsgi import get_wsgi_application
application=get_wsgi_application()
from django.contrib.gis.views import feed
from myapp.strainer import *
from myapp.util import *
from myapp.forms import *
from myapp.models import *
from . import *





# Create your views here.
def index(request):
    
    url = request.GET.get('u')
    if((url is not None) and (len(url) > 5)):

        # 1. Load the model from disk
        print("Setting up")
        #svc_model = pickle.load(open('fakenewsproject/svc_model.sav', 'rb'))
        #mlp_model = pickle.load(open('fakenewsproject/MLPC_model.sav', 'rb'))
        #log_model = pickle.load(open('fakenewsproject/log_model.sav', 'rb'))

        log_model = pickle.load(open('/home/lewis/Documents/FakeNewsProject/fakenewsgui/myapp/log_model.sav', 'rb'))
        svc_model = pickle.load(open('/home/lewis/Documents/FakeNewsProject/fakenewsgui/myapp/svc_model.sav', 'rb'))
        mlp_model = pickle.load(open('/home/lewis/Documents/FakeNewsProject/fakenewsgui/myapp/MLPC_model.sav', 'rb'))
        #gnb_model = pickle.load(open('/home/lewis/Documents/FakeNewsProject/fakenewsgui/myapp/gaussian_model.sav', 'rb'))
        print("Models loaded successful.")


        cDict = loadCanonDict()
        ss = SoupStrainer()
        ss.init()
        print("Setup complete")
        print("Analyzing URL: " + url)

        if(ss.loadAddress(url)):
            articleX = buildExampleRow(ss.extractText, cDict)
        else:
            print("Error on URL, exiting")
            return render(request, 'urlFail.html', {'URL', url})

        articleX = articleX.reshape(1, -1)

        
        # 5. Send the X row to the model to produce a prediction
        svc_prediction = svc_model.predict(articleX)
        svc_probabilities = svc_model.predict_proba(articleX)
        
        mlp_prediction = mlp_model.predict(articleX)
        mlp_probabilities = mlp_model.predict_proba(articleX)
        
        log_prediction = log_model.predict(articleX)
        log_probabilities = log_model.predict_proba(articleX)

        #gnb_prediction = gnb_model.predict(articleX)
        #gnb_probabilities = gnb_model.predict_proba(articleX)

        # The classifications produced as predictions, espcially by the SVC, are sometimes different
        # than the highest probability. So, we'll calculate fake + dodgy and seems legit + true to come up 
        # with a ruling of yes or no, is it real or fake. Then we'll give the probabilties to allow
        # the user to make up their mind.

        #Total Fake = Fake (class 0) probability + Dodgy (class 1) probability

        #Total Real = Seems Legit (class 3) probability + True (class 3) probability

        svc_prb = (svc_probabilities[0][0]*100, svc_probabilities[0][1]*100, svc_probabilities[0][2]*100, svc_probabilities[0][3]*100)
        svc_totFake = (svc_probabilities[0][0]*100) + (svc_probabilities[0][1]*100)
        svc_totReal = (svc_probabilities[0][2]*100) + (svc_probabilities[0][3]*100)

        mlp_prb = (mlp_probabilities[0][0]*100, mlp_probabilities[0][1]*100, mlp_probabilities[0][2]*100, mlp_probabilities[0][3]*100)
        mlp_totFake = (mlp_probabilities[0][0]*100) + (mlp_probabilities[0][1]*100)
        mlp_totReal = (mlp_probabilities[0][2]*100) + (mlp_probabilities[0][3]*100)

        log_prb = (log_probabilities[0][0]*100, log_probabilities[0][1]*100, log_probabilities[0][2]*100, log_probabilities[0][3]*100)
        log_totFake = (log_probabilities[0][0]*100) + (log_probabilities[0][1]*100)
        log_totReal = (log_probabilities[0][2]*100) + (log_probabilities[0][3]*100)

        #gnb_prb = (gnb_probabilities[0][0]*100, gnb_probabilities[0][1]*100, gnb_probabilities[0][2]*100, gnb_probabilities[0][3]*100)
        #gnb_totFake = (gnb_probabilities[0][0]*100) + (gnb_probabilities[0][1]*100)
        #gnb_totReal = (gnb_probabilities[0][2]*100) + (gnb_probabilities[0][3]*100)


        #TOTAL PROBABILITY
        fin_prb = ( (((svc_probabilities[0][0]*100)+(mlp_probabilities[0][0]*100)+(log_probabilities[0][0]*100))/3), 
                    (((svc_probabilities[0][1]*100)+(mlp_probabilities[0][1]*100)+(log_probabilities[0][1]*100))/3),
                    (((svc_probabilities[0][2]*100)+(mlp_probabilities[0][2]*100)+(log_probabilities[0][2]*100))/3),
                    (((svc_probabilities[0][3]*100)+(mlp_probabilities[0][3]*100)+(log_probabilities[0][3]*100))/3) )
        
        fin_totFake = (svc_totFake + mlp_totFake + log_totFake)/3
        fin_totReal = (svc_totReal + mlp_totReal + log_totReal)/3

        #fin_totFake = (gnb_totFake)
        #fin_totReal = (gnb_totReal )

        # 6. Display the processed text and the results
        
        context = {'headline':ss.recHeadline, 'words': ss.extractText, 'url' : url,
                   'svc_totFake': svc_totFake, 
                   'svc_totReal': svc_totReal, 
                   'svc_prediction': svc_prediction, 
                   'svc_probabilities': svc_prb, 
                   'mlp_totFake': mlp_totFake, 
                   'mlp_totReal': mlp_totReal, 
                   'mlp_prediction': mlp_prediction, 
                   'mlp_probabilities': mlp_prb,
                   'log_totFake': log_totFake, 
                   'log_totReal': log_totReal, 
                   'log_prediction': log_prediction, 
                   'log_probabilities': log_prb,
                   'fin_totFake': fin_totFake, 
                   'fin_totReal': fin_totReal, 
                   'fin_probabilities': fin_prb
                   }

        return render(request, '/home/lewis/Documents/FakeNewsProject/fakenewsgui/myapp/templates/results.html', context)
    else:
        #user to add a url
        return render(request, '/home/lewis/Documents/FakeNewsProject/fakenewsgui/myapp/templates/urlForm.html')