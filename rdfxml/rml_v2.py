import os
import rdflib
from rdflib import *
from datetime import date

# format for naming folder according to date
today = date.today()
currentDate = f"{today.year}_{today.month}_{today.day}"

# pull all files from trellis
print("...\nRetrieving graph URIs", flush=True)
graph = Graph()

# bind namespaces to graph
LDP = Namespace('http://www.w3.org/ns/ldp#')
rdac = Namespace('http://rdaregistry.info/Elements/c/')
graph.bind('LDP', LDP)
graph.bind('rdac', rdac)
graph.load('https://trellis.sinopia.io/repository/washington', format='turtle')

URIS = [] # list for record URIs
for o in graph.objects(subject=None,predicate=LDP.contains): # records are described in the parent repo using ldp.contains
    URIS.append(o) # add records to URI list

# lists for each entity
workList = []
expressionList = []
manifestationList = []
itemList = []

"""Serialize RDA files in RDF/XML and save to repo"""

# create directory with today's date for RDF/XML data
if not os.path.exists(f'data/{currentDate}'):
    os.system(f'mkdir data/{currentDate}')

# look for works from trellis according to RDA class
print(f"...\nLocating works")
for uri in URIS:
    fileGraph = Graph()
    fileGraph.load(uri,format='turtle') # load records into graph
    for work in fileGraph.subjects(RDF.type, rdac.C10001): # look for records typed as an RDA work
        workList.append(work) # add to work list

num_of_works = len(workList)

if num_of_works == 0: # if no records are found (some issue has occurred)
    print("...\nNo works found.")

elif num_of_works >= 1:

    # create directory for works
    if not os.path.exists(f'data/{currentDate}/work'):
        print("...\nCreating work directory")
        os.system(f'mkdir data/{currentDate}/work')

    print(f"...\nSaving {num_of_works} works")

    # save to work directory
    for work in workList:
        workGraph = Graph()
        workGraph.load(work, format='turtle') # load records from work list into a new graph
        label = work.split('/')[-1] # selects just the identifier
        workGraph.serialize(destination=f'data/{currentDate}/work/' + label + '.xml', format="xml") # serializes in xml

# look for expressions from trellis according to RDA class
print(f"...\nLocating expressions")
for uri in URIS:
    fileGraph = Graph()
    fileGraph.load(uri,format='turtle')
    for expression in fileGraph.subjects(RDF.type, rdac.C10006): # looks for records typed as an RDA expression
        expressionList.append(expression) # adds to expression list

num_of_expressions = len(expressionList)

if num_of_expressions == 0:
    print("...\nNo expressions found.")

elif num_of_expressions >= 1:
    # create directory for expressions
    if not os.path.exists(f'data/{currentDate}/expression'):
        print("...\nCreating expression directory")
        os.system(f'mkdir data/{currentDate}/expression')

    print(f"...\nSaving {num_of_expressions} expressions")

    # save to expression directory
    for expression in expressionList:
        expressionGraph = Graph()
        expressionGraph.load(expression, format='turtle') # load records from expression list into a new graph
        label = expression.split('/')[-1]
        expressionGraph.serialize(destination=f'data/{currentDate}/expression/' + label + '.xml', format="xml")

# look for manifestations from trellis according to RDA class
print(f"...\nLocating manifestations")
for uri in URIS:
    fileGraph = Graph()
    fileGraph.load(uri,format='turtle')
    for manifestation in fileGraph.subjects(RDF.type, rdac.C10007): # looks for records typed as an RDA manifestation
        manifestationList.append(manifestation) # adds to manifestation list

num_of_manifestations = len(manifestationList)

if num_of_manifestations == 0:
    print("No manifestations found.")

elif num_of_manifestations >= 1:

    # create directory for manifestations
    if not os.path.exists(f'data/{currentDate}/manifestation'):
        print("...\nCreating manifestation directory")
        os.system(f'mkdir data/{currentDate}/manifestation')

    print(f"...\nSaving {num_of_manifestations} manifestations")

    # save to manifestation directory
    for manifestation in manifestationList:
        manifestationGraph = Graph()
        manifestationGraph.load(manifestation, format='turtle')
        label = manifestation.split('/')[-1]
        manifestationGraph.serialize(destination=f'data/{currentDate}/manifestation/' + label + '.xml', format="xml")

# look for items from trellis according to RDA class
print(f"...\nLocating items")
for uri in URIS:
    fileGraph = Graph()
    fileGraph.load(uri,format='turtle')
    for item in fileGraph.subjects(RDF.type, rdac.C10003): # looks for records typed as an RDA item
        itemList.append(item) # adds to item list

num_of_items = len(itemList)

if num_of_items == 0:
    print("No items found.")

elif num_of_items >= 1:
    # create directory for items
    if not os.path.exists(f'data/{currentDate}/item'):
        print("...\nCreating item directory")
        os.system(f'mkdir data/{currentDate}/item')

    print(f"...\nSaving {num_of_items} items")

    # save to item directory
    for item in itemList:
        itemGraph = Graph()
        itemGraph.load(item, format='turtle')
        label = item.split('/')[-1]
        itemGraph.serialize(destination=f'data/{currentDate}/item/' + label + '.xml', format="xml")

"""Transform from RDA to BIBFRAME and serialize as Turtle"""

# functions

# function to replace all RML sources in the work monograph map from a random string (!!workID!!) to the work's identifier
def work_map_replace_to_ID(workID):
    w = open("generateRML/rmlOutput/workRML.ttl", "rt")
    wm = w.read()
    wm = wm.replace("!!workID!!", workID)
    w.close()
    w = open("generateRML/rmlOutput/workRML.ttl", "wt")
    w.write(wm)
    w.close()

# function to replace all RML sources in the work monograph map from the work's identifier back to a random string (!!workID!!)
def work_map_replace_to_default(workID):
    w = open("generateRML/rmlOutput/workRML.ttl", "rt")
    wm = w.read()
    wm = wm.replace(workID, "!!workID!!")
    w.close()
    w = open("generateRML/rmlOutput/workRML.ttl", "wt")
    w.write(wm)
    w.close()

# function to replace all RML sources in the expression monograph map from a random string (!!expressionID!!) to the expression's identifier
def expression_map_replace_to_ID(expressionID):
    e = open("generateRML/rmlOutput/expressionRML.ttl", "rt")
    em = e.read()
    em = em.replace("!!expressionID!!", expressionID)
    e.close()
    e = open("generateRML/rmlOutput/expressionRML.ttl", "wt")
    e.write(em)
    e.close()

# function to replace all RML sources in the expression monograph map from the expression's identifier back to a random string (!!expressionID!!)
def expression_map_replace_to_default(expressionID):
    e = open("generateRML/rmlOutput/expressionRML.ttl", "rt")
    em = e.read()
    em = em.replace(expressionID, "!!expressionID!!")
    e.close()
    e = open("generateRML/rmlOutput/expressionRML.ttl", "wt")
    e.write(em)
    e.close()

# function to replace all RML sources in the manifestation monograph map from a random string (!!manifestationID!!) to the manifestation's identifier
def manifestation_map_replace_to_ID(manifestationID):
    m = open("generateRML/rmlOutput/manifestationRML.ttl", "rt")
    mm = m.read()
    mm = mm.replace("!!manifestationID!!", manifestationID)
    m.close()
    m = open("generateRML/rmlOutput/manifestationRML.ttl", "wt")
    m.write(mm)
    m.close()

# function to replace all RML sources in the manifestation monograph map from the manifestation's identifier back to a random string (!!manifestationID!!)
def manifestation_map_replace_to_default(manifestationID):
    m = open("generateRML/rmlOutput/manifestationRML.ttl", "rt")
    mm = m.read()
    mm = mm.replace(manifestationID, "!!manifestationID!!")
    m.close()
    m = open("generateRML/rmlOutput/manifestationRML.ttl", "wt")
    m.write(mm)
    m.close()

# function to replace all RML sources in the item monograph map from a random string (!!itemID!!) to the item's identifier
def item_map_replace_to_ID(itemID):
    i = open("generateRML/rmlOutput/itemRML.ttl", "rt")
    im = i.read()
    im = im.replace("!!itemID!!", itemID)
    i.close()
    i = open("generateRML/rmlOutput/itemRML.ttl", "wt")
    i.write(im)
    i.close()

# function to replace all RML sources in the item monograph map from the item's identifier back to a random string (!!itemID!!)
def item_map_replace_to_default(itemID):
    i = open("generateRML/rmlOutput/itemRML.ttl", "rt")
    im = i.read()
    im = im.replace(itemID, "!!itemID!!")
    i.close()
    i = open("generateRML/rmlOutput/itemRML.ttl", "wt")
    i.write(im)
    i.close()

# create folder with today's date
if not os.path.exists(f'output/{currentDate}'):
    print(f'...\nCreating directory {currentDate}')
    os.makedirs(f'output/{currentDate}')

# create work directory
if not os.path.exists(f'output/{currentDate}/work_1'):
    print(f'...\nCreating work_1 directory')
    os.makedirs(f'output/{currentDate}/work_1')

print(f"...\nTransforming {num_of_works} from RDA Work to BIBFRAME Work")

# adjust file permissions for map and for data (RML sometimes trips on file permissions)
os.system("chmod u+rwx generateRML/rmlOutput/workRML.ttl")
workPermissionList = os.listdir(f'data/{currentDate}/work/')

for work in workPermissionList:
    os.system(f"chmod u+rwx data/{currentDate}/work/{work}")

for work in workList:
    label = work.split('/')[-1] # save trellis identifier as label
    workID = f"{currentDate}/work/{label}" # use label to make path
    work_map_replace_to_ID(workID) # use path as RML source in work monograph map
    os.system(f"java -jar mapper.jar -m generateRML/rmlOutput/workRML.ttl -o {label}.nq") # run RML, output as nquad file
    workGraph = Graph()
    workGraph.load(f'file:{label}.nq', format='nquads') # add nquad file to new graph
    workGraph.serialize(destination=f'output/{currentDate}/work_1/' + label + '.ttl', format="turtle") # serialize file in turtle
    os.system(f"rm {label}.nq") # delete nquad file
    work_map_replace_to_default(workID) # return work monograph map to default

# create expression directory
if not os.path.exists(f'output/{currentDate}/work_2'):
    print(f'...\nCreating work_2 directory')
    os.makedirs(f'output/{currentDate}/work_2')

print(f"...\nTransforming {num_of_expressions} from RDA Expression to BIBFRAME Work")

# adjust file permissions for map and for data (RML sometimes trips on file permissions)
os.system("chmod u+rwx generateRML/rmlOutput/expressionRML.ttl")
expressionPermissionList = os.listdir(f'data/{currentDate}/expression/')

for expression in expressionPermissionList:
    os.system(f"chmod u+rwx data/{currentDate}/expression/{expression}")

for expression in expressionList:
    label = expression.split('/')[-1] # save trellis identifier as label
    expressionID = f"{currentDate}/expression/{label}" # use label to make path
    expression_map_replace_to_ID(expressionID) # use trellis identifier as RML source in expression monograph map
    os.system(f"java -jar mapper.jar -m generateRML/rmlOutput/expressionRML.ttl -o {label}.nq") # run RML, output as nquad file
    expressionGraph = Graph()
    expressionGraph.load(f'file:{label}.nq', format='nquads') # add nquad file to new graph
    expressionGraph.serialize(destination=f'output/{currentDate}/work_2/' + label + '.ttl', format="turtle") # serialize file in turtle
    os.system(f"rm {label}.nq") # delete nquad file
    expression_map_replace_to_default(expressionID) # return expression monograph map to default

# create manifestation directory
if not os.path.exists(f'output/{currentDate}/instance'):
    print(f'...\nCreating instance directory')
    os.makedirs(f'output/{currentDate}/instance')

print(f"...\nTransforming {num_of_manifestations} from RDA Manifestation to BIBFRAME Instance")

# adjust file permissions for map and for data (RML sometimes trips on file permissions)
os.system("chmod u+rwx generateRML/rmlOutput/manifestationRML.ttl")
manifestationPermissionList = os.listdir(f'data/{currentDate}/manifestation/')

for manifestation in manifestationPermissionList:
    os.system(f"chmod u+rwx data/{currentDate}/manifestation/{manifestation}")

for manifestation in manifestationList:
    label = manifestation.split('/')[-1] # save trellis identifier as label
    manifestationID = f"{currentDate}/manifestation/{label}" # use label to make path
    manifestation_map_replace_to_ID(manifestationID) # use trellis identifier as RML source in manifestation monograph map
    os.system(f"java -jar mapper.jar -m ~/rml/rdfxml/generateRML/rmlOutput/manifestationRML.ttl -o {label}.nq") # run RML, output as nquad file
    manifestationGraph = Graph()
    manifestationGraph.load(f'file:{label}.nq', format='nquads') # add nquad file to new graph
    manifestationGraph.serialize(destination=f'output/{currentDate}/instance/' + label + '.ttl', format="turtle") # serialize file in turtle
    os.system(f"rm {label}.nq") # delete nquad file
    manifestation_map_replace_to_default(manifestationID) # return manifestation monograph map to default

# create item directory
if not os.path.exists(f'output/{currentDate}/item'):
    print(f'...\nCreating item directory')
    os.makedirs(f'output/{currentDate}/item')

print(f"...\nTransforming {num_of_items} from RDA Item to BIBFRAME Item")

# adjust file permissions for map and for data (RML sometimes trips on file permissions)
os.system("chmod u+rwx generateRML/rmlOutput/itemRML.ttl")
itemPermissionList = os.listdir(f'data/{currentDate}/item/')

for item in itemPermissionList:
    os.system(f"chmod u+rwx data/{currentDate}/item/{item}")

for item in itemList:
    label = item.split('/')[-1] # save trellis identifier as label
    itemID = f"{currentDate}/item/{label}" # use label to make path
    item_map_replace_to_ID(itemID) # use trellis identifier as RML source in item monograph map
    os.system(f"java -jar mapper.jar -m ~/rml/rdfxml/generateRML/rmlOutput/itemRML.ttl -o {label}.nq") # run RML, output as nquad file
    itemGraph = Graph()
    itemGraph.load(f'file:{label}.nq', format='nquads') # add nquad file to new graph
    itemGraph.serialize(destination=f'output/{currentDate}/item/' + label + '.ttl', format="turtle") # serialize file in turtle
    os.system(f"rm {label}.nq") # delete nquad file
    item_map_replace_to_default(itemID) # return item monograph map to default

print("...\nDone!")
