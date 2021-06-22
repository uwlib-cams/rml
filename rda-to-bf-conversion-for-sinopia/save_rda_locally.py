from arguments import define_arg
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
ex = Namespace('http://example.org/rules/')
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

def create_uri_dict(source):
	"""Creates a list of all URIs for all records in UW mongoDB"""
	# create temporary output files
	if not os.path.exists('uw_list.json'):
		os.system('touch uw_list.json')
	if not os.path.exists('uw_uri_list.nq'):
		os.system('touch uw_uri_list.nq')

	# pull from mongo + http to get all URIs
	response = requests.get(source)
	with open('uw_list.json', 'w') as output_file:
		output_file.write(response.text)

	# get URIs from JSON-LD into python list
	os.system('java -jar rmlmapper-4.9.1-r328.jar -m json_rml.ttl -o uw_uri_list.nq')
	uri_dict = {"work": [], "expression": [], "manifestation": [], "item": []}
	uriGraph = Graph()
	uriGraph.bind('ex', ex)
	uriGraph.load('file:uw_uri_list.nq', format='nquads')

	for uri in uriGraph.objects(ex.Work_URIs, None):
		uri_dict["work"].append(uri)
	for uri in uriGraph.objects(ex.Expression_URIs, None):
		uri_dict["expression"].append(uri)
	for uri in uriGraph.objects(ex.Manifestation_URIs, None):
		uri_dict["manifestation"].append(uri)
	for uri in uriGraph.objects(ex.Item_URIs, None):
		uri_dict["item"].append(uri)

	# remove temporary output files
	os.system('rm uw_list.json')
	os.system('rm uw_uri_list.nq')

	return uri_dict

def save_all_resources(uri_dict, currentDate):
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

	resource_list = uri_dict["work"] + uri_dict["expression"] + uri_dict["manifestation"] + uri_dict["item"]

	# load RDA from sinopia into graph
	bar = Bar('Parsing all UW resources', max=len(resource_list), suffix='%(percent)d%%')
	for URI in resource_list:
		Graph_sinopiaAll.parse(URI, format="json-ld")
		bar.next()
	bar.finish()

	print('...\nSerializing as RDF/XML')
	Graph_sinopiaAll.serialize(destination=f'{input_location}/{currentDate}/all_resources.xml', format="xml") # serializes in xml

	print('...\nDone!')

def save_works(uri_dict, currentDate):
	"""Look for works from mongoDB according to RDA class"""
	# create directory for works
	if not os.path.exists(f'{input_location}/{currentDate}/work'):
		print(">> Creating work directory")
		os.system(f'mkdir {input_location}/{currentDate}/work')

	work_list = uri_dict["work"]

	bar = Bar('>> Locating works', max=len(work_list), suffix='%(percent)d%%') # progress bar
	for URI in work_list:
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
			Graph_sinopiaWork.serialize(destination=f'{input_location}/{currentDate}/work/' + label + '.xml', format="xml") # serializes in xml
		bar.next()
	bar.finish()

def save_expressions(uri_dict, currentDate):
	"""Look for expressions from mongoDB according to RDA class"""
	# create directory for expressions
	if not os.path.exists(f'{input_location}/{currentDate}/expression'):
		print("\n>> Creating expression directory")
		os.system(f'mkdir {input_location}/{currentDate}/expression')

	expression_list = uri_dict["expression"]

	bar = Bar('>> Locating expressions', max=len(expression_list), suffix='%(percent)d%%') # progress bar
	for URI in expression_list:
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
			Graph_sinopiaExpression.serialize(destination=f'{input_location}/{currentDate}/expression/' + label + '.xml', format="xml") # serialize in xml
		bar.next()
	bar.finish()

def save_manifestations(uri_dict, currentDate):
	"""Look for manifestations from mongoDB according to RDA class"""
	# create directory for manifestations
	if not os.path.exists(f'{input_location}/{currentDate}/manifestation'):
		print("\n>> Creating manifestation directory")
		os.system(f'mkdir {input_location}/{currentDate}/manifestation')

	manifestation_list = uri_dict["manifestation"]

	bar = Bar('>> Locating manifestations', max=len(manifestation_list), suffix='%(percent)d%%') # progress bar
	for URI in manifestation_list:
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
			Graph_sinopiaManifestation.serialize(destination=f'{input_location}/{currentDate}/manifestation/' + label + '.xml', format="xml")
		bar.next()
	bar.finish()

def save_items(uri_dict, currentDate):
	"""Look for items from mongoDB according to RDA class"""
	# create directory for items
	if not os.path.exists(f'{input_location}/{currentDate}/item'):
		print("\n>> Creating item directory")
		os.system(f'mkdir {input_location}/{currentDate}/item')

	item_list = uri_dict["item"]

	bar = Bar('>> Locating items', max=len(item_list), suffix='%(percent)d%%') # progress bar
	for URI in item_list:
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
			Graph_sinopiaItem.serialize(destination=f'{input_location}/{currentDate}/item/' + label + '.xml', format="xml")
		bar.next()
	bar.finish()

"""Variables"""

# format for naming directory according to date
today = date.today()
currentDate = str(today).replace('-', '_')

# arguments from command line
args = define_arg()
source = args.source
input_location = args.input

###

"""Create input folder"""
if not os.path.exists(f'{input_location}'):
	print('>> Creating input directory')
	os.system(f'mkdir {input_location}')

if not os.path.exists(f'{input_location}/{currentDate}'):
	os.system(f'mkdir {input_location}/{currentDate}')

"""Create list of URIs from Sinopia"""
uri_dict = create_uri_dict(source)

"""Save all resources in one file"""
#start = timer()
#save_all_resources(uri_dict, currentDate)
#end = timer()
#print(f"Elapsed time: {round((end - start), 1)} s")

"""Save works"""
start = timer()
save_works(uri_dict, currentDate)
workURIList = os.listdir(f'{input_location}/{currentDate}/work')
end = timer()
print(f"Number of works: {len(workURIList)}")
print(f"Elapsed time: {round((end - start), 1)} s")

"""Save expressions"""
start = timer()
save_expressions(uri_dict, currentDate)
expressionURIList = os.listdir(f'{input_location}/{currentDate}/expression')
end = timer()
print(f"Number of expressions: {len(expressionURIList)}")
print(f"Elapsed time: {round((end - start), 1)} s")

"""Save manifestations"""
start = timer()
save_manifestations(uri_dict, currentDate)
manifestationURIList = os.listdir(f'{input_location}/{currentDate}/manifestation')
end = timer()
print(f"Number of works: {len(manifestationURIList)}")
print(f"Elapsed time: {round((end - start), 1)} s")

"""Save items"""
start = timer()
save_items(uri_dict, currentDate)
itemList = os.listdir(f'{input_location}/{currentDate}/item')
end = timer()
print(f"Number of works: {len(itemList)}")
print(f"Elapsed time: {round((end - start), 1)} s")
