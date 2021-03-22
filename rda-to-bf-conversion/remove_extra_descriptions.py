from datetime import date
import os
from progress.bar import Bar
from rdflib import *
import rdflib
import time
import xml.etree.ElementTree as ET

"""Namespaces"""
bf = Namespace('http://id.loc.gov/ontologies/bibframe/')
bflc = Namespace('http://id.loc.gov/ontologies/bflc/')
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

def remove_extra_descriptions(entity, file):
	"""Remove triples from original RDA/RDF that do not describe the resource in question"""

	# create temporary output file
	if not os.path.exists(f'temp.xml'):
		os.system('touch temp.xml')

	# open xml parser
	tree = ET.parse(f'input_{currentDate}/{entity}/{file}')
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

		# write new XML to a temporary file
		tree.write('temp.xml')

		# reserialize with rdflib to fix namespaces and UTf-8
		g = Graph()
		g.bind('bf', bf)
		g.bind('bflc', bflc)
		g.bind('madsrdf', madsrdf)
		g.bind('rdac', rdac)
		g.bind('rdae', rdae)
		g.bind('rdai', rdai)
		g.bind('rdam', rdam)
		g.bind('rdamdt', rdamdt)
		g.bind('rdaw', rdaw)
		g.bind('rdax', rdax)
		g.bind('sin', sin)
		g.load(f'file:temp.xml', format='xml')
		g.serialize(destination=f'input_{currentDate}/{entity}/{file}', format='xml')

"""Variables"""

# format for naming folder according to date
today = date.today()
currentDate = str(today).replace('-', '_')

"""Lists and Dictionaries"""

workList = os.listdir(f'input_{currentDate}/work')
expressionList = os.listdir(f'input_{currentDate}/expression')
manifestationList = os.listdir(f'input_{currentDate}/manifestation')
itemList = os.listdir(f'input_{currentDate}/item')

resource_dict = {"work": workList, "expression": expressionList, "manifestation": manifestationList, "item": itemList}

###

num_of_resources = len(workList) + len(expressionList) + len(manifestationList) + len(itemList)

bar = Bar(max=num_of_resources, suffix='%(percent)d%%') # progress bar

for entity in resource_dict.keys():
	for resource in resource_dict[entity]:
		remove_extra_descriptions(entity, resource)
		bar.next()
bar.finish()

# remove temporary file
if os.path.exists('temp.xml'):
	os.system('rm temp.xml')
