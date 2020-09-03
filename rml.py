import os
import rdflib
from rdflib import *
from datetime import date

"""Functions"""

def work_map_replace_to_ID(workID):
    """Replace all RML sources in the work monograph map from a random string (!!workID!!) to the work's identifier"""
    w = open("generateRML/rmlOutput/workRML.ttl", "rt")
    wm = w.read()
    wm = wm.replace("!!workID!!", workID)
    w.close()
    w = open("generateRML/rmlOutput/workRML.ttl", "wt")
    w.write(wm)
    w.close()

def work_map_replace_to_default(workID):
    """Replace all RML sources in the work monograph map from the work's identifier back to a random string (!!workID!!)"""
    w = open("generateRML/rmlOutput/workRML.ttl", "rt")
    wm = w.read()
    wm = wm.replace(workID, "!!workID!!")
    w.close()
    w = open("generateRML/rmlOutput/workRML.ttl", "wt")
    w.write(wm)
    w.close()

def expression_map_replace_to_ID(expressionID):
    """Replace all RML sources in the expression monograph map from a random string (!!expressionID!!) to the expression's identifier"""
    e = open("generateRML/rmlOutput/expressionRML.ttl", "rt")
    em = e.read()
    em = em.replace("!!expressionID!!", expressionID)
    e.close()
    e = open("generateRML/rmlOutput/expressionRML.ttl", "wt")
    e.write(em)
    e.close()

def expression_map_replace_to_default(expressionID):
    """Replace all RML sources in the expression monograph map from the expression's identifier back to a random string (!!expressionID!!)"""
    e = open("generateRML/rmlOutput/expressionRML.ttl", "rt")
    em = e.read()
    em = em.replace(expressionID, "!!expressionID!!")
    e.close()
    e = open("generateRML/rmlOutput/expressionRML.ttl", "wt")
    e.write(em)
    e.close()

def manifestation_map_replace_to_ID(manifestationID):
    """Replace all RML sources in the manifestation monograph map from a random string (!!manifestationID!!) to the manifestation's identifier"""
    m = open("generateRML/rmlOutput/manifestationRML.ttl", "rt")
    mm = m.read()
    mm = mm.replace("!!manifestationID!!", manifestationID)
    m.close()
    m = open("generateRML/rmlOutput/manifestationRML.ttl", "wt")
    m.write(mm)
    m.close()

def manifestation_map_replace_to_default(manifestationID):
    """Replace all RML sources in the manifestation monograph map from the manifestation's identifier back to a random string (!!manifestationID!!)"""
    m = open("generateRML/rmlOutput/manifestationRML.ttl", "rt")
    mm = m.read()
    mm = mm.replace(manifestationID, "!!manifestationID!!")
    m.close()
    m = open("generateRML/rmlOutput/manifestationRML.ttl", "wt")
    m.write(mm)
    m.close()

def item_map_replace_to_ID(itemID):
    """Replace all RML sources in the item monograph map from a random string (!!itemID!!) to the item's identifier"""
    i = open("generateRML/rmlOutput/itemRML.ttl", "rt")
    im = i.read()
    im = im.replace("!!itemID!!", itemID)
    i.close()
    i = open("generateRML/rmlOutput/itemRML.ttl", "wt")
    i.write(im)
    i.close()

def item_map_replace_to_default(itemID):
    """Replace all RML sources in the item monograph map from the item's identifier back to a random string (!!itemID!!)"""
    i = open("generateRML/rmlOutput/itemRML.ttl", "rt")
    im = i.read()
    im = im.replace(itemID, "!!itemID!!")
    i.close()
    i = open("generateRML/rmlOutput/itemRML.ttl", "wt")
    i.write(im)
    i.close()

# format for naming folder according to date
today = date.today()
currentDate = f"{today.year}_{today.month}_{today.day}"

print("...\nPulling files from Trellis", flush=True)
Graph_URI = Graph()
# bind namespaces to graph
LDP = Namespace('http://www.w3.org/ns/ldp#')
rdac = Namespace('http://rdaregistry.info/Elements/c/')
Graph_URI.bind('LDP', LDP)
Graph_URI.bind('rdac', rdac)
# load files from trellis
Graph_URI.load('https://trellis.sinopia.io/repository/washington', format='turtle')

URIS = [] # list for record URIs
for o in Graph_URI.objects(subject=None,predicate=LDP.contains): # records are described in the parent repo using ldp.contains
    URIS.append(o) # add records to URI list

# create directory with today's date for RDA-in-RDF/XML data
if not os.path.exists(f'input/{currentDate}'):
    print('...\nCreating input folder')
    os.system(f'mkdir input/{currentDate}')

# create directory with today's date for BF-in-turtle data
if not os.path.exists(f'output/{currentDate}'):
    print('...\nCreating output folder')
    os.makedirs(f'output/{currentDate}')

# adjust file permissions for map (RML sometimes trips on file permissions)
os.system("chmod u+rwx generateRML/rmlOutput/workRML.ttl")

"""RDA Work --> BF Work"""

"""Serialize RDA files in RDF/XML and save to repo"""

# look for works from trellis according to RDA class
#print(f"...\nLocating works")
#for uri in URIS:
#    Graph_allFiles = Graph()
#    Graph_allFiles.load(uri, format='turtle') # load records into graph
#    for work in Graph_allFiles.subjects(RDF.type, rdac.C10001): # look for records typed as an RDA work
        # create directory for works
#        if not os.path.exists(f'input/{currentDate}/work'):
#            print("...\nCreating work directory")
#            os.system(f'mkdir input/{currentDate}/work')
#        Graph_allWorks = Graph()
#        Graph_allWorks.load(work, format='turtle') # load records from work list into a new graph
#        label = work.split('/')[-1] # selects just the identifier
#        Graph_allWorks.serialize(destination=f'input/{currentDate}/work/' + label + '.xml', format="xml") # serializes in xml

"""Prereqs for transformation"""

# create work directory
#if not os.path.exists(f'output/{currentDate}/work_1'):
#    print(f'...\nCreating work_1 directory')
#    os.makedirs(f'output/{currentDate}/work_1')

# add RDA-in-RDF/XML works to new list
#workList = os.listdir(f'input/{currentDate}/work')

"""Transforming from RDA-in-RDF/XML to BF-in-Turtle"""

#print(f"...\nTransforming {len(workList)} files from RDA Work to BIBFRAME Work")

#for work in workList:
#    os.system(f"chmod u+rwx input/{currentDate}/work/{work}") # adjust file permissions for data
#    label = work.split('.')[0] # save trellis identifier as label
#    workID = f"{currentDate}/work/{label}" # use label to make path
#    work_map_replace_to_ID(workID) # use path as RML source in work monograph map
#    os.system(f"java -jar rmlmapper-4.8.1-r262.jar -m generateRML/rmlOutput/workRML.ttl -o {label}.nq") # run RML, output as nquad file
#    Graph_oneWork = Graph()
#    Graph_oneWork.load(f'file:{label}.nq', format='nquads') # add nquad file to new graph
#    Graph_oneWork.serialize(destination=f'output/{currentDate}/work_1/' + label + '.ttl', format="turtle") # serialize file in turtle
#    os.system(f"rm {label}.nq") # delete nquad file
#    work_map_replace_to_default(workID) # return work monograph map to default

"""RDA Expression --> BF Work"""

"""Serialize RDA files in RDF/XML and save to repo"""

# look for expressions from trellis according to RDA class
#print(f"...\nLocating expressions")
#for uri in URIS:
#    Graph_allFiles = Graph()
#    Graph_allFiles.load(uri, format='turtle') # load records into graph
#    for expression in Graph_allFiles.subjects(RDF.type, rdac.C10006): # looks for records typed as an RDA expression
        # create directory for expressions
#        if not os.path.exists(f'input/{currentDate}/expression'):
#            print("...\nCreating expression directory")
#            os.system(f'mkdir input/{currentDate}/expression')
#        Graph_allExpressions = Graph()
#        Graph_allExpressions.load(expression, format='turtle') # load records from expression list into a new graph
#        label = expression.split('/')[-1] # selects just the identifier
#        Graph_allExpressions.serialize(destination=f'input/{currentDate}/expression/' + label + '.xml', format="xml") # serialize in xml

"""Prereqs for transformation"""

# create expression directory
#if not os.path.exists(f'output/{currentDate}/work_2'):
#    print(f'...\nCreating work_2 directory')
#    os.makedirs(f'output/{currentDate}/work_2')

# add RDA-in-RDF/XML expressions to new list
#expressionList = os.listdir(f'input/{currentDate}/expression')

#print(f"...\nTransforming {len(expressionList)} from RDA Expression to BIBFRAME Work")

#for expression in expressionList:
#    os.system(f"chmod u+rwx input/{currentDate}/expression/{expression}") # adjust file permissions for data
#    label = expression.split('.')[0] # save trellis identifier as label
#    expressionID = f"{currentDate}/expression/{label}" # use label to make path
#    expression_map_replace_to_ID(expressionID) # use trellis identifier as RML source in expression monograph map
#    os.system(f"java -jar rmlmapper-4.8.1-r262.jar -m generateRML/rmlOutput/expressionRML.ttl -o {label}.nq") # run RML, output as nquad file
#    Graph_oneExpression = Graph()
#    Graph_oneExpression.load(f'file:{label}.nq', format='nquads') # add nquad file to new graph
#    Graph_oneExpression.serialize(destination=f'output/{currentDate}/work_2/' + label + '.ttl', format="turtle") # serialize file in turtle
#    os.system(f"rm {label}.nq") # delete nquad file
#    expression_map_replace_to_default(expressionID) # return expression monograph map to default

"""RDA Manifestation --> BF Instance"""

"""Serialize RDA files in RDF/XML and save to repo"""

# look for manifestations from trellis according to RDA class
#print(f"...\nLocating manifestations")
#for uri in URIS:
#    Graph_allFiles = Graph()
#    Graph_allFiles.load(uri, format='turtle')
#    for manifestation in Graph_allFiles.subjects(RDF.type, rdac.C10007): # looks for records typed as an RDA manifestation
        # create directory for manifestations
#        if not os.path.exists(f'input/{currentDate}/manifestation'):
#            print("...\nCreating manifestation directory")
#            os.system(f'mkdir input/{currentDate}/manifestation')
#        Graph_allManifestations = Graph()
#        Graph_allManifestations.load(manifestation, format='turtle')
#        label = manifestation.split('/')[-1]
#        Graph_allManifestations.serialize(destination=f'input/{currentDate}/manifestation/' + label + '.xml', format="xml")

"""Prereqs for transformation"""

# create manifestation directory
#if not os.path.exists(f'output/{currentDate}/instance'):
#    print(f'...\nCreating instance directory')
#    os.makedirs(f'output/{currentDate}/instance')

# add RDA-in-RDF/XML manifestations to new list
manifestationList = os.listdir(f'input/{currentDate}/manifestation')

"""Transforming from RDA-in-RDF/XML in BF-in-Turtle"""

print(f"...\nTransforming {len(manifestationList)} files from RDA Manifestation to BIBFRAME Instance")

for manifestation in manifestationList:
    os.system(f"chmod u+rwx input/{currentDate}/manifestation/{manifestation}") # adjust file permissions for data
    label = manifestation.split('.')[0] # save trellis identifier as label
    manifestationID = f"{currentDate}/manifestation/{label}" # use label to make path
    manifestation_map_replace_to_ID(manifestationID) # use trellis identifier as RML source in manifestation monograph map
    os.system(f"java -jar rmlmapper-4.8.1-r262.jar -m generateRML/rmlOutput/manifestationRML.ttl -o {label}.nq") # run RML, output as nquad file
    Graph_oneManifestation = Graph()
    Graph_oneManifestation.load(f'file:{label}.nq', format='nquads') # add nquad file to new graph
    Graph_oneManifestation.serialize(destination=f'output/{currentDate}/instance/' + label + '.ttl', format="turtle") # serialize file in turtle
    os.system(f"rm {label}.nq") # delete nquad file
    manifestation_map_replace_to_default(manifestationID) # return manifestation monograph map to default

"""RDA Item --> BF Item"""

"""Serialize RDA files in RDF/XML and save to repo"""

# look for items from trellis according to RDA class
print(f"...\nLocating items")
for uri in URIS:
    Graph_allFiles = Graph()
    Graph_allFiles.load(uri,format='turtle')
    for item in Graph_allFiles.subjects(RDF.type, rdac.C10003): # looks for records typed as an RDA item
        # create directory for items
        if not os.path.exists(f'input/{currentDate}/item'):
            print("...\nCreating item directory")
            os.system(f'mkdir input/{currentDate}/item')
        Graph_allItems = Graph()
        Graph_allItems.load(item, format='turtle')
        label = item.split('/')[-1]
        Graph_allItems.serialize(destination=f'input/{currentDate}/item/' + label + '.xml', format="xml")

"""Prereqs for transformation"""

# create item directory
if not os.path.exists(f'output/{currentDate}/item'):
    print(f'...\nCreating item directory')
    os.makedirs(f'output/{currentDate}/item')

# add RDA-in-RDF/XML items to new list
itemList = os.listdir(f'input/{currentDate}/item')

"""Transforming from RDA-in-RDF/XML to BF-in-Turtle"""

print(f"...\nTransforming {len(itemList)} files from RDA Item to BIBFRAME Item")
for item in itemList:
    os.system(f"chmod u+rwx input/{currentDate}/item/{item}") # adjust file permissions for data
    label = item.split('.')[0] # save trellis identifier as label
    itemID = f"{currentDate}/item/{label}" # use label to make path
    item_map_replace_to_ID(itemID) # use trellis identifier as RML source in item monograph map
    os.system(f"java -jar rmlmapper-4.8.1-r262.jar -m generateRML/rmlOutput/itemRML.ttl -o {label}.nq") # run RML, output as nquad file
    Graph_oneItem = Graph()
    Graph_oneItem.load(f'file:{label}.nq', format='nquads') # add nquad file to new graph
    Graph_oneItem.serialize(destination=f'output/{currentDate}/item/' + label + '.ttl', format="turtle") # serialize file in turtle
    os.system(f"rm {label}.nq") # delete nquad file
    item_map_replace_to_default(itemID) # return item monograph map to default

print("...\nDone!")
