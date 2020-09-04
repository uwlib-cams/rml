import os
import rdflib
from rdflib import *
from datetime import date

"""Functions"""

## RDFLIB functions

def create_URI_list():
    """Creates a list of all URIs for all records in UW Trellis database"""
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
    return URIS

def save_works(URI_list, currentDate):
    """Look for works from trellis according to RDA class"""
    print(f"...\nLocating works")
    workURIList = []
    for uri in URI_list:
        Graph_trellisFile = Graph()
        rdac = Namespace('http://rdaregistry.info/Elements/c/')
        Graph_trellisFile.bind('rdac', rdac)
        Graph_trellisFile.load(uri, format='turtle') # load record into graph
        for work in Graph_trellisFile.subjects(RDF.type, rdac.C10001): # see if record in graph is typed as an RDA work
            workURIList.append(work)
            # create directory for works
            if not os.path.exists(f'input/{currentDate}/work'):
                print("...\nCreating work directory")
                os.system(f'mkdir input/{currentDate}/work')
            Graph_trellisWork = Graph()
            Graph_trellisWork.load(work, format='turtle') # load work record into a new graph
            label = work.split('/')[-1] # select just the identifier
            Graph_trellisWork.serialize(destination=f'input/{currentDate}/work/' + label + '.xml', format="xml") # serializes in xml
    return workURIList

def save_expressions(URI_list, currentDate, workURIList=[]):
    """Look for expressions from trellis according to RDA class"""
    # remove works from URI list to save time
    for work in workURIList:
        URI_list.remove(work)
    print(f"...\nLocating expressions")
    expressionURIList = []
    for uri in URI_list:
        Graph_trellisFile = Graph()
        rdac = Namespace('http://rdaregistry.info/Elements/c/')
        Graph_trellisFile.bind('rdac', rdac)
        Graph_trellisFile.load(uri, format='turtle') # load record into graph
        for expression in Graph_trellisFile.subjects(RDF.type, rdac.C10006): # looks for records typed as an RDA expression
            expressionURIList.append(expression)
            # create directory for expressions
            if not os.path.exists(f'input/{currentDate}/expression'):
                print("...\nCreating expression directory")
                os.system(f'mkdir input/{currentDate}/expression')
            Graph_trellisExpression = Graph()
            Graph_trellisExpression.load(expression, format='turtle') # load expression record into a new graph
            label = expression.split('/')[-1] # select just the identifier
            Graph_trellisExpression.serialize(destination=f'input/{currentDate}/expression/' + label + '.xml', format="xml") # serialize in xml
    return expressionURIList

def save_manifestations(URI_list, currentDate, expressionURIList=[]):
    """Look for manifestations from trellis according to RDA class"""
    # remove works + expressions from URI list to save time
    for expression in expressionURIList:
        URI_list.remove(expression)
    print(f"...\nLocating manifestations")
    manifestationURIList = []
    for uri in URI_list:
        Graph_trellisFile = Graph()
        rdac = Namespace('http://rdaregistry.info/Elements/c/')
        Graph_trellisFile.bind('rdac', rdac)
        Graph_trellisFile.load(uri, format='turtle')
        for manifestation in Graph_trellisFile.subjects(RDF.type, rdac.C10007): # looks for records typed as an RDA manifestation
            manifestationURIList.append(manifestation)
            # create directory for manifestations
            if not os.path.exists(f'input/{currentDate}/manifestation'):
                print("...\nCreating manifestation directory")
                os.system(f'mkdir input/{currentDate}/manifestation')
            Graph_trellisManifestation = Graph()
            Graph_trellisManifestation.load(manifestation, format='turtle')
            label = manifestation.split('/')[-1]
            Graph_trellisManifestation.serialize(destination=f'input/{currentDate}/manifestation/' + label + '.xml', format="xml")
    return manifestationURIList

def save_items(URI_list, currentDate, manifestationURIList=[]):
    """Look for items from trellis according to RDA class"""
    # remove works, expressions + manifestations from URI list to save time
    for manifestation in manifestationURIList:
        URI_list.remove(manifestation)
    print(f"...\nLocating items")
    for uri in URI_list:
        Graph_trellisFile = Graph()
        rdac = Namespace('http://rdaregistry.info/Elements/c/')
        Graph_trellisFile.bind('rdac', rdac)
        Graph_trellisFile.load(uri,format='turtle')
        for item in Graph_trellisFile.subjects(RDF.type, rdac.C10003): # looks for records typed as an RDA item
            # create directory for items
            if not os.path.exists(f'input/{currentDate}/item'):
                print("...\nCreating item directory")
                os.system(f'mkdir input/{currentDate}/item')
            Graph_trellisItem = Graph()
            Graph_trellisItem.load(item, format='turtle')
            label = item.split('/')[-1]
            Graph_trellisItem.serialize(destination=f'input/{currentDate}/item/' + label + '.xml', format="xml")

## RML functions

def transform_works(workList, currentDate):
    os.system("chmod u+rwx generateRML/rmlOutput/workRML.ttl") # adjust file permissions for map (RML sometimes trips on file permissions)
    # create work output directory
    if not os.path.exists(f'output/{currentDate}/work_1'):
        print(f'...\nCreating work_1 directory')
        os.makedirs(f'output/{currentDate}/work_1')
    print(f"...\nTransforming {len(workList)} files from RDA Work to BIBFRAME Work")
    for work in workList:
        os.system(f"chmod u+rwx input/{currentDate}/work/{work}") # adjust file permissions for data
        label = work.split('.')[0] # save trellis identifier as label
        workID = f"{currentDate}/work/{label}" # use label to make path
        work_map_replace_to_ID(workID) # use path as RML source in work monograph map
        os.system(f"java -jar rmlmapper-4.8.1-r262.jar -m generateRML/rmlOutput/workRML.ttl -o {label}.nq") # run RML, output as nquad file
        Graph_localWork = Graph()
        Graph_localWork.load(f'file:{label}.nq', format='nquads') # add nquad file to new graph
        Graph_localWork.serialize(destination=f'output/{currentDate}/work_1/' + label + '.ttl', format="turtle") # serialize file in turtle
        os.system(f"rm {label}.nq") # delete nquad file
        work_map_replace_to_default(workID) # return work monograph map to default

def transform_expressions(expressionList, currentDate):
    os.system("chmod u+rwx generateRML/rmlOutput/expressionRML.ttl") # adjust file permissions for map (RML sometimes trips on file permissions)
    # create expression directory
    if not os.path.exists(f'output/{currentDate}/work_2'):
        print(f'...\nCreating work_2 directory')
        os.makedirs(f'output/{currentDate}/work_2')
    print(f"...\nTransforming {len(expressionList)} from RDA Expression to BIBFRAME Work")
    for expression in expressionList:
        os.system(f"chmod u+rwx input/{currentDate}/expression/{expression}") # adjust file permissions for data
        label = expression.split('.')[0] # save trellis identifier as label
        expressionID = f"{currentDate}/expression/{label}" # use label to make path
        expression_map_replace_to_ID(expressionID) # use trellis identifier as RML source in expression monograph map
        os.system(f"java -jar rmlmapper-4.8.1-r262.jar -m generateRML/rmlOutput/expressionRML.ttl -o {label}.nq") # run RML, output as nquad file
        Graph_localExpression = Graph()
        Graph_localExpression.load(f'file:{label}.nq', format='nquads') # add nquad file to new graph
        Graph_localExpression.serialize(destination=f'output/{currentDate}/work_2/' + label + '.ttl', format="turtle") # serialize file in turtle
        os.system(f"rm {label}.nq") # delete nquad file
        expression_map_replace_to_default(expressionID) # return expression monograph map to default

def transform_manifestations(manifestationList, currentDate):
    os.system("chmod u+rwx generateRML/rmlOutput/manifestationRML.ttl") # adjust file permissions for map (RML sometimes trips on file permissions)
    # create manifestation directory
    if not os.path.exists(f'output/{currentDate}/instance'):
        print(f'...\nCreating instance directory')
        os.makedirs(f'output/{currentDate}/instance')
    print(f"...\nTransforming {len(manifestationList)} files from RDA Manifestation to BIBFRAME Instance")
    for manifestation in manifestationList:
        os.system(f"chmod u+rwx input/{currentDate}/manifestation/{manifestation}") # adjust file permissions for data
        label = manifestation.split('.')[0] # save trellis identifier as label
        manifestationID = f"{currentDate}/manifestation/{label}" # use label to make path
        manifestation_map_replace_to_ID(manifestationID) # use trellis identifier as RML source in manifestation monograph map
        os.system(f"java -jar rmlmapper-4.8.1-r262.jar -m generateRML/rmlOutput/manifestationRML.ttl -o {label}.nq") # run RML, output as nquad file
        Graph_localManifestation = Graph()
        Graph_localManifestation.load(f'file:{label}.nq', format='nquads') # add nquad file to new graph
        Graph_localManifestation.serialize(destination=f'output/{currentDate}/instance/' + label + '.ttl', format="turtle") # serialize file in turtle
        os.system(f"rm {label}.nq") # delete nquad file
        manifestation_map_replace_to_default(manifestationID) # return manifestation monograph map to default

def transform_items(itemList, currentDate):
    os.system("chmod u+rwx generateRML/rmlOutput/itemRML.ttl") # adjust file permissions for map (RML sometimes trips on file permissions)
    # create item directory
    if not os.path.exists(f'output/{currentDate}/item'):
        print(f'...\nCreating item directory')
        os.makedirs(f'output/{currentDate}/item')
    print(f"...\nTransforming {len(itemList)} files from RDA Item to BIBFRAME Item")
    for item in itemList:
        os.system(f"chmod u+rwx input/{currentDate}/item/{item}") # adjust file permissions for data
        label = item.split('.')[0] # save trellis identifier as label
        itemID = f"{currentDate}/item/{label}" # use label to make path
        item_map_replace_to_ID(itemID) # use trellis identifier as RML source in item monograph map
        os.system(f"java -jar rmlmapper-4.8.1-r262.jar -m generateRML/rmlOutput/itemRML.ttl -o {label}.nq") # run RML, output as nquad file
        Graph_localItem = Graph()
        Graph_localItem.load(f'file:{label}.nq', format='nquads') # add nquad file to new graph
        Graph_localItem.serialize(destination=f'output/{currentDate}/item/' + label + '.ttl', format="turtle") # serialize file in turtle
        os.system(f"rm {label}.nq") # delete nquad file
        item_map_replace_to_default(itemID) # return item monograph map to default

## Find-and-replace functions

def work_map_replace_to_ID(workID):
    """Replace all RML sources in the work monograph map from a random string (!!workID!!) to the work's identifier"""
    w = open("generateRML/rmlOutput/workRML.ttl", "rt")
    w_ = w.read()
    w_ = w_.replace("!!workID!!", workID)
    w.close()
    w = open("generateRML/rmlOutput/workRML.ttl", "wt")
    w.write(w_)

    w.close()

def work_map_replace_to_default(workID):
    """Replace all RML sources in the work monograph map from the work's identifier back to a random string (!!workID!!)"""
    w = open("generateRML/rmlOutput/workRML.ttl", "rt")
    w_ = w.read()
    w_ = w_.replace(workID, "!!workID!!")
    w.close()
    w = open("generateRML/rmlOutput/workRML.ttl", "wt")
    w.write(w_)
    w.close()

def expression_map_replace_to_ID(expressionID):
    """Replace all RML sources in the expression monograph map from a random string (!!expressionID!!) to the expression's identifier"""
    e = open("generateRML/rmlOutput/expressionRML.ttl", "rt")
    e_ = e.read()
    e_ = e_.replace("!!expressionID!!", expressionID)
    e.close()
    e = open("generateRML/rmlOutput/expressionRML.ttl", "wt")
    e.write(e_)
    e.close()

def expression_map_replace_to_default(expressionID):
    """Replace all RML sources in the expression monograph map from the expression's identifier back to a random string (!!expressionID!!)"""
    e = open("generateRML/rmlOutput/expressionRML.ttl", "rt")
    e_ = e.read()
    e_ = e_.replace(expressionID, "!!expressionID!!")
    e.close()
    e = open("generateRML/rmlOutput/expressionRML.ttl", "wt")
    e.write(e_)
    e.close()

def manifestation_map_replace_to_ID(manifestationID):
    """Replace all RML sources in the manifestation monograph map from a random string (!!manifestationID!!) to the manifestation's identifier"""
    m = open("generateRML/rmlOutput/manifestationRML.ttl", "rt")
    m_ = m.read()
    m_ = m_.replace("!!manifestationID!!", manifestationID)
    m.close()
    m = open("generateRML/rmlOutput/manifestationRML.ttl", "wt")
    m.write(m_)
    m.close()

def manifestation_map_replace_to_default(manifestationID):
    """Replace all RML sources in the manifestation monograph map from the manifestation's identifier back to a random string (!!manifestationID!!)"""
    m = open("generateRML/rmlOutput/manifestationRML.ttl", "rt")
    m_ = m.read()
    m_ = m_.replace(manifestationID, "!!manifestationID!!")
    m.close()
    m = open("generateRML/rmlOutput/manifestationRML.ttl", "wt")
    m.write(m_)
    m.close()

def item_map_replace_to_ID(itemID):
    """Replace all RML sources in the item monograph map from a random string (!!itemID!!) to the item's identifier"""
    i = open("generateRML/rmlOutput/itemRML.ttl", "rt")
    i_ = i.read()
    i_ = i_.replace("!!itemID!!", itemID)
    i.close()
    i = open("generateRML/rmlOutput/itemRML.ttl", "wt")
    i.write(i_)
    i.close()

def item_map_replace_to_default(itemID):
    """Replace all RML sources in the item monograph map from the item's identifier back to a random string (!!itemID!!)"""
    i = open("generateRML/rmlOutput/itemRML.ttl", "rt")
    i_ = i.read()
    i_ = i_.replace(itemID, "!!itemID!!")
    i.close()
    i = open("generateRML/rmlOutput/itemRML.ttl", "wt")
    i.write(i_)
    i.close()

"""Variables"""

# format for naming folder according to date
today = date.today()
currentDate = f"{today.year}_{today.month}_{today.day}"

###

URI_list = create_URI_list()

# create directory with today's date for RDA-in-RDF/XML data
if not os.path.exists(f'input/{currentDate}'):
    print('...\nCreating input folder')
    os.system(f'mkdir input/{currentDate}')

workURIList = save_works(URI_list, currentDate)
workList = os.listdir(f'input/{currentDate}/work') # add RDA-in-RDF/XML works to new list

expressionURIList = save_expressions(URI_list, currentDate, workURIList)
expressionList = os.listdir(f'input/{currentDate}/expression') # add RDA-in-RDF/XML expressions to new list

manifestationURIList = save_manifestations(URI_list, currentDate, expressionURIList)
manifestationList = os.listdir(f'input/{currentDate}/manifestation') # add RDA-in-RDF/XML manifestations to new list

save_items(URI_list, currentDate, manifestationURIList)
itemList = os.listdir(f'input/{currentDate}/item') # add RDA-in-RDF/XML items to new list

# create directory with today's date for BF-in-turtle data
if not os.path.exists(f'output/{currentDate}'):
    print('...\nCreating output folder')
    os.makedirs(f'output/{currentDate}')

transform_works(workList, currentDate)
transform_expressions(expressionList, currentDate)
transform_manifestations(manifestationList, currentDate)
transform_items(itemList, currentDate)

print("...\nDone!")
