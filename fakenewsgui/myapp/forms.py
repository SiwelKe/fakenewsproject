# this file isn't needed, I had to create it to get the crispy_tags form, then I modified that to use 
# a GET request to make the final URL shareable

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Submit, Field, Fieldset

from django.forms import ModelForm, Textarea
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
from myapp.strainer import *
from myapp.util import *
from myapp.models import *
from . import *


class ArticleTesterForm(ModelForm):
    def __init__(self, *args, **kwargs):
        
        # first call parent's constructor
        super(ArticleTesterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            ButtonHolder(
                Field('entryURL'),
                Submit('submit', 'Analyze', css_class='btn btn-primary')
            )
            )
     
    class Meta:
        model = UserEntry
        exclude = []