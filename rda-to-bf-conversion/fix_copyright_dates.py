import os
from datetime import date
from progress.bar import Bar
from rdflib import *
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

def reserialize(file):
	"""Reserialize with rdflib to fix namespaces and UTf-8"""
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
	g.load(f'file:{file}', format='xml')
	g.serialize(destination=f'{file}', format='xml')

def fix_copyright_dates(entity, file):
	# open xml parser
	tree = ET.parse(f'input_{currentDate}/{entity}/{file}')
	root = tree.getroot()

	for child in root: # for each node...
		for prop in child: # for each property in node...
			if prop.text is not None: # if the property has a literal value...
				if prop.text == "©": # and if that literal is the copyright symbol and nothing else...
					child.remove(prop) # remove that property

					tree.write(f'input_{currentDate}/{entity}/{file}')

					reserialize(f'input_{currentDate}/{entity}/{file}')

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
		fix_copyright_dates(entity, resource)
		bar.next()
bar.finish()
