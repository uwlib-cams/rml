from datetime import date
import json
import os
from progress.bar import Bar
from rdflib import *
import time
from timeit import default_timer as timer

"""Namespaces"""
bf = Namespace('http://id.loc.gov/ontologies/bibframe/')
bflc = Namespace('http://id.loc.gov/ontologies/bflc/')
madsrdf = Namespace('http://www.loc.gov/mads/rdf/v1#')
owl = Namespace('http://www.w3.org/2002/07/owl#')
sin = Namespace('http://sinopia.io/vocabulary/')
skos = Namespace('http://www.w3.org/2004/02/skos/core#')

"""Variables"""

# format for naming folder according to date
today = date.today()
currentDate = str(today).replace('-', '_')

"""Lists and Dictionaries"""

work_1List = os.listdir(f'../output/{currentDate}/work_1_xml')
work_2List = os.listdir(f'../output/{currentDate}/work_2_xml')
instanceList = os.listdir(f'../output/{currentDate}/instance_xml')
itemList = os.listdir(f'../output/{currentDate}/item_xml')

resource_dict = {"work_1": work_1List, "work_2": work_2List, "instance": instanceList, "item": itemList}
rt_dict = {"work_1": "WAU:RT:BF2:Work", "work_2": "WAU:RT:BF2:Work", "instance": "WAU:RT:BF2:Instance", "item": "WAU:RT:BF2:Item"}
class_dict = {"work_1": "http://id.loc.gov/ontologies/bibframe/Work", "work_2": "http://id.loc.gov/ontologies/bibframe/Work", "instance": "http://id.loc.gov/ontologies/bibframe/Instance", "item": "http://id.loc.gov/ontologies/bibframe/Item"}

"""Functions"""

def add_rt_triple(entity, resource):
	"""Loads RDF/XML into graph, adds triple for resource template, and outputs new graph in JSON-LD"""
	# create output dir, if it does not already exist
	if not os.path.exists(f'../output/{currentDate}/{entity}_json'):
		print(f">> Creating {entity}_json directory")
		os.makedirs(f'../output/{currentDate}/{entity}_json')

	# create new empty graph
	g = Graph()
	# bind namespaces to graph
	g.bind('bf', bf)
	g.bind('bflc', bflc)
	g.bind('madsrdf', madsrdf)
	g.bind('owl', owl)
	g.bind('sin', sin)
	g.bind('skos', skos)
	# load RDF/XMl
	g.load(f'file:../output/{currentDate}/{entity}_xml/{resource}', format='xml')

	# add RT triple
	g.add((URIRef(f"https://api.stage.sinopia.io/resource/{resource.split('.')[0]}"), sin.hasResourceTemplate, Literal(f"{rt_dict[entity]}")))

	# serialize as JSON-LD
	g.serialize(destination=f'../output/{currentDate}/{entity}_json/{resource}', format='json-ld')

def edit_json(entity, resource):
	"""Prepare JSON-LD for upload into Sinopia"""
	with open(f'../output/{currentDate}/{entity}_json/{resource}', 'r') as input_file:
		original_data = json.load(input_file)
		currentTime = time.strftime("%Y-%m-%dT%H:%M:%S")
		resource_id = resource.split('.')[0]
		resource_iri = f"https://api.stage.sinopa.io/resource/{resource_id}"
		sinopia_format = json.dumps({"data": original_data, "user": "mcm104", "group": "washington", "templateId": rt_dict[entity], "types": [ class_dict[entity] ], "id": resource_id, "uri": resource_iri, "timestamp": currentTime})

	with open(f'../output/{currentDate}/{entity}_json/{resource}', 'w') as output_file:
		output_file.write(sinopia_format)

###

for entity in resource_dict.keys():
	for resource in resource_dict[entity]:
		add_rt_triple(entity, resource)
		edit_json(entity, resource)
