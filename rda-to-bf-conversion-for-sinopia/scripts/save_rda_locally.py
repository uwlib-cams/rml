"""Python Libraries/Modules/Packages"""
from datetime import date
import os
from progress.bar import Bar
import requests
from rdflib import *
import rdflib
import time
from timeit import default_timer as timer

"""Imported Functions"""
from scripts.arguments import define_arg

"""Namespaces"""
bf = Namespace('http://id.loc.gov/ontologies/bibframe/')
bflc = Namespace('http://id.loc.gov/ontologies/bflc/')
ex = Namespace('http://example.org/rules/')
madsrdf = Namespace('http://www.loc.gov/mads/rdf/v1#')
rdac = Namespace('http://rdaregistry.info/Elements/c/')
rdae = Namespace('http://rdaregistry.info/Elements/e/')
rdai = Namespace('http://rdaregistry.info/Elements/i/')
rdam = Namespace('http://rdaregistry.info/Elements/m/')
rdamdt = Namespace('http://rdaregistry.info/Elements/m/datatype/')
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
	if os.path.exists('mapper.jar'):
		os.system('java -jar mapper.jar -m other_files/json_rml.ttl -o uw_uri_list.nq')
	else:
		print("RML Mapper file missing.")
		quit()

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

def save_resources(uri_dict, currentDate, entity):
	"""Look for resources from mongoDB and save as RDF/XML"""
	# create directory for resources
	if not os.path.exists(f'{input_location}/{currentDate}/{entity}'):
		print("\n>> Creating resource directory")
		os.system(f'mkdir {input_location}/{currentDate}/{entity}')

	resource_list = uri_dict[entity]

	bar = Bar(f'>> Locating {entity}s', max=len(resource_list), suffix='%(percent)d%%') # progress bar
	for URI in resource_list:
		label = URI.split('/')[-1]
		# create new graph, bind namespaces
		graph = rdflib.Graph()
		graph = rdflib.Graph()
		graph.bind('bf', bf)
		graph.bind('bflc', bflc)
		graph.bind('madsrdf', madsrdf)
		graph.bind('rdac', rdac)
		graph.bind('rdax', rdax)
		graph.bind('sin', sin)
		if entity == "work":
			graph.bind('rdaw', rdaw)
		elif entity == "expression":
			graph.bind('rdae', rdae)
		elif entity == "manifestation":
			graph.bind('rdam', rdam)
			graph.bind('rdamdt', rdamdt)
		elif entity == "item":
			graph.bind('rdai', rdai)

		# load RDA from sinopia into graph
		graph.parse(URI, format="json-ld")

		# look for resources classed as an RDA Item, serialize as XML, and save locally
		graph.serialize(destination=f'{input_location}/{currentDate}/{entity}/' + label + '.xml', format="xml")

		bar.next()
	bar.finish()

def save_all_resources(uri_dict, currentDate):
	"""Saves all resources in one RDF/XML file; *not* currently used in this package"""
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

"""Variables"""

# format for naming directory according to date
today = date.today()
currentDate = str(today).replace('-', '_')

# arguments from command line
args = define_arg()
source = args.source
input_location = args.input

"""Lists & Dictionaries"""
entity_list = ["work", "expression", "manifestation", "item"]

###

"""Create input folder"""
if not os.path.exists(f'{input_location}'):
	print('>> Creating input directory')
	os.system(f'mkdir {input_location}')

if not os.path.exists(f'{input_location}/{currentDate}'):
	os.system(f'mkdir {input_location}/{currentDate}')

"""Create list of URIs from Sinopia"""
uri_dict = create_uri_dict(source)

"""Save resources locally"""
for entity in entity_list:
	start = timer()
	save_resources(uri_dict, currentDate, entity)
	end = timer()

	resourceURIList = os.listdir(f'{input_location}/{currentDate}/{entity}')
	print(f"Number of works: {len(resourceURIList)}")
	print(f"Elapsed time: {round((end - start), 1)} s")
