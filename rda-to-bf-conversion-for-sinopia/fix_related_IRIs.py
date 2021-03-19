import csv
from datetime import date
import os
from progress.bar import Bar
from rdflib import *
import time
import xml.etree.ElementTree as ET

"""Namespaces"""
LDP = Namespace('http://www.w3.org/ns/ldp#')
bf = Namespace('http://id.loc.gov/ontologies/bibframe/')
bflc = Namespace('http://id.loc.gov/ontologies/bflc/')
dbo = Namespace('http://dbpedia.org/ontology/')
madsrdf = Namespace('http://www.loc.gov/mads/rdf/v1#')
owl = Namespace('http://www.w3.org/2002/07/owl#')
rdac = Namespace('http://rdaregistry.info/Elements/c/')
rdae = Namespace('http://rdaregistry.info/Elements/e/')
rdai = Namespace('http://rdaregistry.info/Elements/i/')
rdam = Namespace('http://rdaregistry.info/Elements/m/')
rdamdt = Namespace('http://rdaregistry.info/Elements/m/datatype/')
rdau = Namespace('http://rdaregistry.info/Elements/u/')
rdaw = Namespace('http://rdaregistry.info/Elements/w/')
rdax = Namespace('https://doi.org/10.6069/uwlib.55.d.4#')
sin = Namespace('http://sinopia.io/vocabulary/')

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

"""Functions"""
def reserialize(file):
	"""Reserialize with rdflib to fix namespaces and UTf-8"""
	g = Graph()
	g.bind('bf', bf)
	g.bind('bflc', bflc)
	g.bind('dbo', dbo)
	g.bind('madsrdf', madsrdf)
	g.bind('owl', owl)
	g.bind('rdac', rdac)
	g.bind('rdae', rdae)
	g.bind('rdai', rdai)
	g.bind('rdam', rdam)
	g.bind('rdamdt', rdamdt)
	g.bind('rdau', rdau)
	g.bind('rdaw', rdaw)
	g.bind('rdax', rdax)
	g.bind('sin', sin)
	g.load(f'file:{file}', format='xml')
	g.serialize(destination=f'{file}', format='xml')

def fix_related_IRIs(RDA_ID, BF_ID, entity, file):
	edit = False

	# open xml parser
	tree = ET.parse(f'../output/{currentDate}/{entity}_xml/{file}')
	root = tree.getroot()

	for child in root: # for each node...
		for prop in child: # for each property in node...
			if '{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource' in prop.attrib.keys(): # if the value is an IRI...
				RDA_IRI = f'https://api.sinopia.io/resource/{RDA_ID}'
				if prop.attrib['{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource'] == RDA_IRI: # if that IRI is the RDA IRI in question
					BF_IRI = f'https://api.sinopia.io/resource/{BF_ID}'
					prop.set('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource', BF_IRI) # replace it with its equivalent BF IRI
					edit = True

	if edit == True: # only rewrite / reserialize if an edit was made
		tree.write(f'../output/{currentDate}/{entity}_xml/{file}')

		reserialize(f'../output/{currentDate}/{entity}_xml/{file}')

###

with open(f"RDA_BF_IRI_list_{currentDate}.csv", mode="r") as key_file:
	"""Get number of IRI pairs to iterate through"""
	csv_reader = csv.reader(key_file, delimiter=',')
	total_line_count = 0

	for line in csv_reader:
		total_line_count += 1

with open(f"RDA_BF_IRI_list_{currentDate}.csv", mode="r") as key_file:
	"""For each resource, look for IRI pairs and make appropriate changes"""
	csv_reader = csv.reader(key_file, delimiter=',')
	line_count = 0

	bar = Bar(max=total_line_count, suffix='%(percent)d%%') # progress bar
	for line in csv_reader:
		if line_count == 0: # skip header row
			pass
		else:
			RDA_ID = line[0]
			BF_ID = line[1]

			for entity in resource_dict.keys():
				for resource in resource_dict[entity]:
					fix_related_IRIs(RDA_ID, BF_ID, entity, resource)
		line_count += 1
		bar.next()
	bar.finish()
