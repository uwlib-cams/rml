from datetime import date
import os
from progress.bar import Bar
import requests
from rdflib import *
import rdflib
import time
from timeit import default_timer as timer

"""Namespaces"""
LDP = Namespace('http://www.w3.org/ns/ldp#')
bf = Namespace('http://id.loc.gov/ontologies/bibframe/')
bflc = Namespace('http://id.loc.gov/ontologies/bflc/')
dbo = Namespace('http://dbpedia.org/ontology/')
madsrdf = Namespace('http://www.loc.gov/mads/rdf/v1#')
owl = Namespace('http://www.w3.org/2002/07/owl')
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

def create_URI_list():
	"""Creates a list of all URIs for all records in UW mongoDB"""
	# pull from mongo + http to get all URIs
	response = requests.get('https://api.sinopia.io/resource?limit=1000&group=washington')
	with open('uw_list.json', 'w') as output_file:
		output_file.write(response.text)

	# create temporary output file
	if not os.path.exists('uw_uri_list.nq'):
		os.system('touch uw_uri_list.nq')

	# get URIs from JSON-LD into python list
	os.system('java -jar rmlmapper-4.9.1-r328.jar -m json_rml.ttl -o uw_uri_list.nq')
	URI_list = []
	uriGraph = Graph()
	uriGraph.load('file:uw_uri_list.nq', format='nquads')
	for uri in uriGraph.objects(None, None):
		URI_list.append(uri)

	# remove temporary output file
	os.system('rm uw_uri_list.nq')

	return URI_list

def save_all_resources(URI_list, currentDate):
	# create new graph, bind namespaces
	Graph_sinopiaAll = rdflib.Graph()
	Graph_sinopiaAll.bind('bf', bf)
	Graph_sinopiaAll.bind('bflc', bflc)
	Graph_sinopiaAll.bind('rdac', rdac)
	Graph_sinopiaAll.bind('rdae', rdae)
	Graph_sinopiaAll.bind('rdai', rdai)
	Graph_sinopiaAll.bind('rdam', rdam)
	Graph_sinopiaAll.bind('rdamdt', rdamdt)
	Graph_sinopiaAll.bind('rdaw', rdaw)
	Graph_sinopiaAll.bind('rdax', rdax)
	Graph_sinopiaAll.bind('sin', sin)
	Graph_sinopiaAll.bind('madsrdf', madsrdf)

	# load RDA from sinopia into graph
	bar = Bar('>> Parsing all UW resources', max=len(URI_list), suffix='%(percent)d%%')
	for URI in URI_list:
		Graph_sinopiaAll.parse(URI, format="json-ld")
		bar.next()
	bar.finish()

	print('...\nSerializing as RDF/XML')
	Graph_sinopiaAll.serialize(destination=f'../input/{currentDate}/all_resources.xml', format="xml") # serializes in xml

	print('...\nDone!')

def save_works(URI_list, currentDate):
	"""Look for works from mongoDB according to RDA class"""
	# create directory for works
	if not os.path.exists(f'../input/{currentDate}/work'):
		print("...\n>> Creating work directory")
		os.system(f'mkdir ../input/{currentDate}/work')

	workURIList = []

	print('...')

	bar = Bar('>> Locating works', max=len(URI_list), suffix='%(percent)d%%') # progress bar
	for URI in URI_list:
		label = URI.split('/')[-1]
		# create new graph, bind namespaces
		Graph_sinopiaWork = rdflib.Graph()
		Graph_sinopiaWork.bind('bf', bf)
		Graph_sinopiaWork.bind('bflc', bflc)
		Graph_sinopiaWork.bind('rdac', rdac)
		Graph_sinopiaWork.bind('rdaw', rdaw)
		Graph_sinopiaWork.bind('rdax', rdax)
		Graph_sinopiaWork.bind('sin', sin)
		Graph_sinopiaWork.bind('madsrdf', madsrdf)

		# load RDA from sinopia into graph
		Graph_sinopiaWork.parse(URI, format="json-ld")

		# look for resources classed as an RDA Work, serialize as XML, and save locally
		for work in Graph_sinopiaWork.subjects(RDF.type, rdac.C10001):
			workURIList.append(URI)
			Graph_sinopiaWork.serialize(destination=f'../input/{currentDate}/work/' + label + '.xml', format="xml") # serializes in xml
		bar.next()
	bar.finish()

	return workURIList

def save_expressions(URI_list, currentDate, workURIList=[]):
	"""Look for expressions from mongoDB according to RDA class"""
	# remove works from URI list to save time
	for work in workURIList:
		URI_list.remove(work)

	# create directory for expressions
	if not os.path.exists(f'../input/{currentDate}/expression'):
		print("...\n>> Creating expression directory")
		os.system(f'mkdir ../input/{currentDate}/expression')

	expressionURIList = []

	print('...')

	bar = Bar('>> Locating expressions', max=len(URI_list), suffix='%(percent)d%%') # progress bar
	for URI in URI_list:
		label = URI.split('/')[-1]
		# create new graph, bind namespaces
		Graph_sinopiaExpression = rdflib.Graph()
		Graph_sinopiaExpression.bind('bf', bf)
		Graph_sinopiaExpression.bind('bflc', bflc)
		Graph_sinopiaExpression.bind('rdac', rdac)
		Graph_sinopiaExpression.bind('rdae', rdae)
		Graph_sinopiaExpression.bind('rdax', rdax)
		Graph_sinopiaExpression.bind('sin', sin)
		Graph_sinopiaExpression.bind('madsrdf', madsrdf)

		# load RDA from sinopia into graph
		Graph_sinopiaExpression.parse(URI, format="json-ld")

		# look for resources classed as an RDA Expression, serialize as XML, and save locally
		for expression in Graph_sinopiaExpression.subjects(RDF.type, rdac.C10006):
			expressionURIList.append(URI)
			Graph_sinopiaExpression.serialize(destination=f'../input/{currentDate}/expression/' + label + '.xml', format="xml") # serialize in xml
		bar.next()
	bar.finish()
	return expressionURIList

def save_manifestations(URI_list, currentDate, expressionURIList=[]):
	"""Look for manifestations from mongoDB according to RDA class"""
	# remove expressions from URI list to save time # works removed in previous step
	for expression in expressionURIList:
		URI_list.remove(expression)

	# create directory for manifestations
	if not os.path.exists(f'../input/{currentDate}/manifestation'):
		print("...\n>> Creating manifestation directory")
		os.system(f'mkdir ../input/{currentDate}/manifestation')

	manifestationURIList = []

	print('...')

	bar = Bar('>> Locating manifestations', max=len(URI_list), suffix='%(percent)d%%') # progress bar
	for URI in URI_list:
		label = URI.split('/')[-1]
		# create new graph, bind namespaces
		Graph_sinopiaManifestation = rdflib.Graph()
		Graph_sinopiaManifestation.bind('bf', bf)
		Graph_sinopiaManifestation.bind('bflc', bflc)
		Graph_sinopiaManifestation.bind('rdac', rdac)
		Graph_sinopiaManifestation.bind('rdam', rdam)
		Graph_sinopiaManifestation.bind('rdamdt', rdamdt)
		Graph_sinopiaManifestation.bind('rdax', rdax)
		Graph_sinopiaManifestation.bind('sin', sin)
		Graph_sinopiaManifestation.bind('madsrdf', madsrdf)

		# load RDA from sinopia into graph
		Graph_sinopiaManifestation.parse(URI, format="json-ld")

		# look for resources classed as an RDA Manifestation, serialize as XML, and save locally
		for manifestation in Graph_sinopiaManifestation.subjects(RDF.type, rdac.C10007):
			manifestationURIList.append(URI)
			Graph_sinopiaManifestation.serialize(destination=f'../input/{currentDate}/manifestation/' + label + '.xml', format="xml")
		bar.next()
	bar.finish()
	return manifestationURIList

def save_items(URI_list, currentDate, manifestationURIList=[]):
	"""Look for items from mongoDB according to RDA class"""
	# remove manifestations from URI list to save time # works and expressions removed in previous steps
	for manifestation in manifestationURIList:
		URI_list.remove(manifestation)

	# create directory for items
	if not os.path.exists(f'../input/{currentDate}/item'):
		print("...\n>> Creating item directory")
		os.system(f'mkdir ../input/{currentDate}/item')

	print('...')

	bar = Bar('>> Locating items', max=len(URI_list), suffix='%(percent)d%%') # progress bar
	for URI in URI_list:
		label = URI.split('/')[-1]
		# create new graph, bind namespaces
		Graph_sinopiaItem = rdflib.Graph()
		Graph_sinopiaItem.bind('bf', bf)
		Graph_sinopiaItem.bind('bflc', bflc)
		Graph_sinopiaItem.bind('rdac', rdac)
		Graph_sinopiaItem.bind('rdai', rdai)
		Graph_sinopiaItem.bind('rdax', rdax)
		Graph_sinopiaItem.bind('sin', sin)
		Graph_sinopiaItem.bind('madsrdf', madsrdf)

		# load RDA from sinopia into graph
		Graph_sinopiaItem.parse(URI, format="json-ld")

		# look for resources classed as an RDA Item, serialize as XML, and save locally
		for item in Graph_sinopiaItem.subjects(RDF.type, rdac.C10003):
			Graph_sinopiaItem.serialize(destination=f'../input/{currentDate}/item/' + label + '.xml', format="xml")
		bar.next()
	bar.finish()

"""Variables"""

# format for naming folder according to date
today = date.today()
currentDate = str(today).replace('-', '_')

###

# create directory with today's date for RDA-in-RDF/XML data
if not os.path.exists(f'../input/{currentDate}'):
	print('...\n>> Creating input folder')
	os.system(f'mkdir ../input/{currentDate}')

URI_list = create_URI_list()

#start = timer()
#save_all_resources(URI_list, currentDate)
#end = timer()
#print(f"Number of resources: {len(URI_list)}")
#print(f"Elapsed time: {round((end - start), 1)} s")

start = timer()
workURIList = save_works(URI_list, currentDate)
end = timer()
print(f"Number of works: {len(workURIList)}")
print(f"Elapsed time: {round((end - start), 1)} s")

workList = os.listdir(f'../input/{currentDate}/work')
start = timer()
expressionURIList = save_expressions(URI_list, currentDate, workURIList)
end = timer()
print(f"Number of expressions: {len(expressionURIList)}")
print(f"Elapsed time: {round((end - start), 1)} s")

expressionList = os.listdir(f'../input/{currentDate}/expression')
start = timer()
manifestationURIList = save_manifestations(URI_list, currentDate, expressionURIList)
end = timer()
print(f"Number of works: {len(manifestationURIList)}")
print(f"Elapsed time: {round((end - start), 1)} s")

manifestationList = os.listdir(f'../input/{currentDate}/manifestation')
start = timer()
save_items(URI_list, currentDate, manifestationURIList)
end = timer()
itemList = os.listdir(f'../input/{currentDate}/item')
print(f"Number of works: {len(itemList)}")
print(f"Elapsed time: {round((end - start), 1)} s")
