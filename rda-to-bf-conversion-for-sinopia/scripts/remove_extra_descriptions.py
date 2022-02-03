"""Python Libraries/Modules/Packages"""
from datetime import date
import os
from progress.bar import Bar
from rdflib import *
import time
from timeit import default_timer as timer
import xml.etree.ElementTree as ET

"""Imported Functions"""
from scripts.arguments import define_arg
from scripts.reserialize import reserialize

"""Functions"""
def remove_extra_descriptions(entity, file, input_location):
	"""Remove triples from original RDA/RDF that do not describe the resource in question"""

	num_of_edits = 0

	# create temporary output file
	if not os.path.exists(f'temp.xml'):
		os.system('touch temp.xml')

	# open xml parser
	tree = ET.parse(f'{input_location}/{currentDate}/{entity}/{file}')
	root = tree.getroot()

	resource_identifier = file.split('.')[0]
	IRI = f'https://api.sinopia.io/resource/{resource_identifier}'

	ns = {'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'}

	for desc in root.findall('rdf:Description', ns):
		# create dictionary of attributes for description
		attrib_dict = desc.attrib

		# if it contains rdf:about as an attribute...
		if '{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about' in attrib_dict.keys():
			# and if the value of rdf:about is not the resource in question...
			if attrib_dict['{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about'] != IRI:
				# remove the description
				root.remove(desc)
				num_of_edits += 0

		# write new XML to a temporary file
		tree.write('temp.xml')

		# reserialize with rdflib to fix namespaces and UTf-8
		reserialize('temp.xml', f'{input_location}/{currentDate}/{entity}/{file}', 'xml')

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

bar = Bar(">> Removing extra descriptions", max=num_of_resources, suffix='%(percent)d%%') # progress bar

start = timer()
for entity in resource_dict.keys():
	for resource in resource_dict[entity]:
		edits_made = remove_extra_descriptions(entity, resource, input_location)
		num_of_edits += edits_made
		bar.next()
end = timer()
bar.finish()
print(f"Descriptions removed: {num_of_edits}")
print(f"Elapsed time: {round((end - start), 1)} s")

# remove temporary file
if os.path.exists('temp.xml'):
	os.system('rm temp.xml')
