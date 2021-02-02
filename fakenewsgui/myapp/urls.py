# coding: utf-8
# -*- coding: utf-8 -*-

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
from django.urls import path, re_path
from myapp.strainer import *
from myapp.util import *
from myapp.forms import *
from myapp.views import *
from . import *
from myapp import views

app_name='myapp'

urlpatterns = [
    path('', views.index, name='index'),
    #path('/home/lewis/Documents/FakeNewsProject/fakenewsgui/myapp', myapp.urls),
    #path('urlForm',urlForm)
]