import os
import time
from rdflib import *
import rdflib
from datetime import date
from progress.bar import Bar
import requests

"""Namespaces"""
LDP = Namespace('http://www.w3.org/ns/ldp#')
bf = Namespace('http://id.loc.gov/ontologies/bibframe/')
bflc = Namespace('http://id.loc.gov/ontologies/bflc/')
dbo = Namespace('http://dbpedia.org/ontology/')
madsrdf = Namespace('http://www.loc.gov/mads/rdf/v1#')
rdac = Namespace('http://rdaregistry.info/Elements/c/')
rdae = Namespace('http://rdaregistry.info/Elements/e/')
rdai = Namespace('http://rdaregistry.info/Elements/i/')
rdam = Namespace('http://rdaregistry.info/Elements/m/')
rdamdt = Namespace('http://rdaregistry.info/Elements/m/datatype/')
rdau = Namespace('http://rdaregistry.info/Elements/u/')
rdaw = Namespace('http://rdaregistry.info/Elements/w/')
rdax = Namespace('https://doi.org/10.6069/uwlib.55.d.4#')
sin = Namespace('http://sinopia.io/vocabulary/')

"""Functions"""

## RDFLIB functions

def create_URI_list():
	"""Creates a list of all URIs for all records in UW mongoDB"""
	# pull from mongo + http to get all URIs
	response = requests.get('https://api.sinopia.io/resource?limit=575&group=washington')
	with open('uw_list.json', 'w') as output_file:
		output_file.write(response.text)

	# get URIs from JSON-LD into python list
	os.system('java -jar mapper.jar -m json_rml.ttl -o uw_uri_list.nq')
	URI_list = []
	uriGraph = Graph()
	uriGraph.load('file:uw_uri_list.nq', format='nquads')
	for uri in uriGraph.objects(None, None):
		URI_list.append(uri)
	return URI_list

def save_works(URI_list, currentDate):
	"""Look for works from trellis according to RDA class"""
	# create directory for works
	if not os.path.exists(f'input/{currentDate}/work'):
		print("...\nCreating work directory")
		os.system(f'mkdir input/{currentDate}/work')
	workURIList = []
	bar = Bar('Locating works', max=len(URI_list), suffix='%(percent)d%%')
	for URI in URI_list:
		label = URI.split('/')[-1]
		g = rdflib.Graph()
		g.bind('bf', bf)
		g.bind('bflc', bflc)
		g.bind('rdac', rdac)
		g.bind('rdaw', rdaw)
		g.bind('rdax', rdax)
		g.bind('madsrdf', madsrdf)
		g.parse(URI, format="json-ld")
		for work in g.subjects(RDF.type, rdac.C10001):
			g.serialize(destination=f'input/{currentDate}/work/' + label + '.xml', format="xml") # serializes in xml
		bar.next()
	bar.finish()
	return workURIList

def save_expressions(URI_list, currentDate, workURIList=[]):
	"""Look for expressions from trellis according to RDA class"""
	# remove works from URI list to save time
	for work in workURIList:
		URI_list.remove(work)
	# create directory for expressions
	if not os.path.exists(f'input/{currentDate}/expression'):
		print("...\nCreating expression directory")
		os.system(f'mkdir input/{currentDate}/expression')
	expressionURIList = []
	bar = Bar('Locating expressions', max=len(URI_list), suffix='%(percent)d%%')
	for URI in URI_list:
		label = URI.split('/')[-1]
		g = rdflib.Graph()
		g.bind('bf', bf)
		g.bind('bflc', bflc)
		g.bind('rdac', rdac)
		g.bind('rdae', rdae)
		g.bind('rdax', rdax)
		g.bind('madsrdf', madsrdf)
		g.parse(URI, format="json-ld")
		for work in g.subjects(RDF.type, rdac.C10006):
			g.serialize(destination=f'input/{currentDate}/expression/' + label + '.xml', format="xml") # serialize in xml
		bar.next()
	bar.finish()
	return expressionURIList

def save_manifestations(URI_list, currentDate, expressionURIList=[]):
	"""Look for manifestations from trellis according to RDA class"""
	# remove works + expressions from URI list to save time
	for expression in expressionURIList:
		URI_list.remove(expression)
	# create directory for manifestations
	if not os.path.exists(f'input/{currentDate}/manifestation'):
		print("...\nCreating manifestation directory")
		os.system(f'mkdir input/{currentDate}/manifestation')
	manifestationURIList = []
	bar = Bar('Locating manifestations', max=len(URI_list), suffix='%(percent)d%%')
	for URI in URI_list:
		label = URI.split('/')[-1]
		g = rdflib.Graph()
		g.bind('bf', bf)
		g.bind('bflc', bflc)
		g.bind('rdac', rdac)
		g.bind('rdam', rdam)
		g.bind('rdamdt', rdamdt)
		g.bind('rdax', rdax)
		g.bind('madsrdf', madsrdf)
		g.parse(URI, format="json-ld")
		for work in g.subjects(RDF.type, rdac.C10007):
			g.serialize(destination=f'input/{currentDate}/manifestation/' + label + '.xml', format="xml")
		bar.next()
	bar.finish()
	return manifestationURIList

def save_items(URI_list, currentDate, manifestationURIList=[]):
	"""Look for items from trellis according to RDA class"""
	# remove works, expressions + manifestations from URI list to save time
	for manifestation in manifestationURIList:
		URI_list.remove(manifestation)
	# create directory for items
	if not os.path.exists(f'input/{currentDate}/item'):
		print("...\nCreating item directory")
		os.system(f'mkdir input/{currentDate}/item')
	bar = Bar('Locating items', max=len(URI_list), suffix='%(percent)d%%')
	for URI in URI_list:
		label = URI.split('/')[-1]
		g = rdflib.Graph()
		g.bind('bf', bf)
		g.bind('bflc', bflc)
		g.bind('rdac', rdac)
		g.bind('rdai', rdai)
		g.bind('rdax', rdax)
		g.bind('madsrdf', madsrdf)
		g.parse(URI, format="json-ld")
		for work in g.subjects(RDF.type, rdac.C10003):
			g.serialize(destination=f'input/{currentDate}/item/' + label + '.xml', format="xml")
		bar.next()
	bar.finish()

## RML functions

def transform_works(workList, currentDate):
	os.system("chmod u+rwx generateRML/rmlOutput/workRML.ttl") # adjust file permissions for map (RML sometimes trips on file permissions)
	# create work output directory
	if not os.path.exists(f'output/{currentDate}/work_1'):
		print(f'...\nCreating work_1 directory')
		os.makedirs(f'output/{currentDate}/work_1')
	print("...")
	bar = Bar(f'Transforming {len(workList)} files from RDA Work to BIBFRAME Work', max=len(workList), suffix='%(percent)d%%')
	for work in workList:
		os.system(f"chmod u+rwx input/{currentDate}/work/{work}") # adjust file permissions for data
		label = work.split('.')[0] # save trellis identifier as label
		workID = f"{currentDate}/work/{label}" # use label to make path
		work_map_replace_to_ID(workID) # use path as RML source in work monograph map
		os.system(f"java -jar rmlmapper-4.8.1-r262.jar -m generateRML/rmlOutput/workRML.ttl -o {label}.nq") # run RML, output as nquad file
		# create new empty graph
		Graph_localWork = Graph()
		# bind namespaces to graph
		Graph_localWork.bind('bf', bf)
		Graph_localWork.bind('bflc', bflc)
		Graph_localWork.bind('madsrdf', madsrdf)
		# add nquad file to new graph
		Graph_localWork.load(f'file:{label}.nq', format='nquads')
		# create variables for new triples
		snapshot_bnode = BNode()
		currentTime = time.strftime("%Y-%m-%dT%H:%M:%S+00:00")
		snapshot_literal = Literal(f"rml.py SNAPSHOT: {currentTime}")
		# create new triples
		for s, p, o in Graph_localWork.triples((None, bf.adminMetadata, None)):
			Graph_localWork.add((o, bf.generationProcess, snapshot_bnode))
			Graph_localWork.add((snapshot_bnode, RDF.type, bf.GenerationProcess))
			Graph_localWork.add((snapshot_bnode, RDFS.label, snapshot_literal))
		# serialize graph as turtle
		Graph_localWork.serialize(destination=f'output/{currentDate}/work_1/' + label + '.ttl', format="turtle")
		# delete nquad file
		os.system(f"rm {label}.nq")
		# return work map to default
		work_map_replace_to_default(workID)
		bar.next()
	bar.finish()

def transform_expressions(expressionList, currentDate):
	os.system("chmod u+rwx generateRML/rmlOutput/expressionRML.ttl") # adjust file permissions for map (RML sometimes trips on file permissions)
	# create expression directory
	if not os.path.exists(f'output/{currentDate}/work_2'):
		print(f'...\nCreating work_2 directory')
		os.makedirs(f'output/{currentDate}/work_2')
	print("...")
	bar = Bar(f'Transforming {len(expressionList)} from RDA Expression to BIBFRAME Work', max=len(expressionList), suffix='%(percent)d%%')
	for expression in expressionList:
		os.system(f"chmod u+rwx input/{currentDate}/expression/{expression}") # adjust file permissions for data
		label = expression.split('.')[0] # save trellis identifier as label
		expressionID = f"{currentDate}/expression/{label}" # use label to make path
		expression_map_replace_to_ID(expressionID) # use trellis identifier as RML source in expression monograph map
		os.system(f"java -jar rmlmapper-4.8.1-r262.jar -m generateRML/rmlOutput/expressionRML.ttl -o {label}.nq") # run RML, output as nquad file
		# create new empty graph
		Graph_localExpression = Graph()
		# bind namespaces to graph
		Graph_localExpression.bind('bf', bf)
		Graph_localExpression.bind('bflc', bflc)
		Graph_localExpression.bind('madsrdf', madsrdf)
		# add nquad file to new graph
		Graph_localExpression.load(f'file:{label}.nq', format='nquads')
		# create variables for new triples
		snapshot_bnode = BNode()
		currentTime = time.strftime("%Y-%m-%dT%H:%M:%S+00:00")
		snapshot_literal = Literal(f"rml.py SNAPSHOT: {currentTime}")
		# create new triples
		for s, p, o in Graph_localExpression.triples((None, bf.adminMetadata, None)):
			Graph_localExpression.add((o, bf.generationProcess, snapshot_bnode))
			Graph_localExpression.add((snapshot_bnode, RDF.type, bf.GenerationProcess))
			Graph_localExpression.add((snapshot_bnode, RDFS.label, snapshot_literal))
		# serialize graph as turtle
		Graph_localExpression.serialize(destination=f'output/{currentDate}/work_2/' + label + '.ttl', format="turtle")
		# delete nquad file
		os.system(f"rm {label}.nq")
		# return expression map to default
		expression_map_replace_to_default(expressionID)
		bar.next()
	bar.finish()

def transform_manifestations(manifestationList, currentDate):
	os.system("chmod u+rwx generateRML/rmlOutput/manifestationRML.ttl") # adjust file permissions for map (RML sometimes trips on file permissions)
	# create manifestation directory
	if not os.path.exists(f'output/{currentDate}/instance'):
		print(f'...\nCreating instance directory')
		os.makedirs(f'output/{currentDate}/instance')
	print("...")
	bar = Bar(f'Transforming {len(manifestationList)} files from RDA Manifestation to BIBFRAME Instance', max=len(manifestationList), suffix='%(percent)d%%')
	for manifestation in manifestationList:
		os.system(f"chmod u+rwx input/{currentDate}/manifestation/{manifestation}") # adjust file permissions for data
		label = manifestation.split('.')[0] # save trellis identifier as label
		manifestationID = f"{currentDate}/manifestation/{label}" # use label to make path
		manifestation_map_replace_to_ID(manifestationID) # use trellis identifier as RML source in manifestation monograph map
		os.system(f"java -jar rmlmapper-4.8.1-r262.jar -m generateRML/rmlOutput/manifestationRML.ttl -o {label}.nq") # run RML, output as nquad file
		# create new empty graph
		Graph_localManifestation = Graph()
		# bind namespaces to graph
		Graph_localManifestation.bind('bf', bf)
		Graph_localManifestation.bind('bflc', bflc)
		Graph_localManifestation.bind('madsrdf', madsrdf)
		# add nquad file to new graph
		Graph_localManifestation.load(f'file:{label}.nq', format='nquads')
		# create variables for new triples
		snapshot_bnode = BNode()
		currentTime = time.strftime("%Y-%m-%dT%H:%M:%S+00:00")
		snapshot_literal = Literal(f"rml.py SNAPSHOT: {currentTime}")
		# create new triples
		for s, p, o in Graph_localManifestation.triples((None, bf.adminMetadata, None)):
			Graph_localManifestation.add((o, bf.generationProcess, snapshot_bnode))
			Graph_localManifestation.add((snapshot_bnode, RDF.type, bf.GenerationProcess))
			Graph_localManifestation.add((snapshot_bnode, RDFS.label, snapshot_literal))
		# serialize graph as turtle
		Graph_localManifestation.serialize(destination=f'output/{currentDate}/instance/' + label + '.ttl', format="turtle")
		# delete nquad file
		os.system(f"rm {label}.nq")
		# return manifestation map to default
		manifestation_map_replace_to_default(manifestationID)
		bar.next()
	bar.finish()

def transform_items(itemList, currentDate):
	os.system("chmod u+rwx generateRML/rmlOutput/itemRML.ttl") # adjust file permissions for map (RML sometimes trips on file permissions)
	# create item directory
	if not os.path.exists(f'output/{currentDate}/item'):
		print(f'...\nCreating item directory')
		os.makedirs(f'output/{currentDate}/item')
	print("...")
	bar = Bar(f'Transforming {len(itemList)} files from RDA Item to BIBFRAME Item', max=len(itemList), suffix='%(percent)d%%')
	for item in itemList:
		os.system(f"chmod u+rwx input/{currentDate}/item/{item}") # adjust file permissions for data
		label = item.split('.')[0] # save trellis identifier as label
		itemID = f"{currentDate}/item/{label}" # use label to make path
		item_map_replace_to_ID(itemID) # use trellis identifier as RML source in item monograph map
		os.system(f"java -jar rmlmapper-4.8.1-r262.jar -m generateRML/rmlOutput/itemRML.ttl -o {label}.nq") # run RML, output as nquad file
		# create new empty graph
		Graph_localItem = Graph()
		# bind namespaces to graph
		Graph_localItem.bind('bf', bf)
		Graph_localItem.bind('bflc', bflc)
		Graph_localItem.bind('madsrdf', madsrdf)
		# add nquad file to new graph
		Graph_localItem.load(f'file:{label}.nq', format='nquads')
		# create variables for new triples
		snapshot_bnode = BNode()
		currentTime = time.strftime("%Y-%m-%dT%H:%M:%S+00:00")
		snapshot_literal = Literal(f"rml.py SNAPSHOT: {currentTime}")
		# create new triples
		for s, p, o in Graph_localItem.triples((None, bf.adminMetadata, None)):
			Graph_localItem.add((o, bf.generationProcess, snapshot_bnode))
			Graph_localItem.add((snapshot_bnode, RDF.type, bf.GenerationProcess))
			Graph_localItem.add((snapshot_bnode, RDFS.label, snapshot_literal))
		# serialize file in turtle
		Graph_localItem.serialize(destination=f'output/{currentDate}/item/' + label + '.ttl', format="turtle")
		# delete nquad file
		os.system(f"rm {label}.nq")
		# return item map to default
		item_map_replace_to_default(itemID)
		bar.next()
	bar.finish()

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
currentDate = str(today).replace('-', '_')

###

"""Retrieve RDA Data"""

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

print("...\nCleaning input data")

print(">> Fixing IRIs typed as literals")
import fix_URIs

print(">> Remove blank copyright dates")
import fix_copyright_dates

"""Transform RDA to BIBFRAME"""

# create directory with today's date for BF-in-turtle data
if not os.path.exists(f'output/{currentDate}'):
	print('...\nCreating output folder')
	os.makedirs(f'output/{currentDate}')

transform_works(workList, currentDate)
transform_expressions(expressionList, currentDate)
transform_manifestations(manifestationList, currentDate)
transform_items(itemList, currentDate)

print("...\nCleaning output data")

print(">> Fixing language tags")
import langtags

print(">> Adding datatypes to dates")
import type_dates

print("...\nDone!")
