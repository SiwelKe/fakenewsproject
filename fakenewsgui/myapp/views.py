# pyright: reportMissingImports=false, reportUnusedVariable=false, reportUntypedBaseClass=error,reportUndefinedVariable=false
from django.shortcuts import render
import pandas as pd
import numpy as np
import pickle,os,sys,re,time
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
from myapp.forms import *
from myapp.models import *
from . import *
from django.http import Http404

# Create your views here.
def index(request):
    url = request.GET.get('u')
    if((url is not None) and (len(url) > 5)):

        # 1. Load the models from saved location
        print("STARTING")
    
        log_model = pickle.load(open('/home/lewis/Documents/FakeNewsProject/fakenewsgui/myapp/log_model.sav', 'rb'))
        svc_model = pickle.load(open('/home/lewis/Documents/FakeNewsProject/fakenewsgui/myapp/svc_model.sav', 'rb'))
        mlp_model = pickle.load(open('/home/lewis/Documents/FakeNewsProject/fakenewsgui/myapp/MLPC_model.sav', 'rb'))
        gnb_model = pickle.load(open('/home/lewis/Documents/FakeNewsProject/fakenewsgui/myapp/gaussian_model.sav', 'rb'))
        mnb_model=  pickle.load(open('/home/lewis/Documents/FakeNewsProject/fakenewsgui/myapp/multinomial_model.sav','rb'))
        bernoulli_model = pickle.load(open('/home/lewis/Documents/FakeNewsProject/fakenewsgui/myapp/bernoulli_model.sav', 'rb'))
        
        print("Models have been loaded successful.")


        cDict = loadCanonDict()
        soup = SoupStrainer()
        soup.init()
        print("Setup complete")
        print("Analyzing your link: " + url)

        if(soup.loadAddress(url)):
            
            siteArticle = buildExampleRow(soup.extractText, cDict)
        else:
            raise Http404("YOU ENTERED A URL HAVING WRONG FORMAT OR YOU ARE OFFLINE.PLEASE TRY AGAIN")
            #return render(request, '404.html', {'URL', url})

        siteArticle = siteArticle.reshape(1, -1)

        
        # 5. Send the X row to the model to produce a prediction
        svc_prediction = svc_model.predict(siteArticle)
        svc_prob = svc_model.predict_proba(siteArticle)
        

        mlp_prediction = mlp_model.predict(siteArticle)
        mlp_prob = mlp_model.predict_proba(siteArticle)
        

        log_prediction = log_model.predict(siteArticle)
        log_prob = log_model.predict_proba(siteArticle)


        gnb_prediction = gnb_model.predict(siteArticle)
        gnb_prob = gnb_model.predict_proba(siteArticle)

        mnb_prediction = mnb_model.predict(siteArticle)
        mnb_probabilities = mnb_model.predict_proba(siteArticle)

        bernoulli_prediction = bernoulli_model.predict(siteArticle)
        bernoulli_probabilities = bernoulli_model.predict_proba(siteArticle)

        countlog=0
        countsvc=0
        countbern=0
        countmlp=0
        countmnb=0
        countgnb=0

        if( log_prediction==[4] or log_prediction == [2]):
            countlog+=1
            print(countlog)

        if( svc_prediction==[4] or svc_prediction == [2]):
            countsvc+=1
            print(countsvc)

        if( mlp_prediction==[4] or mlp_prediction == [2]):
            countmlp+=1
            print(countmlp)

        if( bernoulli_prediction==[4] or bernoulli_prediction == [2]):
            countbern+=1
            print(countbern)


        if( mnb_prediction==[4] or mnb_prediction == [2]):
            countmnb+=1
            print(countmnb)

        if( gnb_prediction==[4] or gnb_prediction == [2]):
            countgnb+=1
            print(countgnb)


        counttot=countlog+countmlp+countsvc+countgnb+countmnb+countbern
        
        if (counttot >= 3):
            print("THIS IS REAL NEWS ")
            print("The count is:", counttot)

        elif (counttot < 3):
            print("The count is:", counttot)
            print("THIS IS FAKE NEWS")
        
        


        # 6. Display the processed text and the results
        
        context = {'headline':soup.recHeadline, 'words': soup.extractText, 'url' : url,
                   'counttot': counttot,
                   
                   }

        return render(request, '/home/lewis/Documents/FakeNewsProject/fakenewsgui/myapp/templates/results.html', context)
    else:
        #user to add a url
        return render(request, '/home/lewis/Documents/FakeNewsProject/fakenewsgui/myapp/templates/urlForm.html')



