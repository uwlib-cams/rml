import os
import rdflib
from rdflib import *

# define namespaces
rdae = Namespace("http://rdaregistry.info/Elements/e/")
rdam = Namespace("http://rdaregistry.info/Elements/m/")
rdai = Namespace("http://rdaregistry.info/Elements/i/")

# load data files into separate lists
workList = os.listdir('data/2020_7_28/work/')
expressionList = os.listdir('data/2020_7_28/expression')
manifestationList = os.listdir('data/2020_7_28/manifestation')
itemList = os.listdir('data/2020_7_28/item')

itemGraph = Graph()
for item in itemList: # load items into graph
    itemGraph.load(f"file:///home/mcm104/rml/rdfxml/data/2020_7_28/item/{item}", format="xml")
itemGraph.bind("rdai", rdai) # bind item namespace to graph

manifestationGraph = Graph()
for manifestation in manifestationMatchList: # load manifestations into graph
    manifestationGraph.load(f"file:///home/mcm104/rml/rdfxml/data/2020_7_28/manifestation/{manifestation}.xml", format="xml")
manifestationGraph.bind("rdam", rdam) # bind manifestation namespace to graph

expressionGraph = Graph()
for expression in expressionMatchList: # load expressions into graph
    expressionGraph.load(f"file:///home/mcm104/rml/rdfxml/data/2020_7_28/expression/{expression}.xml", format="xml")
expressionGraph.bind("rdae", rdae) # bind expression namespace to graph

if not os.path.exists("data/WEMI"): # create folder for output
    os.system(f"mkdir data/WEMI")

for item in itemGraph.subjects(predicate=rdai.P40049, object=None): # look for the IRIs of item records that contain the property "has manifestation exemplified"
    recordList = [] # list to contain just the records that belong together
    item_label = item.split('/')[-1] # get just the identifier off the IRI for the item record
    item_filename = f"item/{item_label}.xml" # filename as it appears in the original folder
    recordList.append(item_filename) # add item filename to record list
    for manifestation in itemGraph.objects(subject=item, predicate=rdai.P40049): # look for the IRI of the manifestation record that is exemplified by the current item
        manifestation_label = manifestation.split('/')[-1] # get just the identifier
        manifestation_filename = f"manifestation/{manifestation_label}.xml" # filename as it appears in the original folder
        if not os.path.exists(f"data/2020_7_28/{manifestation_filename}"): # make sure the file exists in the original folder
            pass # if not, skip it
        else: # if it does exist
            recordList.append(manifestation_filename) # add it to record list
        for expression in manifestationGraph.objects(subject=manifestation, predicate=rdam.P30139): # look for the IRI of the expression record that is manifested by the current manifestation
            expression_label = expression.split('/')[-1] # get just the identifier
            expression_filename = f"expression/{expression_label}.xml" # filename as it appears in the original folder
            if not os.path.exists(f"data/2020_7_28/{expression_filename}"): # make sure the file exists in the original folder
                pass # if not, skip it
            else: # if it does exist
                recordList.append(expression_filename) # add it to the record list
            for work in expressionGraph.objects(subject=expression, predicate=rdae.P20231): # look for the IRI of the work record that is expressed by the current expression
                work_label = work.split('/')[-1] # get just the identifier
                work_filename = f"work/{work_label}.xml" # filename as it appears in the original folder
                if not os.path.exists(f"data/2020_7_28/{work_filename}"): # make sure the file exists in the original folder
                    pass # if not, skip it
                else: # if it does exist
                    recordList.append(work_filename) # add it to the record list
    dir_label = item.split('/')[-1] # label for the directory will be the item identifier (because all of these matches are guaranteed to have an item but not the others)
    os.system(f"mkdir data/WEMI/{dir_label}") # create directory
    for record in recordList:
        recordGraph = Graph()
        recordGraph.load(f"file:///home/mcm104/rml/rdfxml/data/2020_7_28/{record}", format="xml") # load just these matches into their own graph
        label = record.split('.')[0] # name them according to their identifiers
        recordGraph.serialize(destination=f"data/WEMI/{dir_label}" + label + ".ttl", format="turtle") # save to directory, serialized as turtle
