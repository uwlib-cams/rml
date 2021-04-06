import os
from datetime import date
from progress.bar import Bar
from rdflib import *
from timeit import default_timer as timer
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
	edit_made = False

	# open xml parser
	tree = ET.parse(f'../input/{currentDate}/{entity}/{file}')
	root = tree.getroot()

	for child in root: # for each node...
		for prop in child: # for each property in node...
			if prop.text is not None: # if the property has a literal value...
				if prop.text == "©": # and if that literal is the copyright symbol and nothing else...
					child.remove(prop) # remove that property
					edit_made = True

					tree.write(f'../input/{currentDate}/{entity}/{file}')

					reserialize(f'../input/{currentDate}/{entity}/{file}')
	return edit_made

"""Variables"""

# format for naming folder according to date
today = date.today()
currentDate = str(today).replace('-', '_')

num_of_edits = 0

"""Lists and Dictionaries"""

workList = os.listdir(f'../input/{currentDate}/work')
expressionList = os.listdir(f'../input/{currentDate}/expression')
manifestationList = os.listdir(f'../input/{currentDate}/manifestation')
itemList = os.listdir(f'../input/{currentDate}/item')

resource_dict = {"work": workList, "expression": expressionList, "manifestation": manifestationList, "item": itemList}

###

num_of_resources = len(workList) + len(expressionList) + len(manifestationList) + len(itemList)

bar = Bar(">> Removing blank copyright dates", max=num_of_resources, suffix='%(percent)d%%') # progress bar

start = timer()
for entity in resource_dict.keys():
	for resource in resource_dict[entity]:
		edit_made = fix_copyright_dates(entity, resource)
		if edit_made == True:
			num_of_edits += 1
		bar.next()
end = timer()
bar.finish()
print(f"Resources edited: {num_of_edits}")
print(f"Elapsed time: {round((end - start), 1)} s")
