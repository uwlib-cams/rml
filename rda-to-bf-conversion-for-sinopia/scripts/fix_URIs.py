"""Python Libraries/Modules/Packages"""
from datetime import date
import os
from progress.bar import Bar
import rdflib
from rdflib import *
from timeit import default_timer as timer

"""Imported Functions"""
from scripts.arguments import define_arg

"""Functions"""
def fix_URIs(entity, file, input_location):
	"""Find URIs that have been entered as literals, and correct them so they are typed as URIs"""

	num_of_edits = 0

	g = Graph()
	g.load(f'{input_location}/{currentDate}/{entity}/{file}', format='xml')

	for s, p, o in g:
		if isinstance(o, rdflib.term.Literal) == True:
			object_literal = "{}".format(o)
			if object_literal[0:4] == "http": # literal is actually an IRI
				new_object = URIRef(object_literal)
				g.remove((s, p, o))
				g.add((s, p, new_object))
				num_of_edits += 1
		elif isinstance(o, rdflib.term.URIRef) == True:
			object_IRI = "{}".format(o)
			if object_IRI == "file:///home/forge/rda.metadataregistry.org/storage/repos/projects/177/xml/termList/rdacc1003": # correcting some incorrect IRIs in our data
				g.remove((s, p, o))
				g.add((s, p, URIRef('http://rdaregistry.info/termList/RDAColourContent/1003')))
				num_of_edits += 1

	g.serialize(destination=f'{input_location}/{currentDate}/{entity}/{file}', format='xml')

	return num_of_edits

"""Variables"""
# format for naming folder according to date
today = date.today()
currentDate = str(today).replace('-', '_')

# arguments from command line
args = define_arg()
input_location = args.input

num_of_edits = 0

"""Lists and Dictionaries"""
workList = os.listdir(f'{input_location}/{currentDate}/work')
expressionList = os.listdir(f'{input_location}/{currentDate}/expression')
manifestationList = os.listdir(f'{input_location}/{currentDate}/manifestation')
itemList = os.listdir(f'{input_location}/{currentDate}/item')

resource_dict = {"work": workList, "expression": expressionList, "manifestation": manifestationList, "item": itemList}

###

num_of_resources = len(workList) + len(expressionList) + len(manifestationList) + len(itemList)

bar = Bar(">> Fixing IRIs typed as literals", max=num_of_resources, suffix='%(percent)d%%') # progress bar

start = timer()
for entity in resource_dict.keys():
	for resource in resource_dict[entity]:
		edits_made = fix_URIs(entity, resource, input_location)
		num_of_edits += edits_made
		bar.next()
end = timer()
bar.finish()
print(f"IRIs corrected: {num_of_edits}")
print(f"Elapsed time: {round((end - start), 1)} s")
