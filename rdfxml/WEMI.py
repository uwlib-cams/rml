import os
import rdflib
from rdflib import *

rdae = Namespace("http://rdaregistry.info/Elements/e/")
rdam = Namespace("http://rdaregistry.info/Elements/m/")
rdai = Namespace("http://rdaregistry.info/Elements/i/")

workList = os.listdir('data/2020_7_28/work/')
expressionList = os.listdir('data/2020_7_28/expression')
manifestationList = os.listdir('data/2020_7_28/manifestation')
itemList = os.listdir('data/2020_7_28/item')

itemMatchList = []

manifestationMatchList = []

itemGraph = Graph()
for item in itemList:
    itemGraph.load(f"file:///home/mcm104/rml/rdfxml/data/2020_7_28/item/{item}", format="xml")
itemGraph.bind("rdai", rdai)
for item in itemGraph.subjects(predicate=rdai.P40049, object=None):
    label = item.split('/')[-1]
    # filename = f"{label}.xml"
    itemMatchList.append(label)
for manifestation in itemGraph.objects(subject=None, predicate=rdai.P40049):
    label = manifestation.split('/')[-1]
    filename = f"{label}.xml"
    i = 0
    if not os.path.exists(f"data/2020_7_28/manifestation/{filename}"):
        i = i + 1
        pass
    else:
        manifestationMatchList.append(label)
print(f"Skipped: {i}")

expressionMatchList = []

manifestationGraph = Graph()
for manifestation in manifestationMatchList:
    manifestationGraph.load(f"file:///home/mcm104/rml/rdfxml/data/2020_7_28/manifestation/{manifestation}.xml", format="xml")
manifestationGraph.bind("rdam", rdam)
for expression in manifestationGraph.objects(subject=None, predicate=rdam.P30139):
    label = expression.split('/')[-1]
    filename = f"{label}.xml"
    i = 0
    if not os.path.exists(f"data/2020_7_28/expression/{filename}"):
        i = i + 1
        pass
    else:
        expressionMatchList.append(label)
print(f"Skipped: {i}")

workMatchList = []

expressionGraph = Graph()
for expression in expressionMatchList:
    expressionGraph.load(f"file:///home/mcm104/rml/rdfxml/data/2020_7_28/expression/{expression}.xml", format="xml")
expressionGraph.bind("rdae", rdae)
for work in expressionGraph.objects(subject=None, predicate=rdae.P20231):
    label = work.split('/')[-1]
    filename = f"{label}.xml"
    i = 0
    if not os.path.exists(f"data/2020_7_28/work/{filename}"):
        i = i + 1
        pass
    else:
        workMatchList.append(label)
print(f"Skipped: {i}")

#fileGraph = Graph()
#fileGraph.bind("rdae", rdae)
#fileGraph.bind("rdam", rdam)
#fileGraph.bind("rdai", rdai)
#for work in workMatchList:
#    if not os.path.exists(f"data/2020_7_28/work/{filename}"):
#        i = i + 1
#        pass
#    else:
#        fileGraph.load(f"file:///home/mcm104/rml/rdfxl/data/2020_7_28/work/{work}.xml", format="xml")
#print(f"Skipped: {i}")
#for expression in expressionMatchList:
#    fileGraph.load(f"file:///home/mcm104/rml/rdfxl/data/2020_7_28/expression/{expression}.xml", format="xml")
#for manifestation in manifestationMatchList:
#    fileGraph.load(f"file:///home/mcm104/rml/rdfxl/data/2020_7_28/manifestation/{manifestation}.xml", format="xml")
#for item in itemMatchList:
#    fileGraph.load(f"file:///home/mcm104/rml/rdfxl/data/2020_7_28/item/{item}.xml", format="xml")

if not os.path.exists("data/WEMI"):
    os.system(f"mkdir data/WEMI")

for item in itemGraph.subjects(predicate=rdai.P40049, object=None):
    recordList = []
    item_label = item.split('/')[-1]
    item_filename = f"item/{item_label}.xml"
    recordList.append(item_filename)
    for manifestation in itemGraph.objects(subject=item, predicate=rdai.P40049):
        manifestation_label = manifestation.split('/')[-1]
        manifestation_filename = f"manifestation/{manifestation_label}.xml"
        if not os.path.exists(f"data/2020_7_28/{manifestation_filename}"):
            pass
        else:
            recordList.append(manifestation_filename)
        for expression in manifestationGraph.objects(subject=manifestation, predicate=rdam.P30139):
            expression_label = expression.split('/')[-1]
            expression_filename = f"expression/{expression_label}.xml"
            if not os.path.exists(f"data/2020_7_28/{expression_filename}"):
                pass
            else:
                recordList.append(expression_filename)
            for work in expressionGraph.objects(subject=expression, predicate=rdae.P20231):
                work_label = work.split('/')[-1]
                work_filename = f"work/{work_label}.xml"
                if not os.path.exists(f"data/2020_7_28/{work_filename}"):
                    pass
                else:
                    recordList.append(work_filename)
    dir_label = item.split('/')[-1]
    os.system(f"mkdir data/WEMI/{dir_label}")
    for record in recordList:
        recordGraph = Graph()
        recordGraph.load(f"file:///home/mcm104/rml/rdfxml/data/2020_7_28/{record}", format="xml")
        label = record.split('.')[0]
        recordGraph.serialize(destination=f"data/WEMI/{dir_label}" + label + ".ttl", format="turtle")
