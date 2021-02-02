# coding: utf-8
# -*- coding: utf-8 -*-
#to return our dictionary of canonical words

#from fakenewsgui.myapp.models import *
#from fakenewsgui.myapp import *

from . import *
import numpy as np
from myapp.models import *

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
        print('.', end='', flush=True)
        #print("." ,end='')

    return( (Y_vector, examplesMatrix))
