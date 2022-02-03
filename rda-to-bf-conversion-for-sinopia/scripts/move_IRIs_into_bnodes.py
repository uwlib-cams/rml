"""Python Libraries/Modules/Packages"""
import os
from datetime import date
from progress.bar import Bar
from rdflib import *
from timeit import default_timer as timer

"""Namespaces"""
bf = Namespace('http://id.loc.gov/ontologies/bibframe/')
bflc = Namespace('http://id.loc.gov/ontologies/bflc/')
dbo = Namespace('http://dbpedia.org/ontology/')
madsrdf = Namespace('http://www.loc.gov/mads/rdf/v1#')
owl = Namespace('http://www.w3.org/2002/07/owl#')
rdf = Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#')
sin = Namespace('http://sinopia.io/vocabulary/')
skos = Namespace('http://www.w3.org/2004/02/skos/core#')

"""Functions"""
def make_URI_values_compatible(entity, file):
	edit_made = False
	# open new graph
	g = Graph()
	# bind namespaces
	g.bind('bf', bf)
	g.bind('bflc', bflc)
	g.bind('dbo', dbo)
	g.bind('madsrdf', madsrdf)
	g.bind('owl', owl)
	g.bind('rdf', rdf)
	g.bind('sin', sin)
	g.bind('skos', skos)
	# load data into graph
	g.load(f'file:../output/{currentDate}/{entity}_xml/{file}', format='xml')

	# look for IRI values
	for s, p, o in g.triples((None, None, None)):
		if p != rdf.type:
			object = "{}".format(o)
			if object[0:4] == "http":
				new_b_node = BNode()
				g.remove((s, p, o))
				g.add((s, p, new_b_node))
				g.add((new_b_node, owl.sameAs, o))
				edit_made = True

	g.serialize(destination=f'../output/{currentDate}/{entity}_xml/{file}', format='xml')

	return edit_made

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

###

num_of_resources = len(work_1List) + len(work_2List) + len(instanceList) + len(itemList)
num_of_edits = 0

start = timer()
bar = Bar(">> Putting IRIs into blank nodes", max=num_of_resources, suffix='%(percent)d%%') # progress bar
for entity in resource_dict.keys():
	for resource in resource_dict[entity]:
		edit_made = make_URI_values_compatible(entity, resource)
		if edit_made == True:
			num_of_edits += 1
		bar.next()
end = timer()
bar.finish()

print(f"Edits made: {num_of_edits}")
print(f"Elapsed time: {round((end - start), 1)} s")
