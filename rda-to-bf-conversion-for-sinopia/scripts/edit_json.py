"""Python Libraries/Modules/Packages"""
from datetime import date
import json
import os
from progress.bar import Bar
from rdflib import *
from datetime import datetime
from timeit import default_timer as timer

"""Imported Functions"""
from scripts.arguments import define_arg

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

# arguments from command line
args = define_arg()
output_location = args.output

"""Lists and Dictionaries"""
work_1List = os.listdir(f'{output_location}/{currentDate}/work_1_xml')
work_2List = os.listdir(f'{output_location}/{currentDate}/work_2_xml')
instanceList = os.listdir(f'{output_location}/{currentDate}/instance_xml')
itemList = os.listdir(f'{output_location}/{currentDate}/item_xml')

resource_dict = {"work_1": work_1List, "work_2": work_2List, "instance": instanceList, "item": itemList}
rt_dict = {"work_1": "WAU:RT:BF2:Works", "work_2": "WAU:RT:BF2:Works", "instance": "WAU:RT:BF2:Instance", "item": "WAU:RT:BF2:Item"}
class_dict = {"work_1": "http://id.loc.gov/ontologies/bibframe/Work", "work_2": "http://id.loc.gov/ontologies/bibframe/Work", "instance": "http://id.loc.gov/ontologies/bibframe/Instance", "item": "http://id.loc.gov/ontologies/bibframe/Item"}

"""Functions"""
def add_rt_triple(entity, resource, output_location):
	"""Loads RDF/XML into graph, adds triple for resource template, and outputs new graph in JSON-LD"""
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
	g.load(f'file:{output_location}/{currentDate}/{entity}_xml/{resource}', format='xml')

	# add RT triple
	g.add((URIRef(f"https://api.sinopia.io/resource/{resource.split('.')[0]}"), sin.hasResourceTemplate, Literal(f"{rt_dict[entity]}")))

	# serialize as JSON-LD
	g.serialize(destination=f"{output_location}/{currentDate}/{entity}_json/{resource.split('.')[0]}.json", format='json-ld')

def edit_json(entity, resource, output_location):
	resource = resource.split('.')[0] + '.json'
	"""Prepare JSON-LD for upload into Sinopia"""
	with open(f'{output_location}/{currentDate}/{entity}_json/{resource}', 'r') as input_file:
		original_data = json.load(input_file)
		currentTime = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
		resource_id = resource.split('.')[0]
		resource_iri = f"https://api.sinopia.io/resource/{resource_id}"
		sinopia_format = json.dumps({"data": original_data, "user": "mcm104", "group": "washington", "editGroups": [], "templateId": rt_dict[entity], "types": [ class_dict[entity] ], "bfAdminMetadataRefs": [], "sinopiaLocalAdminMetadataForRefs": [], "bfItemRefs": [], "bfInstanceRefs": [], "bfWorkRefs": [], "id": resource_id, "uri": resource_iri, "timestamp": currentTime})

	with open(f'{output_location}/{currentDate}/{entity}_json/{resource}', 'w') as output_file:
		output_file.write(sinopia_format)

###

start = timer()
for entity in resource_dict.keys():
	# create output dir, if it does not already exist
	if not os.path.exists(f'{output_location}/{currentDate}/{entity}_json'):
		print(f">> Creating {entity}_json directory")
		os.makedirs(f'{output_location}/{currentDate}/{entity}_json')

	bar = Bar(f'>> Converting {entity} files', max=len(resource_dict[entity]), suffix='%(percent)d%%') # progress bar
	for resource in resource_dict[entity]:
		add_rt_triple(entity, resource, output_location)
		edit_json(entity, resource, output_location)
		bar.next()
	bar.finish()
end = timer()
print(f"Elapsed time: {round((end - start), 2)} s")
