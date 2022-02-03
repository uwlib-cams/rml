"""Python Libraries/Modules/Packages"""
import os
from datetime import date
from progress.bar import Bar
from rdflib import *
from timeit import default_timer as timer
import xml.etree.ElementTree as ET

"""Imported Functions"""
from scripts.arguments import define_arg
from scripts.reserialize import reserialize

"""Functions"""
def fix_URIs(entity, file, input_location):
	"""Find URIs that have been entered as literals, and correct them so they are typed as URIs"""

	num_of_edits = 0

	# open xml parser
	tree = ET.parse(f'{input_location}/{currentDate}/{entity}/{file}')
	root = tree.getroot()

	for child in root: # for each node...
		for prop in child: # for each property in node...
			if prop.text is not None: # if the property has a literal value...
				if prop.text[0:4] == "http": # and if that literal is actually an IRI...
					IRI = prop.text
					prop.clear() # clear literal value
					prop.set('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource', IRI) # add IRI as attribute
					num_of_edits += 1

					tree.write(f'{input_location}/{currentDate}/{entity}/{file}')

					reserialize(f'{input_location}/{currentDate}/{entity}/{file}', f'{input_location}/{currentDate}/{entity}/{file}', 'xml')
			elif '{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource' in prop.attrib.keys():
				if prop.attrib['{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource'] == 'file:///home/forge/rda.metadataregistry.org/storage/repos/projects/177/xml/termList/rdacc1003':
					prop.clear()
					prop.set('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource', 'http://rdaregistry.info/termList/RDAColourContent/1003')
					num_of_edits += 1

					tree.write(f'{input_location}/{currentDate}/{entity}/{file}')

					reserialize(f'{input_location}/{currentDate}/{entity}/{file}', f'{input_location}/{currentDate}/{entity}/{file}', 'xml')
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
