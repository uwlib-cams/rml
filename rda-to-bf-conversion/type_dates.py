from datetime import date
import os
from progress.bar import Bar
from rdflib import *
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

today = date.today()
currentDate = str(today).replace('-','_')

"""Lists and Dictionaries"""

bf_date_prop_list = ["date", "originDate", "legalDate", "copyrightDate", "changeDate", "creationDate", "generationDate"]

work_1_list = os.listdir(f"output_{currentDate}/work_1/")
work_2_list = os.listdir(f"output_{currentDate}/work_2/")
instance_list = os.listdir(f"output_{currentDate}/instance/")
item_list = os.listdir(f"output_{currentDate}/item/")

resource_dict = {"work_1": work_1_list, "work_2": work_2_list, "instance": instance_list, "item": item_list}

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

def determine_date_type(value):
	num_of_dashes = 0
	time_included = False
	for character in value:
		if character == '-':
			num_of_dashes += 1
		elif character == ':':
			time_included = True

	if num_of_dashes == 0: # e.g. "1886"
		date_type = "gYear"
	elif num_of_dashes == 1: # e.g. "1886-02"
		date_type = 'gYearMonth'
	elif num_of_dashes == 2: # e.g. "1886-02-14" or "2021-03-17T12:00:00+00:00"
		if time_included == True:
			date_type = 'dateTime'
		else:
			date_type = 'date'

	return date_type

def add_dates_in_xml(currentDate, entity, file):
	# open xml parser
	tree = ET.parse(f'output_{currentDate}/{entity}/{file}')
	root = tree.getroot()

	for child in root:
		for prop in child:
			if prop.tag.split('}')[-1] in bf_date_prop_list:
				date_type = determine_date_type(prop.text)
				prop.set('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}datatype', f"http://www.w3.org/2001/XMLSchema#{date_type}")
			elif prop.tag.split('}')[-1] == 'label':
				if prop.text == None:
					pass
				elif prop.text[0:15] == "rml.py SNAPSHOT":
					date_type = determine_date_type(prop.text)
					prop.set('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}datatype', f"http://www.w3.org/2001/XMLSchema#{date_type}")

	tree.write(f'output_{currentDate}/{entity}/{file}')

	reserialize(f'output_{currentDate}/{entity}/{file}')

###
num_of_resources = len(work_1_list) + len(work_2_list) + len(instance_list) + len(item_list)

bar = Bar(max=num_of_resources, suffix='%(percent)d%%') # progress bar
for entity in resource_dict.keys():
	for resource in resource_dict[entity]:
		add_dates_in_xml(currentDate, entity, resource)
		bar.next()
bar.finish()
